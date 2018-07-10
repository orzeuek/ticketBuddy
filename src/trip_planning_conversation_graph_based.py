import src.default_extraction as default_extractor
import src.origin_destination_extraction as orig_dest_extractor
import abc


class StepsDefinitionInterface:

    def __init__(self, station_classifier):
        self._stations_classifier = station_classifier

    @abc.abstractmethod
    def dialog_initialization(self, state):
        pass


def proceed(state, steps_definition: StepsDefinitionInterface, entry_point="dialog_initialization"):
    current_step_result = getattr(steps_definition, entry_point)(state)

    if current_step_result["prompt"] is not None:
        return current_step_result

    return proceed(current_step_result, steps_definition, current_step_result["step"])


class StepsDefinition:

    def __init__(self, station_classifier):
        self._stations_classifier = station_classifier

    def dialog_initialization(self, state):
        state["prompt"] = [
            "Hello, my name is Jane - train tickets issuing Chatbot",
            "I will help you find best tickets for you!",
            "Please tell me where you want travel to, where you want to begin your journey and when you want to depart?"
        ]
        state["step"] = "extract"

        return state

    def extract(self, state):
        state["prompt"] = None
        default_extractor.extract(state, self._stations_classifier)

        state["step"] = "has_origin"

        return state

    def has_origin(self, state):
        state["prompt"] = None
        if state["has_origin"] is True:
            state["step"] = "has_destination"
        else:
            state["step"] = "ask_about_origin_station"

        return state

    def ask_about_origin_station(self, state):
        state["prompt"] = ["where are you travel from?"]
        state["step"] = "extract_origin"

        return state

    def extract_origin(self, state):
        state["prompt"] = None
        ## @todo replace default extractor with more "smart" one
        # state = default_extractor.extract(state, self._stations_classifier)

        ## replaced
        orig_dest_extractor.extract(state, self._stations_classifier)

        state["step"] = "has_origin"

        return state

    def has_destination(self, state):
        state["prompt"] = None
        if state["has_destination"] is True:
            state["step"] = "has_date"
        else:
            state["step"] = "ask_about_destination_station"

        return state

    def ask_about_destination_station(self, state):
        state["prompt"] = ["where are you travel to?"]
        state["step"] = "extract_destination"

        return state

    def extract_destination(self, state):
        state["prompt"] = None
        ## @todo replace default extractor with more "smart" one
        # state = default_extractor.extract(state, self._stations_classifier)

        ## replaced
        orig_dest_extractor.extract(state, self._stations_classifier)

        state["step"] = "has_destination"

        return state

    def has_date(self, state):
        state["prompt"] = None
        if state["has_travel_date"] is True:
            state["step"] = "has_time"
        else:
            state["step"] = "ask_about_date"

        return state

    def ask_about_date(self, state):
        state["prompt"] = ["when do you want to depart?"]
        state["step"] = "extract_date"

        return state

    def extract_date(self, state):
        state["prompt"] = None
        ## @todo replace default extractor with more "smart" one
        state = default_extractor.extract(state, self._stations_classifier)
        state["step"] = "has_date"

        return state

    def has_time(self, state):
        state["prompt"] = None
        if state["has_travel_time"] is True:
            state["step"] = "send_jp_request"
        else:
            state["step"] = "ask_about_time"

        return state

    def ask_about_time(self, state):
        state["prompt"] = ["what time do you want to depart ?"]
        state["step"] = "extract_time"

        return state

    def extract_time(self, state):
        state["prompt"] = None
        ## @todo replace default extractor with more "smart" one
        state = default_extractor.extract(state, self._stations_classifier)
        state["step"] = "has_time"

        return state

    def send_jp_request(self, state):
        state["prompt"] = [
            "Sending request to journey planner !"
        ]

        return state


