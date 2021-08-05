from subete import SampleProgram

TEST_FILE_NAME = "hello_world.py"
TEST_FILE_PATH = "samples/"
TEST_LANG = "python"

def test_sample_program_language():
    test = SampleProgram(TEST_FILE_PATH, TEST_FILE_NAME, TEST_LANG)
    assert test.language() == TEST_LANG

def test_sample_program_code():
    test = SampleProgram(TEST_FILE_PATH, TEST_FILE_NAME, TEST_LANG)
    assert test.code() == 'print("Hello, World!")\n'
