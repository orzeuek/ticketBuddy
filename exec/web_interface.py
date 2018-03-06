import cherrypy
import pprint, pickle, redis, json
import sys, os

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = DIR + '/../'
sys.path.append(ROOT_DIR)

from src.state import *
import src.state, src.trip_planning_conversation

stations_classifier = pickle.load(open(ROOT_DIR + "src/assets/trained_classifiers/stations_classifier.p", "rb"))


class Client(object):
    @cherrypy.expose
    def default(self, input_text):
        json_object = json.loads(input_text)
        text = json_object["text"]
        session_id = json_object["session_id"]

        state_repo = StateRepository(StateStorage(host='redis', port=6379))

        state = state_repo.get_state(text, session_id)
        state = src.trip_planning_conversation.proceed(
            state,
            stations_classifier
        )

        if (session_id is not None):
            state_repo.save_state(state, session_id)

        return json.dumps(state)


cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Client())
