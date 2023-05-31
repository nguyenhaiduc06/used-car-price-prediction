from crawler import Crawler
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import *

DATA_PATH = "data/san_xe_hot"
PATH_TO_CARS = DATA_PATH + "/cars.csv"
PATH_TO_LINKS = DATA_PATH + "/links.csv"


class SanXeHotCrawler(Crawler):
    def crawl(self):
        """crawl cars data and save to csv file"""
        cars_df = create_empty_cars_df()
        links_df = self.getLinks()

        for index, row in links_df.iterrows():
            link = row["link"]
            car_df = self.get_car_df(link)
            cars_df = pd.concat([cars_df, car_df], ignore_index=True)

        cars_df.to_csv(PATH_TO_CARS)

    def getLinks(self):
        """
        Returns:
            DataFrame: a DataFrame with at least a "link" column
        """
        try:
            links_df = pd.read_csv(PATH_TO_LINKS)
            return links_df
        except:
            pass

        # feel free to refactor the code below
        links = {"link": [], "car_type": []}
        url_list = [
            "https://www.sanxehot.vn/mua-ban-xe/loai-xe-cu-pg" + str(i)
            for i in range(1, 2)
        ]

        for url in url_list:
            res = self.requests_session.get(url).text
            soup = BeautifulSoup(res, "html.parser")
            table_selector = "body > main > div.section > div > div > div.col.m7.s12 > div > div > section.car > ul"
            lis = soup.select(table_selector)[0].find_all("li")
            li_len = len(lis)
            for i in range(1, li_len + 1):
                link_selector = f"body > main > div.section > div > div > div.col.m7.s12 > div > div > section.car > ul > li:nth-child({i}) > div:nth-child(1) > div.col.m8 > h2 > a"
                link = soup.select(link_selector)[0]["href"]

                type_selector = f"body > main > div.section > div > div > div.col.m7.s12 > div > div > section.car > ul > li:nth-child({i}) > div:nth-child(2) > div.col.m8.s12 > table > tbody > tr:nth-child(2) > td"
                type_ = soup.select(type_selector)[0].text

                links["link"].append(link)
                links["car_type"].append(type_)

        links_df = pd.DataFrame(links)
        links_df.to_csv(PATH_TO_LINKS)

        return links_df

    def get_car_df(self, link):
        """
        Args:
            link (str): link to the detail page of a car

        Returns:
            DataFrame: a DataFrame with 1 row - a record of a car
        """

        # TODO: implement logic for extracting car features from a link
        # use requests.get to get html content
        # html = requests.get(link).text

        # use BeautifulSoup to parse html and extract data using css selector
        # soup = BeautifulSoup(html, "html.parser")

        brand = "Brand name"

        return create_car_df_from_features(brand=brand)
