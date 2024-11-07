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


def validate_dict_againt_schema(validator: Draft202012Validator, data: dict):
    validator.validate(data)


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
    for file in DATAFILES:
        schema_path = DATAFILES[file]["schema"]
        try:
            with open(schema_path) as schemafile:
                schema = json.load(schemafile)
        except JSONDecodeError as e:
            raise IntegrityError(f"{schema_path} is not a valid JSON-File. Check the file's syntax and try again.\n" +
                                 str(e))

        try:
            validate_schema(schema)
            DATAFILES[file]["schema_validator"] = Draft202012Validator(schema)
        except SchemaError:
            raise IntegrityError("Invlaid Schema (schema file does not conform to Jsonschema-2020-12 standard: "
                                 + schema_path)


def check_all_data_files_against_schema():
    for file in DATAFILES:
        data_file_path = DATAFILES[file]["data"]
        schema_file_path = DATAFILES[file]["schema"]
        validator = DATAFILES[file]["schema_validator"]

        if validator is None:
            check_all_schema_file_validity()
            validator = DATAFILES[file]["schema_validator"]

        try:
            with open(data_file_path) as datafile:
                data = json.load(datafile)
        except JSONDecodeError as e:
            raise IntegrityError(f"{data_file_path} is not a valid JSON-File. Check file syntax and try again.\n" +
                                 str(e))

        try:
            validate_dict_againt_schema(validator, data)
        except ValidationError as e:
            raise IntegrityError(
                "JSON-File does not conform to its schema\n"
                "JSON: " + data_file_path + "\n"
                                            "Schema: " + schema_file_path +
                "Error Detail:\n" + str(e)
            )


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
    check_all_data_files_against_schema()