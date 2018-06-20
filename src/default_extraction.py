import src.origin_destination_extraction as stations
import src.dates_extraction as dates
import pprint
import config.configuration as conf


def extract(state, stations_classifier):
    try:
        state.update(stations.extract(state, stations_classifier))
    except Exception as e:
        pprint.pprint(e)

    try:
        state.update(
            dates.extract(
                state,
                dates.DatesService(
                    "http://" + conf.get_duckling_host() + ":" + conf.get_duckling_port()
                )
            )
        )
    except Exception as e:
        pprint.pprint(e)

    return state
