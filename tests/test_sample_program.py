from typing import List
import subete
from subete.repo import LanguageCollection

TEST_PATH: str = "tests/python/"
TEST_LANG: str = "python"
TEST_FILES: List[str] = ["hello_world.py", "testinfo.yml", "README.md"]
TEST_PROJECTS: List[subete.Project] = [
    subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False}), 
    subete.Project("reverse-string", {"words": ["reverse", "string"], "requires_parameters": True}),
    subete.Project("rot13", {"words": ["rot13"], "requires_parameters": False}),
]
TEST_LANG_COLLECTION: subete.LanguageCollection = subete.LanguageCollection(
    TEST_LANG, 
    TEST_PATH, 
    TEST_FILES, 
    TEST_PROJECTS
)


def test_sample_program_str():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert str(test) == "Hello World in Python"


def test_sample_program_language():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert test.language_collection() == TEST_LANG_COLLECTION


def test_sample_program_code():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert test.code() == 'print("Hello, World!")\n'


def test_sample_program_line_count():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert test.line_count() == 1


def test_sample_program_size():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert test.size() > 0


def test_sample_program_requirements_url():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert test.project().requirements_url(
    ) == "https://sampleprograms.io/projects/hello-world"


def test_sample_program_documentation_url():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert test.documentation_url() == "https://sampleprograms.io/projects/hello-world/python"


def test_sample_program_issue_query_url():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert test.article_issue_query_url(
    ) == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+python"


def test_generate_project_hyphen_branch():
    test = subete.SampleProgram(
        "tests/c", 
        "rot13.c", 
        LanguageCollection(
            "c",
            "tests/c",
            ["rot13.c", "testinfo.yml", "README.md"],
            TEST_PROJECTS
        )
    )
    assert test.project_pathlike_name() == "rot13"


def test_generate_project_multiple_extensions():
    test = subete.SampleProgram(
        "tests/ti-basic",
        "hello-world.8xp.txt",
        LanguageCollection(
            "ti-basic",
            "tests/ti-basic",
            ["hello-world.8xp.txt", "testinfo.yml", "README.md"],
            TEST_PROJECTS
        )
    )
    assert test.project_pathlike_name() == "hello-world"

def test_sample_program_equality():
    test1 = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    test2 = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    assert test1 == test2


def test_sample_program_inequality():
    test1 = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    test2 = subete.SampleProgram(
        "tests/c", 
        "rot13.c", 
        LanguageCollection(
            "c",
            "tests/c",
            ["rot13.c", "testinfo.yml", "README.md"],
            TEST_PROJECTS
        )
    )
    assert test1 != test2


def test_sample_program_diff_class():
    test1 = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG_COLLECTION)
    test2 = "foo"
    assert test1 != test2
