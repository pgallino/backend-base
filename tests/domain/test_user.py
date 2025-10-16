from src.domain.user import build_user, User


def test_build_user_fields():
    result = build_user("BackendBase", "dev")
    assert isinstance(result, User)
    assert result.username == "backendbase_user"
    assert result.email == "backendbase_user@dev.com"
