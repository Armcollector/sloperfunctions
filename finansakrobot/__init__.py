import json
import logging

import azure.functions as func
import yfinance as yf


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    ticker = req.form["text"]

    if "." not in ticker:
        ticker += ".OL"
    tick_dict = yf.Ticker(ticker).info

    return func.HttpResponse(
        json.dumps(
            {
                "response_type": "in_channel",
                "text": f"{tick_dict['shortName']} : {tick_dict['regularMarketPrice']}",
            }
        ),
        status_code=200,
    )
