from __future__ import annotations

import datetime
import logging
import os
import random
import re
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from contextlib import contextmanager

import git
import yaml

from . import imghdr

logger = logging.getLogger(__name__)


class Repo:
    """
    An object representing the Sample Programs repository.

    :param str source_dir: the location of the repo archive (e.g., C://.../sample-programs/archive)
    """

    def __init__(self, sample_programs_repo_dir: Optional[str] = None, sample_programs_website_repo_dir: Optional[str] = None) -> None:
        
        # Sets up the sample programs repo variables
        self._sample_programs_temp_dir = tempfile.TemporaryDirectory()
        self._sample_programs_repo_dir = self._sample_programs_temp_dir.name
        if sample_programs_repo_dir:
            self._sample_programs_repo_dir = sample_programs_repo_dir
            self._sample_programs_repo: git.Repo = git.Repo(self._sample_programs_repo_dir, search_parent_directories=True)          
        else:
            self._sample_programs_repo: git.Repo = git.Repo.clone_from("https://github.com/TheRenegadeCoder/sample-programs.git", self._sample_programs_repo_dir)
        
        # Sets up the sample programs website repo variables
        self._sample_programs_website_temp_dir = tempfile.TemporaryDirectory()
        self._sample_programs_website_repo_dir = self._sample_programs_website_temp_dir.name
        if sample_programs_website_repo_dir:
            self._sample_programs_website_repo_dir = sample_programs_website_repo_dir
            self._sample_programs_website_repo: git.Repo = git.Repo(self._sample_programs_website_repo_dir, search_parent_directories=True) 
        else:
            self._sample_programs_website_repo: git.Repo = git.Repo.clone_from("https://github.com/TheRenegadeCoder/sample-programs-website.git", self._sample_programs_website_repo_dir)
        
        # Sets up paths to relevant directories
        self._docs_source_dir: str = os.path.join(self._sample_programs_website_repo_dir, "sources")
        self._archive_dir: str = os.path.join(self._sample_programs_repo_dir, "archive")
        
        # Performs data collection from the repos
        self._tested_projects: dict = self._collect_tested_projects()
        self._projects: List[Project] = self._collect_projects()
        self._languages: Dict[str, LanguageCollection] = self._collect_languages()
        self._total_snippets: int = sum(x.total_programs() for _, x in self._languages.items())
        self._total_tests: int = sum(1 for _, x in self._languages.items() if x.has_testinfo())
        self._total_untestables: int = sum(1 for _, x in self._languages.items() if x.has_untestable_info())

        # Post generation updates
        self._load_git_data()
        self._load_docs_data()

        # Closes repositories
        self._sample_programs_repo.close()
        self._sample_programs_website_repo.close()

    def __getitem__(self, language: str) -> LanguageCollection:
        """
        Makes a repo subscriptable. In this case, the subscript retrieves a 
        language collection. 

        Assuming you have a Repo object called repo, here's how you would use
        this method::

            language: LanguageCollection = repo["Python"]

        :param str language: the name of the language to lookup
        :return: the language collection by name
        """
        return self._languages[language]

    def __iter__(self) -> iter:
        """
        A convenience method for iterating over all language collections in the repo.

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            for language in repo:
                print(language)

        :return: an iterator over all language collections
        """
        return iter(self._languages.values())

    def sample_programs_repo_dir(self) -> str:
        """
        Retreives the directory containing the sample programs repository

        :return: the sample programs repository directory
        """
        return self._sample_programs_repo_dir

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

    def total_untestables(self) -> int:
        """
        Retrieves the total number of untestable languages in the repo. This value
        is based on the number of untestable info files in the repo.

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            count: int = repo.total_untestables()

        :return: the total number of tested languages as an int
        """
        return self._total_untestables

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
        unsorted_letters = os.listdir(self._archive_dir)
        return sorted(unsorted_letters, key=lambda s: s.casefold())

    def _collect_languages(self) -> Dict[str, LanguageCollection]:
        """
        Builds a list of language collections.

        :return: the list of language collections
        """
        languages = {}
        for root, directories, files in os.walk(self._archive_dir):
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
        logger.info(f"Collecting projects along path: {self._docs_source_dir}")
        projects = []
        for project_dir in Path(self._docs_source_dir, "projects").iterdir():
            if project_dir.is_dir():
                project_test = self._tested_projects.get("".join(project_dir.name.split("-")))
                logger.info(f"Generating project from: {project_dir.name}, {project_test}")
                projects.append(Project(project_dir.name, project_test))
        return projects

    def _collect_tested_projects(self) -> dict:
        """
        Generates the dictionary of tested projects from the
        Glotter YAML file. 

        :return: contents of Glotter YAML file or empty dictionary
        """
        p = Path(self._sample_programs_repo_dir) / ".glotter.yml"
        if p.exists():
            with open(p, "r") as f:
                data = yaml.safe_load(f)["projects"]
            logger.info(f"Collected tested projects: {data}")
            return data
        else:
            return {}

    def _load_git_data(self) -> None:
        """
        Once the repo is loaded, this method will load the git data from the repo
        and inject that data into the repo object. This was done for simplicity.
        It seems like way more of a pain to try to pass the git data around.
        """

        with _maybe_create_delete_git_blame_ignore_revs(self._sample_programs_repo_dir):
            for language in self:
                language: LanguageCollection
                for program in language:
                    program: SampleProgram
                    authors, times = _get_git_blame_data(
                        self._sample_programs_repo, f"{program._path}/{program._file_name}"
                    )
                    program._authors |= authors
                    program._created = min(times)
                    program._modified = max(times)
                    logger.info(
                        f"Loaded git data into existing program ({program}): "
                        f"{_datetime_to_str(program._created)} - "
                        f"{_datetime_to_str(program._modified)} "
                        f"by {program._authors}"
                    )

    def _load_docs_data(self) -> None:
        """
        Once the repo is loaded, this method will load the documentation data from
        the website repo and inject that data into the repo object.
        """
        required_files: List[str]
        with _maybe_create_delete_git_blame_ignore_revs(self._sample_programs_website_repo_dir):
            # Loads project docs
            required_files = ["description.md", "requirements.md"]
            for project in self._projects:
                project: Project
                project_docs_path = Path(self._docs_source_dir, "projects", project.pathlike_name())
                if _has_any_required_files(project_docs_path, required_files):
                    logger.info(f"Project has documentation at {project_docs_path}")
                    project._docs_path = project_docs_path
                    (
                        project._doc_authors,
                        project._doc_created,
                        project._doc_modified,
                        project._docs_files
                    ) = _get_doc_common_info(
                        self._sample_programs_website_repo, project_docs_path, required_files
                    )
                    logger.info(
                        f"Loaded git data into existing project article ({project}): "
                        f"{_datetime_to_str(project._doc_created)} - "
                        f"{_datetime_to_str(project._doc_modified)} "
                        f"by {project._doc_authors}"
                    )

            # Loads language docs
            required_files = ["description.md"]
            for language in self:
                language: LanguageCollection
                language_docs_path = Path(self._docs_source_dir, "languages", language.pathlike_name())
                if _has_any_required_files(language_docs_path, required_files):
                    language._docs_path = language_docs_path
                    (
                        language._doc_authors,
                        language._doc_created,
                        language._doc_modified,
                        language._docs_files
                    ) = _get_doc_common_info(
                        self._sample_programs_website_repo, language_docs_path, required_files
                    )
                    logger.info(
                        f"Loaded git data into existing language article ({language}): "
                        f"{_datetime_to_str(language._doc_created)} - "
                        f"{_datetime_to_str(language._doc_modified)} "
                        f"by {language._doc_authors}"
                    )

            # Loads sample programs docs
            required_files = ["how-to-implement-the-solution.md", "how-to-run-the-solution.md"]
            for language in self:
                language: LanguageCollection
                for program in language:
                    program: SampleProgram
                    program_docs_path = Path(
                        self._docs_source_dir, "programs",
                        program.project_pathlike_name(),
                        program.language_pathlike_name()
                    )
                    if _has_any_required_files(program_docs_path, required_files):
                        logger.info(f"Program has documentation at {program_docs_path}")
                        program._docs_path = program_docs_path
                        (
                            program._doc_authors,
                            program._doc_created,
                            program._doc_modified,
                            program._docs_files
                        ) = _get_doc_common_info(
                            self._sample_programs_website_repo, program_docs_path, required_files
                        )
                        logger.info(
                            f"Loaded git data into existing program article ({program}): "
                            f"{_datetime_to_str(program._doc_created)} - "
                            f"{_datetime_to_str(program._doc_modified)} by "
                            f"{program._doc_authors}"
                        )


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
        self._docs_path: Optional[str] = None
        self._docs_files: Optional[List[str]] = None
        self._doc_authors: Set[str] = set()
        self._doc_created: Optional[datetime.datetime] = None
        self._doc_modified: Optional[datetime.datetime] = None
        self._first_letter: str = name[0]
        self._sample_programs: Dict[str, SampleProgram] = self._collect_sample_programs()
        self._test_file_path: Optional[str] = self._collect_test_file()
        self._untestable_file_path: Optional[str] = self._collect_untestable_file()
        self._read_me_path: Optional[str] = self._collect_readme()
        self._lang_docs_url: str = f"https://sampleprograms.io/languages/{self._name}"
        self._testinfo_url: str = f"https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/{self._name[0]}/{self._name}/testinfo.yml"
        self._untestable_info_url: str = f"https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/{self._name[0]}/{self._name}/untestable.yml"
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

        - Example: google-apps-script -> Google Apps Script
        - Example: c-sharp -> C#

        Assuming you have a LanguageCollection object called language,
        you can use the following code to get the language name::

            name: str = str(language)

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

    def __getitem__(self, program: str) -> str:
        """
        Makes a language collection subscriptable. In this case, the subscript 
        retrieves a sample program. 

        Assuming you have a LanguageCollection object called language,
        you can access a sample program as follows::

            program: SampleProgram = language["Hello World"]

        :param str program: the name of the program to lookup
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

    def untestable_info(self) -> Optional[dict]:
        """
        Retrieves the data from the untestable info file. The YAML data
        is loaded into a Python dictionary.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            data: dict = language.untestable_info()

        :return: the untestable info data as a dictionary
        """
        logger.info(f"Retrieving untestable info for {self}: {self._name}")
        untestable_data = None
        if self._untestable_file_path:
            with open(self._untestable_file_path) as untestable_file:
                untestable_data = yaml.safe_load(untestable_file)
        return untestable_data

    def has_untestable_info(self) -> bool:
        """
        Retrieves the state of the untestable info file. Helpful when
        trying to figure out if this language is untestable.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            state: bool = language.has_untestable_info()

        :return: True if a test info file exists; False otherwise
        """
        logger.info(f"Retrieving untestable info state for {self}: {self._name}")
        return bool(self._untestable_file_path)

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
    
    def has_docs(self) -> bool:
        """
        Retrieves the documentation state of this language. Note that documentation
        may not be complete or up to date. 
        
        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            state: bool = language.has_docs() 

        :return: returns true if the language has a documentation folder created for it; false otherwise
        """
        return bool(self._docs_path)

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

    def untestable_info_url(self) -> str:
        """
        Retrieves the URL to the untestable file for this language on GitHub. 
        The untestable URL is assumed to exist and therefore not validated. The 
        untestable info URL is in the following form:

        ``https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/{letter}/{lang}/untestable.yml``

        For example, here is a link to the
        `Mathematica untestable info file <https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/m/mathematica/untestable.yml>`_.

        Assuming you have a LanguageCollection object called language, 
        here's how you would use this method::

            link: str = language.untestable_info_url()  

        :return: the testinfo URL as a string
        """
        logger.info(f"Retrieving untestable info URL for {self}: {self._untestable_info_url}")
        return self._untestable_info_url

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
            filename, file_ext = os.path.splitext(file)
            if "." in filename:
                file_ext = os.path.splitext(filename)[1] + file_ext
            file_ext = file_ext.lower()
            if file_ext not in (".md", "", ".yml"):
                try:
                    program = SampleProgram(self._path, file, self)
                except KeyError:
                    continue

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

    def _collect_untestable_file(self) -> Optional[str]:
        """
        Generates the path to a untestable file for this language collection
        if it exists.

        :return: the path to a untestable info file
        """
        if "untestable.yml" in self._file_list:
            logger.debug(f"New untestable file collected for {self}")
            return os.path.join(self._path, "untestable.yml")

    def _collect_readme(self) -> Optional[str]:
        """
        Generates the path to the README for this language collection
        if it exists.

        :return: the path to a readme
        """
        if "README.md" in self._file_list:
            logger.debug(f"New README collected for {self}")
            return os.path.join(self._path, "README.md")

    def doc_authors(self) -> Set[str]:
        """
        Retrieves the set of authors for this language article. Author names
        are generated from git blame. 

        Assuming you have a LanguageCollection object called language,
        here's how you would use this method::

            doc_authors: Set[str] = language.doc_authors()

        :return: the set of language article authors
        """
        return self._doc_authors

    def doc_created(self) -> Optional[datetime.datetime]:
        """
        Retrieves the date the language article was created. Created dates
        are generated from git blame, specifically the article author commits.

        Assuming you have a LanguageCollection object called language,
        here's how you would use this method::

            doc_created: Optional[datetime.datetime] = language.doc_created()

        :return: the date the language article was created
        """
        return self._doc_created

    def doc_modified(self) -> Optional[datetime.datetime]:
        """
        Retrieves the date the language article was last modified. Modified
        dates are generated from git blame, specifically the author commits.

        Assuming you have a LanguageCollection object called language,
        here's how you would use this method::

            doc_modified: Optional[datetime.datetime] = language.doc_modified()
        
        :return: the date the language article was last modified
        """
        return self._doc_modified


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
        self._project: Optional[Project] = self._generate_project()
        if not self._project:
            raise KeyError(f"Project cannot be found for {file_name}")

        self._sample_program_doc_url: str = self._generate_doc_url()
        self._sample_program_issue_url: str = self._generate_issue_url()
        self._line_count: int = len(self.code().splitlines())
        self._authors: Set[str] = set()
        self._created: Optional[datetime.datetime] = None
        self._modified: Optional[datetime.datetime] = None
        self._docs_path: Optional[str] = None
        self._docs_files: List[str] = None
        self._doc_authors: Set[str] = set()
        self._doc_created: Optional[datetime.datetime] = None
        self._doc_modified: Optional[datetime.datetime] = None

    def __str__(self) -> str:
        """
        Renders the Sample Program in the following form: {name} in {language}.

        Assuming you have a SampleProgram object called sample_program,
        here's how you would use this method::

            name: str = str(sample_program)

        :return: the sample program as a string
        """
        return f'{self.project_name()} in {self.language_name()}'

    def __eq__(self, o: object) -> bool:
        """
        Compares an object to the sample program. Returns True if the object
        is an instance of SampleProgram and matches the following three fields:

            - _file_name
            - _path
            - _language

        Assuming you have a SampleProgram object called sample_program,
        here's how you would use this method::

            is_sample_program: bool = sample_program == other_sample_program

        :return: True if the object matches the Sample Program; False otherwise.
        """
        if isinstance(o, self.__class__):
            return self._file_name == o._file_name and self._path == self._path and self._language == o._language
        return False

    def authors(self) -> Set[str]:
        """
        Retrieves the set of authors for this sample program. Author names
        are generated from git blame. 

        Assuming you have a SampleProgram object called sample_program,
        here's how you would use this method::

            authors: Set[str] = sample_program.authors()

        :return: the set of authors
        """
        return self._authors

    def created(self) -> Optional[datetime.datetime]:
        """
        Retrieves the date the sample program was created. Created dates
        are generated from git blame, specifically the author commits.

        Assuming you have a SampleProgram object called sample_program,
        here's how you would use this method::

            created: Optional[datetime.datetime] = sample_program.created()

        :return: the date the sample program was created
        """
        return self._created

    def modified(self) -> Optional[datetime.datetime]:
        """
        Retrieves the date the sample program was last modified. Modified
        dates are generated from git blame, specifically the author commits.

        Assuming you have a SampleProgram object called sample_program,
        here's how you would use this method::

            modified: Optional[datetime.datetime] = sample_program.modified()
        
        :return: the date the sample program was last modified
        """
        return self._modified
    
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
        return self._project.name() if self._project else ""

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
        return self._project.pathlike_name() if self._project else ""

    def project_path(self) -> str:
        """
        Retrieves the path to the project file.

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            project_path: str = program.project_path()

        :return: the project path (e.g., .../archive/p/python/hello_world.py)
        """
        return os.path.join(self._path, self._file_name)

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

    def image_type(self) -> str:
        """
        Determine if sample program is actual an image, and if so, what type.

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            image_type: str = program.image_type()

        :return: Image type if sample program is an image (e.g., "png"),
            empty string otherwise
        """
        return imghdr.what(Path(self._path, self._file_name)) or ""

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
    
    def has_docs(self) -> bool:
        """
        Retrieves the documentation state of this program. Note that documentation
        may not be complete or up to date. 
        
        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            state: bool = program.has_docs() 

        :return: returns true if the program has a documentation folder created for it; false otherwise
        """
        return bool(self._docs_path)

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
        projects = self._language._projects
        stem = os.path.splitext(self._file_name)[0]
        if "." in stem:
            stem = os.path.splitext(stem)[0]
        if len(stem.split("-")) > 1:
            url = stem.lower()
        elif len(stem.split("_")) > 1:
            url = stem.replace("_", "-").lower()
        else:
            # TODO: this is brutal. At some point, we should loop in the glotter test file.
            url = "-".join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', stem)).split()).lower()
        logger.info(f"Constructed a normalized form of the program {url}")
        for project in projects:
            if url in project.pathlike_name():
                return project
        project_names = [project.pathlike_name() for project in projects]
        logger.error(f"Could not find a project for {self._file_name} with name {url} in {project_names}.")
        return None

    def _generate_doc_url(self) -> str:
        """
        A helper method for generating the expected docs URL for
        this sample program.

        FYI: this function depends on _sample_program_req_url, so
        it must be generated first. 

        :return: the expected docs URL
        """
        return f"{self._project.requirements_url()}/{Path(self._path).name}" if self._project else ""

    def _generate_issue_url(self) -> str:
        """
        A helper method for generating the expected issues URL for
        this sample program. 

        :return: the expected issues URL
        """
        issue_url_base = "https://github.com//TheRenegadeCoder/" \
                         "sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"
        program = self._project.pathlike_name().replace("-", "+") if self._project else None
        return f"{issue_url_base}{program}+{str(self._language).replace(' ', '+').lower()}"

    def doc_authors(self) -> Set[str]:
        """
        Retrieves the set of authors for this sample program article. Author names
        are generated from git blame. 

        Assuming you have a SampleProgram object called sample_program,
        here's how you would use this method::

            doc_authors: Set[str] = sample_program.doc_authors()

        :return: the set of article authors
        """
        return self._doc_authors

    def doc_created(self) -> Optional[datetime.datetime]:
        """
        Retrieves the date the sample program article was created. Created dates
        are generated from git blame, specifically the article author commits.

        Assuming you have a SampleProgram object called sample_program,
        here's how you would use this method::

            doc_created: Optional[datetime.datetime] = sample_program.doc_created()

        :return: the date the sample program article was created
        """
        return self._doc_created

    def doc_modified(self) -> Optional[datetime.datetime]:
        """
        Retrieves the date the sample program article was last modified. Modified
        dates are generated from git blame, specifically the author commits.

        Assuming you have a SampleProgram object called sample_program,
        here's how you would use this method::

            doc_modified: Optional[datetime.datetime] = sample_program.doc_modified()
        
        :return: the date the sample program article was last modified
        """
        return self._doc_modified


class Project:
    """
    An object representing a Project in the Sample Programs repo.

    :param str name: the name of the project in its pathlike form (e.g., hello-world) 
    :param project_tests: a dictionary containing the test rules for the project
    """

    def __init__(self, name: str, project_tests: Optional[Dict]):
        self._project_tests = project_tests
        self._name: str = name
        self._requirements_url: str = self._generate_requirements_url()
        self._docs_path: str = None
        self._docs_files: List[str] = None
        self._doc_authors: Set[str] = set()
        self._doc_created: Optional[datetime.datetime] = None
        self._doc_modified: Optional[datetime.datetime] = None

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

    def doc_authors(self) -> Set[str]:
        """
        Retrieves the set of authors for this project article. Author names
        are generated from git blame. 

        Assuming you have a Project object called project,
        here's how you would use this method::

            doc_authors: Set[str] = project.doc_authors()

        :return: the set of project article authors
        """
        return self._doc_authors

    def doc_created(self) -> Optional[datetime.datetime]:
        """
        Retrieves the date the project article was created. Created dates
        are generated from git blame, specifically the article author commits.

        Assuming you have a Project object called project,
        here's how you would use this method::

            doc_created: Optional[datetime.datetime] = project.doc_created()

        :return: the date the project article was created
        """
        return self._doc_created

    def doc_modified(self) -> Optional[datetime.datetime]:
        """
        Retrieves the date the project article was last modified. Modified
        dates are generated from git blame, specifically the author commits.

        Assuming you have a Project object called project,
        here's how you would use this method::

            doc_modified: Optional[datetime.datetime] = project.doc_modified()
        
        :return: the date the project article was last modified
        """
        return self._doc_modified


@contextmanager
def _maybe_create_delete_git_blame_ignore_revs(root_dir: str) -> None:
    """
    Create `.git-blame-ignore-revs` if it does not exist and delete it
    it did not exist previously.

    :param str root_dir: root directory of repository.
    """

    blame_path = Path(f"{root_dir}/.git-blame-ignore-revs")
    blame_path_exists = blame_path.exists()
    try:
        # Make sure .git-blame-ignore-revs exists for older versions of git and
        # keep track of whether it existed before
        blame_path.touch()
        yield
    finally:
        # Delete .git-blame-ignore-revs if it did not exist before
        if not blame_path_exists:
            blame_path.unlink()


def _get_git_blame_data(
    repo: git.Repo, file_path: str
) -> Tuple[Set[str], List[datetime.datetime]]:
    """
    Get the following git blame date:

    - Set of author names
    - List of date/times when commits were done

    :param git.Repo repo: git repository.
    :param str file_path: path to file
    :return: tuple containing set of author names and list of date/times
    """
    blame = repo.blame('HEAD', file_path)
    authors: Set[str] = set()
    times: List[datetime.datetime] = []
    for commit, _ in blame:
        commit: git.Commit
        authors.add(commit.author.name)
        times.append(commit.authored_datetime)

    return (authors, times)


def _has_any_required_files(path: Path, required_files: List[str]) -> bool:
    """
    Indicate if the specified path has the required files.

    :param pathlib.Path path: path to check.
    :param List[str] required_files: list of required file names.
    :return: True if at least one required file is found, False otherwise.
    """
    return any((path / required_file).exists() for required_file in required_files)


def _get_doc_common_info(
    repo: git.Repo, docs_path: Path, required_files: List[str]
) -> Tuple[Set[str], Optional[datetime.datetime], Optional[datetime.datetime], List[str]]:
    """
    Get the following common information about articles:

    - Set of author names
    - Date/time when article was created
    - Date/time when article was last modified
    - List of article files

    :param git.Repo: git repository.
    :param pathlib.Path docs_path: directory path where article files are located.
    :param List[str] required_files: list of required file names.
    :return: tuple containing set of author names, creation date/time, last modified
        date/time, and list of article files.
    """
    doc_authors: Set[str] = set()
    doc_created: Optional[datetime.datetime] = None
    doc_modified: Optional[datetime.datetime] = None
    doc_times: List[datetime.datetime] = []
    doc_files: List[str] = []
    for file in docs_path.glob("*"):
        if file.name in required_files:
            doc_files.append(file.name)
            doc_file_authors, doc_file_times = _get_git_blame_data(repo, str(file))
            doc_authors |= doc_file_authors
            doc_times += doc_file_times

    if doc_times:
        doc_created = min(doc_times)
        doc_modified = max(doc_times)

    return (doc_authors, doc_created, doc_modified, doc_files)


def _datetime_to_str(value: Optional[datetime.datetime]) -> str:
    """
    Convert date/time to a string

    :param Optional[datetime.datetime] value: date/time value.
    :return: string representing date/time value
    """
    return (
        value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(value, datetime.datetime)
        else str(value)
    )
