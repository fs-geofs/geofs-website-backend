from flask import Flask, make_response
import json

from jsonschema.exceptions import ValidationError
import utils
from os.path import join
from functools import wraps

from datafiles import DATAFILES, OTHER_FILES

from errors import IntegrityError

import sys


try:
    utils.check_template_file_presence()  # Check if all data templates are there:
    utils.check_schema_file_presence()  # check if all schema files are there:
    utils.check_all_schema_file_validity()  # check if all schema files are valid jsonschema-2020-12 schemas
    utils.create_data_folder_structure()  # Check if the data folder structure exists; If not, create it
    utils.check_all_data_files_against_schema()  # check if all data files conform to their schema
except IntegrityError as e:
    print("Startup Checks for backend server failed.")
    print(e)

    # DO NOT CHANGE EXIT CODE 4!!!!!!
    # Code 4 is required to take effect in gunicorn deployment
    # Gunicorn is used inside Docker build
    sys.exit(4)
except Exception as e:
    print("Startup Checks for backend server failed. An unforseen error occured:")
    print(e)

    # DO NOT CHANGE EXIT CODE 4!!!!!!
    # Code 4 is required to take effect in gunicorn deployment
    # Gunicorn is used inside Docker build
    sys.exit(4)


app = Flask(__name__)


def handle_errors(func):
    """
    A decorator that wraps around any endpoint to catch and handle any error that may occur
    :param func: Callback function
    :return: the wrapped function
    """
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except json.JSONDecodeError as e:
            print("File is not a valid JSON file")
            print(e)
            return {"error": "File is not a valid json file"}, 500
        except ValidationError as e:
            print("JSON file does not conform to its associated JSON-Schema")
            print(e)
            return {"error": "File does not validate against its schema"}, 500
        except FileNotFoundError as e:
            print("Could not find specified file")
            print(e)
            return {"error": "Could not locate a specific file. See console output for details"}, 500
        except Exception as e:
            print(e)
            return {"error": "An internal server error has occured."}, 500
    return wrapper_func


@app.route("/")
def hello():
    return {"version": "1.0"}


@app.route('/erstiwoche')
@handle_errors
def erstiwoche():
    with open(DATAFILES["gi_erstiwoche"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["gi_erstiwoche"]["schema_validator"], data)
    return data


@app.route("/erstiwochenende")
@handle_errors
def erstiwochenende():
    with open(DATAFILES["gi_erstiwochenende"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["gi_erstiwochenende"]["schema_validator"], data)
    return data


@app.route("/erstistundenplan")
@handle_errors
def stundenplan():
    with open(DATAFILES["gi_stundenplan"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["gi_stundenplan"]["schema_validator"], data)
    return data


@app.route("/fachschaft_rollen")
@handle_errors
def rollen():
    with open(DATAFILES["gi_rollen"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["gi_rollen"]["schema_validator"], data)
    return data


@app.route("/praesidienste")
@handle_errors
def praesidienste():
    with open(DATAFILES["gi_praesidienste"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["gi_praesidienste"]["schema_validator"], data)
    return data


@app.route("/termine")
@handle_errors
def termine():
    with open(DATAFILES["gi_termine"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["gi_termine"]["schema_validator"], data)
    return data


@app.route("/jahrgaenge")
@handle_errors
def jahrgaenge():
    with open(DATAFILES["gi_jahrgaenge"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["gi_jahrgaenge"]["schema_validator"], data)
    return data


@app.route("/joblistings")
@handle_errors
def jobs():

    path = "data/gi/jobs"
    filenames = utils.get_html_filenames_in_directory(path)

    data = []
    for filename in filenames:
        with open(join(path, filename)) as file:
            filecontent = file.read().replace("\n", " ")  # read file and replace newline with dash
        data.append({"id": filename, "content": filecontent})
    return data


@app.route("/news")
@handle_errors
def news():

    path = "data/gi/news"
    filenames = utils.get_html_filenames_in_directory(path)

    data = []
    for filename in filenames:
        with open(join(path, filename)) as file:
            filecontent = file.read().replace("\n", " ")  # read file and replace newline with dash
        data.append({
            "id": filename,
            "date": filename.split("_")[0],
            "content": filecontent
        })
    return data


@app.route("/foto_gi")
@handle_errors
def foto_gi_fachschaft():
    with open(OTHER_FILES["foto_gi"]["data"], "rb") as file:
        data = file.read()
    response = make_response(data)
    response.headers["Content-Type"] = "image/jpeg"
    response.headers["Content-Disposition"] = "inline; filename=fachschaft.jpg"
    return response


@app.route("/geoloek_praesidienste")
@handle_errors
def geoloek_praesidienste():
    with open(DATAFILES["geoloek_praesidienste"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["geoloek_praesidienste"]["schema_validator"], data)
    return data


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
