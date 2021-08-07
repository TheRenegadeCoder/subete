import logging
import os
import re
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

import git
import yaml

logger = logging.getLogger(__name__)


class SampleProgram:
    """
    An object representing a sample program in the repo.

    :param path: the path to the sample program without the file name
    :param file_name: the name of the file including the extension
    :param language: the programming language of this sample program
    """

    def __init__(self, path: str, file_name: str, language: str) -> None:
        self._path = path
        self._file_name = file_name
        self._language = language
        self._normalized_name: str = self._normalize_program_name()
        self._sample_program_req_url: str = self._generate_requirements_url()
        self._sample_program_doc_url: str = self._generate_doc_url()
        self._sample_program_issue_url: str = self._generate_issue_url()
        self._line_count: int = len(self.code().splitlines())

    def __str__(self) -> str:
        """
        Renders the Sample Program in the following form: {name} in {language}.

        :return: the sample program as a string
        """
        return f'{self.project()} in {self.language()}'

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

    def language(self) -> str:
        """
        Retrieves the language name for this sample program. Language
        name is generated from a call to str() for the source
        LanguageCollection. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.language()

        :return: the programming language as a titlecase string
        """
        return self._language

    def project(self) -> str:
        """
        Retrieves the project name of this sample program. Project name is
        generated from the file name.

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.project()

        :return: the project name as a titlecase string
        """
        return self._normalized_name.replace("-", " ").title()

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
        logger.debug(f"Attempting to retrieve code from {self._path}/{self._file_name}")
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

        ``https://sample-programs.therenegadecoder.com/projects/{project}/``

        For example, here is a link to the
        `Hello World documentation <https://sample-programs.therenegadecoder.com/projects/hello-world/>`_. 

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

        ``https://sample-programs.therenegadecoder.com/projects/{project}/{lang}/``

        For example, here is a link to the
        `Hello World in Python documentation <https://sample-programs.therenegadecoder.com/projects/hello-world/python/>`_. 

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
        return url

    def _generate_requirements_url(self) -> str:
        """
        A helper method for generating the expected requirements URL 
        for this sample program.

        :return: the expected requirements URL 
        """
        doc_url_base = "https://sample-programs.therenegadecoder.com/projects"
        if "export" in self._normalized_name or "import" in self._normalized_name:
            return f"{doc_url_base}/import-export"
        else:
            return f"{doc_url_base}/{self._normalized_name}"

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
        program = self._normalized_name.replace("-", "+")
        return f"{issue_url_base}{program}+{self._language.replace(' ', '+').lower()}"


class LanguageCollection:
    """
    An object representing a collection of sample programs files for a particular programming language.

    :param name: the name of the language (e.g., python)
    :param path: the path of the language (e.g., .../archive/p/python/)
    :param file_list: the list of files in language collection
    """

    def __init__(self, name: str, path: str, file_list: List[str]) -> None:
        self._name: str = name
        self._path: str = path
        self._file_list: List[str] = file_list
        self._first_letter: str = name[0]
        self._sample_programs: Dict[str, SampleProgram] = self._collect_sample_programs()
        self._test_file_path: Optional[str] = self._collect_test_file()
        self._read_me_path: Optional[str] = self._collect_readme()
        self._lang_docs_url: str = f"https://sample-programs.therenegadecoder.com/languages/{self._name}"
        self._testinfo_url: str = f"https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/{self._name[0]}/{self._name}/testinfo.yml"
        self._total_snippets: int = len(self._sample_programs)
        self._total_dir_size: int = sum(x.size() for _, x in self._sample_programs.items())
        self._total_line_count: int = sum(x.line_count() for _, x in self._sample_programs.items())

    def __str__(self) -> str:
        """
        Generates as close to the proper language name as possible given a language
        name in plain text separated by hyphens.

        | Example: google-apps-script -> Google Apps Script
        | Example: c-sharp -> C#

        :return: a readable representation of the language name
        """
        text_to_symbol = {
            "plus": "+",
            "sharp": "#",
            "star": r"\*"
        }
        tokens = [text_to_symbol.get(token, token) for token in self._name.split("-")]
        if any(token in text_to_symbol.values() for token in tokens):
            return "".join(tokens).title()
        else:
            return " ".join(tokens).title()

    def testinfo(self) -> Optional[dict]:
        """
        Retrieves the test data from the testinfo file. The YAML data
        is loaded into a Python dictionary.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            data: dict = language.testinfo()

        :return: the test info data as a dictionary
        """
        test_data = None
        if self._test_file_path:
            with open(self._test_file_path) as test_file:
                test_data = yaml.safe_load(test_file)
        return test_data

    def has_testinfo(self) -> bool:
        """
        Retrieves the state of the testinfo file. Helpful when
        trying to figure out if this language has a testinfo file.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            state: bool = language.has_testinfo()

        :return: True if a test info file exists; False otherwise
        """
        return bool(self._test_file_path)

    def readme(self) -> Optional[str]:
        """
        Retrieves the README contents. README contents are in
        the form of a markdown string.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            contents: str = language.readme()

        :return: the README contents as a string
        """
        if self._read_me_path:
            return Path(self._read_me_path).read_text()

    def sample_programs(self) -> List[SampleProgram]:
        """
        Retrieves the list of sample programs associated with this language.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            programs: List[SampleProgram] = language.sample_programs()

        :return: the list of sample programs
        """
        return self._sample_programs

    def total_programs(self) -> int:
        """
        Retrieves the total number of sample programs in the language collection.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            programs_count: int = language.total_programs()

        :return: the number of sample programs as an int
        """
        return self._total_snippets

    def total_size(self) -> int:
        """
        Retrieves the total byte size of the sample programs in the language collection.
        Size is computed from the size of all sample programs and is not computed
        from the testinfo or README files. 

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            size: int = language.total_size()

        :return: the total byte size of the language collection as an int
        """
        return self._total_dir_size

    def total_line_count(self) -> int:
        """
        Retrieves the total line count of the language collection. Line count
        is computed from the sample programs only and does not include lines of
        code in testinfo or README files. 

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            lines: int = language.total_line_count() 

        :return: the total line count of the language collection as an int
        """
        return self._total_line_count

    def lang_docs_url(self) -> str:
        """
        Retrieves the URL to the language documentation. The language URL is assumed
        to exist and therefore not validated. The language documentation URL is
        in the following form:

        ``https://sample-programs.therenegadecoder.com/languages/{lang}/``

        For example, here is a link to the
        `Python documentation <https://sample-programs.therenegadecoder.com/languages/python/>`_. 

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            link: str = language.lang_docs_url() 

        :return: the language documentation URL as a string
        """
        return self._lang_docs_url

    def testinfo_url(self) -> str:
        """
        Retrieves the URL to the testinfo file for this language on GitHub. 
        The testinfo URL is assumed to exist and therefore not validated. The 
        testinfo URL is in the following form:

        ``https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/{letter}/{lang}/testinfo.yml``

        For example, here is a link to the
        `Python testinfo file <https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/p/python/testinfo.yml>`_.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            link: str = language.testinfo_url()  

        :return: the testinfo URL as a string
        """
        return self._testinfo_url

    def _collect_sample_programs(self) -> Dict[str, SampleProgram]:
        """
        Generates a list of sample program objects from all of the files in this language collection.

        :return: a collection of sample programs
        """
        sample_programs = {}
        for file in self._file_list:
            _, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower()
            if file_ext not in (".md", "", ".yml"):
                program = SampleProgram(self._path, file, str(self))
                print(program)
                sample_programs[program.project()] = program
        sample_programs = dict(sorted(sample_programs.items()))
        return sample_programs

    def _collect_test_file(self) -> Optional[str]:
        """
        Generates the path to a test file for this language collection
        if it exists.

        :return: the path to a test info file
        """
        if "testinfo.yml" in self._file_list:
            return os.path.join(self._path, "testinfo.yml")

    def _collect_readme(self) -> Optional[str]:
        """
        Generates the path to the README for this language collection
        if it exists.

        :return: the path to a readme
        """
        if "README.md" in self._file_list:
            return os.path.join(self._path, "README.md")


class Repo:
    """
    An object representing the Sample Programs repository.

    :param source_dir: the location of the repo archive (e.g., C://.../sample-programs/archive)
    """

    def __init__(self, source_dir: Optional[str] = None) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self._source_dir: str = self._generate_source_dir(source_dir)
        self._languages: Dict[str: LanguageCollection] = self._collect_languages()
        self._total_snippets: int = sum(x.total_programs() for _, x in self._languages.items())
        self._total_tests: int = sum(1 for _, x in self._languages.items() if x.has_testinfo())

    def language_collections(self) -> Dict[str, LanguageCollection]:
        """
        Retrieves the list of language names mapped to their language collections in 
        the Sample Programs repo.

        Assuming you have a Repo object called repo, here’s how you would use 
        this method::

            languages: Dict[str, LanguageCollection] = repo.language_collections()

        :return: the dictionary of language names mapped to language collections
        """
        return self._languages

    def total_programs(self) -> int:
        """
        Retrieves the total number of programs in the sample programs repo.
        This total does not include any additional files such as README
        or testinfo files. 

        Assuming you have a Repo object called repo, here’s how you would use 
        this method::

            count: int = repo.total_programs()

        :return: the total number of programs as an int
        """
        return self._total_snippets

    def total_tests(self) -> int:
        """
        Retrieves the total number of tested languages in the repo. This value
        is based on the number of testinfo files in the repo.

        Assuming you have a Repo object called repo, here’s how you would use 
        this method::

            count: int = repo.total_tests()

        :return: the total number of tested languages as an int
        """
        return self._total_tests

    def get_languages_by_letter(self, letter: str) -> List[LanguageCollection]:
        """
        A convenience method for retrieving all language collections that start with a 
        particular letter.

        Assuming you have a Repo object called repo, here’s how you would use 
        this method::

            langs: List[LanguageCollection] = repo.get_languages_by_letter("p")

        :param letter: a character to search by
        :return: a list of language collections where the language starts with the provided letter
        """
        language_list = [
            language 
            for name, language in self._languages.items() 
            if name.lower().startswith(letter)
        ]
        return sorted(language_list, key=lambda s: s._name.casefold())

    def get_sorted_language_letters(self) -> List[str]:
        """
        A convenience method which generates a list of sorted letters from the sample 
        programs archive. This will return a list of letters that match the directory
        structure of the archive.

        Assuming you have a Repo object called repo, here’s how you would use 
        this method::

            letters: List[str] = repo.get_sorted_language_letters()

        :return: a sorted list of letters
        """
        unsorted_letters = os.listdir(self._source_dir)
        return sorted(unsorted_letters, key=lambda s: s.casefold())

    def _collect_languages(self) -> Dict[str, LanguageCollection]:
        """
        Builds a list of language collections.

        :return: the list of language collections
        """
        languages = {}
        for root, directories, files in os.walk(self._source_dir):
            if not directories:
                language = LanguageCollection(os.path.basename(root), root, files)
                languages[str(language)] = language
        languages = dict(sorted(languages.items()))
        return languages

    def _generate_source_dir(self, source_dir: Optional[str]) -> str:
        """
        A helper method which generates the Sample Programs repo
        from Git if it's not provided on the source directory.

        :return: a path to the source directory of the archive directory
        """
        if not source_dir:
            git.Repo.clone_from(
                "https://github.com/TheRenegadeCoder/sample-programs.git", self._temp_dir.name)
            return os.path.join(self._temp_dir.name, "archive")
        return source_dir
