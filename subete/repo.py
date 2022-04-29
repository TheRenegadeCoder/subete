import logging
import os
import tempfile
import random
from pathlib import Path
from typing import Dict, List, Optional

import git

from subete.language_collection import LanguageCollection
from subete.sample_program import SampleProgram

logger = logging.getLogger(__name__)


class Repo:
    """
    An object representing the Sample Programs repository.

    :param source_dir: the location of the repo archive (e.g., C://.../sample-programs/archive)
    """

    def __init__(self, source_dir: Optional[str] = None) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        self._source_dir: str = self._generate_source_dir(source_dir)
        self._docs_dir: str = self._generate_docs_dir(source_dir)
        self._projects: list[str] = self._collect_projects()
        self._languages: Dict[str: LanguageCollection] = self._collect_languages()
        self._total_snippets: int = sum(x.total_programs() for _, x in self._languages.items())
        self._total_tests: int = sum(1 for _, x in self._languages.items() if x.has_testinfo())

    def __getitem__(self, language) -> LanguageCollection:
        """
        Makes a repo subscriptable. In this case, the subscript retrieves a 
        language collection. 

        :param language: the name of the language to lookup
        :return: the language collection by name
        """
        return self._languages[language]

    def language_collections(self) -> Dict[str, LanguageCollection]:
        """
        Retrieves the list of language names mapped to their language collections in 
        the Sample Programs repo.

        Assuming you have a Repo object called repo, here's how you would use 
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

    def approved_projects(self) -> List[str]:
        """
        Retrieves the list of approved projects in the repo. Projects are
        returned as a list of strings where the strings represent the full
        project name (e.g., Hello World).

        Assuming you have a Repo object called repo, here's how you would use 
        this method::

            approved_projects: List[str] = repo.approved_projects()

        :return: the list of approved projects
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
        language = random.choice(list(self.language_collections().values()))
        program = random.choice(list(language.sample_programs().values()))
        logger.debug(f"Generated random program: {program}")
        return program

    def languages_by_letter(self, letter: str) -> List[LanguageCollection]:
        """
        A convenience method for retrieving all language collections that start with a 
        particular letter.

        Assuming you have a Repo object called repo, here’s how you would use 
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

        Assuming you have a Repo object called repo, here’s how you would use 
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

    def _collect_projects(self) -> List[str]:
        """
        A helper method for collecting the projects from the 
        sample-programs-website repository. 

        :return: a list of string objects representing the projects
        """
        projects = []
        for project_dir in Path(self._docs_dir, "projects").iterdir():
            if project_dir.is_dir():
                projects.append(project_dir.name)
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
            return os.path.join(self._temp_dir.name, "docs")
        return os.path.join(source_dir, os.pardir, "docs")
