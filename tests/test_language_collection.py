from typing import List
from subete.repo import SampleProgram
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

def test_language_collection_sample_programs():
    test = LanguageCollection(TEST_LANG, TEST_PATH, TEST_FILES)
    sample_programs = test.sample_programs()
    assert sample_programs != None
    assert SampleProgram(TEST_PATH, TEST_FILES[0], TEST_LANG.title()) in sample_programs

