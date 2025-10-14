import re

from src.domain.system import _build_status_message


def test_build_status_message_returns_ok_status():
    result = _build_status_message("BackendBase", "dev")
    assert result["status"] == "ok"


def test_build_status_message_contains_project_and_env():
    project = "BackendBase"
    env = "dev"
    result = _build_status_message(project, env)

    assert project in result["message"]
    assert env in result["message"]


def test_build_status_message_format():
    project = "BackendBase"
    env = "dev"
    result = _build_status_message(project, env)

    # Verificamos un patrón aproximado del mensaje
    assert re.search(r"Proyecto '\w+' \[ENV: \w+\]", result["message"]) is not None
