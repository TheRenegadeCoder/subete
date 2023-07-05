import tempfile
from pathlib import Path

import git
import pytest

import subete


def test_bad_repo_total_projects(bad_test_repo):
    assert bad_test_repo.total_approved_projects() == 1


def test_bad_repo_languages(bad_test_repo):
    assert len(list(bad_test_repo)) == 1


def test_bad_repo_total_programs(bad_test_repo):
    assert bad_test_repo.total_programs() == 1


def test_bad_repo_total_tests(bad_test_repo):
    assert bad_test_repo.total_tests() == 0


@pytest.fixture(scope="module")
def bad_test_repo():
    with tempfile.TemporaryDirectory() as repo_dir, tempfile.TemporaryDirectory() as website_repo_dir:
        # Create repo
        repo: git.Repo = git.Repo.init(repo_dir)

        archive_dir = f"{repo_dir}/archive/f/foo"
        sample_program_file = f"{archive_dir}/whatever.foo"
        Path(archive_dir).mkdir(parents=True)
        Path(sample_program_file).write_text("hello\n")

        repo.index.add([sample_program_file])
        repo.index.commit("Initial commit")

        # Create website repo
        website_repo: git.Repo = git.Repo.init(website_repo_dir)

        project_doc_dir = f"{website_repo_dir}/sources/projects/bad"
        project_doc_file = f"{project_doc_dir}/something.md"
        Path(project_doc_dir).mkdir(parents=True)
        Path(project_doc_file).write_text("hello\n")

        website_repo.index.add([project_doc_file])
        website_repo.index.commit("Initial commit")

        yield subete.load(repo_dir, website_repo_dir)

        repo.close()
        website_repo.close()
