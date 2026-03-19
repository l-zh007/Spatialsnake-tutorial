compare_stage.yaml 参数说明
============================

该配置文件对应 ``--option=compare_stage``，用于差异表达比较与双样本 CellChat 网络比较。

.. list-table::
   :header-rows: 1
   :widths: 32 20 48

   * - 参数
     - 默认值
     - 作用
   * - ``option``
     - ``compare_stage``
     - 固定阶段标识。
   * - ``results_folder`` / ``data_fold`` / ``sample_list``
     - ``results`` / ``data`` / ``sample.txt``
     - 输出目录、数据目录与样本表。
   * - ``run_type`` / ``channel``
     - ``visium`` / ``compare_analysis``
     - 平台与通道。
   * - ``runpipe``
     - ``compare_gene``
     - 比较分支选择（``compare_gene`` 或 ``cellchat``）。
   * - ``compare_algorithm``
     - ``DEseq2``
     - 差异表达算法。
   * - ``cell_focus``
     - ``CAF``
     - 关注的细胞类型。
   * - ``spacies``
     - ``human``
     - 富集背景物种。
   * - ``cellchat_compare_output_dir``
     - ``results/compare_cellchat``
     - CellChat 比较结果目录。
   * - ``cellchat_compare_sample_name1`` / ``cellchat_compare_sample_name2``
     - ``group_Non_Lesional`` / ``group_Lesional``
     - 两组显示名称。
   * - ``cellchat_compare_pathways``
     - ``""``
     - 指定比较通路列表。
   * - ``cellchat_compare_source_cells`` / ``cellchat_compare_target_cells``
     - ``1,2,3`` / ``1,2,3``
     - 发送端与接收端细胞筛选。
   * - ``cellchat_compare_receiver_cells``
     - ``1,2,3``
     - aggregate 图接收端设置。
   * - ``cellchat_compare_bubble_angle``
     - ``45``
     - 气泡图坐标角度。
   * - ``cellchat_compare_bubble_remove_isolate``
     - ``True``
     - 是否去除孤立节点。
   * - ``cellchat_compare_do_ranknet`` / ``cellchat_compare_do_role_heatmap``
     - ``True`` / ``False``
     - 是否输出 rankNet 与角色热图。
   * - ``cellchat_compare_do_pathway_plots`` / ``cellchat_compare_do_compare_overview``
     - ``True`` / ``True``
     - 是否输出通路汇总与总体比较图。
   * - ``cellchat_compare_do_compare_bubble`` / ``cellchat_compare_do_single_bubble``
     - ``True`` / ``True``
     - 是否输出双组和单组气泡图。
   * - ``cellchat_compare_do_gene_expression``
     - ``False``
     - 是否输出配体受体表达图。
   * - ``cellchat_compare_gene_colors``
     - ``white,#FEC44F,#D95F0E``
     - 表达图配色。
   * - ``cellchat_compare_gene_plot_type``
     - ``dot``
     - 表达图类型。
   * - ``cellchat_compare_save_merged``
     - ``True``
     - 是否保存合并对象。

调参建议
--------

1. ``runpipe=compare_gene`` 时优先关注 ``compare_algorithm`` 与 ``cell_focus``。
2. ``runpipe=cellchat`` 时优先明确 source/target 细胞与通路集合。
3. 图件较多时可先关闭部分 ``cellchat_compare_do_*`` 选项进行快速迭代。
