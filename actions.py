import os
import sys
import time
from time import sleep

import psycopg2
import requests as r
from bs4 import BeautifulSoup as bs
from psycopg2 import Error


def scrape(sleepBefore, databaseConnection):
    """
    load HTML, extract/generate data and save to G-Spreadsheet
    :return:
    """
    try:
        sleep(sleepBefore)
        element_value = getValueFromWebsite(0)

        # prepare data and time
        date_and_time = time.strftime("%Y-%m-%d %H:%M:%S.000000", time.localtime())

        # insert to database
        cursor = databaseConnection.cursor()
        postgres_insert_query = """ INSERT INTO public.sauna_cb_occupancy (row_id, timestamp, occupancy) VALUES (%s,%s,%s)"""
        record_to_insert = (5, date_and_time, element_value)
        cursor.execute(postgres_insert_query, record_to_insert)
        databaseConnection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)
    except BaseException as e:
        sys.stderr.write('scraping failed\n')


def isTimeframeAroundWholeHour():
    """
    return True if time is between XX:00 and XX:05
    :return: boolean
    """
    minutes = time.localtime().tm_min
    return True if minutes in range(55, 2) else False


def getValueFromWebsite(sleepBefore):
    """
    load HTML & extract data
    :param sleepBefore: secs to sleep before request
    :return: sauna occupancy
    """
    sleep(sleepBefore)
    # load html of page and parse
    page = r.get('https://www.szcb.cz')
    soup = bs(page.content, "html.parser")

    # find all elements p and select 25th element of result list
    all_p = soup.find_all("p")
    element = all_p[25].find("span").contents
    element_value = int(element[0])
    return element_value


def getDBconn():
    try:
        # Connect to an existing database
        db_pass = os.getenv("db_pass")
        connection = psycopg2.connect(user="pavelpetrcz",
                                      password=db_pass,
                                      host="172.17.0.2",
                                      port="5432",
                                      database="sauna_occupancy")

        return connection
    except (Exception, Error) as error:
        sys.stderr.write("error when establishing DB connection")
