"""
Very small script to validate all datafiles from a corresponding datafile repository.
Mainly used in github action when updating datafiles.
"""

import os

from geofs_website_backend import git_utils, utils
from geofs_website_backend.errors import EnvVariableError

BRANCH_NAME = os.environ.get("BRANCH_NAME", "main")
if BRANCH_NAME is None:
    raise EnvVariableError("Env BRANCH_NAME is not set.")


def main():
    git_utils.clone_folder_structure()  # check if git repo is not cloned yet, and clone it
    git_utils.switch_branch(BRANCH_NAME)  # pull lates updates from repo
    utils.check_all_data_files_against_schema()  # check if all data files conform to their schema


if __name__ == "__main__":
    main()
