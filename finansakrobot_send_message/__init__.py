import logging
import os

import azure.functions as func
import yfinance as yf
from slack import WebClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    tick_dict = yf.Ticker(req.params["ticker"]).info

    channel = req.params["channel"]

    client = WebClient(token=os.environ["token"])
    client.chat_postMessage(
        channel=channel,
        text=f"{tick_dict['shortName']},  bid:{tick_dict['bid']}, ask: {tick_dict['ask']}",
    )
    return func.HttpResponse(status_code=200)
