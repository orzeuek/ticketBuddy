import json
import os
import nltk
import pprint
import src.stations_extraction

# PRO TIP:
# to see all available POS (part of speech) use:  nltk.help.upenn_tagset()

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = DIR + '/../'

def prepare_pos_tagged_sentences(training_set):
    tagged_sentences = [
        nltk.pos_tag(nltk.word_tokenize(element["text"].lower())) for element in training_set
    ]

    json_structure = [
        [{"word": element[0], "pos": element[1], "classification": ""} for element in sentence] for sentence in tagged_sentences
    ]

    # uncomment it to print "ready to copy" json :)
    # json_string = json.dumps(json_structure)
    # pprint.pprint(json_string)
    return json_structure


def get_trained_unigram_tagger():
    train_data_input = json.load(open(ROOT_DIR + '/src/assets/training_Sets/stationsExtractionTrainingSet.json'))
    train_data = [[(element["pos"], element["classification"]) for element in sentence] for sentence in train_data_input]
    return nltk.UnigramTagger(train_data)

## already done. Results in /src/assets/training_Sets/stationsExtractionTrainingSet.json
# result = prepare_pos_tagged_sentences(json.load(open(ROOT_DIR + '/src/assets/training_Sets/stationsExtractionInput.json')))
#
# pprint.pprint(result)

src.stations_extraction.train_tagger()
