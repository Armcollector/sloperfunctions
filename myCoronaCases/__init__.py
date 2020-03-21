import logging
import os
import azure.functions as func
import pyodbc


def get_cursor_and_connection():
    cnxn = pyodbc.connect(os.environ.get('DATABASECONNECTIONSTRING'))
    # Create a cursor from the connection
    cursor = cnxn.cursor()

    return cursor, cnxn

def insert_values_db(nor_cases, nor_dead, world_cases, world_dead):

    crsr, _ = get_cursor_and_connection()

    crsr.execute('insert into corona values (GETDATE(),?,?,?,?)', nor_cases, nor_dead, world_cases, world_dead)
    crsr.commit()
    crsr.close()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    insert_values_db(1,2,3,4)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
