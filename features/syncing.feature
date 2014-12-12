Feature: keep files synced

  Scenario: a file on BeeP doesn't exist on disk
    Given the website is reachable
    When a file is not available locally
    Then I should get a local copy

  Scenario: a file on BeeP is newer than the local copy (creation time)
    Given the website is reachable
    When a file on BeeP is newer than the local copy
    Then I should get the updated file

  Scenario: a file exists locally but not on BeeP
    Given the website is reachable
    When a local file doesn't exist on BeeP
    Then nothing should happen