Feature: Handle storing, retrieving and deleting customer details # test/features/user.feature:1

  Scenario: Retrieve a customers details
    Given some users are in the system
    When I retrieve the customer 'jasonb'
    Then I should get a "200" response
    And the following user details are returned:
      | name         |
      | Jason Bourne |

  Scenario: Get all users
    Given at least two users are in the system, which are
      | key    | name            |
      | brend  | Brenda Dichiara |
      | luciom | Lucio Mansilla  |
    When I request system users
    Then I should get following response:
      | key    | name            |
      | brend  | Brenda Dichiara |
      | luciom | Lucio Mansilla  |

  Scenario: Add a new user
    Given user 'aylen' isn't exist in the system
    When I add user "aylen" with name "Aylen Dichiara"
    Then I should insert correctly to user 'aylen'

  Scenario: Update a user
    Given user with the following information exists in the system:
      | key   | name            |
      | brend | Brenda Dichiara |
    When I update user "brend" with new name "Brenda Leone"
    Then I should get following data:
      | name         |
      | Brenda Leone |

  Scenario: Delete a user
    Given user with the following information exists in the system:
      | key   | name            |
      | brend | Brenda Dichiara |
    When I delete user "brend"
    Then I should delete correctly to user "brend"


