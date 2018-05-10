import os, pickle, json, nltk
from nltk.util import bigrams

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = DIR + '/../'


# get new, freshly trained instance of UnigramTagger.
def train_tagger():
    train_data_input = json.load(open(ROOT_DIR + '/src/assets/training_Sets/stationsExtractionTrainingSet.json'))
    train_data = [[(element["pos"], element["classification"]) for element in sentence] for sentence in
                  train_data_input]
    tagger = nltk.UnigramTagger(train_data)
    pickle.dump(tagger, open(ROOT_DIR + "/src/assets/trained_classifiers/stations_classifier.p", "wb"))

    return tagger


# load already trained classifier
def load_trained_tagger():
    return pickle.load(open(ROOT_DIR + "/src/assets/trained_classifiers/stations_classifier.p", "rb"))


def categorize_stations(text, stations_tagger: nltk.UnigramTagger = None):
    stations_tagger = load_trained_tagger() if stations_tagger is None else stations_tagger

    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(text))
    tagged_pos = stations_tagger.tag([element[1] for element in tagged_sentence])
    tagging_result = list(map(
        lambda tagged_word: (tagged_word[0][0], tagged_word[1][1]),  # extract (<word>, <category>)
        list(zip(tagged_sentence, tagged_pos))  # merge (<word>, <pos>) with (<pos>, <category>)
    ))
    return _extract_stations_list_from_tagged_sentence(tagging_result)


# I'm too lame in functional programming to do it in functional way :)
def _extract_stations_list_from_tagged_sentence(tagged_sentence):
    result = []
    is_first_element = True

    for (word1, class1), (word2, class2) in list(bigrams(tagged_sentence)):
        if is_first_element:
            is_first_element = False
            if class1 != 'STATION':
                continue
            result.append(word1)

        if class2 != 'STATION':
            continue

        if class1 == 'STATION':
            last_station = result.pop()
            result.append(last_station + ' ' + word2)
        else:
            result.append(word2)

    return result