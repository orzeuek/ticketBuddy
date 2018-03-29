## request:
## curl -XPOST http://0.0.0.0:8000/parse --data 'locale=en_GB&text=tomorrow at eight'

## response: 
# [
#   {
#     "dim": "time",
#     "body": "tomorrow at eight",
#     "value": {
#       "values": [
#         {
#           "value": "2018-03-01T08:00:00.000-08:00",
#           "grain": "hour",
#           "type": "value"
#         },
#         {
#           "value": "2018-03-01T20:00:00.000-08:00",
#           "grain": "hour",
#           "type": "value"
#         }
#       ],
#       "value": "2018-03-01T08:00:00.000-08:00",
#       "grain": "hour",
#       "type": "value"
#     },
#     "start": 0,
#     "end": 17
#   }
# ]

import requests
import json
import datetime

class DatesService:

    def __init__(self, base_uri):
        self.base_uri = base_uri

    def get_from_text(self, text):
        """
        :param text:
         any text which you want to extract date from.
        :return:
         {'value': {'value': '2018-03-07T00:00:00.000-08:00', 'grain': 'day'}}
        """
        response_json = json.loads(
            requests.post(
                self.base_uri + "/parse", {"locale":"en_GB","text": text}
            ).content
        )

        time_response = list(filter(lambda element: element["dim"] == "time",response_json))

        if(len(time_response) == 0):
            raise Exception("no dates found in text: "+text)

        ## @todo - consider case when we will have more then one date
        return {
            "value": time_response[0]["value"]["value"],
            "grain": time_response[0]["value"]["grain"]

        }

    ## taken from: https://github.com/facebook/duckling/blob/master/Duckling/TimeGrain/EN/Rules.hs#L23-L31
    @staticmethod
    def get_time_grains():
        return ["hour", "minute", "hour"]

    ## taken from: https://github.com/facebook/duckling/blob/master/Duckling/TimeGrain/EN/Rules.hs#L23-L31
    @staticmethod
    def get_date_grains():
        return ["day"]

    ## taken from: https://github.com/facebook/duckling/blob/master/Duckling/TimeGrain/EN/Rules.hs#L23-L31
    @staticmethod
    def get_not_precise_grains():
        return ["week", "month", "quarter", "year"]


def extract(input, service):
    """

    :param input:
    {
        "has_travel_date": False,
        "travel_date": None,
        "has_travel_time": False,
        "travel_time": None,
        "text": "tomorrow at eight"
    }
    :param service:
    instance of DatesService or other interface for "Duckling"
    :return:
    {
        "has_travel_date": True,
        "travel_date": "2018-03-02,
        "has_travel_time": True,
        "travel_time": "08:00",
        "text": "tomorrow at eight"
    }
    """

    return update_state(
        input,
        service.get_from_text(input["text"])
    )

def update_state(state, date_value):
    """

    :param state: {
        "has_travel_date": False,
        "travel_date": None,
        "has_travel_time": False,
        "travel_time": None,
        "text": "tomorrow at eight"
    }
    :param date_value: result of DatesService.get_from_text()
     {'value': {'value': '2018-03-07T08:00:00.000-08:00', 'grain': 'hour'}}
    :return: {
        "has_travel_date": True,
        "travel_date": "2018-03-07",
        "has_travel_time": True,
        "travel_time": "08:00:00",
        "text": "tomorrow at eight"
    }
    """

    ## @todo
    ## current implementation will override existing values,
    ## make it more smart....
    datetime_object = datetime.datetime.strptime(date_value["value"][:-6], "%Y-%m-%dT%H:%M:%S.%f")
    has_travel_date = date_value["grain"] in DatesService.get_date_grains() or date_value["grain"] in DatesService.get_time_grains()
    travel_date = datetime_object.date().__format__("%Y-%m-%d") if has_travel_date else None
    has_travel_time = date_value["grain"] in DatesService.get_time_grains()
    travel_time = datetime_object.time().__format__("%H:%M:%S") if has_travel_time else None

    state.update({
        "has_travel_date": has_travel_date,
        "has_travel_time": has_travel_time,
        "travel_date": travel_date,
        "travel_time": travel_time
    })

    return state