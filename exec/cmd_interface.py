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

    src.state.set_redis_storage(redis.StrictRedis(host='redis', port=6379, db=0))

    state = src.state.get_state(text, session_id)
    state = src.trip_planning_conversation.proceed(
        state,
        pickle.load(open(ROOT_DIR + "src/assets/trained_classifiers/stations_classifier.p", "rb"))
    )
    pprint.pprint(state)
    if (session_id is not None):
        src.state.save_state(state, session_id)


if __name__ == '__main__':
    import sys, os

    DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = DIR + '/../'
    sys.path.append(ROOT_DIR)

    import argparse, pprint, pickle, redis
    import src.state, src.trip_planning_conversation

    main()
