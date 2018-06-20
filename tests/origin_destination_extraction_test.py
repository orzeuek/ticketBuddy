from src.origin_destination_extraction import *


def testExtractForNotFullStationInfo():
    input = {
        "has_origin": False,
        "has_destination": False,
        "text": "I want to go to Horsham"
    }
    result = extract(input, train_classifier([input]))
    expected = {
        "has_origin": False,
        "has_destination": True,
        "destination": "horsham",
        "text": "I want to go to Horsham"
    }
    assert expected == result


def testExtractForSingleStation():
    input = {
        "has_origin": True,
        "origin": "london",
        "has_destination": False,
        "text": "Horsham"
    }
    result = extract(input, train_classifier([input]))
    expected = {
        "has_origin": True,
        "origin": "london",
        "has_destination": True,
        "destination": "horsham",
        "text": "Horsham"
    }
    assert expected == result


def testExtract():
    input = {
        "has_origin": False,
        "has_destination": False,
        "text": "I want to buy a ticket from London to Horsham"
    }
    result = extract(input, train_classifier([input]))
    expected = {
        "has_origin": True,
        "origin": "london",
        "has_destination": True,
        "destination": "horsham",
        "text": "I want to buy a ticket from London to Horsham"
    }
    assert expected == result


def testPrepareTrainSet():
    input = [
        {
            "has_origin": False,
            "has_destination": False,
            "text": "I want to buy a ticket from London to Horsham"
        }
    ]
    result = prepare_train_set(input)
    expected = [
        (
            {
                "has_origin": False,
                "has_destination": False,
                "from_STATION_to": True
            },
            "ORIGIN"
        ),
        (
            {
                "has_origin": False,
                "has_destination": False,
                "to_STATION_": True
            },
            "DESTINATION"
        )
    ]
    assert expected == result


def testPrepareFeaturesWithStations():
    input = [
        {
            "has_origin": False,
            "has_destination": False,
            "text": "I want to buy a ticket from London to Horsham"
        }
    ]
    result = prepare_features_with_stations(input)
    expected = [
        (
            {
                "has_origin": False,
                "has_destination": False,
                "from_STATION_to": True
            },
            "london"
        ),
        (
            {
                "has_origin": False,
                "has_destination": False,
                "to_STATION_": True
            },
            "horsham"
        )
    ]
    assert expected == result


def testExtractStationFromTextByPattern():
    input = "I want to buy a ticket from London Euston to Horsham"
    pattern1 = "from_STATION_to"
    assert "london euston" == extract_station_from_text_by_pattern(pattern1, input)
    pattern2 = "to_STATION_"
    assert "horsham" == extract_station_from_text_by_pattern(pattern2, input)
    pattern3 = "_STATION_to"
    assert "london" == extract_station_from_text_by_pattern(pattern3, "London to Horsham")
    pattern4 = "_STATION_"
    assert "london" == extract_station_from_text_by_pattern(pattern4, "London")
    pattern5 = "to_STATION_"
    assert "london" == extract_station_from_text_by_pattern(pattern5, "to London")


def testPrepareFeaturesSet():
    input = [
        {
            "has_origin": False,
            "has_destination": False,
            "text": "I want to buy a ticket from London to Horsham"
        },
        {
            "has_origin": False,
            "has_destination": True,
            "text": "london"
        },
        {
            "has_origin": True,
            "has_destination": False,
            "text": "to horsham"
        }
    ]
    result = prepare_features_set(input)
    expected = [
        {
            "has_origin": False,
            "has_destination": False,
            "from_STATION_to": True
        },
        {
            "has_origin": False,
            "has_destination": False,
            "to_STATION_": True
        },
        {
            "has_origin": False,
            "has_destination": True,
            "_STATION_": True
        },
        {
            "has_origin": True,
            "has_destination": False,
            "to_STATION_": True
        }
    ]
    assert expected == result


def testExtractStationFeature():
    input = "I want to buy a ticket from London to Horsham"
    result = extract_station_feature(input)
    assert ["from_STATION_to", "to_STATION_"] == result


def testExtractStationFeatureWith1WordsSentence():
    input = "London"
    result = extract_station_feature(input)
    assert ["_STATION_"] == result


def testExtractStationFeatureWith2WordsSentence():
    input = "to Horsham"
    result = extract_station_feature(input)
    assert ["to_STATION_"] == result


def testTagStations():
    input = "I want to buy a ticket from London Euston to Horsham"
    result = tag_stations(input, ["london euston", "horsham"])
    assert [
            ("i", ""),
            ("want", ""),
            ("to", ""),
            ("buy", ""),
            ("a", ""),
            ("ticket", ""),
            ("from", ""),
            ("london euston", "STATION"),
            ("to", ""),
            ("horsham", "STATION"),
        ] == result

