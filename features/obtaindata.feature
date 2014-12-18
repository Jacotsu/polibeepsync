Feature: obtain data from the website

  @courses
  Scenario: retrieve courses
    When I ask for the courses
    Then I get the courses list

  @courses
  Scenario: retrieve course files and directories
    When I select a course
    And I ask for files
    Then I get files

  @courses
  Scenario: add new courses
    When a new course is available
    Then it should be added to the local copy

  @courses
  Scenario: remove courses no more available
    When a course is no more available
    Then it should be removed from the local copy
