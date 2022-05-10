import subete


def test_project_str():
    test = subete.Project("hello-world", {"words": ["hello", "world"], "requires_parameters": False})
    assert str(test) == "Hello World"
