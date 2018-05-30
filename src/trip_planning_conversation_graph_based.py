dialog_graph = {
    "dialog_initialization": {
        "Any": "extract_keywords"
    },
    "extract_keywords": {
        "Any": "has_origin"
    },
    "has_origin": {
        "True": "has_destination",
        "False": "ask_about_origin_station"
    },
    "ask_about_origin_station": {
        "Any": "has_origin"
    },
    "has_destination": {
        "True": "has_date",
        "False": "ask_about_destination_station"
    },
    "ask_about_destination_station": {
        "Any": "has_destination"
    },
    "has_date": {
        "True": "has_time",
        "False": "ask_about_date"
    },
    "ask_about_date": {
        "Any": "has_date"
    },
    "has_time": {
        "True": "send_jp_request",
        "False": "ask_about_time"
    },
    "ask_about_time": {
        "Any": "has_time"
    },
    "send_jp_request": {
        "Any": "complete"
    }
}

def proceed(state, steps_definition, entry_point):
    """
    flow:
      execute steps_definition.entry_point(state)
      if state has any prompt:
        return state (show prompt to client)

      if next step is "Any" then execute next step recursively
      else proceed with next step depending on what was result of entry_point(state) execution (True/False).
    """

    ## @todo add recursion limit to 3 repetitions.
    current_step_result = getattr(steps_definition, entry_point)(state)
    if state["prompt"] is not None:
        return state

    possible_steps = dialog_graph[entry_point]
    if "Any" in possible_steps.keys():
        next_step_name = possible_steps["Any"]
        proceed(state, steps_definition, next_step_name)
    else:
        proceed(
            state,
            steps_definition,
            possible_steps["True"] if current_step_result is True else possible_steps["False"]
        )

    return state