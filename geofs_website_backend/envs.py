from .errors import EnvVariableError
import os
import git_utils


# Secret for generating sha-256 signature in github webhook
# used to verify that github request was actually made by our repo(s)
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", None)

# Git repository where the content files (datafiles) are hosted.
# Not required, but makes backups and editing easier.
# Required if github webhook should be used to update website content
# All required datafiles must exist in repo, otherwise backend will not start
# Use in the following way: orga/repo, i.e. fs-geofs/geofs-website-content
GIT_CONTENT_REPO = os.environ.get("GIT_CONTENT_REPO", None)
if GIT_CONTENT_REPO is not None:
    valid_repo = git_utils.check_repo_name(GIT_CONTENT_REPO)
    if not valid_repo:
        raise EnvVariableError(
            "GIT_CONTENT_REPO is not a valid env. "
            "Must be format orga/repo, i.e. fs-geofs/geofs-website-content"
        )

    GIT_CONTENT_DIR = GIT_CONTENT_REPO.split("/")[-1]
    GIT_CONTENT_PATH = "../" + GIT_CONTENT_DIR
    GIT_CONTENT_URL = f"https://github.com/{GIT_CONTENT_REPO}.git"
else:
    GIT_CONTENT_DIR = None
    GIT_CONTENT_PATH = None
    GIT_CONTENT_URL = None
