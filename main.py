import scraper
from time import sleep

if __name__ == '__main__':
    while True:
        # run every minute
        sleep(60)
        scraper.scrape()
