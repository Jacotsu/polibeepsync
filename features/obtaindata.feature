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