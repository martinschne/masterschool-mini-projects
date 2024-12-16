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
        output += "<li class='cards__item'>"
        output += f"Name: {animal["name"]}<br>\n" if "name" in animal else ""
        output += f"Diet: {animal["characteristics"]["diet"]}<br>\n" if "diet" in animal["characteristics"] else ""
        output += f"Location: {animal["locations"][0]}<br>\n" if "locations" in animal else ''
        output += f"Type: {animal["characteristics"]["type"]}<br>" if "type" in animal["characteristics"] else ""
        output += "</li>"

    animals_template_site = load_file("animals_template.html")
    animals_template_site = animals_template_site.replace("__REPLACE_ANIMALS_INFO__", output)
    write_to_file("animals.html", animals_template_site)


if __name__ == "__main__":
    main()