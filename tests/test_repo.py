from subete import Repo

TEST_REPO = Repo()


def test_repo_languages():
    assert len(TEST_REPO.language_collections()) > 0


def test_repo_total_programs():
    assert TEST_REPO.total_programs() > 0
