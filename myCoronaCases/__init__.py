import logging
import os
import azure.functions as func
import pyodbc
import requests
import re


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

def get_latest_values_df():

    crsr, _ = get_cursor_and_connection()

    crsr.execute('select top 1 nor_cases, nor_dead, world_cases, world_dead from corona order by date_time desc')

    vals = crsr.fetchone()

    crsr.close()

    return vals

def norway_numbers_vg():
    """
        Get latest numbers from vg
    """
    
    totals = requests.get('https://redutv-api.vg.no/corona/v1/sheets/norway-table-overview/?region=county').json()['totals']

    cases = totals['confirmed']
    dead = totals['dead']

    return cases, dead

def world_numbers():
    """
        Get latest world numbers from worldometers
    """

    ww_cases, ww_deaths = re.match('.*<title>Coronavirus Update \(Live\): (\d*,\d*) Cases and (\d*,\d*)', str(requests.get('https://www.worldometers.info/coronavirus/').content)).groups()
    return int(ww_cases.replace(',','')) , int(ww_deaths.replace(',',''))


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    insert_values_db(1,2,3,4)

    nor_cases, nor_dead, world_cases, world_dead  = get_latest_values_df()

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
