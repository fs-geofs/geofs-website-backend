from flask import Flask, make_response, request
import json

from jsonschema.exceptions import ValidationError
from . import utils
from os.path import join
from functools import wraps

from .datafiles import DATAFILES, OTHER_FILES

from .errors import IntegrityError

import sys

############################
#  Perform startup checks  #
############################


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


########################
#  Endpoints for FS-GI  #
########################


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
    # This URL has support for a query param called page (/news?page=2)
    # This param must be an integer >= 0
    # Reason: If the website grows and we have more and more news articles, it will eventually become slow
    # if all articles had to be opened and sent to the frontend
    # Therefore, only the first 5 latest articles are read by default (page=0),
    # the next 5 articles can be read on page 1, and so on...

    path = "data/gi/news"
    filenames = utils.get_html_filenames_in_directory(path)

    page = request.args.get("page")
    items_per_page = 5

    # set page parameter in case it was not given in URL
    if page is None:
        page = 0

    # cast page to integer
    try:
        page = int(page)
    except ValueError:
        page = 0

    # ignore negative page numbers
    if page < 0:
        page = 0

    if page*items_per_page >= len(filenames):
        page = 0

    start_index = page*items_per_page
    end_index = start_index + items_per_page

    response = {
        "next": page+1 if (page+1)*items_per_page < len(filenames) else None,
        "prev": page-1 if page != 0 else None
    }
    data = []
    for filename in filenames[start_index:end_index]:
        with open(join(path, filename)) as file:
            filecontent = file.read().replace("\n", " ")  # read file and replace newline with dash
        data.append({
            "id": filename,
            "date": filename.split("_")[0],
            "content": filecontent
        })
    response["news"] = data
    return response


@app.route("/foto_gi")
@handle_errors
def foto_gi_fachschaft():
    with open(OTHER_FILES["foto_gi"]["data"], "rb") as file:
        data = file.read()
    response = make_response(data)
    response.headers["Content-Type"] = "image/jpeg"
    response.headers["Content-Disposition"] = "inline; filename=fachschaft.jpg"
    return response


##############################
#  Endpoints for FS-Geoloek  #
##############################


@app.route("/geoloek_praesidienste")
@handle_errors
def geoloek_praesidienste():
    with open(DATAFILES["geoloek_praesidienste"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["geoloek_praesidienste"]["schema_validator"], data)
    return data


@app.route("/geoloek_termine")
@handle_errors
def geoloek_termine():
    with open(DATAFILES["geoloek_termine"]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES["geoloek_termine"]["schema_validator"], data)
    return data
