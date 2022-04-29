import logging
import os
from pathlib import Path
import re
from subete.repo import LanguageCollection

logger = logging.getLogger(__name__)


class SampleProgram:
    """
    An object representing a sample program in the repo.

    :param str path: the path to the sample program without the file name
    :param str file_name: the name of the file including the extension
    :param LanguageCollection language: a reference to the programming language 
        collection of this sample program
    """

    def __init__(self, path: str, file_name: str, language: LanguageCollection) -> None:
        self._path = path
        self._file_name = file_name
        self._language = language
        self._normalized_program_name: str = self._normalize_program_name()
        self._sample_program_req_url: str = self._generate_requirements_url()
        self._sample_program_doc_url: str = self._generate_doc_url()
        self._sample_program_issue_url: str = self._generate_issue_url()
        self._line_count: int = len(self.code().splitlines())

    def __str__(self) -> str:
        """
        Renders the Sample Program in the following form: {name} in {language}.

        :return: the sample program as a string
        """
        return f'{self.project_name()} in {self.language_collection()}'

    def __eq__(self, o: object) -> bool:
        """
        Compares an object to the sample program. Returns True if the object
        is an instance of SampleProgram and has the following three fields:

            - _file_name
            - _path
            - _language

        :return: True if the object matches the Sample Program; False otherwise.
        """
        if isinstance(o, self.__class__):
            return self._file_name == o._file_name and self._path == self._path and self._language == o._language
        return False

    def size(self) -> int:
        """
        Retrieves the size of the sample program in bytes. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            size: int = program.size()

        :return: the size of the sample program as an integer
        """
        relative_path = os.path.join(self._path, self._file_name)
        return os.path.getsize(relative_path)

    def language_collection(self) -> LanguageCollection:
        """
        Retrieves the language collection object that this sample 
        program is a part of.  

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.language_collection()

        :return: the language collection that this program belongs to.
        """
        return self._language

    def language_name(self) -> str:
        """
        Retrieves the language name for this sample program. Language
        name is generated from a call to str() for the source
        LanguageCollection. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.language_name()

        :return: the programming language as a titlecase string (e.g., Python)
        """
        return str(self._language)

    def language_pathlike_name(self) -> str:
        """
        Retrieves the language name in the form of a path for URL purposes.
        This is a convenience method that pulls directly from language
        collection's `pathlike_name()` method.

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.language_pathlike_name()

        :return: the language name as a path name (e.g., google-apps-script, python)
        """
        return self._language.pathlike_name()
    
    def project_name(self) -> str:
        """
        Retrieves the project name of this sample program. Project name is
        generated from the file name. Specifically, multiword project names
        are converted to titlecase (e.g., Convex Hull) while acronyms of 
        three or less characters are uppercased (e.g., LPS).

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.project_name()

        :return: the project name as a titlecase string (e.g., Hello World, MST)
        """
        return (
            self._normalized_program_name.replace("-", " ").title() 
            if len(self._normalized_program_name) <= 3 
            else self._normalized_program_name.upper()
        )

    def project_pathlike_name(self) -> str:
        """
        Retrieves the project name in the form of a path for URL purposes.

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.project_pathlike_name()

        :return: the project name as a path name (e.g., hello-world, convex-hull)
        """
        return self._normalized_program_name

    def code(self) -> str:
        """
        Retrieves the code for this sample program. To save space
        in memory, code is loaded from the source file on each invocation 
        of this method. As a result, there may be an IO performance
        penalty if this function is used many times. It's recommended
        to store the result of this function if it is used often.

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            code: str = program.code()

        :return: the code for the sample program as a string
        """
        logger.debug(
            f"Attempting to retrieve code from {self._path}/{self._file_name}")
        return Path(self._path, self._file_name).read_text(errors="replace")

    def line_count(self) -> int:
        """
        Retrieves the number of lines in the sample program. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            code: int = program.line_count()

        :return: the number of lines for the sample program as an integer
        """
        return self._line_count

    def requirements_url(self) -> str:
        """
        Retrieves the URL to the requirements documentation for
        this sample program. Requirements URL is assumed to exist
        and therefore not validated. The requirements documentation 
        URL is in the following form:

        ``https://sampleprograms.io/projects/{project}/``

        For example, here is a link to the
        `Hello World documentation <https://sampleprograms.io/projects/hello-world/>`_. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            url: str = program.requirements_url()

        :return: the requirments URL as a string 
        """
        return self._sample_program_req_url

    def documentation_url(self) -> str:
        """
        Retrieves the URL to the documentation for this
        sample program. Documentation URL is assumed to exist
        and therefore not validated. The documentation 
        URL is in the following form:

        ``https://sampleprograms.io/projects/{project}/{lang}/``

        For example, here is a link to the
        `Hello World in Python documentation <https://sampleprograms.io/projects/hello-world/python/>`_. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            url: str = program.documentation_url()

        :return: the documentation URL as a string
        """
        return self._sample_program_doc_url

    def article_issue_query_url(self) -> str:
        """
        Retrieves the URL to the article issue query for this sample
        program. The article issue query URL is guaranteed to be a valid
        search query on GitHub, but it is not guaranteed to have any 
        results. The issue query url is in the following form:

        ``https://github.com//TheRenegadeCoder/sample-programs-website/issues?{query}"``

        For example, here is a link to the
        `Hello World in Python query <https://github.com/TheRenegadeCoder/sample-programs-website/issues?q=is%3Aissue+is%3Aopen+hello+world+python>`_. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            url: str = program.article_issue_query_url()

        :return: the issue query URL as a string
        """
        return self._sample_program_issue_url

    def _normalize_program_name(self) -> str:
        """
        A helper function which converts the program name into
        a standard representation (i.e. hello_world -> hello-world).

        :return: the sample program as a lowercase string separated by hyphens
        """
        stem = os.path.splitext(self._file_name)[0]
        if len(stem.split("-")) > 1:
            url = stem.lower()
        elif len(stem.split("_")) > 1:
            url = stem.replace("_", "-").lower()
        else:
            # TODO: this is brutal. At some point, we should loop in the glotter test file.
            url = re.sub(
                '((?<=[a-z])[A-Z0-9]|(?!^)[A-Z](?=[a-z]))', r'-\1', stem).lower()
        logger.info(f"Constructed a normalized form of the program {url}")
        return url

    def _generate_requirements_url(self) -> str:
        """
        A helper method for generating the expected requirements URL 
        for this sample program.

        :return: the expected requirements URL 
        """
        doc_url_base = "https://sampleprograms.io/projects"
        if "export" in self._normalized_program_name or "import" in self._normalized_program_name:
            return f"{doc_url_base}/import-export"
        else:
            return f"{doc_url_base}/{self._normalized_program_name}"

    def _generate_doc_url(self) -> str:
        """
        A helper method for generating the expected docs URL for
        this sample program.

        FYI: this function depends on _sample_program_req_url, so
        it must be generated first. 

        :return: the expected docs URL
        """
        return f"{self._sample_program_req_url}/{Path(self._path).name}"

    def _generate_issue_url(self) -> str:
        """
        A helper method for generating the expected issues URL for
        this sample program. 

        :return: the expected issues URL
        """
        issue_url_base = "https://github.com//TheRenegadeCoder/" \
                         "sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"
        program = self._normalized_program_name.replace("-", "+")
        return f"{issue_url_base}{program}+{str(self._language).replace(' ', '+').lower()}"
