import unittest, unittest.mock
import src.trip_planning_conversation_graph_based as planning
from src.state import StateRepository


class TripPlanningConversationGraphBasedTest(unittest.TestCase):

    def test_graph_walking(self):
        steps_definition = MockedSteps()
        state = StateRepository(unittest.mock.Mock())._get_empty_state("XXX")

        result1 = planning.proceed(state, steps_definition, "dialog_initialization")
        self.assertEqual(result1["prompt"], "ask_origin")

        result2 = planning.proceed(state, steps_definition, result1["step"])
        self.assertEqual(result2["has_origin"], True)
        self.assertEqual(result2["prompt"], "ask_destination")

        result3 = planning.proceed(state, steps_definition, result2["step"])
        self.assertEqual(result3["has_origin"], True)
        self.assertEqual(result3["has_destination"], True)
        self.assertEqual(result3["prompt"], "ask_date")

        result4 = planning.proceed(state, steps_definition, result3["step"])
        self.assertEqual(result4["has_origin"], True)
        self.assertEqual(result4["has_destination"], True)
        self.assertEqual(result4["has_travel_date"], True)
        self.assertEqual(result4["prompt"], "ask_time")

        result5 = planning.proceed(state, steps_definition, result4["step"])
        self.assertEqual(result5["has_origin"], True)
        self.assertEqual(result5["has_destination"], True)
        self.assertEqual(result5["has_travel_date"], True)
        self.assertEqual(result5["has_travel_time"], True)
        self.assertEqual(result5["prompt"], "complete")


class MockedSteps():

    visited = []

    def dialog_initialization(self, state):
        self.visited.append("dialog_initialization")
        return state

    def extract_keywords(self, state):
        self.visited.append("extract_keywords")
        return state

    def has_origin(self, state):
        self.visited.append("has_origin")
        return state["has_origin"]

    def ask_about_origin_station(self, state):
        self.visited.append("ask_about_origin_station")
        if state["prompt"] is None:
            state["prompt"] = "ask_origin"
            state["step"] = "ask_about_origin_station"
        elif state["step"] is "ask_about_origin_station":
            state["prompt"] = None
            state["has_origin"] = True
            state["step"] = None
        return state

    def has_destination(self, state):
        self.visited.append("has_destination")
        return state["has_destination"]

    def ask_about_destination_station(self, state):
        self.visited.append("ask_about_destination_station")
        if state["prompt"] is None:
            state["prompt"] = "ask_destination"
            state["step"] = "ask_about_destination_station"
        elif state["step"] is "ask_about_destination_station":
            state["prompt"] = None
            state["has_destination"] = True
            state["step"] = None
        return state

    def has_date(self, state):
        self.visited.append("has_date")
        return state["has_travel_date"]

    def ask_about_date(self, state):
        self.visited.append("ask_about_date")
        if state["prompt"] is None:
            state["prompt"] = "ask_date"
            state["step"] = "ask_about_date"
        elif state["step"] is "ask_about_date":
            state["prompt"] = None
            state["has_travel_date"] = True
            state["step"] = None
        return state

    def has_time(self, state):
        self.visited.append("has_time")
        return state["has_travel_time"]

    def ask_about_time(self, state):
        self.visited.append("ask_about_time")
        if state["prompt"] is None:
            state["prompt"] = "ask_time"
            state["step"] = "ask_about_time"
        elif state["step"] is "ask_about_time":
            state["prompt"] = None
            state["has_travel_time"] = True
            state["step"] = None
        return state

    def send_jp_request(self, state):
        state["prompt"] = "complete"
        return state