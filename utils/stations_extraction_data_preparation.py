import json
import sys, os
import nltk
import pprint

# PRO TIP:
# to see all available POS (part of speech) use:  nltk.help.upenn_tagset()

DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = DIR + '/../'
sys.path.append(ROOT_DIR)


def prepare_pos_tagged_sentences(training_set):
    tagged_sentences = [
        nltk.pos_tag(nltk.word_tokenize(element["text"])) for element in training_set
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
# prepare_pos_tagged_sentences(json.load(open(ROOT_DIR + '/src/assets/training_Sets/stationsExtractionInput.json')))

tagger = get_trained_unigram_tagger()

train_data_input = json.load(open(ROOT_DIR + '/src/assets/training_Sets/stationsExtractionTrainingSet.json'))
test_sentence = [{"text": "I want to travel from Manchester Airport to Zgierz"}]
test_data = prepare_pos_tagged_sentences(test_sentence)

tagged = tagger.tag([element["pos"] for element in test_data[0]])

pprint.pprint(" ".join([element["word"] for element in test_data[0]]))
pprint.pprint(tagged)