import sys
import time
from time import sleep

import psycopg2
import requests as r
import uuid as uuid
from bs4 import BeautifulSoup as bs


# noinspection SqlNoDataSourceInspection,PyBroadException
def scrapeValueAndSaveToDb(sleepBefore, databaseConnection):
    """
    call scraping request to scrape occupancy from the web and save to database
    :param sleepBefore: time to wait before next request
    :param databaseConnection: object with database connection
    :return: return scraped data
    """
    try:
        sleep(sleepBefore)
        # scrape occupancy
        element_value = getValueFromWebsite(0)

        # prepare data and time
        date_and_time = time.strftime("%Y-%m-%d %H:%M:%S.000000", time.localtime())

        # prepare unique id of row
        u = uuid.uuid4()

        # insert to database
        cursor = databaseConnection.cursor()
        postgres_insert_query = "INSERT INTO public.sauna_cb_occupancy (row_id, timestamp, occupancy) VALUES (%s,%s,%s)"
        record_to_insert = (u, date_and_time, element_value)
        cursor.execute(postgres_insert_query, record_to_insert)
        databaseConnection.commit()
        sys.stderr.write('scrapeValueAndSaveToDb value:' + str(element_value))
        return element_value
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)
    except BaseException as e:
        sys.stderr.write(str(e) + ' scraping failed\n')


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
