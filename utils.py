import os.path
from os import listdir
from os.path import isfile, join
import shutil


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
    for filepath in REQUIRED_DATA_FILE_PATHES:
        if not os.path.exists("data_templates/" + filepath):
            raise FileNotFoundError("Could not locate template: data_templates/" + filepath)


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

    required_files_path = [
        "data/gi/studium/jahrgaenge.json",
        "data/gi/start/praesidienste.json",
        "data/gi/start/termine.json",
        "data/gi/fachschaft/rollen.json",
        "data/gi/erstsemester/erstiwoche.json",
        "data/gi/erstsemester/erstiwochenende.json",
        "data/gi/erstsemester/stundenplan.json",
    ]

    for path in required_files_path:
        if not os.path.exists(path):
            shutil.copy("data_templates/" + path, path)

if __name__=="__main__":
    create_data_folder_structure()