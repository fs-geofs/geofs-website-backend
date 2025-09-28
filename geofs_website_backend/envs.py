import os
import re

from .errors import EnvVariableError


def _check_github_repo_name(repo_name: str):
    """
    Check whether a string is a valid github repo, i.e. fs-geofs/geofs-website-content
    :param repo_name: The string to be checked
    :return:
    """

    pattern = re.compile(
        r"^(?![-_.])(?!.*[-_.]$)([A-Za-z0-9._-]{1,39})\/(?![-_.])(?!.*[-_.]$)([A-Za-z0-9._-]{1,100})$"
    )
    valid = bool(pattern.match(repo_name))
    return valid


LOCAL_CONTENT_PATH = "data"

# Secret for generating sha-256 signature in github webhook
# used to verify that github request was actually made by our repo(s)
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", None)

# Git repository where the content files (datafiles) are hosted.
# Not required, but makes backups and editing easier.
# Required if github webhook should be used to update website content
# All required datafiles must exist in repo, otherwise backend will not start
# Use in the following way: orga/repo, i.e. fs-geofs/geofs-website-content
GITHUB_CONTENT_REPO = os.environ.get("GITHUB_CONTENT_REPO", None)

# Check that both ENVs are set
if (GITHUB_WEBHOOK_SECRET is None) != (GITHUB_CONTENT_REPO is None):
    raise EnvVariableError(
        "Invalid state of ENVs:\n"
        "Only one of GITHUB_WEBHOOK_SECRET or GITHUB_CONTENT_REPO is set.\n"
        "Set both to use the backend in File mode, or set both to use the backend "
        "in Github Mode. Setting"
    )


if GITHUB_CONTENT_REPO is not None:
    valid_repo = _check_github_repo_name(GITHUB_CONTENT_REPO)
    if not valid_repo:
        raise EnvVariableError(
            "GIT_CONTENT_REPO is invalid. "
            "Must be format orga/repo, i.e. fs-geofs/geofs-website-content"
        )

    GIT_CONTENT_DIR = GITHUB_CONTENT_REPO.split("/")[-1]  # name of the repo w/o author
    GIT_CONTENT_BASE_PATH = "../git-content"  # path in which the repo will be cloned
    GIT_CONTENT_URL = (
        f"https://github.com/{GITHUB_CONTENT_REPO}.git"  # repo URL to clone
    )
else:
    GIT_CONTENT_DIR = None
    GIT_CONTENT_BASE_PATH = None
    GIT_CONTENT_URL = None

CONTENT_PATH = (
    f"{GIT_CONTENT_BASE_PATH}/{GIT_CONTENT_DIR}" if GITHUB_CONTENT_REPO else "data"
)
