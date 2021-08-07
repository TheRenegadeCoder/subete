import subete

TEST_REPO = subete.load()


def test_repo_languages():
    assert len(TEST_REPO.language_collections()) > 0


def test_repo_total_programs():
    assert TEST_REPO.total_programs() > 0


def test_repo_total_tests():
    assert TEST_REPO.total_tests() > 0


def test_repo_languages_by_letter():
    assert len(TEST_REPO.languages_by_letter("p")) > 0


def test_random_program():
    assert TEST_REPO.random_program() != TEST_REPO.random_program()
