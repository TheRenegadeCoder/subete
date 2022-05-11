Documentation
=============

The documentation page lists out all of the relevant classes
and functions for interacting with the Sample Programs repo.

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

subete.Repo
-------------------------

.. autoclass:: subete.repo.Repo
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __iter__, __getitem__

subete.LanguageCollection
-------------------------

.. autoclass:: subete.repo.LanguageCollection
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __iter__, __getitem__, __str__

subete.SampleProgram
-------------------------

.. autoclass:: subete.repo.SampleProgram
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __str__, __eq__

subete.Project
-------------------------

.. autoclass:: subete.repo.Project
   :members:
   :undoc-members:
   :show-inheritance:
