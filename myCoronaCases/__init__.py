import logging
import os
import azure.functions as func
import pyodbc
import requests
import re
import datetime


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

def get_latest_values_db():

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

    return int(cases), int(dead)

def world_numbers():
    """
        Get latest world numbers from worldometers
    """

    ww_cases, ww_dead = re.match('.*<title>Coronavirus Update \(Live\): (\d*,\d*,\d*) Cases and (\d*,\d*)', str(requests.get('https://www.worldometers.info/coronavirus/').content)).groups()

    return int(ww_cases.replace(',','')) , int(ww_dead.replace(',',''))

def post_text(nor_cases, nor_dead, world_cases, world_dead):
    """
        Post text to telegram channel
    """
    token = os.environ.get('TELEGRAMTOKEN')
    method = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(method, data = {"chat_id": "-1001181973339",
                  "text": f'Norway: { nor_cases:, } cases and {nor_dead:,} dead.  World wide: {world_cases:,} cases and {world_dead:,} dead.'
               })

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()


    logging.info('Python timer trigger function ran at %s', utc_timestamp)


    nor_cases, nor_dead, _, _  = get_latest_values_db()

    new_nor_cases, new_nor_dead = norway_numbers_vg()

    if new_nor_cases > nor_cases or new_nor_dead > nor_dead:
        new_world_cases, new_world_dead = world_numbers()

        insert_values_db(new_nor_cases, new_nor_dead, new_world_cases, new_world_dead)
        post_text(new_nor_cases, new_nor_dead, new_world_cases, new_world_dead)
