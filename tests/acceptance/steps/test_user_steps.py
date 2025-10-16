from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
import pytest

from src.app import app
from src.config import settings


# Load scenarios from the feature
scenarios("../features/user.feature")


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def context():
    return {}


@given("the API is running")
def api_is_running(client: TestClient):
    assert client is not None


@when(parsers.parse('I GET "{path}"'))
def i_get_path(client: TestClient, context: dict, path: str):
    context["response"] = client.get(path)


@then(parsers.parse("the response status code should be {status_code:d}"))
def response_status_should_be(context: dict, status_code: int):
    resp = context["response"]
    assert resp.status_code == status_code


@then(parsers.parse('the response should contain key "{key}" with value "{value}"'))
def response_should_contain_key_value(context: dict, key: str, value: str):
    payload = context["response"].json()
    # Allow placeholders {PROJECT_NAME} and {ENVIRONMENT} in feature files.
    expected = value

    if "{PROJECT_NAME}" in expected:
        # username in the implementation is lower(PROJECT_NAME + '_user')
        if key == "username":
            expected = f"{settings.PROJECT_NAME}_user".lower()
        else:
            expected = expected.replace("{PROJECT_NAME}", settings.PROJECT_NAME)

    if "{ENVIRONMENT}" in expected:
        expected = expected.replace("{ENVIRONMENT}", settings.ENVIRONMENT)

    # Ensure email username part is lowercased if feature used {PROJECT_NAME}_user
    if key == "email":
        # replace any occurrence of PROJECT_NAME_user with its lower variant
        proj_user = f"{settings.PROJECT_NAME}_user"
        expected = expected.replace(proj_user, proj_user.lower())

    assert str(payload.get(key)) == expected
