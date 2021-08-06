Documentation
=============

The documentation page lists out all of the relevant classes
and functions for generating markdown documents in Python.

subete
-------------------

The subete module contains all the classes need to represent the Sample Programs repo.
This module was designed with the intent of creating read-only objects that fully
represent the underlying repo. Ideally, classes that make use of these objects
should not need to know how they were generated. For example, we do not want users
to poke around the source directory that was used to generate these files. As a result,
users should make use of the public methods only.

.. automodule:: subete
   :members:

.. automodule:: subete.repo
   :members:
   :undoc-members:
   :show-inheritance:
