import json

with open("configs/utils_configs/programming_languages_to_extension_mapping.json","r") as file:
    mapping=json.load(file)


def ExtensionToProgrammingLanguage(extension:str) -> str|None:
    for key,value in mapping.items():
        if extension in value:
            return key

    return None