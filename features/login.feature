Feature: login to website
In order to keep files updated
As a common user
I will get a valid session

@require_login
Scenario: login with correct username and password
	Given I have correct username and password
	And the website is reachable
	When I visit the login page
	Then I should access the private area

 @require_login
 @wrongcodes
Scenario: login with wrong username or password
	Given I have wrong username or password
	And the website is reachable
	When I visit the login page
	Then I should get an exception "Invalid username or password"
   And logged variable is false


