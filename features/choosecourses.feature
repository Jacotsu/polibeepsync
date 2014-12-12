Feature: choose courses to be synced
  Scenario: show available courses
    When I select the courses tab
    Then I get all available courses


  Scenario: select all courses
    When I press the button "select all"
    Then All courses should be selected

  Scenario: unselect all courses
    When I press the button "unselect all"
    Then No course should be selected

  Scenario: default selection
    When I'm presented with the course list
    Then all courses are selected except "BeeP Channel"