人工注释（mannul）
==================

``mannul`` 是 ``annotion`` 步骤中的手动注释分支，用于将 ``clusters`` 映射为可解释的 ``celltype`` 标签，并将结果写回分析对象。
与 ``annotion_help`` 的 marker 推断不同，``mannul`` 不再自动生成新注释结论，而是执行“您给出映射表 -> 管线回写标签并导出结果”的标准化流程。

注释的依据为annotation_help中的marker_genes_pval.csv基因列表，您可通过气泡图等方式可视化出已有文献所发现的marker基因查看是否在此数据集合中高度表达
同时，若您觉得为每个cluster都查询marker基因的操作繁琐，可以使用现有的高级工具 如GPT celltype 等，利用大语言模型给出注释建议节省时间。

处理逻辑概述
------------
1. 读取 ``sample.txt`` 第二列指向的下游对象（``.zarr`` 或 ``.h5ad``）。
2. 读取注释映射文件并解析 cluster 到 celltype 的对应关系。
3. 将 ``obs['clusters']`` 映射为 ``obs['celltype']`` 并写回对象。
4. 输出 UMAP、比例图、空间叠加图（非 slide_seq）与注释导出表。
5. 生成 ``annotion`` 阶段对象，供后续比较分析或下游模块复用。

.. note::

   建议先完成 ``annotion_help`` 并确认 marker 与通路证据后，再进入 ``mannul``。若映射表与真实 cluster 语义不一致，后续比较分析会放大误差。


准备映射表annotation.txt
-------------------------

当前实现会跳过第一行，并读取第二行作为注释内容。第二行按逗号分隔，顺序对应 ``cluster 0,1,2...``。

.. code-block:: text

   celltype
   Tumor,T_cell,Fibroblast

上例表示 ``0->Tumor``、``1->T_cell``、``2->Fibroblast``。若您的聚类有更多编号，请继续在同一行补齐。


Run the command
------------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt
   spatialsnake compare_analysis sample.txt visium_HD --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt


运行可选的参数设置(命令行版)
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 18 58

   * - 参数
     - 示例
     - 作用
   * - ``--anno_algorithm``
     - ``mannul``
     - 指定进入手动注释分支
   * - ``--annotation-file``
     - ``annotion.txt``
     - 指定 cluster 到 celltype 的映射文件
   * - ``--image_type``
     - ``hires``
     - 多图层对象中用于空间叠加图筛选的图像关键字
   * - ``--shape_type``
     - ``cell_boundaries``
     - 空间形状图层关键字（用于形状渲染筛选）

其中 ``--anno_algorithm`` 与 ``--annotation-file`` 为手动注释核心参数；``--image_type``、``--shape_type`` 主要影响可视化输出，不改变注释映射本身。


运行可选的参数设置(配置文件版)
------------------------------------------------------------
若您需要在多轮注释迭代中保持参数可复现，建议使用 yaml 统一管理。

请参考配置文件并根据下述说明进行设置 :doc:`../config_reference/annotion_yaml`。

运行下列命令获取 yaml 模板

.. code-block:: bash

   spatialsnake produce-file --option=annotion

在 ``annotion.yaml`` 中，``mannul`` 分支常用字段包括：

.. code-block:: text

   anno_algorithm: mannul
   annotion_list: annotion.txt
   image_type: hires
   shape_type: cell_boundaries
   image_slice: False


运行最终运行命令吧
----------------------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium_HD --option=annotion --configfile annotion.yaml


结果文件结构
------------

当前示例为 ``visium_HD`` 单样本手动注释。建议先确认 ``{sample}.zarr`` 与 ``*_cell_clusters.csv`` 已生成，再检查图像是否支持您的注释结论。

.. code-block:: text

   results/
   └── {sample}_{bin}um/
       └── annotion/
           ├── {sample}.zarr/
           ├── celltype_proportion.png
           ├── {sample}UMAP.png
           ├── {sample}_gene_enrich.png
           ├── [image]_Clusters.png
           ├── {region}_cell_clusters.csv
           └── ...

其中，``{sample}.zarr`` 是后续分析复用的核心对象；``*_cell_clusters.csv`` 是用于外部审阅或下游工具对接的标签导出文件。
若 ``run_type=xenium``，导出命名会变为 ``*_cell_groups.csv``。


多样本/不同平台运行命令和结果差异性
------------------------------------

运行命令的差异
--------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 76

   * - 场景
     - 推荐命令
   * - 单样本（Visium HD，本节演示）
     - ``spatialsnake single_analysis sample.txt visium_HD --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt``
   * - 单样本（常规 zarr 平台：visium / xenium / visium_segment）
     - ``spatialsnake single_analysis sample.txt visium --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt``
   * - 单样本（slide_seq）
     - ``spatialsnake single_analysis sample.txt slide_seq --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt``
   * - 多样本联合对象手动注释
     - ``spatialsnake compare_analysis sample.txt visium --option=annotion --anno_algorithm=mannul --annotation-file=annotion.txt``


关键参数建议
------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - 参数类别
     - 单样本建议
     - 多样本或跨条件建议
   * - 注释映射表（``annotion_list`` / ``--annotation-file``）
     - 按 cluster 编号顺序完整填写，先覆盖主要群体
     - 先基于整合对象统一命名体系，再细化到样本差异
   * - ``image_type`` / ``shape_type``
     - 先用默认值快速出图，确认注释方向
     - 所有样本保持同一图层类型，减少可视化基准偏移
   * - ``image_slice`` + 坐标
     - 通常关闭，先评估全局组织结构
     - 仅在目标区域复核时开启，并固定裁剪坐标用于复现


输入输出结构的差异
------------------
``mannul`` 读取的是下游对象路径，而不是原始测序目录。建议在 ``sample.txt`` 第二列填写 clustering 或 annotion_help 之后的对象路径。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 分析模式
     - 输入
     - 输出
   * - single_analysis（常规 zarr 类型）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；``input_path`` 常用 ``results/{sample}/clustering/{sample}.zarr``
     - ``results/{sample}/annotion/{sample}.zarr`` 与 ``results/{sample}/annotion/*_cell_clusters.csv``
   * - single_analysis（visium_HD）
     - ``sample.txt`` 至少包含 ``sample_id input_path bin``；``input_path`` 常用 ``results/{sample}_{bin}um/clustering/{sample}.zarr``
     - ``results/{sample}_{bin}um/annotion/{sample}.zarr`` 与 ``results/{sample}_{bin}um/annotion/*_cell_clusters.csv``
   * - single_analysis（slide_seq）
     - ``sample.txt`` 至少包含 ``sample_id input_path``；``input_path`` 常用 ``results/{sample}/clustering/{sample}.h5ad``
     - ``results/{sample}/annotion/{sample}.h5ad`` 与 ``results/{sample}/annotion/*_cell_clusters.csv``
   * - compare_analysis
     - ``sample.txt`` 至少包含 ``sample_id input_path group``（visium_HD 需额外 ``bin``）；当前实现会基于联合对象执行映射
     - ``results/merge_data/annotion/concatenated_sdata`` 与 ``results/merge_data/annotion/*_cell_clusters.csv``


结果解读
----------------

建议按“结果展示 → 解释 → 回调建议”的顺序判读，并始终回到 ``annotion_help`` 的 marker 证据进行交叉验证。

1. 注释后 UMAP（``{sample}UMAP.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/annotation/mannul/UMAP.png]

解释：
UMAP 主要用于观察映射后的 ``celltype`` 在低维空间中的分离与过渡关系。若多个细胞类型高度重叠且缺乏过渡梯度，常提示映射粒度与聚类分辨率不匹配。

建议：
优先回查映射表是否把生物学差异较大的 cluster 合并到了同一 celltype，必要时先调整 cluster 层级再重做映射。

2. 空间叠加图（``[image]_Clusters.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/annotation/mannul/[image]_Clusters.png]

解释：
该图用于检查注释后细胞类型在组织空间中的位置是否合理。若某类型呈现离散噪点式散布且与组织学结构不符，需警惕误映射或聚类噪声。

建议：
将空间连贯性与 UMAP 结构联合评估，只有两者一致时再固定最终命名。

3. 组成比例图（``celltype_proportion.png``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（图片占位）：

.. code-block:: text

   [在此插入图片路径：/_static/images/annotation/mannul/celltype_proportion.png]

解释：
比例图用于比较不同区域/样本中的 celltype 组成。若某类型在单一区域异常富集，需结合组织背景与采样策略判断是生物学信号还是技术偏差。

建议：
在多样本场景中先确认样本规模与测序深度差异，再解释比例变化，避免将规模效应误判为生物学差异。

4. 导出注释表（``*_cell_clusters.csv`` 或 ``*_cell_groups.csv``）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

结果展示（文件占位）：

.. code-block:: text

   [在此插入文件路径：results/.../annotion/*_cell_clusters.csv]

解释：
该文件提供条形码到注释标签的直接映射，是后续差异分析、可视化平台共享与人工复核的标准交换格式。

建议：
在进入下游分析前，先抽样核对若干高占比 celltype 的条形码映射是否与原对象 ``obs['celltype']`` 一致。


结果检查与下一步
----------------
建议在进入比较分析或高级分析前完成以下检查：

1. 输出对象中已包含 ``obs['celltype']`` 且类别数量与映射预期一致。
2. UMAP、空间叠加图与比例图对主要 celltype 的结论一致。
3. ``*_cell_clusters.csv``（或 xenium 的 ``*_cell_groups.csv``）可被外部工具正常读取。

若以上任一项不满足，建议先修订映射表并重跑 ``mannul``，必要时回到 ``annotion_help`` 重新核对 marker 与通路证据。
