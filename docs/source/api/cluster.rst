jip.cluster
===========

.. automodule:: jip.cluster

Methods
-------
.. autofunction:: jip.cluster.get

Abstract Cluster class
----------------------
.. autoclass:: jip.cluster.Cluster
    :members:

Exceptions
----------
.. autoexception:: jip.cluster.SubmissionError

.. autoexception:: jip.cluster.ClusterImplementationError

Implementations
---------------
.. autoclass:: jip.cluster.Slurm
    :members:

.. autoclass:: jip.cluster.SGE
    :members:

.. autoclass:: jip.cluster.PBS
    :members:

.. autoclass:: jip.cluster.LSF
    :members:

