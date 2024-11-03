from os import listdir
from os.path import isfile, join


def get_html_filenames_in_directory(path: str) -> list[str]:
    # list all files in given directory
    files = [f for f in listdir(path) if isfile(join(path, f)) and f.split(".")[-1] == "html"]
    files.sort(reverse=True)
    return files
