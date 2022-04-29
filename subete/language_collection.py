import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from subete.sample_program import SampleProgram

logger = logging.getLogger(__name__)


class LanguageCollection:
    """
    An object representing a collection of sample programs files for a particular programming language.

    :param name: the name of the language (e.g., python)
    :param path: the path of the language (e.g., .../archive/p/python/)
    :param file_list: the list of files in language collection
    :param projects: the list of approved projects according to the Sample Programs docs
    """

    def __init__(self, name: str, path: str, file_list: List[str], projects: List[str]) -> None:
        self._name: str = name
        self._path: str = path
        self._file_list: List[str] = file_list
        self._projects: List[str] = projects
        self._first_letter: str = name[0]
        self._sample_programs: Dict[str,
                                    SampleProgram] = self._collect_sample_programs()
        self._test_file_path: Optional[str] = self._collect_test_file()
        self._read_me_path: Optional[str] = self._collect_readme()
        self._lang_docs_url: str = f"https://sampleprograms.io/languages/{self._name}"
        self._testinfo_url: str = f"https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/{self._name[0]}/{self._name}/testinfo.yml"
        self._total_snippets: int = len(self._sample_programs)
        self._total_dir_size: int = sum(x.size()
                                        for _, x in self._sample_programs.items())
        self._total_line_count: int = sum(
            x.line_count() for _, x in self._sample_programs.items())
        self._missing_programs: List[str] = self._collect_missing_programs()

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
        logger.info(
            f"Retrieving testinfo URL for {self}: {self._test_info_url}")
        return self._testinfo_url

    def missing_programs(self) -> List[str]:
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

    def _collect_missing_programs(self) -> List[str]:
        """
        Generates a list of sample programs that are missing from the language collection.

        :return: a list of missing sample programs
        """
        programs = set(program._normalize_program_name()
                       for program in self._sample_programs.values())
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
                program = SampleProgram(self._path, file, str(self))
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
