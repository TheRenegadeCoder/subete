from subete import SampleProgram

TEST_FILE_NAME = "repo.py"
TEST_FILE_PATH = "../subete/"

def test_sample_program_language():
    test = SampleProgram(TEST_FILE_PATH, TEST_FILE_NAME, "python")
    assert test.language() == "python"
