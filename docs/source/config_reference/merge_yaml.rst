merge.yaml 参数说明
===================

该配置文件对应 ``spatialsnake useful_tool --option=merge``，用于对象拼接与外部注释回写。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - 参数
     - 默认值
     - 作用
   * - ``output_dir``
     - ``results/useful_results``
     - 合并结果目录。
   * - ``merge_by``
     - ``sample``
     - 合并策略（sample/clusters/celltype/reannotation）。
   * - ``reordering``
     - ``False``
     - 是否重排簇标签顺序。
   * - ``re_sample``
     - ``False``
     - 是否重建样本名。
   * - ``cluster_key``
     - ``clusters``
     - 聚类字段名称。
   * - ``annotation_csv``
     - ``""``
     - 外部注释文件路径（reannotation 分支）。
   * - ``csv_cell_col``
     - ``Barcode``
     - 外部注释中细胞 ID 列名。
   * - ``csv_label_col``
     - ``Grouped_Annotation``
     - 外部注释中标签列名。
   * - ``input_cell_col``
     - ``cell_id``
     - 输入对象细胞 ID 列名。
   * - ``target_col``
     - ``sub_celltype``
     - 回写目标列名。
   * - ``original_celltype_col``
     - ``celltype``
     - 回写失败时的原始标签参考列。

调参建议
--------

1. 常规合并仅需 ``merge_by`` 与 ``output_dir``。
2. 外部注释回写必须优先核对 ``csv_cell_col`` 与 ``input_cell_col``。
3. 回写新标签时建议修改 ``target_col``，保留原始 ``celltype`` 便于追溯。
