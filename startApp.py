import sys
import actions

if __name__ == '__main__':
    try:
        dbConn = actions.getDBconn()
        while True:
            actual_occupancy = 1
            if actual_occupancy == 0:
                if actions.isTimeframeAroundWholeHour():
                    wait = 20
                else:
                    wait = 300
                actual_occupancy = actions.getValueFromWebsite(wait)
            else:
                actual_occupancy = actions.scrape(60, dbConn)
                sys.stderr.write('scraped content\n')
    except BaseException as e:
        sys.stderr.write('main activity failed\n')
