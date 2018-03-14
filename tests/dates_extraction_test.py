from src.dates_extraction import *
import pprint


def __get_test_texts():
    return [
        {"text": "tomorrow"},
        {"text": "today"},
        {"text": "next week"},
        {"text": "next sunday"},
        {"text": "yesterday"},
        {"text": "9 a.m."},
        {"text": "10 p.m."},
        {"text": "quarter past 10"},
        {"text": "at noon"},
        {"text": "at midnight"},
        {"text": "tmorrow at noon"},
        {"text": "next monday at 12:15"},
        {"text": "next week at 9 a.m."},
    ]


def test_DateService():
    dates_service = DatesService(conf.get_duckling_host() + ":" + conf.get_duckling_port())
    result = list(map(lambda element:
        dates_service.get_from_text(element["text"])
    , __get_test_texts()))

    assert len(result) == 13


def test_extract():
    test_set = [
        {"input": {'value': '2018-03-07T00:00:00.000-08:00', 'grain': 'day'}, "expected": {"has_travel_date": True,"has_travel_time": False,"travel_date": "2018-03-07","travel_time": None}},
        {"input": {'value': '2018-03-06T00:00:00.000-08:00', 'grain': 'day'}, "expected": {"has_travel_date": True,"has_travel_time": False,"travel_date": "2018-03-06","travel_time": None}},
        {"input": {'value': '2018-03-12T00:00:00.000-07:00', 'grain': 'week'}, "expected": {"has_travel_date": False,"has_travel_time": False,"travel_date": None,"travel_time": None}},
        {"input": {'value': '2018-03-06T09:00:00.000-08:00', 'grain': 'hour'}, "expected": {"has_travel_date": True,"has_travel_time": True,"travel_date": "2018-03-06","travel_time": "09:00:00"}},
        {"input": {'value': '2018-03-06T22:00:00.000-08:00', 'grain': 'hour'}, "expected": {"has_travel_date": True,"has_travel_time": True,"travel_date": "2018-03-06","travel_time": "22:00:00"}},
        {"input": {'value': '2018-03-06T10:15:00.000-08:00', 'grain': 'minute'}, "expected": {"has_travel_date": True,"has_travel_time": True,"travel_date": "2018-03-06","travel_time": "10:15:00"}},
        {"input": {'value': '2018-03-07T00:00:00.000-08:00', 'grain': 'hour'}, "expected": {"has_travel_date": True,"has_travel_time": True,"travel_date": "2018-03-07","travel_time": "00:00:00"}},
        {"input": {'value': '2018-03-12T00:15:00.000-07:00', 'grain': 'minute'}, "expected": {"has_travel_date": True,"has_travel_time": True,"travel_date": "2018-03-12","travel_time": "00:15:00"}},
    ]

    for element in test_set:
        result = update_state({}, element["input"])
        assert result == element["expected"], "difference in test case: " + element["input"]["value"]
