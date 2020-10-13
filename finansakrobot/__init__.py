import logging

import azure.functions as func
import yfinance as yf


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ticker = req.params.get('text')
    if not ticker:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            ticker = req_body.get('text')


    if "." not in ticker:
        ticker += ".OL"
    tick_dict = yf.Ticker(ticker)


    return func.HttpResponse(
            f"{tick_dict['shortName']} : {tick_dict['regularMarketPrice']}",
            status_code=200
    )

