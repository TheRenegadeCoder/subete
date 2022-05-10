from __future__ import annotations

import logging
import os
import random
import re
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

import git
import yaml

logger = logging.getLogger(__name__)


class Repo:
    """
    An object representing the Sample Programs repository.

    :param str source_dir: the location of the repo archive (e.g., C://.../sample-programs/archive)
    """

    def __init__(self, source_dir: Optional[str] = None) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self._source_dir: str = self._generate_source_dir(source_dir)
        self._docs_dir: str = self._generate_docs_dir(source_dir)
        self._tested_projects: Dict = self._collect_tested_projects()
        self._projects: List[Project] = self._collect_projects()
        self._languages: Dict[str: LanguageCollection] = self._collect_languages()
        self._total_snippets: int = sum(x.total_programs() for _, x in self._languages.items())
        self._total_tests: int = sum(1 for _, x in self._languages.items() if x.has_testinfo())

    def __getitem__(self, language) -> LanguageCollection:
        """
        Makes a repo subscriptable. In this case, the subscript retrieves a 
        language collection. 

        :param str language: the name of the language to lookup
        :return: the language collection by name
        """
        return self._languages[language]

    def __iter__(self):
        """
        A convenience method for iterating over all language collections in the repo.

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            for language in repo:
                print(language)

        :return: an iterator over all language collections
        """
        return iter(self._languages.values())

    def total_programs(self) -> int:
        """
        Retrieves the total number of programs in the sample programs repo.
        This total does not include any additional files such as README
        or testinfo files. 

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            count: int = repo.total_programs()

        :return: the total number of programs as an int
        """
        return self._total_snippets

    def total_tests(self) -> int:
        """
        Retrieves the total number of tested languages in the repo. This value
        is based on the number of testinfo files in the repo.

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            count: int = repo.total_tests()

        :return: the total number of tested languages as an int
        """
        return self._total_tests

    def approved_projects(self) -> List[Project]:
        """
        Retrieves the list of approved projects in the repo. Projects are
        returned as a list of strings where the strings represent the pathlike 
        project names (e.g., hello-world).

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            approved_projects: List[str] = repo.approved_projects()

        :return: the list of approved projects (e.g. [hello-world, mst])
        """
        return self._projects

    def total_approved_projects(self) -> int:
        """
        Retrieves the total number of approved projects in the repo. This value is
        derived from the number of projects listed in the projects directory of
        the website repo.

        Assuming you have a Repo object called repo, here's how you would use
        this method::

            count: int = repo.total_approved_projects()

        :return: the total number of approved projects as an int
        """
        return len(self._projects)

    def random_program(self) -> SampleProgram:
        """
        A convenience method for retrieving a random program from the repository.

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            program: SampleProgram = repo.random_program()

        :return: a random sample program from the Sample Programs repository
        """
        language = random.choice(list(self))
        program = random.choice(list(language))
        logger.debug(f"Generated random program: {program}")
        return program

    def languages_by_letter(self, letter: str) -> List[LanguageCollection]:
        """
        A convenience method for retrieving all language collections that start with a 
        particular letter.

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            langs: List[LanguageCollection] = repo.languages_by_letter("p")

        :param letter: a character to search by
        :return: a list of language collections where the language starts with the provided letter
        """
        language_list = [
            language 
            for name, language in self._languages.items() 
            if name.lower().startswith(letter)
        ]
        return sorted(language_list, key=lambda s: s._name.casefold())

    def sorted_language_letters(self) -> List[str]:
        """
        A convenience method which generates a list of sorted letters from the sample 
        programs archive. This will return a list of letters that match the directory
        structure of the archive.

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            letters: List[str] = repo.sorted_language_letters()

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
                language = LanguageCollection(os.path.basename(root), root, files, self._projects)
                languages[str(language)] = language
                logger.debug(f"New language collected: {language}")
        languages = dict(sorted(languages.items()))
        return languages

    def _collect_projects(self) -> List[Project]:
        """
        A helper method for collecting the projects from the 
        sample-programs-website repository. 

        :return: a list of string objects representing the projects
        """
        logger.info(f"Collecting projects along path: {self._docs_dir}")
        projects = []
        for project_dir in Path(self._docs_dir, "projects").iterdir():
            if project_dir.is_dir():
                project_test = self._tested_projects.get("".join(project_dir.name.split("-")))
                projects.append(Project(project_dir.name, project_test))
        return projects

    def _generate_source_dir(self, source_dir: Optional[str]) -> str:
        """
        A helper method which generates the Sample Programs repo
        from Git if it's not provided on the source directory.

        :return: a path to the source directory of the archive directory
        """
        if not source_dir:
            logger.info(f"Source directory is not provided. Cloning the Sample Programs repo to a temporary directory: {self._temp_dir.name}.")
            git.Repo.clone_from("https://github.com/TheRenegadeCoder/sample-programs.git", self._temp_dir.name, multi_options=["--recursive"])
            return os.path.join(self._temp_dir.name, "archive")
        logger.info(f"Source directory provided: {source_dir}")
        return source_dir

    def _generate_docs_dir(self, source_dir: Optional[str]) -> str:
        """
        A helper methods which generates the path to the documentation.
        This method is needed because the provided source directory is meant
        to point at archive (for historical purposes). This is normally
        a non-issue if the directory is generated using Git, but can be more
        annoying if the user provides a source. 

        :return: a path to the documentation directory
        """
        if not source_dir:
            return os.path.join(self._temp_dir.name, "docs", "sources")
        return os.path.join(source_dir, os.pardir, "docs", "sources")

    def _collect_tested_projects(self) -> str:
        """
        Generates the dictionary of tested projects from the
        Glotter YAML file. 
        """
        p = Path(self._source_dir).parents[0] / ".glotter.yml"
        if p.exists():
            with open(p, "r") as f:
                data = yaml.safe_load(f)
            return data
        else:
            return None


class LanguageCollection:
    """
    An object representing a collection of sample programs files for a particular programming language.

    :param str name: the name of the language (e.g., python)
    :param str path: the path of the language (e.g., .../archive/p/python/)
    :param list[str] file_list: the list of files in language collection
    :param list[Project] projects: the list of approved projects according to the Sample Programs docs
    """

    def __init__(self, name: str, path: str, file_list: List[str], projects: List[Project]) -> None:
        assert isinstance(name, str), "name must be a string"
        assert isinstance(path, str), "path must be a string"
        assert isinstance(file_list, list), "file_list must be a list"
        assert isinstance(projects, list), "projects must be a list"
        self._name: str = name
        self._path: str = path
        self._file_list: List[str] = file_list
        self._projects: List[Project] = projects
        self._first_letter: str = name[0]
        self._sample_programs: Dict[str, SampleProgram] = self._collect_sample_programs()
        self._test_file_path: Optional[str] = self._collect_test_file()
        self._read_me_path: Optional[str] = self._collect_readme()
        self._lang_docs_url: str = f"https://sampleprograms.io/languages/{self._name}"
        self._testinfo_url: str = f"https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/{self._name[0]}/{self._name}/testinfo.yml"
        self._total_snippets: int = len(self._sample_programs)
        self._total_dir_size: int = sum(
            x.size() for _, x in self._sample_programs.items()
        )
        self._total_line_count: int = sum(
            x.line_count() for _, x in self._sample_programs.items()
        )
        self._missing_programs: List[Project] = self._collect_missing_programs()

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
        tokens = [text_to_symbol.get(token, token)
                  for token in self._name.split("-")]
        if any(token in text_to_symbol.values() for token in tokens):
            return "".join(tokens).title()
        else:
            return " ".join(tokens).title()

    def __getitem__(self, program) -> str:
        """
        Makes a language collection subscriptable. In this case, the subscript 
        retrieves a sample program. 

        :param program: the name of the program to lookup
        :return: the sample program by name
        """
        return self._sample_programs[program]

    def __iter__(self):
        """
        Iterates over all sample programs in the language collection.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            for program in language:
                print(program)

        :return: an iterator over all sample programs in the language collection
        """
        return iter(self._sample_programs.values())

    def name(self) -> str:
        """
        Retrieves the name of the language in a human-readable format.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            name: str = language.name()

        :return: the name of the programming language (e.g., Python, Google Apps Script, C#)
        """
        return str(self)

    def pathlike_name(self):
        """
        Retrieves a pathlike name for this language. For example,
        instead of returning C# it would return c-sharp. Names
        are based on the folder names in the Sample Programs repo.
        These names are generated from the file names directly.
        Use `name()` to get the human-readable name or `str(self)`.

        :return: the pathlike name of this programming language (e.g., c-plus-plus)
        """
        logger.info(f"Retrieving pathlike name for {self}: {self._name}")
        return self._name

    def testinfo(self) -> Optional[dict]:
        """
        Retrieves the test data from the testinfo file. The YAML data
        is loaded into a Python dictionary.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            data: dict = language.testinfo()

        :return: the test info data as a dictionary
        """
        logger.info(f"Retrieving testinfo for {self}: {self._name}")
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
        logger.info(f"Retrieving testinfo state for {self}: {self._name}")
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
        logger.info(f"Retrieving README for {self}: {self._read_me_path}")
        if self._read_me_path:
            return Path(self._read_me_path).read_text()

    def total_programs(self) -> int:
        """
        Retrieves the total number of sample programs in the language collection.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            programs_count: int = language.total_programs()

        :return: the number of sample programs as an int
        """
        logger.info(
            f"Retrieving total programs for {self}: {self._total_snippets}")
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
        logger.info(
            f"Retrieving total size for {self}: {self._total_dir_size}")
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
        logger.info(
            f"Retrieving total line count for {self}: {self._total_line_count}")
        return self._total_line_count

    def lang_docs_url(self) -> str:
        """
        Retrieves the URL to the language documentation. The language URL is assumed
        to exist and therefore not validated. The language documentation URL is
        in the following form:

        ``https://sampleprograms.io/languages/{lang}/``

        For example, here is a link to the
        `Python documentation <https://sampleprograms.io/languages/python/>`_. 

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            link: str = language.lang_docs_url() 

        :return: the language documentation URL as a string
        """
        logger.info(
            f"Retrieving language documentation URL for {self}: {self._lang_docs_url}")
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
        logger.info(f"Retrieving testinfo URL for {self}: {self._testinfo_url}")
        return self._testinfo_url

    def missing_programs(self) -> List[Project]:
        """
        Retrieves the list of missing sample programs for this language.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            missing_programs: List[str] = language.missing_programs()

        :return: a list of missing sample programs
        """
        return self._missing_programs

    def missing_programs_count(self) -> int:
        """
        Retrieves the number of missing sample programs for this language.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            missing_programs_count: int = language.missing_programs_count()

        :return: the number of missing sample programs
        """
        return len(self._missing_programs)

    def _collect_missing_programs(self) -> List[Project]:
        """
        Generates a list of sample programs that are missing from the language collection.

        :return: a list of missing sample programs
        """
        programs = set(program.project() for program in self)
        projects = set(self._projects)
        return list(projects - programs)

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
                program = SampleProgram(self._path, file, self)
                sample_programs[program.project_name()] = program
                logger.debug(f"New sample program collected: {program}")
        sample_programs = dict(sorted(sample_programs.items()))
        return sample_programs

    def _collect_test_file(self) -> Optional[str]:
        """
        Generates the path to a test file for this language collection
        if it exists.

        :return: the path to a test info file
        """
        if "testinfo.yml" in self._file_list:
            logger.debug(f"New test file collected for {self}")
            return os.path.join(self._path, "testinfo.yml")

    def _collect_readme(self) -> Optional[str]:
        """
        Generates the path to the README for this language collection
        if it exists.

        :return: the path to a readme
        """
        if "README.md" in self._file_list:
            logger.debug(f"New README collected for {self}")
            return os.path.join(self._path, "README.md")


class SampleProgram:
    """
    An object representing a sample program in the repo.

    :param str path: the path to the sample program without the file name
    :param str file_name: the name of the file including the extension
    :param LanguageCollection language: a reference to the programming language 
        collection of this sample program
    """

    def __init__(self, path: str, file_name: str, language: LanguageCollection) -> None:
        assert isinstance(path, str), "path must be a string"
        assert isinstance(file_name, str), "file_name must be a string"
        assert isinstance(language, LanguageCollection), "language must be a LanguageCollection"
        self._path: str = path
        self._file_name: str = file_name
        self._language: LanguageCollection = language
        self._project: Project = self._generate_project()
        self._sample_program_doc_url: str = self._generate_doc_url()
        self._sample_program_issue_url: str = self._generate_issue_url()
        self._line_count: int = len(self.code().splitlines())

    def __str__(self) -> str:
        """
        Renders the Sample Program in the following form: {name} in {language}.

        :return: the sample program as a string
        """
        return f'{self.project_name()} in {self.language_name()}'

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
        logger.info(f'Retrieving language collection for {self}: {self._language}')
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
        logger.info(f'Retrieving language pathlike name for {self}: {self._language.pathlike_name()}')
        return self._language.pathlike_name()

    def project(self) -> Project:
        """
        Retrieves the project object for this sample program.

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            project: Project = program.project()

        :return: the project object for this sample program
        """
        logger.info(f'Retrieving project for {self}: {self._project}')
        return self._project
    
    def project_name(self) -> str:
        """
        Retrieves the project name of this sample program. Project name is
        generated from the file name. Specifically, multiword project names
        are converted to titlecase (e.g., Convex Hull) while acronyms of 
        three or less characters are uppercased (e.g., LPS). This
        method is an alias for `project.name()`. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.project_name()

        :return: the project name as a titlecase string (e.g., Hello World, MST)
        """
        return self._project.name()

    def project_pathlike_name(self) -> str:
        """
        Retrieves the project name in the form of a path for URL purposes.
        This method is an alias for `project.pathlike_name()`.

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            name: str = program.project_pathlike_name()

        :return: the project name as a path name (e.g., hello-world, convex-hull)
        """
        logger.info(f'Retrieving project pathlike name for {self}: {self._project}')
        return self._project.pathlike_name()

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
        logger.info(f"Retrieving code from {self._path}/{self._file_name}")
        return Path(self._path, self._file_name).read_text(errors="replace")

    def line_count(self) -> int:
        """
        Retrieves the number of lines in the sample program. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            code: int = program.line_count()

        :return: the number of lines for the sample program as an integer
        """
        logger.info(f'Retrieving line count for {self}: {self._line_count}')
        return self._line_count

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
        logger.info(f'Retrieving documentation URL for {self}: {self._sample_program_doc_url}')
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
        logger.info(f'Retrieving article issue query URL for {self}: {self._sample_program_issue_url}')
        return self._sample_program_issue_url

    def _generate_project(self) -> Optional[Project]:
        """
        A helper function which converts the program name into
        a standard representation (i.e. hello_world -> hello-world).

        :return: the sample program as a Project object or None if the project is not approved
        """
        projects = self.language_collection()._projects
        stem = os.path.splitext(self._file_name)[0]
        if len(stem.split("-")) > 1:
            url = stem.lower()
        elif len(stem.split("_")) > 1:
            url = stem.replace("_", "-").lower()
        else:
            # TODO: this is brutal. At some point, we should loop in the glotter test file.
            url = re.sub('((?<=[a-z])[A-Z0-9]|(?!^)[A-Z](?=[a-z]))', r'-\1', stem).lower()
        logger.info(f"Constructed a normalized form of the program {url}")
        for project in projects:
            if project.pathlike_name() == url:
                return project
        return None

    def _generate_doc_url(self) -> str:
        """
        A helper method for generating the expected docs URL for
        this sample program.

        FYI: this function depends on _sample_program_req_url, so
        it must be generated first. 

        :return: the expected docs URL
        """
        return f"{self.project().requirements_url()}/{Path(self._path).name}"

    def _generate_issue_url(self) -> str:
        """
        A helper method for generating the expected issues URL for
        this sample program. 

        :return: the expected issues URL
        """
        issue_url_base = "https://github.com//TheRenegadeCoder/" \
                         "sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"
        program = self._project.pathlike_name().replace("-", "+")
        return f"{issue_url_base}{program}+{str(self._language).replace(' ', '+').lower()}"


class Project:
    """
    An object representing a Project in the Sample Programs repo.

    :param str name: the name of the project in its pathlike form (e.g., hello-world) 
    """

    def __init__(self, name: str, project_tests: Optional[Dict]):
        self._project_tests = project_tests
        self._name: str = Project._generate_name(name)
        self._requirements_url: str = self._generate_requirements_url()

    def __str__(self) -> str:
        logger.info(f"Generating name from {self._name}")
        return (
            self._name.replace("-", " ").title() 
            if len(self._name) > 3 
            else self._name.upper()
        )

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Project) and self._name == __o._name

    def __hash__(self) -> int:
        return hash(self._name)

    def has_testing(self) -> bool:
        """
        Responds true if the project has tests. 

        :return: True if the project is tested, False otherwise
        """
        return self._project_tests is not None

    def name(self) -> str:
        """
        Retrieves the name of the project in its human-readable form.

        Assuming you have a Project object called project, here's how you would
        use this method::

            name: str = project.name()

        :return: the name of the project as a string
        """
        logger.info(f'Retrieving project name for {self}')
        return str(self)

    def pathlike_name(self) -> str:
        """
        Retrieves the name of the project in its pathlike form (e.g., hello-world).

        Assuming you have a Project object called project, here's how you would
        use this method::

            pathlike_name: str = project.pathlike_name()

        :return: the name of the project in its pathlike form as a string
        """
        return self._name

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
        logger.info(f'Retrieving requirements URL for {self}: {self._requirements_url}')
        return self._requirements_url

    def _generate_requirements_url(self) -> str:
        """
        A helper method for generating the expected requirements URL 
        for this sample program.

        :return: the expected requirements URL 
        """
        doc_url_base = "https://sampleprograms.io/projects"
        return f"{doc_url_base}/{self.pathlike_name()}"

    @staticmethod
    def _generate_name(name: str) -> str:
        """
        Creates the project name from some input string.

        :param str name: the name of the project in its pathlike form (e.g., hello-world)
        :return: the name of the project in its pathlike form (e.g., hello-world)
        """
        if "export" in name or "import" in name:
            return "import-export"
        return name
