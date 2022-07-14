import os
import sys
import psycopg2
from psycopg2 import Error


def getDBconn():
    """
    Establish connection to PostgreSQL DB
    :return: conn object
    """
    try:
        # Load env variables
        db_pass = os.getenv("db_pass")
        user = os.getenv("user")
        host = os.getenv("host")
        port = os.getenv("port")
        database = os.getenv("database")

        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                      password=db_pass,
                                      host=host,
                                      port=port,
                                      database=database)

        return connection
    except (Exception, Error) as error:
        sys.stderr.write("error when establishing DB connection" + str(error))
