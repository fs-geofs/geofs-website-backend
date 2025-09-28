import os
import subprocess

from .envs import (
    CONTENT_PATH,
    GIT_CONTENT_BASE_PATH,
    GIT_CONTENT_URL,
    LOCAL_CONTENT_PATH,
)
from .errors import GitError


def clone_folder_structure():
    # nothing to clone if it exists already
    if os.path.exists(CONTENT_PATH):
        return

    if not os.path.exists(GIT_CONTENT_BASE_PATH):
        os.mkdir(GIT_CONTENT_BASE_PATH)

    proc = subprocess.run(
        ["git", "clone", GIT_CONTENT_URL],
        cwd=GIT_CONTENT_BASE_PATH,
        capture_output=True,
    )

    if proc.returncode != 0:
        raise GitError(proc.stderr.decode())


def pull_updates():
    proc = subprocess.run(["git", "pull"], cwd=CONTENT_PATH, capture_output=True)

    if proc.returncode != 0:
        raise GitError(proc.stderr.decode())


def make_loacal_dummy_data_folder():
    # make a local dummy folder and place a file in it explaining where the content is
    # to not confuse people who are used to the local "data" content path
    if not os.path.exists(LOCAL_CONTENT_PATH):
        os.mkdir(LOCAL_CONTENT_PATH)

    cnt = (
        f"This backend is running in github-mode.\n"
        f"Files are hosted on github.\n"
        f"They should be edited on github, not locally.\n"
        f"Therefore, this directory does not contain the content files.\n"
        f"To edit website content, edit the files on {GIT_CONTENT_URL}"
    )

    cnt_file_path = f"{LOCAL_CONTENT_PATH}/where_are_the_files.txt"
    with open(cnt_file_path, "w") as file:
        file.write(cnt)
