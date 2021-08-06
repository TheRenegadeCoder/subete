from subete import LanguageCollection

TEST_PATH = "tests/python/"
TEST_LANG = "python"
TEST_FILES = ["hello_world.py", "testinfo.yml", "README.md"]

def test_language_collection_test_file():
    test = LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES)
    assert test.testinfo() != None

def test_language_collection_readme():
    test = LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES)
    assert test.readme() != None
