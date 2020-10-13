import logging

import azure.functions as func
import yfinance as yf
from slack import WebClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    tick_dict = yf.Ticker(req.params["ticker"]).info

    client = WebClient(token="xoxb-11406248935-1437312894113-m0FnzReJEtCbmufHAGhhX1XU")
    client.chat_postMessage(
        channel=os.environ["SLACKCHANNEL"],
        text=f"{tick_dict['shortName']},  bid:{tick_dict['bid']}, ask: {tick_dict['ask']}",
    )
    return func.HttpResponse(status_code=200)
