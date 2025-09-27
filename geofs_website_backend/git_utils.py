import re
import subprocess


def check_repo_name(repo_name: str):
    """
    Check whether a string is a valid github repo, i.e. fs-geofs/geofs-website-content
    :param repo_name: The string to be checked
    :return:
    """

    pattern = re.compile(r"^(?![-_.])(?!.*[-_.]$)([A-Za-z0-9._-]{1,39})\/(?![-_.])(?!.*[-_.]$)([A-Za-z0-9._-]{1,100})$")
    valid = bool(pattern.match(repo_name))
    return valid

def clone_folder_structure():
    pass

def pull_updates():
    pass
