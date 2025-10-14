from src.domain.system_service import SystemService


def test_system_service_get_system_status():
    service = SystemService()
    project = "BackendBase"
    env = "dev"

    result = service.get_system_status(project, env)

    assert result["status"] == "ok"
    assert project in result["message"]
    assert env in result["message"]
