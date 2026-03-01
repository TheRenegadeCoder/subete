from pathlib import Path
from typing import List

from glotter_core.source import CoreLanguage, CoreSource
from glotter_core.project import CoreProject

import subete

TEST_PATH: str = "tests/python/"
TEST_LANG: str = "python"
TEST_FILE: str = "hello_world.py"
TEST_INFO_PATH = Path(TEST_PATH, "testinfo.yml")
TEST_SOURCE = CoreSource(
    filename=TEST_FILE,
    language=TEST_LANG,
    path=TEST_PATH,
    test_info=TEST_INFO_PATH.read_text(),
    project_type="helloworld"
)
TEST_LANGUAGE_INFO = CoreLanguage([TEST_SOURCE], TEST_SOURCE.test_info, TEST_INFO_PATH)
TEST_PROJECTS: List[subete.Project] = [
    subete.Project(
        "hello-world",
        CoreProject({"words": ["hello", "world"], "requires_parameters": False})
    ),
    subete.Project(
        "reverse-string",
        CoreProject({"words": ["reverse", "string"], "requires_parameters": True})
    ),
]

UNTESTABLE_PATH: str = "tests/mathematica"
UNTESTABLE_LANG: str = "mathematica"
UNTESTABLE_FILE = "reverse-string.nb"
UNTESTABLE_INFO_PATH = Path(UNTESTABLE_PATH, "untestable.yml")
UNTESTABLE_SOURCE = CoreSource(
    filename=UNTESTABLE_FILE,
    language=UNTESTABLE_LANG,
    path=UNTESTABLE_PATH,
    test_info="""\
folder:
    extension: ".nb"
    naming: "hyphen"
notes:
    - "Mathematica requires a commercial license, so it cannot be tested"
""",
    project_type="reversestring"
)
UNTESTABLE_LANGUAGE_INFO = CoreLanguage([UNTESTABLE_SOURCE], UNTESTABLE_SOURCE.test_info, UNTESTABLE_INFO_PATH)


def test_language_collection_str():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert str(test) == "Python"


def test_language_collection_name():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.name() == "Python"


def test_language_collection_testinfo_file_for_testable_language():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.testinfo() is not None


def test_language_collection_testinfo_file_for_untestable_language():
    test = subete.LanguageCollection(UNTESTABLE_LANG, UNTESTABLE_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.testinfo() is None


def test_language_collection_untestable_file_for_testable_language():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.untestable_info() is None


def test_language_collection_untestable_file_for_untestable_language():
    test = subete.LanguageCollection(UNTESTABLE_LANG, UNTESTABLE_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.untestable_info() is not None


def test_language_collection_readme():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.readme() is not None


def test_language_collection_no_readme():
    test = subete.LanguageCollection(UNTESTABLE_LANG, UNTESTABLE_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.readme() is None


def test_language_collection_sample_programs():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test is not None
    assert subete.SampleProgram(TEST_SOURCE, test) in test


def test_language_collection_total_programs():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.total_programs() == 1


def test_language_collection_total_size():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.total_size() > 0


def test_language_collection_total_line_count():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.total_line_count() == 1


def test_language_collection_language_url():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.lang_docs_url() == "https://sampleprograms.io/languages/python"


def test_missing_programs():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.missing_programs() == [TEST_PROJECTS[1]]


def test_missing_programs_count():
    test = subete.LanguageCollection(TEST_LANG, TEST_LANGUAGE_INFO, TEST_PROJECTS)
    assert test.missing_programs_count() == 1
