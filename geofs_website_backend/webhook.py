from flask import request
import hashlib
import hmac
from .envs import GITHUB_WEBHOOK_SECRET
from .git_utils import pull_updates
from .errors import GitError, IntegrityError
from .utils import check_all_data_files_against_schema


def _verify_signature(payload_body: bytes, signature_header: str) -> tuple[bool, int, str]:
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        signature_header: header received from GitHub (x-hub-signature-256)
    """

    if not signature_header:
        return False, 403, "x-hub-signature-256 header is missing!"

    hash_object = hmac.new(GITHUB_WEBHOOK_SECRET.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        return False, 403, "Request signatures didn't match!"

    return True, 201, "success"


def github_webhook():

    payload = request.data
    signature_header = request.headers.get("x-hub-signature-256", None)

    # verify signature to make sure that it is actually our repo which sends the request
    valid, err_code, msg = _verify_signature(payload, signature_header)

    if not valid:
        return msg, err_code

    data = request.json

    # Make sure the webhook was triggered because a push happend on branch "main"
    if "ref" not in data or data["ref"] != "refs/heads/main":
        return "Nothing to do, no push on main", 201

    try:
        pull_updates()
    except GitError as e:
        return f"Failed to pull updates from github.", 500

    try:
        check_all_data_files_against_schema()
    except IntegrityError:
        err = ("Changes pulled, but one or more file are invalid.\n"
               "Either, one file is either no valid JSON, or does not conform to its schema.\n"
               "The changed content is not visible on website.")
        return err, 400

    return "Contents pulled, validated and updated on website.", 200


def webhook_disabled():
    return "Webhook integration disabled", 404
