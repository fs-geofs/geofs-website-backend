from flask import Flask, url_for
import json
import utils
from os.path import join
from functools import wraps

from datafiles import DATAFILES

# Check if all data templates are there:
utils.check_template_file_presence()

# check if all schema files are there:
utils.check_schema_file_presence()

# check if all schema files are valid jsonschema-2020-12 schemas
utils.check_all_schema_file_validity()

# Check if the data folder structure exists.
# If not, create it
utils.create_data_folder_structure()

# check if all data files conform to their schema
utils.check_all_data_files_against_schema()


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
        except FileNotFoundError as e:
            print("Could not find specified file")
            print(e)
            return {"error": "Could not locate a specific file. See console output for details"}
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
    return data


@app.route("/erstiwochenende")
@handle_errors
def erstiwochenende():
    with open(DATAFILES["gi_erstiwochenende"]["data"]) as file:
        data = json.load(file)
    return data


@app.route("/erstistundenplan")
@handle_errors
def stundenplan():
    with open(DATAFILES["gi_stundenplan"]["data"]) as file:
        data = json.load(file)
    return data


@app.route("/fachschaft_rollen")
@handle_errors
def rollen():
    with open(DATAFILES["gi_rollen"]["data"]) as file:
        data = json.load(file)
    return data


@app.route("/praesidienste")
@handle_errors
def praesidienste():
    with open(DATAFILES["gi_praesidienste"]["data"]) as file:
        data = json.load(file)
    return data


@app.route("/termine")
@handle_errors
def termine():
    with open(DATAFILES["gi_termine"]["data"]) as file:
        data = json.load(file)
    return data


@app.route("/jahrgaenge")
@handle_errors
def jahrgaenge():
    with open(DATAFILES["gi_jahrgaenge"]["data"]) as file:
        data = json.load(file)
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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
