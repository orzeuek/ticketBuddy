Feature: User should be able to conversate with Jane

  Scenario: Basic flow
    Given initialize new session_id
    When user say "Hi"
    Then bot respond with
      | field | value   |
      | step  | extract |
    And bot respond prompt was like "Hello, my name is Jane"
    When user say "find me a tickets to Horsham"
    Then bot respond with
      | field       | value          |
      | destination | horsham        |
      | step        | extract_origin |
    And bot respond prompt was like "where are you travel from"
    When user say "from Manchester Airport"
    Then bot respond with
      | field       | value              |
      | destination | horsham            |
      | origin      | manchester airport |
      | step        | extract_date       |
    And bot respond prompt was like "when do you want to depart"
    When user say "21-07-2018"
    Then bot respond with
      | field       | value        |
      | travel_date | 2018-07-21   |
      | step        | extract_time |
    And bot respond prompt was like "what time do you want to depart"
    When user say "quarter past 10"
    Then bot respond with
      | field       | value           |
      | travel_time | 10:15:00        |
      | step        | send_jp_request |
    And bot respond prompt was like "Sending request to journey planner"

  Scenario: Extract few fields at once
    Given initialize new session_id
    When user say "Hi"
    Then bot respond prompt was like "Hello, my name is Jane"
    When user say "I need tickets to Horsham, I will depart from Manchester Airport"
    Then bot respond with
      | field       | value              |
      | destination | horsham            |
      | origin      | manchester airport |
      | step        | extract_date       |
    And bot respond prompt was like "when do you want to depart"
    When user say "21-07-2018, quarter past 10"
    Then bot respond with
      | field       | value              |
      | destination | horsham            |
      | origin      | manchester airport |
      | travel_date | 2018-07-21         |
      | travel_time | 10:15:00           |
      | step        | send_jp_request    |
    And bot respond prompt was like "Sending request to journey planner"