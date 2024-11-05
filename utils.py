import os.path
from os import listdir
from os.path import isfile, join
import shutil
import json
from jsonschema import Draft202012Validator

from datafiles import DATAFILES


def validate_schema(schema: dict):
    """
    Checks whether a schema is a valid Draft-2020-12 JSON Schema
    :param schema: The schema to be tested
    """
    Draft202012Validator.check_schema(schema)
    return True


def validate_dict_againt_schema(schema: dict, data: dict):
    validator = Draft202012Validator(schema)
    validator.validate(data)
    return True


def validate_json_file_against_schema_file(schema_path: str, data_path: str):
    """
    Validates a json file against a json-schema file
    :param schema_path: Path to the json-schema file
    :param data_path: Path to the json-data file
    """
    with open(schema_path) as schemafile:
        schema = json.load(schemafile)
    with open(data_path) as datafile:
        data = json.load(datafile)

    validate_dict_againt_schema(schema, data)


def get_html_filenames_in_directory(path: str) -> list[str]:
    """
    Lists all .html files within a given directory
    :param path: path to the directory
    :return: List of all html filenames
    """
    # list all files in given directory
    files = [f for f in listdir(path) if isfile(join(path, f)) and f.split(".")[-1] == "html"]
    files.sort(reverse=True)
    return files


def check_template_file_presence():
    for template_path in [DATAFILES[file]["template"] for file in DATAFILES]:
        if not os.path.exists(template_path):
            raise FileNotFoundError("Could not locate template: " + template_path)


def check_schema_file_presence():
    for schema_path in [DATAFILES[file]["schema"] for file in DATAFILES]:
        if not os.path.exists(schema_path):
            raise FileNotFoundError("Could not locate schema file: " + schema_path)


def check_all_schema_file_validity():
    for schema_path in [DATAFILES[file]["schema"] for file in DATAFILES]:
        with open(schema_path) as schemafile:
            schema = json.load(schemafile)
        validate_schema(schema)


def check_all_data_files_against_schema():
    for file in [DATAFILES[file] for file in DATAFILES]:
        validate_json_file_against_schema_file(file["schema"], file["data"])


def create_data_folder_structure():

    # order of directories is important
    # check for parent directories first
    required_directories_paths = [
        "data",
        "data/gi",
        "data/gi/erstsemester",
        "data/gi/fachschaft",
        "data/gi/jobs",
        "data/gi/news",
        "data/gi/start",
        "data/gi/studium",
        "data/geoloek"
    ]

    for path in required_directories_paths:
        if not os.path.exists(path):
            os.makedirs(path)

    for datafile in [DATAFILES[file] for file in DATAFILES]:
        if not os.path.exists(datafile["data"]):
            shutil.copy(datafile["template"], datafile["data"])


if __name__=="__main__":
    create_data_folder_structure()
    check_all_data_files_against_schema()