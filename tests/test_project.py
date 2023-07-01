import pytest
import subete


def test_project_str():
    test = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    assert str(test) == "Hello World"


def test_name():
    test = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    assert test.name() == "Hello World"


def test_pathlike_name():
    test = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    assert test.pathlike_name() == "hello-world"


@pytest.mark.parametrize("name", ["import-blah", "blah-export"])
def test_pathlike_name_when_import_or_export(name):
    test = subete.Project(name, {"words": name.split("-"), "requires_parameters": False})
    assert test.pathlike_name() == "import-export"


def test_has_testing():
    test = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    assert test.has_testing()


def test_project_equality():
    test1 = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    test2 = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    assert test1 == test2


def test_project_inequality():
    test1 = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    test2 = subete.Project("goodbye-world", {"words": ["goodbye", "world"], "requires_parameters": False})
    assert test1 != test2


def test_project_diff_class():
    test1 = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    test2 = "hello"
    assert test1 != test2
