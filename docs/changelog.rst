Changelog
=========

Below you'll find all the changes that have been made to the code with
newest changes first.

0.19.x
------

* v0.19.0
    * Support extensions with mulitple dots (like TI-Basic which has an extension
        of ``.8xp.txt``)
    * Drop support for python 3.7.

0.18.x
------

* v0.18.1
    * Do not index sample programs that do not correspond to a valid project.

* v0.18.0
    * Add ability to get information about untestable languages.
    * Indicate support for python 3.11.
    * Upgrade PyYAML dependency to 6.x.

0.17.x
------

* v0.17.0
    * Added ability to get authors, date/time created, date/time modified for
      language, sample program, and project articles.

0.16.x
------

* v0.16.0
    * Added ability to detect if sample program is an image and return image type
    * Added ability to get path to sample program

0.15.x
------

* v0.15.0
    * Added ability to get sample program repository directory

0.14.x
------

* v0.14.0
    * Added a feature to lets you check if programs have sources for documentation

0.13.x
------

* v0.13.0
    * Updated subete to pull from archive and docs separately, rather than relying on submodules which might be out of date

0.12.x
------

* v0.12.1
    * Fixed an issue where older versions of Git could not handle use of blame

* v0.12.0
    * Reworked the way project names are parsed to support new naming conventions
    * Cleaned up error logs for readability

0.11.x
-------

* v0.11.2
    * Fixed a bug where code could not be loaded because the repo was deleted

* v0.11.1
    * Fixed an issue where local repo could cause stack overflow 
    * Added sections to the changelog

* v0.11.0
    * Added support for git data: SampleProgram objects now include authors, created dates, and modified dates 
    * Reorganized documentation, so objects have their own sections in the table of contents

0.10.x
-------

* v0.10.0
    * Added support for the Glotter testing file: users can now check if a project is tested by Glotter 

0.9.x
------

* v0.9.3
    * Changed docs dir to sources

* v0.9.2
    * Fixed an issue with the use of the SampleProgram constructor
    * Fixed an issue where the missing_programs() method did not work correctly

* v0.9.1
    * Updated official documentation
    * Fixed an issue where one of the type hints was wrong

* v0.9.0
    * Reworked several of the methods to use the new docs location for website

0.8.x
------

* v0.8.0
    * Updated URL from sample-programs.therenegadecoder.com to sampleprograms.io

0.7.x
------

* v0.7.2
    * Fixed a bug where the missing programs list shared the entire path 

* v0.7.1
    * Fixed a bug where the missing programs feature failed for provided repos 

* v0.7.0
    * Added Plausible support for analytics
    * Added feature which allows us to retrieve list of missing programs for a language

0.6.x
------

* v0.6.0
    * Added random program functionality
    * Fixed several documentation issues
    * Renamed some repo functions to match naming conventions
    * Expanded testing to include tests for random functions

0.5.x
------

* v0.5.0
    * Updated README to indicate alpha stage of project
    * Added logging support
    * Added method of retrieving pathlike name of LanguageCollection
    * Fixed type hinting of sample_programs() method
    * Removed extraneous print statement
    * Made Repo and LanguageCollection subscriptable

0.4.x
------

* v0.4.1
    * Fixed an issue where generated links were broken

* v0.4.0
    * Forced a convention for LanguageCollection and SampleProgram as strings
    * Added test URL functionality to LanguageCollection
    * Created usage docs

0.3.x
------

* v0.3.1
    * Fixed an issue where provided source directories would not run correctly

* v0.3.0
    * Refactored the majority of the underlying library
    * Added testing for Python 3.6 to 3.9

0.2.x
------

* v0.2.1
    * Fixed an issue where documentation wouldn't build due to sphinx_issues dependency

* v0.2.0
    * Added support for Sphinx documentation

0.1.x
------

* v0.1.0
    * Launches the library under the exact conditions it was in when it was removed from sample-programs-docs-generator
