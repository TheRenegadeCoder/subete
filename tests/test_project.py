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

def test_has_testing():
    test = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    assert test.has_testing()
