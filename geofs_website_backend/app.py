from flask import Flask, make_response, request, Response
import json

from jsonschema.exceptions import ValidationError
from . import utils
from . import git_utils
from os.path import join
from functools import wraps

from .datafiles import DATAFILES, OTHER_FILES, DatafileKeys, OtherfilesKeys

from .errors import IntegrityError, EnvVariableError, GitError

from .webhook import github_webhook, webhook_disabled

from .envs import GIT_CONTENT_REPO

import sys

############################
#  Perform startup checks  #
############################

def shutdown_on_error():
    # DO NOT CHANGE EXIT CODE 4!!!!!!
    # Code 4 is required to take effect in gunicorn deployment
    # Gunicorn is used inside Docker build
    sys.exit(4)


try:
    utils.check_template_file_presence()  # Check if all data templates are there:
    utils.check_schema_file_presence()  # check if all schema files are there:
    utils.check_all_schema_file_validity()  # check if all schema files are valid jsonschema-2020-12 schemas
    if GIT_CONTENT_REPO is None:
        utils.create_data_folder_structure()  # Check if the data folder structure exists; If not, create it
    else:
        git_utils.clone_folder_structure()  # check if git repo is not cloned yet, and clone it
        git_utils.pull_updates()  # pull lates updates from repo
    utils.check_all_data_files_against_schema()  # check if all data files conform to their schema
except IntegrityError as e:
    print("Startup Checks for backend server failed.")
    print(e)
    shutdown_on_error()
except EnvVariableError as e:
    print("Startup Checks for backend server failed. Invalid Environment variable.")
    print(e)
    shutdown_on_error()
except GitError as e:
    print("Startup checks for backend server failed due to issues with git.")
    print(e)
    shutdown_on_error()
except Exception as e:
    print("Startup Checks for backend server failed. An unforseen error occured:")
    print(e)
    shutdown_on_error()


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
        except json.JSONDecodeError as err:
            print("File is not a valid JSON file")
            print(err)
            return {"error": "File is not a valid json file"}, 500
        except ValidationError as err:
            print("JSON file does not conform to its associated JSON-Schema")
            print(err)
            return {"error": "File does not validate against its schema"}, 500
        except FileNotFoundError as err:
            print("Could not find specified file")
            print(err)
            return {"error": "Could not locate a specific file. See console output for details"}, 500
        except Exception as err:
            print(err)
            return {"error": "An internal server error has occured."}, 500
    return wrapper_func


def get_json_data(datafiles_key: DatafileKeys) -> dict:
    """
    Check a JSON file against its JSON-Schema, then send it as as a response
    :param datafiles_key: Key for the entry in the DATAFILES dictionary
    :return:
    """
    with open(DATAFILES[datafiles_key]["data"]) as file:
        data = json.load(file)
    utils.validate_dict_againt_schema(DATAFILES[datafiles_key]["schema_validator"], data)
    return data


def make_photo_response(otherfiles_key: OtherfilesKeys) -> Response:
    with open(OTHER_FILES[otherfiles_key]["data"], "rb") as file:
        data = file.read()
    response = make_response(data)
    response.headers["Content-Type"] = "image/jpeg"
    response.headers["Content-Disposition"] = "inline; filename=fachschaft.jpg"
    return response


def make_news_response(path: str, page: str) -> dict:
    filenames = utils.get_html_filenames_in_directory(path)
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

    if page * items_per_page >= len(filenames):
        page = 0

    start_index = page * items_per_page
    end_index = start_index + items_per_page

    response = {
        "next": page + 1 if (page + 1) * items_per_page < len(filenames) else None,
        "prev": page - 1 if page != 0 else None
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


def make_jobs_response(path: str) -> list:
    filenames = utils.get_html_filenames_in_directory(path)

    data = []
    for filename in filenames:
        with open(join(path, filename)) as file:
            filecontent = file.read().replace("\n", " ")  # read file and replace newline with dash
        data.append({"id": filename, "content": filecontent})
    return data


#######################
#  Special endpoints  #
#######################

# webhook for geofs-website-content to fetch updates to website content from github
if GIT_CONTENT_REPO is not None:
    app.route("/webhook/update-website-content", methods=["POST"])(github_webhook)
else:
    app.route("/webhook/update-website-content", methods=["POST"])(webhook_disabled)


########################
#  Endpoints for both  #
########################


@app.route("/")
def hello():
    return {"version": "1.0"}


@app.route("/gremien")
@handle_errors
def gremien():
    return get_json_data("gremien")


########################
#  Endpoints for FS-GI  #
########################


@app.route('/erstiwoche')
@handle_errors
def erstiwoche():
    return get_json_data("gi_erstiwoche")


@app.route("/erstiwochenende")
@handle_errors
def erstiwochenende():
    return get_json_data("gi_erstiwochenende")


@app.route("/erstistundenplan")
@handle_errors
def stundenplan():
    return get_json_data("gi_stundenplan")


@app.route("/fachschaft_rollen")
@handle_errors
def rollen():
    return get_json_data("gi_rollen")


@app.route("/praesidienste")
@handle_errors
def praesidienste():
    return get_json_data("gi_praesidienste")


@app.route("/termine")
@handle_errors
def termine():
    return get_json_data("gi_termine")


@app.route("/jahrgaenge")
@handle_errors
def jahrgaenge():
    return get_json_data("gi_jahrgaenge")


@app.route("/joblistings")
@handle_errors
def jobs():

    path = "data/gi/jobs"
    return make_jobs_response(path)


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
    page = request.args.get("page")
    return make_news_response(path, page)


@app.route("/foto_gi")
@handle_errors
def foto_gi_fachschaft():
    return make_photo_response("foto_gi")


##############################
#  Endpoints for FS-Geoloek  #
##############################


@app.route("/geoloek_praesidienste")
@handle_errors
def geoloek_praesidienste():
    return get_json_data("geoloek_praesidienste")


@app.route("/geoloek_termine")
@handle_errors
def geoloek_termine():
    return get_json_data("geoloek_termine")


@app.route("/geoloek_erstiwoche_geo")
@handle_errors
def geoloek_erstiwoche_geo():
    return get_json_data("geoloek_erstiwoche_geo")


@app.route("/geoloek_erstiwoche_loek")
@handle_errors
def geoloek_erstiwoche_loek():
    return get_json_data("geoloek_erstiwoche_loek")


@app.route("/geoloek_erstiwoche_2fb")
@handle_errors
def geoloek_erstiwoche_2fb():
    return get_json_data("geoloek_erstiwoche_2fb")


@app.route("/geoloek_organisation")
@handle_errors
def geoloek_organisation():
    return get_json_data("geoloek_organisation")


@app.route("/foto_geoloek")
@handle_errors
def foto_geoloek():
    return make_photo_response("foto_geoloek")


@app.route("/geoloek_news")
@handle_errors
def geoloek_news():
    # This URL has support for a query param called page (/geoloek_news?page=2)
    # This param must be an integer >= 0
    # Reason: If the website grows and we have more and more news articles, it will eventually become slow
    # if all articles had to be opened and sent to the frontend
    # Therefore, only the first 5 latest articles are read by default (page=0),
    # the next 5 articles can be read on page 1, and so on...

    path = "data/geoloek/news"
    page = request.args.get("page")
    return make_news_response(path, page)


@app.route("/geoloek_joblistings")
@handle_errors
def geoloek_jobs():
    path = "data/geoloek/jobs"
    return make_jobs_response(path)
