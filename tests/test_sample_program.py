from pathlib import Path
from typing import List

from glotter_core.source import CoreSource, CoreLanguage
from glotter_core.project import CoreProject
import pytest

import subete
from subete.repo import LanguageCollection

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
    subete.Project(
        "rot13",
        CoreProject({"words": ["rot13"], "requires_parameters": False})
    ),
]
TEST_LANG_COLLECTION: subete.LanguageCollection = subete.LanguageCollection(
    TEST_LANG, 
    TEST_LANGUAGE_INFO,
    TEST_PROJECTS
)


def test_sample_program_str():
    test = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert str(test) == "Hello World in Python"


def test_sample_program_language():
    test = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert test.language_collection() == TEST_LANG_COLLECTION


def test_sample_program_code():
    test = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert test.code() == 'print("Hello, World!")\n'


def test_sample_program_line_count():
    test = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert test.line_count() == 1


def test_sample_program_size():
    test = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert test.size() > 0


def test_sample_program_requirements_url():
    test = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert test.project().requirements_url(
    ) == "https://sampleprograms.io/projects/hello-world"


def test_sample_program_documentation_url():
    test = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert test.documentation_url() == "https://sampleprograms.io/projects/hello-world/python"


def test_sample_program_issue_query_url():
    test = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert test.article_issue_query_url(
    ) == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+python"


def test_generate_project_hyphen_branch():
    filename = "rot13.c"
    path = "tests/c"
    language_name = "c"
    test_info_path = Path(path, "testinfo.yml")
    source = CoreSource(
        filename=filename,
        language=language_name,
        path=path,
        test_info=test_info_path.read_text(),
        project_type="rot13"
    )
    language_info = CoreLanguage([source], source.test_info, test_info_path)
    language = LanguageCollection(language_name, language_info, TEST_PROJECTS)
    test = subete.SampleProgram(source, language)
    assert test.project_pathlike_name() == "rot13"


def test_generate_project_multiple_extensions():
    filename = "hello-world.8xp.txt"
    path = "tests/ti-basic"
    language_name = "ti-basic"
    test_info_path = Path(path, "testinfo.yml")
    source = CoreSource(
        filename=filename,
        language=language_name,
        path=path,
        test_info=test_info_path.read_text(),
        project_type="helloworld"
    )
    language_info = CoreLanguage([source], source.test_info, test_info_path)
    language = LanguageCollection(language_name, language_info, TEST_PROJECTS)
    test = subete.SampleProgram(source, language)
    assert test.project_pathlike_name() == "hello-world"

def test_sample_program_equality():
    test1 = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    test2 = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    assert test1 == test2


def test_sample_program_inequality():
    test1 = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)

    filename = "rot13.c"
    path = "tests/c"
    language_name = "c"
    test_info_path = Path(path, "testinfo.yml")
    source = CoreSource(
        filename=filename,
        language=language_name,
        path=path,
        test_info=test_info_path.read_text(),
        project_type="rot13"
    )
    language_info = CoreLanguage([source], source.test_info, test_info_path)
    language = LanguageCollection(language_name, language_info, TEST_PROJECTS)
    test2 = subete.SampleProgram(source, language)

    assert test1 != test2


def test_sample_program_diff_class():
    test1 = subete.SampleProgram(TEST_SOURCE, TEST_LANG_COLLECTION)
    test2 = "foo"
    assert test1 != test2


def test_sample_program_invalid_project():
    filename = "rot14.c"
    path = "tests/c"
    language_name = "c"
    test_info_path = Path(path, "testinfo.yml")
    source = CoreSource(
        filename=filename,
        language=language_name,
        path=path,
        test_info=test_info_path.read_text(),
        project_type="rot14"
    )
    language_info = CoreLanguage([source], source.test_info, test_info_path)
    language = LanguageCollection(language_name, language_info, TEST_PROJECTS)
    with pytest.raises(KeyError):
        subete.SampleProgram(source, language)
