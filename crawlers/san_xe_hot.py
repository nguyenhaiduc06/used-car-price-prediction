from Crawler import Crawler
import requests
from bs4 import BeautifulSoup
import pandas as pd

PATH = "data/san_xe_hot"


class SanXeHotCrawler(Crawler):
    def __init__(self) -> None:
        self.requests_session = requests.session()
        self.cars_df = pd.DataFrame(
            columns=[
                "name",
                "brand",
                "model",
                "year",
                "type",
                "km_driven",
                "seats",
                "internal_color",
                "external_color",
                "fuel",
                "transmission",
                "wheel_drive",
                "price",
            ]
        )

    def getLinks(self):
        # get links to details page for each car
        # TODO: get links from file if file exists, otherwise, get links and write data to file
        return [0]
        pass

    def crawl(self):
        links = self.getLinks()

        for link in links:
            # html = self.requests_session.get(link).text
            # soup = BeautifulSoup(html, "html.parser")
            # get name, brand, model, year, type, km_driven, seats, internal_color, external_color, fuel, transmission, wheel_drive, price
            car = pd.Series(
                {
                    "name": "1",
                    "brand": "2",
                }
            )
            self.cars_df = self.cars_df.add(car)

        self.save()

    def save(self):
        self.cars_df.to_csv(PATH + "/san_xe_hot.csv")
