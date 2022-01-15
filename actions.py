import logging
import time
from time import sleep

import pandas as pd
import requests as r
from bs4 import BeautifulSoup as bs
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2
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

        # prepare list of values
        datalist = [date_and_time, element_value]
        datalist = [datalist]

        databaseConnection.c


    except BaseException as e:
        logging.warning("scraping failed")
        logging.exception(e)


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
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="postgres")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        return cursor
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

