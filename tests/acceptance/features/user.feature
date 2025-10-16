Feature: User endpoint
  As a client I want to get a default user profile via HTTP

  Scenario: Get user profile
    Given the API is running
    When I GET "/user"
    Then the response status code should be 200
    And the response should contain key "id" with value "1"
    And the response should contain key "username" with value "{PROJECT_NAME}_user"
    And the response should contain key "name" with value "{PROJECT_NAME} Default User"
    And the response should contain key "email" with value "{PROJECT_NAME}_user@{ENVIRONMENT}.com"
