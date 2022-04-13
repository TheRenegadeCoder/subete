from subete.repo import LanguageCollection, SampleProgram
import subete

TEST_REPO = subete.load()


def test_doc_url_multiword_lang():
    language: LanguageCollection = TEST_REPO["Google Apps Script"]
    assert language.lang_docs_url() == "https://sampleprograms.io/languages/google-apps-script"


def test_doc_url_symbol_lang():
    language: LanguageCollection = TEST_REPO["C#"]
    assert language.lang_docs_url() == "https://sampleprograms.io/languages/c-sharp"


def test_testinfo_url_multiword_lang():
    language: LanguageCollection = TEST_REPO["Google Apps Script"]
    assert language.testinfo_url() == "https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/g/google-apps-script/testinfo.yml"


def test_testinfo_url_symbol_lang():
    language: LanguageCollection = TEST_REPO["C#"]
    assert language.testinfo_url() == "https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/c/c-sharp/testinfo.yml"


def test_requirements_url_multiword_lang():
    program: SampleProgram = TEST_REPO["Google Apps Script"]["Hello World"]
    assert program.requirements_url() == "https://sampleprograms.io/projects/hello-world"


def test_requirements_url_symbol_lang():
    program: SampleProgram = TEST_REPO["C#"]["Hello World"]
    assert program.requirements_url() == "https://sampleprograms.io/projects/hello-world"


def test_documentation_url_multiword_lang():
    program: SampleProgram = TEST_REPO["Google Apps Script"]["Hello World"]
    assert program.documentation_url() == "https://sampleprograms.io/projects/hello-world/google-apps-script"


def test_documentation_url_symbol_lang():
    program: SampleProgram = TEST_REPO["C#"]["Hello World"]
    assert program.documentation_url() == "https://sampleprograms.io/projects/hello-world/c-sharp"


def test_article_issue_url_multiword_lang():
    program: SampleProgram = TEST_REPO["Google Apps Script"]["Hello World"]
    assert program.article_issue_query_url() == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+google+apps+script"


def test_article_issue_url_symbol_lang():
    program: SampleProgram = TEST_REPO["C#"]["Hello World"]
    assert program.article_issue_query_url() == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+c#"
