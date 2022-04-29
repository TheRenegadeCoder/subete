Usage
=====

Interested in interacting with the Sample Programs
library in Python? Then subete is the official way
to do it! 

Installation
------------

To get started, download and install subete 
using pip:

.. code-block:: Shell

    pip install subete

Basic Usage
-----------

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

    languages = list(repo)

From there, you can browse the individual sample programs
available for each language:

.. code-block:: Python

    programs = list(languages)

Finally, you can access information about each individual
program. For example, you can retrieve the raw code as
follows:

.. code-block:: Python

    code = programs[0].code()

There are many ways to interact with the repo. Feel free
to use this Python API as needed. 

Advanced Usage
--------------

Depending on your needs, Subete can be used to
access information in more direct ways. For example,
both the Repo and LanguageCollection objects are
dictionaries under the hood. Rather than exposing
that data, we made the objects directly subscriptable.
For example, if you want to check out the Python
collection, the following will get you there:

.. code-block:: Python

    python_code = repo["Python"]

And to access an explicit program, you can use the
any of the existing project names:

.. code-block:: Python

    python_hello_world = repo["Python"]["Hello World"]

In addition to being subscriptable, both objects are
also iterable. For example, to iterate over all of the
languages in the repo, you can use the following:

.. code-block:: Python

    for language in repo:
        print(language)

Unsurprisingly, the same can be done for each language:

.. code-block:: Python

    for program in repo["Python"]:
        print(program)

Beyond that, the API is available for looking up
any additional information you made need for each
program or language. 
