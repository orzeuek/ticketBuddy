import nltk
import os, inspect, pickle, json
import src.stations_extraction


def extract(input, classifier):
    """
    :param input:
     {
         "has_origin": False,
         "has_destination": False,
         "text": "I want to buy a ticket from London to Horsham"
     }
    :param classifier:
    :return
    [
        {
            "has_origin": True,
            "origin": "London",
            "has_destination": True,
            "destination": "Horsham",
            "text": "I want to buy a ticket from London to Horsham"
        }
    ]
    """

    features_with_stations = prepare_features_with_stations([input])
    classified = [(classifier.classify(feature), station) for feature, station in features_with_stations]
    for entry in classified:
        feature = entry[0].lower()
        input[feature] = entry[1]
        input['has_' + feature] = True

    return input


def train_classifier(input_dictionary):
    features_set = prepare_train_set(input_dictionary)
    return nltk.NaiveBayesClassifier.train(features_set)


def prepare_train_set(input_dictionary):
    """
    :param input_dictionary:
    [
        {
            "has_origin": False,
            "has_destination": False,
            "text": "I want to buy a ticket from London to Horsham"
        },
        {...}, {...}
    ]
    :return:
    [
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
    """
    features_with_stations = prepare_features_with_stations(input_dictionary)

    return [(features, 'ORIGIN' if station == 'london' else 'DESTINATION') for features, station in
            features_with_stations]


def prepare_features_with_stations(input_dictionary):
    """
    :param input_dictionary:
     [
        {
            "has_origin": False,
            "has_destination": False,
            "text": "I want to buy a ticket from London to Horsham"
        },
        {...}, {...}
     ]
    :return:
    [
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
    """
    features_with_texts = [
        {'text': element['text'], 'features': prepare_features_set([element])} for
        element in input_dictionary
        ]
    features_with_stations = []
    for element in features_with_texts:
        for features in element['features']:
            # little bit of magic to extract only "pattern feature" (ie. 'from_STATION_to')
            extracted_features = [key for key in features if '_STATION_' in key]
            pattern = extracted_features[0]
            features_with_stations.append(
                (features, extract_station_from_text_by_pattern(pattern, element['text']))
            )
    return features_with_stations


def extract_station_from_text_by_pattern(pattern, text):
    """
    :param pattern: "from_STATION_to"
    :param text: "I want to buy a ticket from London Euston to Horsham"
    :return: "london euston"
    """
    tagged_input = tag_stations(text)
    exploded_pattern = pattern.split("_")
    prefix = None if exploded_pattern[0] == "" else exploded_pattern[0]
    postfix = None if exploded_pattern[2] == "" else exploded_pattern[len(exploded_pattern) - 1]

    if len(tagged_input) == 1 and tagged_input[0][1] == "STATION":
        return tagged_input[0][0]
    if len(tagged_input) == 2:
        for (w1, t1), (w2, t2) in nltk.bigrams(tagged_input):
            if t1 == "STATION":
                return w1
            elif t2 == "STATION":
                return w2
            else:
                raise Exception("STATION not found in text!")

    for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(tagged_input):
        if t1 == "STATION" and prefix is None and w2 == postfix:
            return w1
        if t2 == "STATION" and w1 == prefix and w3 == postfix:
            return w2
        if t3 == "STATION" and w2 == prefix and postfix is None:
            return w3


def prepare_features_set(input_dictionary):
    """
    :param input_dictionary:
    [
        {
            "has_origin": False,
            "has_destination": False,
            "text": "I want to buy a ticket from London to Horsham"
        },
        {...}, {...}
    ]
    :return:
    [
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
        {...},{...}
    ]
    """
    out = []
    for element in input_dictionary:
        for station_feature in extract_station_feature(element['text']):
            element_features = {
                "has_origin": element['has_origin'],
                "has_destination": element['has_destination']
            }
            element_features.update({station_feature: True})
            out.append(element_features)

    return out


def extract_station_feature(sentence):
    """
    :param sentence: sentence where we want to find stations features
    :return: list of feature strings:
     ["from_STATION_to", "to_STATION_"]
    """
    sentence = sentence.lower()
    tagged_sentence = tag_stations(sentence)
    features = []
    if len(tagged_sentence) == 1 and tagged_sentence[0][1] == "STATION":
        return ["_STATION_"]
    if len(tagged_sentence) == 2:
        for (w1, t1), (w2, t2) in nltk.bigrams(tagged_sentence):
            if w1 == tagged_sentence[0][0] and t1 == "STATION":
                features.append("_".join(["", t1, w2]))
            elif t2 == "STATION":
                features.append("_".join([w1, t2, ""]))
        return features

    for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(tagged_sentence):
        if w1 == tagged_sentence[0][0] and t1 == "STATION":
            features.append("_".join(["", t1, w2]))
        elif t2 == "STATION":
            features.append("_".join([w1, t2, w3]))
        elif w3 == tagged_sentence[-1][0] and t3 == "STATION":
            features.append("_".join([w2, t3, ""]))
        else:
            continue
    if len(features) == 0:
        raise Exception("No station found in sentence: " + sentence)
    return features


def tag_stations(sentence, stations_list=None):
    """
    :param sentence: string where we want to find stations
    :param stations_list: list of stations, all should be lower case.
    :return: list of tuples:
     [
        ("from", ""),
        ("london euston", "STATION"),
        ("to", ""),
        ("horsham", "STATION"),
     ],
    """
    # return src.stations_extraction.extract(sentence, stations_list=stations_list)
    if stations_list is None:
        file_path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        ) + '/assets/stations_list.txt'
        with open(file_path) as f:
            stations_list = [line.strip().lower() for line in f if len(line.strip()) > 0]

    sentence = sentence.lower()
    implode_marker = '____'
    stations_matched = []
    for station in stations_list:
        if station in sentence:
            station_tokenized = implode_marker.join(station.split(" "))
            sentence = sentence.replace(station, station_tokenized)
            stations_matched.append(station_tokenized)
    return [
        (token.replace(implode_marker, " "), "STATION" if token in stations_matched else "")
        for token in nltk.tokenize.word_tokenize(sentence)
        ]


def train_stations_classifier():
    files = [
        "/assets/training_sets/hasOriginNoDestination.json",
        "/assets/training_sets/noOriginHasDestination.json",
        "/assets/training_sets/noOriginNoDestination.json"
    ]
    absolute_path = os.path.abspath(os.path.dirname(__file__))
    data = []
    for file in files:
        json_data = open(absolute_path + file).read()
        data += (json.loads(json_data))

    classifier = train_classifier(data)
    pickle.dump(classifier, open("origin_destination_classifier.p", "wb"))

    return classifier
