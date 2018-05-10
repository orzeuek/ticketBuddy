def get_cmd_args():
    parser = argparse.ArgumentParser(description='Train tickets vending chatbot.')
    parser.add_argument('--text', dest='text', action='store')
    parser.add_argument('--session_id', dest='session_id', type=int, action='store')
    args = parser.parse_args()

    return {
        "text": args.text,
        "session_id": str(args.session_id),
    }



def main():
    args = get_cmd_args()
    text = args["text"]
    session_id = args["session_id"]

    state_repo = StateRepository(StateStorage(host=conf.get_redis_host(), port=6379))

    state = state_repo.get_state(text, session_id)
    state = src.trip_planning_conversation.proceed(
        state,
        pickle.load(open(ROOT_DIR + "src/assets/trained_classifiers/origin_destination_classifier.p", "rb"))
    )
    pprint.pprint(state)
    if (session_id is not None):
        state_repo.save_state(state, session_id)


if __name__ == '__main__':
    import sys, os

    DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = DIR + '/../'
    sys.path.append(ROOT_DIR)

    import argparse, pprint, pickle, redis
    import src.state, src.trip_planning_conversation
    from src.state import *
    import config.configuration as conf

    main()
