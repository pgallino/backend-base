
import json
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from src.app import app
from src.config import settings

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

@given("a user with id 1 exists")
def user_with_id_1_exists(client: TestClient):
    payload = {
        "username": f"{settings.PROJECT_NAME}_user".lower(),
        "name": f"{settings.PROJECT_NAME} Default User",
        "email": f"{settings.PROJECT_NAME}_user@{settings.ENVIRONMENT}.com".lower()
    }
    client.post("/user", json=payload)

@when(parsers.parse('I GET "{path}"'))
def i_get_path(client: TestClient, context: dict, path: str):
    context["response"] = client.get(path)

@when(parsers.parse('I POST "/user" with body \'{body}\''))
def post_user_with_body(client, context, body):
    payload = json.loads(body)
    response = client.post("/user", json=payload)
    context["response"] = response

@then(parsers.parse("the response status code should be {status_code:d}"))
def response_status_should_be(context: dict, status_code: int):
    resp = context["response"]
    assert resp.status_code == status_code

@then(parsers.parse('the response should contain key "{key}" with value "{value}"'))
def response_should_contain_key_value(context: dict, key: str, value: str):
    payload = context["response"].json()
    expected = value
    if "{PROJECT_NAME}" in expected:
        if key == "username":
            expected = f"{settings.PROJECT_NAME}_user".lower()
        else:
            expected = expected.replace("{PROJECT_NAME}", settings.PROJECT_NAME)
    if "{ENVIRONMENT}" in expected:
        expected = expected.replace("{ENVIRONMENT}", settings.ENVIRONMENT)
    if key == "email":
        proj_user = f"{settings.PROJECT_NAME}_user"
        expected = expected.replace(proj_user, proj_user.lower())
    assert str(payload.get(key)) == expected
