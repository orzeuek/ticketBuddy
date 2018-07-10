import src.stations_extraction
import unittest


class StationsExtractionTest(unittest.TestCase):

    def test_categorize_stations(self):
        test_sentence = "Plan me a journey from Manchester Airport to London"
        result = src.stations_extraction.categorize_stations(test_sentence)

        expected = [("plan", ""), ("me", ""), ("a", ""), ("journey", ""), ("from", ""),
                    ("manchester airport", "STATION"), ("to", ""), ("london", "STATION")]

        self.assertSequenceEqual(seq1=result, seq2=expected)

    def test_extract_with_keyword_match(self):
        test_sentence = "I want to travel from Manchester Airport to Zgierz"
        stations_list = ["zgierz"]
        trained_tagger = src.stations_extraction.load_trained_tagger()

        result = src.stations_extraction.extract(test_sentence, trained_tagger, stations_list)

        expected = [
            ("i", ""),
            ("want", ""),
            ("to", ""),
            ("travel", ""),
            ("from", ""),
            ("manchester", ""),
            ("airport", ""),
            ("to", ""),
            ("zgierz", "STATION"),
        ]

        self.assertSequenceEqual(expected, result)

    def test_extract_with_tagger_match(self):
        test_sentence = "I want to travel from Manchester Airport to Zgierz"
        stations_list = []
        trained_tagger = src.stations_extraction.load_trained_tagger()

        result = src.stations_extraction.extract(test_sentence, trained_tagger, stations_list)

        expected = [
            ("i", ""),
            ("want", ""),
            ("to", ""),
            ("travel", ""),
            ("from", ""),
            ("manchester airport", "STATION"),
            ("to", ""),
            ("zgierz", ""),
        ]

        self.assertSequenceEqual(expected, result)
