import subprocess
import os

from .envs import GIT_CONTENT_BASE_PATH, GIT_CONTENT_URL, CONTENT_PATH
from .errors import GitError


def clone_folder_structure():

    # nothing to clone if it exists already
    if os.path.exists(CONTENT_PATH):
        return

    proc = subprocess.run(
        ["git", "clone", GIT_CONTENT_URL],
        cwd=GIT_CONTENT_BASE_PATH,
        capture_output=True
    )

    if proc.returncode != 0:
        raise GitError(proc.stderr.decode())


def pull_updates():
    proc = subprocess.run(
        ["git", "pull"],
        cwd=CONTENT_PATH,
        capture_output=True
    )

    if proc.returncode != 0:
        raise GitError(proc.stderr.decode())
