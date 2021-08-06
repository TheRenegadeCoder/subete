from subete import SampleProgram

TEST_FILE_NAME = "hello_world.py"
TEST_FILE_PATH = "tests/samples/"
TEST_LANG = "python"

def test_sample_program_language():
    test = SampleProgram(TEST_FILE_PATH, TEST_FILE_NAME, TEST_LANG)
    assert test.language() == TEST_LANG

def test_sample_program_code():
    test = SampleProgram(TEST_FILE_PATH, TEST_FILE_NAME, TEST_LANG)
    assert test.code() == 'print("Hello, World!")\n'

def test_sample_program_line_count():
    test = SampleProgram(TEST_FILE_PATH, TEST_FILE_NAME, TEST_LANG)
    assert test.line_count() == 1

def test_sample_program_size():
    test = SampleProgram(TEST_FILE_PATH, TEST_FILE_NAME, TEST_LANG)
    assert test.size() == 24

def test_sample_program_requirements_url():
    test = SampleProgram(TEST_FILE_PATH, TEST_FILE_NAME, TEST_LANG)
    assert test.requirements_url() == "https://sample-programs.therenegadecoder.com/projects/hello-world"
