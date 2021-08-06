import logging
import os
import re
from pathlib import Path
from typing import List, Optional

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

    def __str__(self) -> str:
        """
        Renders the Sample Program in the following form: {name} in {language}.

        :return: the sample program as a string
        """
        return f'{self._normalized_name.replace("-", " ").title()} in {self._language.title()}'

    def size(self) -> int:
        """
        Retrieves the size of the sample program in bytes.

        :return: the size of the sample program as an integer
        """
        relative_path = os.path.join(self._path, self._file_name)
        return os.path.getsize(relative_path)

    def language(self) -> str:
        """
        Retrieves the language name for this sample program.

        :return: the language of the sample program as a string
        """
        return self._language

    def code(self) -> str:
        """
        Retrieves the code for this sample program.

        :return: the code for the sample program as a string
        """
        logger.debug(
            f"Attempting to retrieve code from {self._path}/{self._file_name}")
        return Path(self._path, self._file_name).read_text()

    def line_count(self) -> int:
        """
        Retrieves the number of lines in the sample program.

        :return: the number of lines for the sample program as an integer
        """
        return len(self.code().splitlines())

    def requirements_url(self) -> str:
        """
        Retrieves the URL to the requirements documentation for
        this sample program. Requirements URL is assumed to exist
        and therefore not validated. 

        :return: the requirments URL as a string 
        """
        return self._sample_program_req_url

    def documentation_url(self) -> str:
        """
        Retrieves the URL to the documentation for this
        sample program. Documentation URL is assumed to exist
        and therefore not validated.

        :return: the documentation URL as a string
        """
        return self._sample_program_doc_url

    def issue_query_url(self) -> str:
        """
        Retrieves the URL to the issue query for this sample
        program. Issue query URL is guaranteed to be a valid
        search query on GitHub, but it is not guaranteed to 
        have any results.

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
        return f"{self._sample_program_req_url}/{self._language}"

    def _generate_issue_url(self) -> str:
        """
        A helper method for generating the expected issues URL for
        this sample program. 

        :return: the expected issues URL
        """
        issue_url_base = "https://github.com//TheRenegadeCoder/" \
                         "sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+"
        program = self._normalized_name.replace("-", "+")
        return f"{issue_url_base}{program}+{self._language}"


class Repo:
    """
    An object representing the Sample Programs repository.

    :param source_dir: the location of the repo (e.g., C://.../sample-programs)
    """

    def __init__(self, source_dir: str) -> None:
        self._source_dir: str = source_dir
        self.languages: List[LanguageCollection] = list()
        self.total_snippets: int = 0
        self.total_tests: int = 0
        self._collect_languages()
        self._analyze_repo()
        self._organize_repo()

    def _collect_languages(self) -> None:
        """
        Builds a list of language collections.

        :return: None
        """
        for root, directories, files in os.walk(self._source_dir):
            if not directories:
                language = LanguageCollection(
                    os.path.basename(root), root, files)
                self.languages.append(language)

    def _analyze_repo(self) -> None:
        """
        Provides analytics for the repo.

        :return: None
        """
        for language in self.languages:
            self.total_snippets += language._total_snippets
            self.total_tests += 1 if language._test_file_path else 0

    def _organize_repo(self) -> None:
        """
        Sorts the repo in alphabetical order by language name.

        :return: None
        """
        self.languages.sort(key=lambda lang: lang._name.casefold())

    def get_languages_by_letter(self, letter: str) -> list:
        """
        A utility method for retrieving all language collections that start with a particular letter.

        :param letter: a character to search by
        :return: a list of programming languages starting with the provided letter
        """
        language_list = [
            language for language in self.languages if language._name.startswith(letter)]
        return sorted(language_list, key=lambda s: s._name.casefold())

    def get_sorted_language_letters(self):
        """
        A utility method which generates a list of sorted letters from the sample programs archive.
        :return: a sorted list of letters
        """
        unsorted_letters = os.listdir(self._source_dir)
        return sorted(unsorted_letters, key=lambda s: s.casefold())


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
        self._sample_programs: List[SampleProgram] = self._collect_sample_programs()
        self._test_file_path: Optional[str] = self._collect_test_file()
        self._read_me_path: Optional[str] = self._collect_readme()
        self._sample_program_url: Optional[str] = None
        self._total_snippets: int = len(self._sample_programs)
        self._total_dir_size: int = sum(x.size() for x in self._sample_programs)
        self._generate_urls()
        self._organize_collection()

    def __str__(self) -> str:
        return self._name + ";" + str(self._total_snippets) + ";" + str(self._total_dir_size)

    def _collect_sample_programs(self) -> List[SampleProgram]:
        """
        Generates a list of sample program objects from all of the files in this language collection.

        :return: a collection of sample programs
        """
        sample_programs = []
        for file in self._file_list:
            _, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower()
            if file_ext not in (".md", "", ".yml"):
                sample_programs.append(SampleProgram(self._path, file, self._name))
        return sample_programs

    def _collect_test_file(self) -> Optional[str]:
        """
        Generates the path to a test file for this language collection
        if it exists.

        :return: the path to a test info file
        """
        if "testinfo.yml" in self._file_list:
            return os.path.join()

    def _collect_readme(self) -> Optional[str]:
        """
        Generates the path to the README for this language collection
        if it exists.

        :return: the path to a readme
        """
        if "README.md" in self._file_list:
            return os.path.join(self._path, "README.md")

    def _generate_urls(self) -> None:
        self._sample_program_url = f"https://sample-programs.therenegadecoder.com/languages/{self._name}"

    def _organize_collection(self):
        self._sample_programs.sort(
            key=lambda program: program._normalized_name.casefold())

    def get_readable_name(self) -> str:
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

    def get_test_data(self) -> Optional[dict]:
        test_data = None
        if self._test_file_path:
            with open(os.path.join(self._path, self._test_file_path)) as test_file:
                test_data = yaml.safe_load(test_file)
        return test_data
