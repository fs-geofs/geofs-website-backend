import os


# Secret for generating sha-256 signature in github webhook
# used to verify that github request was actually made by our repo(s)
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", None)

# Git repository where the content files (datafiles) are hosted.
# Not required, but makes backups and editing easier.
# Required if github webhook should be used to update website content
GIT_CONTENT_REPO = os.environ.get("GIT_CONTENT_REPO", None)
