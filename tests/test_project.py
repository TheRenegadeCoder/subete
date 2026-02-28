from glotter_core.project import CoreProject

import subete

PROJECT_TESTS = CoreProject({"words": ["hello", "world"], "requires_parameters": False})


def test_project_str():
    test = subete.Project("hello-world", PROJECT_TESTS)
    assert str(test) == "Hello World"


def test_name():
    test = subete.Project("hello-world", PROJECT_TESTS)
    assert test.name() == "Hello World"


def test_pathlike_name():
    test = subete.Project("hello-world", PROJECT_TESTS)
    assert test.pathlike_name() == "hello-world"


def test_has_testing():
    test = subete.Project("hello-world", PROJECT_TESTS)
    assert test.has_testing()


def test_project_equality():
    test1 = subete.Project("hello-world", PROJECT_TESTS)
    test2 = subete.Project("hello-world", PROJECT_TESTS)
    assert test1 == test2


def test_project_inequality():
    test1 = subete.Project("hello-world", PROJECT_TESTS)
    test2 = subete.Project(
        "goodbye-world",
        CoreProject({"words": ["goodbye", "world"], "requires_parameters": False})
    )
    assert test1 != test2


def test_project_diff_class():
    test1 = subete.Project("hello-world", PROJECT_TESTS)
    test2 = "hello"
    assert test1 != test2
