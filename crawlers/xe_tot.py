from crawler import Crawler
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import *

DATA_PATH = "data/xe_tot"
PATH_TO_LINKS = DATA_PATH + "/links.csv"
PATH_TO_CARS = DATA_PATH + "cars.csv"


class XeTotCrawler(Crawler):
    def crawl(self):
        """crawl cars data and save to csv file"""
        cars_df = create_empty_cars_df()
        links_df = self.get_links()

        for index, row in links_df.iterrows():
            link = row["link"]
            car_df = self.get_car_df(link)
            cars_df = pd.concat([cars_df, car_df], ignore_index=True)

        cars_df.to_csv(PATH_TO_CARS)

    def get_links(self):
        """
        Returns:
            DataFrame: a DataFrame with at least a "link" column
        """
        try:
            links_df = pd.read_csv(PATH_TO_LINKS)
            return links_df
        except:
            pass

        # TODO: implement logic for getting links to car details
        links = {
            "links": [],
        }
        links_df = pd.DataFrame(links)

        # write data to file so we don't have to get links again
        links_df.to_csv(PATH_TO_LINKS)

        return links_df

    def get_car_df(self, link):
        # TODO: implement logic for extracting car features from a link
        brand = "Example Brand"
        return create_car_df_from_features(brand=brand)
