import subete

TEST_REPO = subete.load()


def test_doc_url_multiword_lang():
    language: subete.LanguageCollection = TEST_REPO["Google Apps Script"]
    assert language.lang_docs_url() == "https://sampleprograms.io/languages/google-apps-script"


def test_doc_url_symbol_lang():
    language: subete.LanguageCollection = TEST_REPO["C#"]
    assert language.lang_docs_url() == "https://sampleprograms.io/languages/c-sharp"


def test_testinfo_url_multiword_lang():
    language: subete.LanguageCollection = TEST_REPO["Google Apps Script"]
    assert language.testinfo_url(
    ) == "https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/g/google-apps-script/testinfo.yml"


def test_testinfo_url_symbol_lang():
    language: subete.LanguageCollection = TEST_REPO["C#"]
    assert language.testinfo_url(
    ) == "https://github.com/TheRenegadeCoder/sample-programs/blob/main/archive/c/c-sharp/testinfo.yml"


def test_requirements_url_multiword_lang():
    program: subete.SampleProgram = TEST_REPO["Google Apps Script"]["Hello World"]
    assert program.project().requirements_url(
    ) == "https://sampleprograms.io/projects/hello-world"


def test_requirements_url_symbol_lang():
    program: subete.SampleProgram = TEST_REPO["C#"]["Hello World"]
    assert program.project().requirements_url(
    ) == "https://sampleprograms.io/projects/hello-world"


def test_documentation_url_multiword_lang():
    program: subete.SampleProgram = TEST_REPO["Google Apps Script"]["Hello World"]
    assert program.documentation_url(
    ) == "https://sampleprograms.io/projects/hello-world/google-apps-script"


def test_documentation_url_symbol_lang():
    program: subete.SampleProgram = TEST_REPO["C#"]["Hello World"]
    assert program.documentation_url(
    ) == "https://sampleprograms.io/projects/hello-world/c-sharp"


def test_article_issue_url_multiword_lang():
    program: subete.SampleProgram = TEST_REPO["Google Apps Script"]["Hello World"]
    assert program.article_issue_query_url(
    ) == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+google+apps+script"


def test_article_issue_url_symbol_lang():
    program: subete.SampleProgram = TEST_REPO["C#"]["Hello World"]
    assert program.article_issue_query_url(
    ) == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+c#"


def test_authors():
    program: subete.SampleProgram = TEST_REPO["Python"]["Hello World"]
    assert "Jeremy Griffith" in program.authors()


def test_created_not_none():
    program: subete.SampleProgram = TEST_REPO["Python"]["Hello World"]
    assert program.created() is not None


def test_modified_not_none():
    program: subete.SampleProgram = TEST_REPO["Python"]["Hello World"]
    assert program.modified() is not None


def test_code():
    program: subete.SampleProgram = TEST_REPO["Python"]["Hello World"]
    assert program.code() == "print('Hello, World!')\n"


def test_project_has_test():
    program: subete.SampleProgram = TEST_REPO["Google Apps Script"]["Hello World"]
    assert program.project().has_testing()


def test_repo_languages():
    assert len(list(TEST_REPO)) > 0


def test_repo_total_programs():
    assert TEST_REPO.total_programs() > 0


def test_repo_total_tests():
    assert TEST_REPO.total_tests() > 0


def test_repo_languages_by_letter():
    assert len(TEST_REPO.languages_by_letter("p")) > 0


def test_random_program():
    assert TEST_REPO.random_program() != TEST_REPO.random_program()


def test_total_approved_projects():
    assert TEST_REPO.total_approved_projects() > 0


def test_program_has_docs():
    program: subete.SampleProgram = TEST_REPO["Python"]["Hello World"]
    assert program.has_docs()
