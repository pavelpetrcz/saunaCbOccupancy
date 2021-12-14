import actions
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/saunaCbOccupancy.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')
    try:
        while True:
            actual_occupancy = 1
            if actual_occupancy == 0:
                if actions.isCloseToWholeHour():
                    wait = 20
                else:
                    wait = 300
                actual_occupancy = actions.getValueFromPage(wait)
            else:
                actual_occupancy = actions.scrape(60)
    except BaseException as e:
        logging.warning("main activity failed")
        logging.exception(e)
