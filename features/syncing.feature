Feature: keep files synced

  @files
  Scenario: a file on BeeP doesn't exist on disk
    When a file is not available locally
    Then I should get a local copy

  @files
  Scenario: a file on BeeP is newer than the local copy (creation time)
    When a file on BeeP is newer than the local copy
    Then I should get the updated file

  @files
  Scenario: a file exists locally but not on BeeP
    When a local file doesn't exist on BeeP
    Then nothing should happen