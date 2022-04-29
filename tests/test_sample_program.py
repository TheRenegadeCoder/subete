import subete

TEST_PATH: str = "tests/python/"
TEST_LANG: str = "python"
TEST_FILES: list[str] = ["hello_world.py", "testinfo.yml", "README.md"]
TEST_PROJECTS: list[subete.Project] = [
    subete.Project("hello-world"), 
    subete.Project("reverse-string")
]
TEST_LANG_COLLECTION: subete.LanguageCollection = subete.LanguageCollection(
    TEST_LANG, 
    TEST_PATH, 
    TEST_FILES, 
    TEST_PROJECTS
)


def test_sample_program_str():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG)
    assert str(test) == "Hello World in Python"


def test_sample_program_language():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG)
    assert test.language_collection() == TEST_LANG


def test_sample_program_code():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG)
    assert test.code() == 'print("Hello, World!")\n'


def test_sample_program_line_count():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG)
    assert test.line_count() == 1


def test_sample_program_size():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG)
    assert test.size() > 0


def test_sample_program_requirements_url():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG)
    assert test.project().requirements_url(
    ) == "https://sampleprograms.io/projects/hello-world"


def test_sample_program_documentation_url():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG)
    assert test.documentation_url() == "https://sampleprograms.io/projects/hello-world/python"


def test_sample_program_issue_query_url():
    test = subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG)
    assert test.article_issue_query_url(
    ) == "https://github.com//TheRenegadeCoder/sample-programs-website/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+hello+world+python"
