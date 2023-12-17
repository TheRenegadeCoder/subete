from unittest.mock import patch
import tempfile

import pytest

import subete

SAMPLE_PROGRAMS_TEMP_DIR = tempfile.TemporaryDirectory()
SAMPLE_PROGRAMS_WEBSITE_TEMP_DIR = tempfile.TemporaryDirectory()


def test_doc_url_multiword_lang(test_repo):
    language: subete.LanguageCollection = test_repo["Commodore Basic"]
    assert language.lang_docs_url() == "https://sampleprograms.io/languages/commodore-basic"


def test_doc_url_symbol_lang(test_repo):
    language: subete.LanguageCollection = test_repo["C#"]
    assert language.lang_docs_url() == "https://sampleprograms.io/languages/c-sharp"


def test_testinfo_url_multiword_lang(test_repo):
    language: subete.LanguageCollection = test_repo["Commodore Basic"]
    assert language.testinfo_url(
    ) == "https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/c/commodore-basic/testinfo.yml"


def test_testinfo_url_symbol_lang(test_repo):
    language: subete.LanguageCollection = test_repo["C#"]
    assert language.testinfo_url(
    ) == "https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/c/c-sharp/testinfo.yml"


def test_untesting_info_url(test_repo):
    language: subete.LanguageCollection = test_repo["Mathematica"]
    assert language.untestable_info_url(
    ) == "https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/m/mathematica/untestable.yml"


def test_requirements_url_multiword_lang(test_repo):
    program: subete.SampleProgram = test_repo["Commodore Basic"]["Hello World"]
    assert program.project().requirements_url(
    ) == "https://sampleprograms.io/projects/hello-world"


def test_requirements_url_symbol_lang(test_repo):
    program: subete.SampleProgram = test_repo["C#"]["Hello World"]
    assert program.project().requirements_url(
    ) == "https://sampleprograms.io/projects/hello-world"


def test_documentation_url_multiword_lang(test_repo):
    program: subete.SampleProgram = test_repo["Commodore Basic"]["Hello World"]
    assert program.documentation_url(
    ) == "https://sampleprograms.io/projects/hello-world/commodore-basic"


def test_documentation_url_symbol_lang(test_repo):
    program: subete.SampleProgram = test_repo["C#"]["Hello World"]
    assert program.documentation_url(
    ) == "https://sampleprograms.io/projects/hello-world/c-sharp"


def test_article_issue_url_multiword_lang(test_repo):
    program: subete.SampleProgram = test_repo["Commodore Basic"]["Hello World"]
    assert program.article_issue_query_url(
    ) == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+commodore+basic"


def test_article_issue_url_symbol_lang(test_repo):
    program: subete.SampleProgram = test_repo["C#"]["Hello World"]
    assert program.article_issue_query_url(
    ) == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+c#"


def test_authors(test_repo):
    program: subete.SampleProgram = test_repo["Python"]["Hello World"]
    assert "Jeremy Griffith" in program.authors()


def test_created_not_none(test_repo):
    program: subete.SampleProgram = test_repo["Python"]["Hello World"]
    assert program.created() is not None


def test_modified_not_none(test_repo):
    program: subete.SampleProgram = test_repo["Python"]["Hello World"]
    assert program.modified() is not None


def test_code(test_repo):
    program: subete.SampleProgram = test_repo["Python"]["Hello World"]
    assert program.code() == "print('Hello, World!')\n"


@pytest.mark.parametrize(
    "language,expected_result",
    [
        ("Piet", "png"),
        ("Python", ""),
    ]
)
def test_image_type(language, expected_result, test_repo):
    program: subete.SampleProgram = test_repo[language]["Hello World"]
    assert program.image_type() == expected_result


def test_doc_authors(test_repo):
    program: subete.SampleProgram = test_repo["Yoix"]["Hello World"]
    assert "rzuckerm" in program.doc_authors()


def test_doc_created(test_repo):
    program: subete.SampleProgram = test_repo["Yoix"]["Hello World"]
    assert program.doc_created() is not None


def test_doc_modified(test_repo):
    program: subete.SampleProgram = test_repo["Yoix"]["Hello World"]
    assert program.doc_modified() is not None


def test_project_path(test_repo):
    program: subete.SampleProgram = test_repo["Python"]["Hello World"]
    assert program.project_path().endswith("/archive/p/python/hello_world.py")


def test_project_has_test(test_repo):
    program: subete.SampleProgram = test_repo["Commodore Basic"]["Hello World"]
    assert program.project().has_testing()


def test_repo_languages(test_repo):
    assert len(list(test_repo)) > 0


def test_repo_total_programs(test_repo):
    assert test_repo.total_programs() > 0


def test_repo_total_tests(test_repo):
    assert test_repo.total_tests() > 0


def test_repo_total_untestables(test_repo):
    assert test_repo.total_untestables() > 0


def test_repo_languages_by_letter(test_repo):
    assert len(test_repo.languages_by_letter("p")) > 0


def test_random_program(test_repo):
    assert test_repo.random_program() != test_repo.random_program()


def test_approved_projects(test_repo):
    assert len(test_repo.approved_projects()) > 0


def test_total_approved_projects(test_repo):
    assert test_repo.total_approved_projects() > 0


def test_sorted_language_letters(test_repo):
    assert "p" in test_repo.sorted_language_letters()


def test_program_has_docs(test_repo):
    program: subete.SampleProgram = test_repo["Python"]["Hello World"]
    assert program.has_docs()


def test_sample_programs_repo_dir(test_repo):
    assert test_repo.sample_programs_repo_dir() == SAMPLE_PROGRAMS_TEMP_DIR.name


def test_language_has_docs(test_repo):
    language: subete.LanguageCollection = test_repo["Befunge"]
    assert language.has_docs()


def test_language_doc_author(test_repo):
    language: subete.LanguageCollection = test_repo["Befunge"]
    assert "Stuart Irwin" in language.doc_authors()


def test_language_doc_created(test_repo):
    language: subete.LanguageCollection = test_repo["Befunge"]
    assert language.doc_created() is not None


def test_language_doc_modified(test_repo):
    language: subete.LanguageCollection = test_repo["Befunge"]
    assert language.doc_modified() is not None


def test_project_doc_author(test_repo):
    project: subete.Project = test_repo["Python"]["Selection Sort"].project()
    assert "Parker Johansen" in project.doc_authors()


def test_project_doc_created(test_repo):
    project: subete.Project = test_repo["Python"]["Selection Sort"].project()
    assert project.doc_created() is not None


def test_project_doc_modified(test_repo):
    project: subete.Project = test_repo["Python"]["Selection Sort"].project()
    assert project.doc_modified() is not None


@pytest.fixture(scope="module")
def test_repo():
    with patch("subete.repo.tempfile.TemporaryDirectory") as mock:
        mock.side_effect = [SAMPLE_PROGRAMS_TEMP_DIR, SAMPLE_PROGRAMS_WEBSITE_TEMP_DIR]
        yield subete.load()

    SAMPLE_PROGRAMS_TEMP_DIR.cleanup()
    SAMPLE_PROGRAMS_WEBSITE_TEMP_DIR.cleanup()
