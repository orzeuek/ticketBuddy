import src.stations_extraction

def test_categorize_stations():
    test_sentence = "Plan me a journey from Manchester Airport to London"
    result = src.stations_extraction.categorize_stations(test_sentence)

    assert result == ["Manchester Airport", "London"]