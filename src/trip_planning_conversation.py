import random
import src.stations_extraction
# import src.dates_extraction_via_dialogflow


def proceed(state, stations_classifier):
    try:
        state.update(src.stations_extraction.extract(state, stations_classifier))
    except Exception as e:
        print(str(e))
        pass
    # try:
    #     state.update(src.dates_extraction_via_dialogflow.get_date_time(state))
    # except Exception as e:
    #     pass
    return state


def get_next_missing_information_prompt(state):
    """
    :param state:
     {
        "has_origin": false,
        "has_destination": false,
        "has_travel_date": false,
        "has_travel_time": false,
        "text": "Hello there, can you please plan me a trip?"
     }
    :return:
    {
        "feature_flag": "destination",
        "text": "Please, tell me where you want to travel?"
    }
    """
    if (state["has_destination"] is False):
        questions = questions_about_destination()
    elif (state["has_origin"] is False):
        questions = questions_about_origin()
    elif (state["has_travel_date"] is False):
        questions = questions_about_date()
    elif (state["has_travel_time"] is False):
        questions = questions_about_time()
    else:
        questions = ["thank you, I've got everything I need"]

    return questions[random.randint(0, len(questions) - 1)]


def questions_about_origin():
    return [
        "Where are you travel from?",
        "Where you want to start you journey?",
        "What is origin station"
    ]


def questions_about_destination():
    return [
        "Where are you travel to?",
        "Where you want to finish you journey?",
        "What is destination station"
    ]


def questions_about_date():
    return [
        "when do you want to travel?"
    ]


def questions_about_time():
    return [
        "What time do you want to depart?"
    ]
