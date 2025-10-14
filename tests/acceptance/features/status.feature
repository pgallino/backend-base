Feature: System status endpoint
  As a client I want to check the system status via HTTP

  Scenario: Get system status
    Given the API is running
    When I GET "/status"
    Then the response status code should be 200
    And the response should contain key "status" with value "ok"
