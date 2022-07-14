import sys

import databaseService
import helpers
import scraperService

if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        dbConn = databaseService.getDBconn()

        while True:
            # noinspection PyRedeclaration
            actual_occupancy = 1
            if actual_occupancy == 0:
                if helpers.isTimeframeAroundWholeHour():
                    wait = 20
                else:
                    wait = 300
                actual_occupancy = scraperService.getValueFromWebsite(wait)
            else:
                actual_occupancy = scraperService.scrapeValueAndSaveToDb(60, dbConn)
                sys.stderr.write('scraped content\n')
    except BaseException as e:
        sys.stderr.write('main activity failed\n')
