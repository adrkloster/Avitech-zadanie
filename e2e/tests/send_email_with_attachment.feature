Feature: Mailosaur Email Actions
  Scenario: Login, create email, attach file, send email, and logout
    Given I navigate to the Yahoo login page
    When I enter my Yahoo email and password
    When I click on the login button
    Then I should see the Yahoo dashboard
    When I navigate to my contacts
    When I create email
    When I attach a file to the email
    When I send the email
    When I click on the logout button
    Then I should be logged out