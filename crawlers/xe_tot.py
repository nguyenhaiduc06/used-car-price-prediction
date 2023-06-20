from crawler import Crawler
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import *

DATA_PATH = "data/xe_tot"
PATH_TO_LINKS = DATA_PATH + "/links.csv"
PATH_TO_CARS = DATA_PATH + "/raw_cars.csv"
BASE_URL = "https://xetot.com"


class XeTotCrawler(Crawler):
    def crawl(self):
        """crawl cars data and save to csv file"""
        links = self.get_links()[:1]
        cars = []

        for link in links:
            res = requests.get(link).text
            soup = BeautifulSoup(res, "html.parser")
            tableSelector = ".product-info > .list-unstyled"
            liTags = soup.select(tableSelector)[0].find_all('li')
            car = {}
            for liTag in liTags:
                feature = liTag.find_all('div', class_="info-label")[0].text.strip()
                value = liTag.find_all('div', class_="info-show")[0].text.strip()
                car[feature] = value
            cars.append(car)

        cars_df = pd.DataFrame.from_records(cars)
        cars_df.to_csv(PATH_TO_CARS)

    def get_links(self):
        try:
            links_df = pd.read_csv(PATH_TO_LINKS)
            links = links_df[0].values.tolist()
            if links:
                return links
        except:
            pass

        links = []

        page_urls = [
            "https://xetot.com/toan-quoc/mua-ban-oto?page=" + str(i)
            for i in range(1, 2) # TODO: change range to 1, 100 depend on page data
        ]

        for page_url in page_urls:
            res = requests.get(page_url).text
            soup = BeautifulSoup(res, "html.parser")
            ulSelector = ".list-archive-item > ul"
            ul = soup.select(ulSelector)[0]
            aTags = ul.find_all("a", class_="item-title")

            links += [BASE_URL + a['href'] for a in aTags]

        links_df = pd.DataFrame(links)

        # write data to file so we don't have to get links again
        links_df.to_csv(PATH_TO_LINKS)

        return links
