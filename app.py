from flask import Flask
import json
from utils import get_html_filenames_in_directory
from os.path import join

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return {"version": "1.0"}


@app.route('/erstiwoche')
def erstiwoche():
    with open("data/gi/erstsemester/erstiwoche.json") as file:
        data = json.load(file)
    return data


@app.route("/erstiwochenende")
def erstiwochenende():
    with open("data/gi/erstsemester/erstiwochenende.json") as file:
        data = json.load(file)
    return data


@app.route("/erstistundenplan")
def stundenplan():
    with open("data/gi/erstsemester/stundenplan.json") as file:
        data = json.load(file)
    return data


@app.route("/fachschaft_rollen")
def rollen():
    with open("data/gi/fachschaft/rollen.json") as file:
        data = json.load(file)
    return data


@app.route("/praesidienste")
def praesidienste():
    with open("data/gi/start/praesidienste.json") as file:
        data = json.load(file)
    return data


@app.route("/termine")
def termine():
    with open("data/gi/start/termine.json") as file:
        data = json.load(file)
    return data


@app.route("/jahrgaenge")
def jahrgaenge():
    with open("data/gi/studium/jahrgaenge.json") as file:
        data = json.load(file)
    return data


@app.route("/joblistings")
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
