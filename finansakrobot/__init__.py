import json
import logging
import os
import time

import azure.functions as func
from requests_futures.sessions import FuturesSession


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    ticker = req.form["text"]

    if "." not in ticker:
        ticker += ".OL"

    session = FuturesSession()
    # first request is started in background
    url = os.environ["SendMessageFunctionUrl"]
    future_one = session.get(f"{url}?ticker={ticker}")

    logging.info("returning")
    return func.HttpResponse(
        status_code=200,
    )
