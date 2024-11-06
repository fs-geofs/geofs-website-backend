import os.path
from os import listdir
from os.path import isfile, join
import shutil

import json
from json.decoder import JSONDecodeError

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from datafiles import DATAFILES, OTHER_FILES

from errors import IntegrityError


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


def validate_json_file_against_schema_file(schema_path: str, data_path: str):
    """
    Validates a json file against a json-schema file
    :param schema_path: Path to the json-schema file
    :param data_path: Path to the json-data file
    """
    try:
        with open(schema_path) as schemafile:
            schema = json.load(schemafile)
    except JSONDecodeError as e:
        raise IntegrityError(f"{schema_path} is not a valid JSON-File. Check the file's syntax and try again.\n" +
                             str(e))

    try:
        with open(data_path) as datafile:
            data = json.load(datafile)
    except JSONDecodeError as e:
        raise IntegrityError(f"{schema_path} is not a valid JSON-File. Check the file's syntax and try again.\n" +
                             str(e))

    try:
        validate_dict_againt_schema(schema, data)
    except ValidationError as e:
        raise IntegrityError(
            "JSON-File does not conform to its schema\n"
            "JSON: " + data_path + "\n"
            "Schema: " + schema_path +
            "Error Detail:\n" + str(e)
        )


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

    # json files
    for template_path in [DATAFILES[file]["template"] for file in DATAFILES]:
        if not os.path.exists(template_path):
            raise IntegrityError("Could not locate template: " + template_path)

    # other files
    for template_path in [OTHER_FILES[file]["template"] for file in OTHER_FILES]:
        if not os.path.exists(template_path):
            raise IntegrityError("Could not locate template: " + template_path)


def check_schema_file_presence():
    for schema_path in [DATAFILES[file]["schema"] for file in DATAFILES]:
        if not os.path.exists(schema_path):
            raise IntegrityError("Could not locate schema file: " + schema_path)


def check_all_schema_file_validity():
    for schema_path in [DATAFILES[file]["schema"] for file in DATAFILES]:
        try:
            with open(schema_path) as schemafile:
                schema = json.load(schemafile)
        except JSONDecodeError as e:
            raise IntegrityError(f"{schema_path} is not a valid JSON-File. Check the file's syntax and try again.\n" +
                                 str(e))

        try:
            validate_schema(schema)
        except SchemaError:
            raise IntegrityError("Invlaid Schema (schema file does not conform to Jsonschema-2020-12 standard: "
                                 + schema_path)


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

    for other_file in [OTHER_FILES[file] for file in OTHER_FILES]:
        if not os.path.exists(other_file["data"]):
            shutil.copy(other_file["template"], other_file["data"])


if __name__=="__main__":
    create_data_folder_structure()
    check_all_data_files_against_schema()