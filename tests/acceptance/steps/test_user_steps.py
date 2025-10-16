from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
import pytest

from src.app import app


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
    assert str(payload.get(key)) == value
