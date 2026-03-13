模块 0：下游输入规范
====================

下游模块统一走 ``--option=advance_analysis``，输入通常为已注释对象（``annotion`` 输出）。

准备 ``sample.txt``
--------------------

.. code-block:: text

   S1    results/S1/annotion/S1.zarr

统一命令入口
------------

.. code-block:: bash

   spatialsnake single_analysis sample.txt visium --option=advance_analysis --runpipe=<module>

可选模块
--------

- ``cellPhoneDB``
- ``pysenic``
- ``liana``
- ``cellcharter``
- ``banksy``
- ``cellchat``
