import subete

TEST_PATH = "tests/python/"
TEST_LANG = "python"
TEST_FILES = ["hello_world.py", "testinfo.yml", "README.md"]
TEST_PROJECTS = ["hello-world", "reverse-string"]


def test_language_collection_str():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert str(test) == "Python"


def test_language_collection_test_file():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert test.testinfo() != None


def test_language_collection_readme():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert test.readme() != None


def test_language_collection_sample_programs():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert test != None
    assert subete.SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG.title()) in test


def test_language_collection_total_programs():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert test.total_programs() == 1


def test_language_collection_total_size():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert test.total_size() > 0


def test_language_collection_total_line_count():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert test.total_line_count() == 1


def test_language_collection_language_url():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert test.lang_docs_url() == "https://sampleprograms.io/languages/python"


def test_missing_programs():
    test = subete.LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES, TEST_PROJECTS)
    assert test.missing_programs() == ["reverse-string"]
