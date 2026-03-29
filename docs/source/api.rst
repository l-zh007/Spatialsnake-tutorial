Contribution and Software Version
=================================

我们的自动化工具基于snakemake框架搭建，采用 ``Python CLI + Snakemake workflow + rule/script`` 的分层结构。
若您想为我们的工具贡献代码或新增模块，建议Fork 仓库并创建功能分支


框架总览
--------

1. 命令行入口（``spatialsnake/command_line.py``）负责解析参数、加载配置、拼接 Snakemake 命令。
2. 调度层（``spatialsnake/workflow/Snakefile``）负责根据 ``option`` 与 ``runpipe`` 选择规则文件。
3. 执行层（``spatialsnake/workflow/rules/*.smk`` + ``spatialsnake/workflow/scripts/*``）负责具体分析任务。
4. 环境层（``environment.yml`` + ``requirements.txt`` + ``spatialsnake/workflow/envs/*.yaml``）负责基础运行环境与步骤配置。

该设计使“参数管理、流程调度、算法实现”相互解耦，便于扩展新模块并保持复现性。


How Snakemake organized
--------------------------

在当前实现中，命令行会自动执行如下核心流程：

1. 根据 ``--option`` 读取默认配置文件 ``spatialsnake/workflow/envs/{option}.yaml``（或使用自定义 ``--configfile``）。
2. 将 ``sample_list``、``channel``、``run_type`` 等关键参数传入 Snakemake ``--config``。
3. 在 ``workflow/Snakefile`` 内依据 ``option`` / ``runpipe`` 分支 ``include`` 对应 ``rules/*.smk``。
4. ``rule all`` 聚合目标输出，保证任务只在目标文件缺失或过期时重跑。

核心调度分支可概括为：

- integrate / preprocess / clustering / reclustering / annotion_help / annotion
- advance_analysis（通过 runpipe 分发到 cellPhoneDB、pysenic、liana、cellcharter、banksy、cellchat）
- compare_stage（差异比较与 CellChat 比较）


GitHub 贡献与模块复写
---------------------

项目主页与问题反馈入口：

- Homepage: https://github.com/l-zh007/spatialsnake
- Issues: https://github.com/l-zh007/spatialsnake/issues

建议贡献路径（适用于新增模块或复写现有模块）：

1. Fork 仓库并创建功能分支（例如 ``feature/new_module``）。
2. 在 ``spatialsnake/workflow/scripts/`` 中新增或复写分析脚本。
3. 在 ``spatialsnake/workflow/rules/`` 中新增规则文件，并声明输入、输出、日志与 shell/python 调用。
4. 在 ``spatialsnake/workflow/Snakefile`` 中注册新分支（``option`` 或 ``runpipe``）及对应输出目标。
5. 在 ``spatialsnake/workflow/envs/`` 增补默认 YAML 参数模板，确保命令行可自动加载。
6. 如涉及新 CLI 行为，同步更新 ``spatialsnake/command_line.py`` 的可选项与参数解析。
7. 同步更新教程页面与配置说明后，提交 Pull Request 并在说明中附最小可复现实验命令。

建议在 PR 中至少说明以下信息：

- 模块输入对象格式（``.zarr/.h5ad/.rds`` 等）
- 输出文件清单与关键字段
- 默认参数与可调参数范围
- 典型单样本与多样本运行命令


Software Version
----------------

以下版本来自项目环境文件与依赖文件（锁定版本）：

.. list-table:: Core runtime (from ``environment.yml``)
   :header-rows: 1
   :widths: 36 20 44

   * - 组件
     - 版本
     - 说明
   * - Python
     - 3.12.11
     - 主运行时版本
   * - snakemake-minimal
     - 9.8.1
     - 工作流调度核心
   * - snakemake-interface-common
     - 1.20.2
     - Snakemake 接口层
   * - snakemake-interface-executor-plugins
     - 9.3.8
     - 执行器插件接口
   * - snakemake-interface-storage-plugins
     - 4.2.1
     - 存储插件接口
   * - pip
     - 25.2
     - Python 包管理

.. list-table:: Key Python packages (from ``requirements.txt``)
   :header-rows: 1
   :widths: 36 20 44

   * - 包
     - 版本
     - 用途
   * - spatialdata
     - 0.5.0
     - 统一空间转录组对象
   * - spatialdata-io
     - 0.3.0
     - 多平台读写支持
   * - spatialdata-plot
     - 0.2.11
     - 空间可视化
   * - scanpy
     - 1.10.4
     - 单细胞/空间下游分析基础
   * - anndata
     - 0.12.0
     - 矩阵与注释数据结构
   * - squidpy
     - 1.6.5
     - 空间邻域与图分析
   * - cellphonedb
     - 5.0.1
     - 配体-受体通讯分析
   * - cell2location
     - 0.1.5
     - 细胞定位注释方法
   * - scvi-tools
     - 1.4.0
     - 深度生成模型工具集
   * - torch
     - 2.8.0
     - 深度学习后端
   * - numpy
     - 2.2.6
     - 数值计算
   * - pandas
     - 2.2.3
     - 表格处理
   * - scipy
     - 1.13.1
     - 科学计算
   * - scikit-learn
     - 1.7.2
     - 机器学习算法
   * - matplotlib
     - 3.9.4
     - 绘图基础
   * - pydeseq2
     - 0.5.2
     - 差异表达分析


Citation
--------

若在研究中使用 Spatialsnake，建议在方法学部分同时引用工作流框架与项目仓库：

1. paper:
2. Spatialsnake project repository: https://github.com/l-zh007/spatialsnake
