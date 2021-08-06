from subete import LanguageCollection

TEST_PATH = "tests/python/"
TEST_LANG = "python"
TEST_FILES = ["hello_world.py", "testinfo.yml"]

def test_language_collection_test_file():
    test = LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES)
    assert test.get_test_data() != None
