import os, inspect, pickle, json, nltk
from nltk.util import bigrams

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = DIR + '/../'


def extract(sentence, stations_tagger=None, stations_list=None):
    """
    it merge 2 strategies:
    1. key-word based search (using predefined list of stations)
    2. free-text search (using UnigramTagger - see categorize_stations() )
    :param sentence: string where we want to find stations
    :return: list of tuples:
     [
        ("from", ""),
        ("unknown station", "STATION"),
        ("to", ""),
        ("horsham", "STATION"),
     ],
    """
    stations_tagger = load_trained_tagger() if stations_tagger is None else stations_tagger
    stations_list = load_stations_list() if stations_list is None else stations_list

    keywords_result = tag_stations_using_keywords(sentence, stations_list)
    tagging_result = categorize_stations(sentence, stations_tagger)

    return merge_results(keywords_result, tagging_result)

def merge_results(result1, result2):
    """

    :param result1:
    [
        ('i', ''), ('want', ''), ('to', ''), ('travel', ''), ('from', ''),
        ('manchester', ''), ('airport', ''), ('to', ''), ('zgierz', 'STATION')
    ]
    :param result2:
    [
        ('i', ''), ('want', ''), ('to', ''), ('travel', ''), ('from', ''),
        ('manchester airport', 'STATION'), ('to', ''), ('zgierz', '')
    ]
    :return:
    [
        ('i', ''), ('want', ''), ('to', ''), ('travel', ''), ('from', ''),
        ('manchester airport', 'STATION'), ('to', ''), ('zgierz', 'STATION')
    ]
    """
    pass


def load_stations_list():
    file_path = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    ) + '/assets/stations_list.txt'
    with open(file_path) as f:
        stations_list = [line.strip().lower() for line in f if len(line.strip()) > 0]

    return stations_list


def train_tagger():
    """
    Get new, freshly trained instance of UnigramTagger.
    :return:
    """
    train_data_input = json.load(open(ROOT_DIR + '/src/assets/training_Sets/stationsExtractionTrainingSet.json'))
    train_data = [[(element["pos"], element["classification"]) for element in sentence] for sentence in
                  train_data_input]
    tagger = nltk.UnigramTagger(train_data)
    pickle.dump(tagger, open(ROOT_DIR + "/src/assets/trained_classifiers/stations_classifier.p", "wb"))

    return tagger


def load_trained_tagger():
    """
    load already trained classifier
    :return:
    """
    return pickle.load(open(ROOT_DIR + "/src/assets/trained_classifiers/stations_classifier.p", "rb"))


def categorize_stations(text, stations_tagger: nltk.UnigramTagger = None):
    """
    Categorize stations in a "smart way" - use it to find stations which are not known.

    :param text: simple string
    :param stations_tagger: nltk.UnigramTagger - use load_trained_tagger() to get trained one
    :return:
    """
    stations_tagger = load_trained_tagger() if stations_tagger is None else stations_tagger

    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(text))
    tagged_pos = stations_tagger.tag([element[1] for element in tagged_sentence])
    tagging_result = list(map(
        lambda tagged_word: (tagged_word[0][0], tagged_word[1][1]),  # extract (<word>, <category>)
        list(zip(tagged_sentence, tagged_pos))  # merge (<word>, <pos>) with (<pos>, <category>)
    ))
    return _tag_stations_full_names(tagging_result)


def _tag_stations_full_names(tagged_sentence):
    """
    I'm too lame in functional programming to do it in functional way :)
    Probably Knuth-Smith-Pratt algorithm could be used here, but first I implemented that,
    and then I discovered KSP algorithm :D

    :param tagged_sentence:
    [
        ('Plan', 'O'), ('me', 'O'), ('a', 'O'), ('journey', 'O'), ('from', 'O'),
        ('Manchester', 'STATION'), ('Airport', 'STATION'), ('to', 'O'), ('London', 'STATION')
    ]
    :return:
    [
        ('Plan', ''), ('a', ''), ('journey', ''), ('from', ''),
        ('Manchester Airport', 'STATION'), ('to', ''), ('London', 'STATION')
    ]
    """
    result = []
    is_first_element = True

    for (word1, class1), (word2, class2) in list(bigrams(tagged_sentence)):
        # special handling for 1st element of sequence
        if is_first_element:
            is_first_element = False
            if class1 != 'STATION':
                result.append((word1.lower(), ''))
            else:
                result.append((word1.lower(), 'STATION'))

        # regular logic for all other elements
        if class2 != 'STATION':
            result.append((word2.lower(), ''))
            continue

        if class1 == 'STATION':
            last_station = result.pop()
            result.append((last_station[0] + ' ' + word2.lower(), 'STATION'))
        else:
            result.append((word2.lower(), 'STATION'))

    return result


def tag_stations_using_keywords(sentence, stations_list):
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
