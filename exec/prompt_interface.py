def main():
    stations_classifier = pickle.load(open(ROOT_DIR + "src/assets/trained_classifiers/stations_classifier.p", "rb"))
    src.state.STATE_STORAGE = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)
    while True:
        input_text = input("input json >")
        try:
            json_object = json.loads(input_text)
            text = json_object["text"]
            session_id = json_object["session_id"]
        except Exception:
            print("Invalid input!")
            continue;

        state = src.state.get_state(text, session_id)
        state = src.trip_planning_conversation.proceed(
            state,
            stations_classifier
        )
        pprint.pprint(state)
        if (session_id is not None):
            src.state.save_state(state, session_id)


if __name__ == '__main__':
    import sys, os

    DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = DIR + '/../'
    sys.path.append(ROOT_DIR)

    import pprint, pickle, redis, json
    import src.state, src.trip_planning_conversation

    main()


    ## {"text":"to London", "session_id": 12345}
