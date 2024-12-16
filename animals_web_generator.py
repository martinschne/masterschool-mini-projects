import json


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


def main():
    """
    Main method to run the program
    :return: None
    """
    animals_data = load_json("animals_data.json")
    output = "" # define an empty string

    for animal in animals_data:
        # serializing to html format
        output += "            <li class=\"cards__item\">\n"
        output += f"                <div class=\"card__title\">{animal["name"]}</div>\n" if "name" in animal else ""
        output += "                 <p class=\"card__text\">\n"
        output += f"                    <strong>Diet:</strong> {animal["characteristics"]["diet"]}<br>\n" if "diet" in animal["characteristics"] else ""
        output += f"                    <strong>Location:</strong> {animal["locations"][0]}<br>\n" if "locations" in animal else ''
        output += f"                    <strong>Type:</strong> {animal["characteristics"]["type"]}<br>\n" if "type" in animal["characteristics"] else ""
        output += "                 </p>\n"
        output += "            </li>\n"

    output = output[12:-1] # remove the first spaces and last newline after serializing all items

    animals_template_site = load_file("animals_template.html")
    animals_template_site = animals_template_site.replace("__REPLACE_ANIMALS_INFO__", output)
    write_to_file("animals.html", animals_template_site)


if __name__ == "__main__":
    main()