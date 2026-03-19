重注释（reannotation）
======================

``reannotation`` 是 ``annotion`` 步骤中的重注释分支，用于在已有 ``clusters`` 或 ``recluster`` 标签基础上重新映射 ``celltype``。
与 ``mannul`` 相比，``reannotation`` 侧重“快速修订已有标签并标准化导出”，适用于聚类稳定后的小范围命名调整。

配置文件详解请见 :doc:`../config_reference/annotion_yaml`。

处理逻辑概述
------------
1. 读取 ``sample.txt`` 第二列给出的下游对象（``.zarr`` 或 ``.h5ad``）。
2. 读取注释映射并解析 cluster/recluster 到 celltype 的对应关系。
3. 优先使用 ``obs['recluster']``（若存在），否则使用 ``obs['clusters']`` 完成映射。
4. 将映射结果写入 ``obs['celltype']``，未命中的标签自动写为 ``Unknown``。
5. 输出重注释对象与 ``celltype_annotations.csv``，用于后续比较分析或结果交付。

.. note::

   建议先完成 ``clustering`` 或 ``reclustering`` 并确认分群结构，再执行 ``reannotation``。若分群本身不稳定，重注释只能放大已有偏差。


准备映射表 annotation.txt
-------------------------

当前实现会跳过第一行，并读取第二行作为映射内容。第二行按逗号分隔，顺序对应 ``0,1,2...`` 的 cluster/recluster 编号。

.. code-block:: text

   celltype
   Tumor,T_cell,Fibroblast,Endothelial

上例表示 ``0->Tumor``、``1->T_cell``、``2->Fibroblast``、``3->Endothelial``。如存在更多编号，请在同一行继续补齐。


Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=reannotation --annotation-file=annotion.txt
   spatialsnake compare_analysis sample.txt visium --option=annotion --anno_algorithm=reannotation --annotation-file=annotion.txt


运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--anno_algorithm``
     - ``reannotation``
     - 指定进入重注释分支
   * - ``--annotation-file``
     - ``annotion.txt``
     - 注释映射文件路径（核心参数）
   * - ``--results_folder``
     - ``results``
     - 结果目录根路径

说明：``reannotation`` 分支实际核心只依赖 ``--anno_algorithm`` 与 ``--annotation-file``；``shape_type``、``image_type``、``device`` 等注释模块通用参数在该分支中不参与主要计算。


运行可选的参数设置(配置文件版)
------------------------------------------------------------
若您希望在多次修订中保持参数可复现，建议使用 yaml 管理。

运行下列命令获取 yaml 模板

.. code-block:: bash

   spatialsnake produce-file --option=annotion

在 ``annotion.yaml`` 中，``reannotation`` 常用字段如下：

.. code-block:: text

   anno_algorithm: reannotation
   annotion_list: annotion.txt
   results_folder: results
   run_type: visium
   channel: single_analysis

其中 ``annotion_list`` 对应命令行 ``--annotation-file``。


运行最终运行命令吧
----------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=annotion --configfile annotion.yaml


结果文件结构
------------

当前示例为单样本 ``visium`` 重注释。建议先确认 ``{sample}.zarr`` 与 ``celltype_annotations.csv`` 已生成，再进入下游分析。

.. code-block:: text

   results/
   └── {sample}/
       └── reannotation/
           ├── {sample}.zarr/                 # slide_seq 下为 {sample}.h5ad
           └── celltype_annotations.csv

其中，``{sample}.zarr``（或 ``.h5ad``）包含更新后的 ``obs['celltype']``；``celltype_annotations.csv`` 是标准化导出表，适合外部共享与复核。


多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 场景
     - 推荐命令
   * - 单样本（常规 zarr 平台：visium / xenium / visium_segment）
     - ``spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=reannotation --annotation-file=annotion.txt``
   * - 单样本（visium_HD）
     - ``spatialsnake single_analysis sample.txt visium_HD --option=annotion --anno_algorithm=reannotation --annotation-file=annotion.txt``
   * - 单样本（slide_seq）
     - ``spatialsnake single_analysis sample.txt slide_seq --option=annotion --anno_algorithm=reannotation --annotation-file=annotion.txt``
   * - 多样本联合对象重注释
     - ``spatialsnake compare_analysis sample.txt visium --option=annotion --anno_algorithm=reannotation --annotation-file=annotion.txt``


关键参数建议
------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - 参数类别
     - 单样本建议
     - 多样本或跨条件建议
   * - 映射表（``annotion_list`` / ``--annotation-file``）
     - 先覆盖主要群体，再细化边缘簇命名
     - 联合对象建议先统一命名体系，再分条件细化
   * - ``anno_algorithm``
     - 固定为 ``reannotation``，保证走重注释逻辑
     - 多样本迭代时保持一致，避免不同分支混用导致结果不可比
   * - 结果目录（``results_folder``）
     - 默认即可
     - 建议按版本区分目录，便于记录多轮注释修订


输入输出结构的差异
------------------
``reannotation`` 读取下游对象路径，而不是原始测序目录。建议 ``sample.txt`` 第二列填写 ``clustering`` 或 ``reclustering`` 阶段输出对象。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 分析模式
     - 输入
     - 输出
   * - single_analysis（常规 zarr 类型）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；``input_path`` 常用 ``results/{sample}/clustering/{sample}.zarr`` 或 ``results/{sample}/reclustering/{sample}.zarr``
     - ``results/{sample}/reannotation/{sample}.zarr`` 与 ``results/{sample}/reannotation/celltype_annotations.csv``
   * - single_analysis（visium_HD）
     - ``sample.txt`` 至少包含 ``sample_id input_path bin``；``input_path`` 常用 ``results/{sample}_{bin}um/clustering/{sample}.zarr``
     - ``results/{sample}/reannotation/{sample}.zarr`` 与 ``results/{sample}/reannotation/celltype_annotations.csv``
   * - single_analysis（slide_seq）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；``input_path`` 常用 ``results/{sample}/clustering/{sample}.h5ad``
     - ``results/{sample}/reannotation/{sample}.h5ad`` 与 ``results/{sample}/reannotation/celltype_annotations.csv``
   * - compare_analysis
     - ``sample.txt`` 至少包含 ``sample_id input_path group``；在该模式下通常提供联合对象路径并执行统一重注释
     - 汇总输出位于 results/merge_data/reannotation/concatenated_sdata（流程目标）并伴随导出注释表


结果解读
----------------

建议按“结果展示 → 解释 → 回调建议”的顺序判读。

1. 重注释对象（``{sample}.zarr`` / ``{sample}.h5ad``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入文件路径：results/.../reannotation/{sample}.zarr]

解释：
该对象保存更新后的 ``celltype`` 列，是后续差异分析、比较分析和可视化的主输入。脚本会优先依据 ``recluster`` 映射，若不存在则回退到 ``clusters``。

建议：
优先检查 ``obs['celltype']`` 的类别数量与映射表是否一致；若大量 ``Unknown``，通常提示映射表长度不足或编号不匹配。

2. 注释导出表（``celltype_annotations.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入文件路径：results/.../reannotation/celltype_annotations.csv]

解释：
该文件记录条形码与最终注释标签对应关系，便于交付、人工复核或外部分析工具调用。

建议：
抽样核对高占比细胞类型在对象与 CSV 中是否一致，确保导出过程未发生样本列错配。

3. ``Unknown`` 标签占比
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（统计占位）：

.. code-block:: text

   [在此插入统计：Unknown 占比 = X%]

解释：
``Unknown`` 来自未命中映射项的 cluster/recluster 编号，是重注释质量最直接的报警信号。

建议：
若占比偏高，优先补全映射表；若仅集中在极小簇，可回到聚类阶段评估是否为噪声簇并决定是否合并。


结果检查与下一步
----------------
建议在进入 ``compare_stage`` 或其他下游步骤前完成以下检查：

1. 输出对象中 ``obs['celltype']`` 已生成，且类别数量与预期一致。
2. ``celltype_annotations.csv`` 可正常读取，且与对象内部标签一致。
3. ``Unknown`` 占比在可接受范围内，主要细胞群体已完成明确命名。

若任一项不满足，建议先修订 ``annotion.txt`` 并重跑 ``reannotation``，必要时回到 ``clustering`` 或 ``reclustering`` 调整分群后再注释。
