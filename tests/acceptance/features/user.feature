Feature: User endpoint
  As a client I want to get a default user profile via HTTP

  Scenario: Get user profile
    Given the API is running
    And a user with id 1 exists
    When I GET "/user/1"
    Then the response status code should be 200
    And the response should contain key "id" with value "1"
    And the response should contain key "username" with value "{PROJECT_NAME}_user"
    And the response should contain key "name" with value "{PROJECT_NAME} Default User"
    And the response should contain key "email" with value "{PROJECT_NAME}_user@{ENVIRONMENT}.com"

    Scenario: Create user
      Given the API is running
      When I POST "/user" with body '{"username": "testuser", "name": "Test User", "email": "testuser@example.com"}'
      Then the response status code should be 201
      And the response should contain key "username" with value "testuser"
      And the response should contain key "name" with value "Test User"
      And the response should contain key "email" with value "testuser@example.com"
