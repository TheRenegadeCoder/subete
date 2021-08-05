from subete import SampleProgram

def test_sample_program_language():
    test = SampleProgram(None, None, "python")
    assert test.language() == "python"
