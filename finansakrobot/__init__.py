import logging

import azure.functions as func


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
            f"{tick_dict["shortName"]} : {tick_dict["regularMarketPrice"]}",
            status_code=200
    )


#'token=KwFR72oXnE603fNS5vkB2Iv7&team_id=T0BBY7ATH&team_domain=sonatconsulting&channel_id=D4JEYNQGM&channel_name=directmessage&user_id=U4K3A5BHV&user_name=christiansloper&command=%2Ffinansakrobot&text=test&api_app_id=A01CC799WR3&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT0BBY7ATH%2F1416704205270%2FOlIxr9OxTCzOZ5d70WfKicGn&trigger_id=1447277879568.11406248935.1fed91f59bcc2d5c0255dde3cc6dcf53''
