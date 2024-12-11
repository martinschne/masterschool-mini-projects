import json


def load_data(file_path: str) -> list[dict]:
    """
    Loads JSON file
    :param file_path: relative path to the JSON file
    :return: JSON object
    """
    with open(file_path, 'r') as handle:
        return json.load(handle)


def get_prop_value(animal: list[dict], prop_description: str, keys: list[str]) -> tuple[str | None, any]:
    """
    Get property value nested in 'animal' under keys accessors
    :param animal: source of lookup
    :param prop_description: property description
    :param keys: list of ordered access keys for lookup
    :return: tuple (prop_description, value) or
    (None, None) if value was not found under keys
    """
    current_value = animal
    for key in keys:
        current_value = current_value.get(key, {})

    if current_value != {}:
        return prop_description, current_value
    return None, None


def print_prop_value(prop_description: str, value):
    """
    Print property description and given value in set format
    'prop_description: value'
    :param prop_description: description of the property value
    :param value: any value provided
    :return None
    """
    if prop_description is not None:
        print(f"{prop_description}: {value}")


def main():
    """
    Main method to run the program
    :return: None
    """
    animals_data = load_data("animals_data.json")

    for animal in animals_data:
        print_prop_value(*get_prop_value(animal, "Name", ["name"]))
        print_prop_value(*get_prop_value(animal, "Diet", ["characteristics", "diet"]))

        (prop_name, value) = get_prop_value(animal, "Location", ["locations"])
        print_prop_value(prop_name, value[0])

        print_prop_value(*get_prop_value(animal, "Type", ["characteristics", "type"]))
        print()


if __name__ == "__main__":
    main()
