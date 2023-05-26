import os


def get_environment_input_data() -> dict:
    """Get the input data from the environment variables."""
    search_phrase = os.getenv("SEARCH_PHRASE"),

    if type(search_phrase) == tuple:
        search_phrase = search_phrase[0]

    if os.getenv("SECTION") is not None:
        section = [sect.strip() for sect in os.getenv("SECTION").split(",")]
    else:
        section = []

    number_of_months = os.getenv("NUMBER_OF_MONTHS")

    if number_of_months is not None and number_of_months.isdigit():
        number_of_months = int(number_of_months)
    else:
        number_of_months = 0

    return {
        "search_phrase": search_phrase,
        "section": section,
        "number_of_months": number_of_months
    }
