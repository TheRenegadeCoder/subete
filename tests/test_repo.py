from subete import Repo

TEST_REPO = Repo()


def test_repo_init():
    assert len(TEST_REPO._languages) > 0
