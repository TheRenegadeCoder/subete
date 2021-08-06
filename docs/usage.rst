Usage
=====

Interested in interacting with the Sample Programs
library in Python? Then subete is the official way
to do it! To get started, download and install subete 
using pip:

.. code-block:: Python

    pip install subete

From there, you can import the subete library as follows:

.. code-block:: Python

    import subete

Then, all that's left to do is to load the Sample Programs
repo:

.. code-block:: Python

    repo = subete.load()

Keep in mind that the load() function relies on Git being
available on the system to be able to clone the Sample
Programs repo. Alternatively, you can download the Sample
Programs repo yourself and supply the path as an argument:

.. code-block:: Python

    repo = subete.load(source_dir="path/to/sample-programs/archive")

With that out of the way, the rest is up to you! Feel free
to explore the repo as needed. For example, you can access
the list of languages as follows:

.. code-block:: Python

    languages = repo.language_collections()

From there, you can browse the individual sample programs
available for each language:

.. code-block:: Python

    programs = languages[0].sample_programs()

Finally, you can access information about each individual
program. For example, you can retrieve the raw code as
follows:

.. code-block:: Python

    code = programs[0].code()

There are many ways to interact with the repo. Feel free
to use this Python API as needed. 
