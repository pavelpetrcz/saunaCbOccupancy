import scraper
from time import sleep

if __name__ == '__main__':
    while True:
        # run ever two minutes
        sleep(120)
        scraper.scrape()
