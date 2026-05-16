Subcluster Annotation
=====================

This module focuses on iterative refinement after the initial major-cell-type annotation.
It is intended for cases where a broad cell class has already been identified and you now need to resolve finer subpopulations and assign biologically meaningful labels.

The recommended order is:

1. Run ``reclustering`` on a selected subset to identify finer subclusters.
2. Run ``reannotation`` to assign interpretable labels to those refined groups.

Before starting this module, make sure the upstream object is already stable and the target population has been isolated appropriately.

.. toctree::
   :maxdepth: 1
   :titlesonly:

   reclustering
   reannotation
