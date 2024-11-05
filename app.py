from flask import Flask, url_for
import json
from utils import get_html_filenames_in_directory, create_data_folder_structure
from os.path import join
from functools import wraps


# Check if the data folder structure exists.
# If not, create it
create_data_folder_structure()
# todo: check if files conform to schema


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
    with open("data/gi/erstsemester/erstiwoche.json") as file:
        data = json.load(file)
    return data


@app.route("/erstiwochenende")
@handle_errors
def erstiwochenende():
    with open("data/gi/erstsemester/erstiwochenende.json") as file:
        data = json.load(file)
    return data


@app.route("/erstistundenplan")
@handle_errors
def stundenplan():
    with open("data/gi/erstsemester/stundenplan.json") as file:
        data = json.load(file)
    return data


@app.route("/fachschaft_rollen")
@handle_errors
def rollen():
    with open("data/gi/fachschaft/rollen.json") as file:
        data = json.load(file)
    return data


@app.route("/praesidienste")
@handle_errors
def praesidienste():
    with open("data/gi/start/praesidienste.json") as file:
        data = json.load(file)
    return data


@app.route("/termine")
@handle_errors
def termine():
    with open("data/gi/start/termine.json") as file:
        data = json.load(file)
    return data


@app.route("/jahrgaenge")
@handle_errors
def jahrgaenge():
    with open("data/gi/studium/jahrgaenge.json") as file:
        data = json.load(file)
    return data


@app.route("/joblistings")
@handle_errors
def jobs():

    path = "data/gi/jobs"
    filenames = get_html_filenames_in_directory(path)

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
    filenames = get_html_filenames_in_directory(path)

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
