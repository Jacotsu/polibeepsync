Feature: choose courses to be synced

  Scenario: select all courses
    Given I'm logged in
    And the website is reachable
    When I press the button "select all"
    Then All courses should be selected

  Scenario: unselect all courses
    Given I'm logged in
    And the website is reachable
    When I press the button "unselect all"
    Then No course should be selected

  Scenario: default selection
    Given I'm logged in
    And the website is reachable
    When I'm presented with the course list
    Then all courses are selected except "BeeP Channel"