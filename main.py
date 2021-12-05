import scraper
from time import time, sleep

if __name__ == '__main__':
    while True:
        sleep(60 - time() % 60)
        scraper.scrape()
