import os
import json


def get_project_root_directory() -> str:
    utils_directory = os.path.dirname(os.path.abspath(__file__))

    return os.path.dirname(utils_directory)


def get_config_path() -> str:
    root_directory = get_project_root_directory()

    return os.path.join(root_directory, "config.json")


def get_config() -> dict[str, str]:
    config = open(get_config_path())

    return json.load(config)


def get_documents_path() -> str:
    config = get_config()

    return os.path.join(get_project_root_directory(), config["scrapped_documents_path"])
