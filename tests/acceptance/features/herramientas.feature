Feature: Herramientas endpoint
  Como cliente quiero crear y listar herramientas del repositorio

  Scenario: Create tool
    Given the API is running
    When I POST "/herramientas" with body '{"name": "fastapi", "description": "web framework"}'
    Then the response status code should be 201
    And the response should contain key "name" with value "fastapi"
    And the response should contain key "description" with value "web framework"

  Scenario: List tools
    Given the API is running
    And a tool exists
    When I GET "/herramientas"
    Then the response status code should be 200
    And the response should contain key "name" with value "fastapi"

  Scenario: Get tool by id
    Given the API is running
    And a tool exists
    When I GET tool by id
    Then the response status code should be 200
    And the response should contain key "name" with value "fastapi"