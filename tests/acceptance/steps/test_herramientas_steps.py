import json
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient

scenarios("../features/herramientas.feature")

@given("the API is running")
def api_is_running(client: TestClient):
    assert client is not None

@given("a tool exists")
def tool_exists(client: TestClient, context: dict):
    payload = {"name": "fastapi", "description": "web framework"}
    resp = client.post("/herramientas", json=payload)
    try:
        data = resp.json()
        context["created_id"] = int(data.get("id"))
    except Exception:
        # fallback: assume id 1 if not present
        context["created_id"] = 1


@when("I GET tool by id")
def i_get_tool_by_id(client: TestClient, context: dict):
    tool_id = context.get("created_id", 1)
    context["response"] = client.get(f"/herramientas/{tool_id}")


@when(parsers.parse('I POST "{path}" with body \'{body}\''))
def post_path_with_body(client: TestClient, context: dict, path: str, body: str):
    payload = json.loads(body)
    response = client.post(path, json=payload)
    context["response"] = response


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
    # payload may be a list (for GET /herramientas), handle both
    if isinstance(payload, list):
        # check any element has the expected key/value
        assert any(str(item.get(key)) == value for item in payload)
    else:
        assert str(payload.get(key)) == value
