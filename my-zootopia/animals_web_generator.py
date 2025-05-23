import json


TEMPLATE_HTML_FILENAME = "animals_template.html"
GENERATED_HTML_FILENAME = "animals.html"

ANIMALS_LIST_PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"


def load_json(file_path: str) -> list[dict]:
    """
    Loads a JSON file as a readable
    :param file_path: relative path to the JSON file
    :return: JSON object
    """
    with open(file_path, 'r') as handle:
        return json.load(handle)


def load_file(file_path: str) -> str:
    """
    Load a file and return it as a string
    :param file_path: relative path to the file
    :return: content of the file as a string
    """
    with open(file_path, 'r') as file:
        return file.read()


def write_to_file(file_path: str, content: str):
    """
    Write content to the file
    :param file_path: relative path to the file
    :param content: content to write to the file
    """
    with open(file_path, 'w') as file:
        file.write(content)


def serialize_animal(animal_obj: dict, key: str, value: str) -> str:
    """
    Serialize animal object properties to html format
    :param animal_obj: source of animal properties
    :param key: get value under key in animal characteristics
    :param value: for comparing value under key with desired value
    :return: serialized html as a string or empty string if not desired value under key
    """
    output = ""
    # return pre
    if key in animal_obj["characteristics"] and animal_obj["characteristics"][key].lower() != value.lower():
        return ""

    # serializing to html format
    output += "            <li class=\"cards__item\">\n"
    output += f"                <div class=\"card__title\">{animal_obj["name"]}</div>\n"
    output += "                <p class=\"card__text\">\n"

    output += "                    <ul class=\"card__info\">\n"
    output += f"                       <li><strong>Diet:</strong> {animal_obj["characteristics"]["diet"]}</li>\n" \
        if "diet" in animal_obj["characteristics"] else ""

    output += f"                       <li><strong>Location:</strong> {animal_obj["locations"][0]}</li>\n" \
        if "locations" in animal_obj else ""

    output += (f"                       <li><strong>Type:</strong> "
               f"{animal_obj["characteristics"]["type"].capitalize()}</li>\n") \
        if "type" in animal_obj["characteristics"] else ""

    output += f"                       <li><strong>Family:</strong> {animal_obj["taxonomy"]["family"]}</li>\n"
    output += (f"                       <li><strong>Skin type:</strong> "
               f"{animal_obj["characteristics"]["skin_type"]}</li>\n") \
        if "skin_type" in animal_obj["characteristics"] else ""
    output += "                    </ul>\n"
    output += "                </p>\n"
    output += "            </li>\n"

    return output


def get_characteristic_values(animals_data: list[dict], key: str) -> list[str]:
    """
    Get all possible values for a property (key) in characteristics of an animal
    :param animals_data: data source of animal objects
    :param key: animal property
    :return: list of all distinct values under given key present in data source
    """
    values = set()
    for animal in animals_data:
        if key not in animal["characteristics"]:
            continue
        values.add(str(animal["characteristics"][key]))

    return list(values)


def main():
    """
    Main method to run the program
    :return: None
    """
    # Load animal data
    animals_data = load_json("animals_data.json")
    filter_by = "skin_type"

    print("Filter animals by skin type: ")
    selecting = True
    values = get_characteristic_values(animals_data, filter_by)
    while selecting:
        for value in values:
            print(value)

        selected_skin_type = input("Please enter the skin type: ")
        if selected_skin_type.lower() not in [prop.lower() for prop in values]:
            print("Invalid choice, please try again.")
            continue

        animals_template: str = load_file(TEMPLATE_HTML_FILENAME)

        # Load properties of animals, generate animals list
        animals_list_output = ""
        for animal in animals_data:
            animals_list_output += serialize_animal(animal, filter_by, selected_skin_type)

        # remove the first spaces and last newline after serializing all items
        animals_list_output = animals_list_output[12:-1]

        # Generate animal list and insert into template
        print(f"Generating page for animals with '{selected_skin_type.lower()}' skin type...")
        animals_template = animals_template.replace(ANIMALS_LIST_PLACEHOLDER, animals_list_output)
        write_to_file(GENERATED_HTML_FILENAME, animals_template)
        print("Done")

        selecting = False


if __name__ == "__main__":
    main()