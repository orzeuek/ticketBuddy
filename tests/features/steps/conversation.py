from behave import *
import pprint
import requests
import random

# ugly but good enough for now :)
_URL = 'http://localhost:8080/'
_SESSION_ID = None
_LAST_RESPONSE = None


@given('initialize new session_id')
def init_session_id(context):
    global _SESSION_ID
    _SESSION_ID = str(random.randint(100000000, 999999999999))


@when('user say "{text}"')
def user_say(context, text):
    send_to_bot(text)


@then('bot respond with')
def bot_respond_with(context):
    global _LAST_RESPONSE

    response = _LAST_RESPONSE.json()
    for row in context.table:
        assert response[row['field']] == row['value'], "response was: " + str(response[row['field']])


@then('bot respond prompt was like "{text}"')
def assert_prompt_contain(context, text):
    global _LAST_RESPONSE

    found = False
    prompt = _LAST_RESPONSE.json()['prompt']

    for row in prompt:
        if text in row:
            found = True
            break

    assert found, "'" + text + "' not found"


def send_to_bot(text):
    global _LAST_RESPONSE
    _LAST_RESPONSE = requests.get(_URL + '?input_text={"text":"' + text + '","session_id": "' + _SESSION_ID + '"}')
