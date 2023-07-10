from crawler import Crawler
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

DATA_PATH = "data/xe_tot"
PATH_TO_STATES = DATA_PATH + "/states.json"
PATH_TO_LINKS = DATA_PATH + "/links.csv"
PATH_TO_RAW_CARS = DATA_PATH + "/raw_cars.csv"
PATH_TO_STD_CARS = DATA_PATH + "/std_cars.csv"
BASE_URL = "https://xetot.com"


class XeTotCrawler:
    def crawl(self, part):
        """crawl cars data and save to csv file"""
        links_df = pd.read_csv(PATH_TO_LINKS, index_col=0)
        links = links_df["0"].values.tolist()[1000:]  # TODO: edit here
        cars = []

        for index, link in enumerate(links):
            print("Crawling data for car number", index)
            car = XeTotExtractor(link).extract()
            cars.append(car)

        cars_df = pd.DataFrame.from_records(cars)
        cars_df.to_csv(DATA_PATH + "/cars_" + str(5) + ".csv")  # TODO: and str(3)
        print("[xe_tot] Crawled data written to " + PATH_TO_RAW_CARS)

    def get_links(self):
        links = []

        print("Crawling links for cars")

        page_urls = [
            "https://xetot.com/toan-quoc/mua-ban-oto?page=" + str(i)
            for i in range(1, 50)
        ]

        for index, page_url in enumerate(page_urls):
            print("Crawling links number", index)
            res = requests.get(page_url).text
            soup = BeautifulSoup(res, "html.parser")
            ulSelector = ".list-archive-item > ul"
            ul = soup.select(ulSelector)[0]
            aTags = ul.find_all("a", class_="item-title")

            links += [BASE_URL + a["href"] for a in aTags]

        links_df = pd.DataFrame(links)

        # write data to file so we don't have to get links again
        links_df.to_csv(PATH_TO_LINKS)

        return links


class XeTotExtractor:
    def __init__(self, url):
        self.url = url
        res = requests.get(self.url).text
        self.soup = BeautifulSoup(res, "html.parser")

    def get_name(self):
        try:
            name_selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > div.product-gab > h2"
            name_container = self.soup.select(name_selector)[0].text
            name = [text for text in name_container.split("\n") if text][0]
        except BaseException:
            name = "None"

        return name

    def get_model(self):
        try:
            model_selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(3) > div.info-show"
            model_container = self.soup.select(model_selector)[0].text
            model = [text for text in model_container.split("\n") if text][0]
        except BaseException:
            model = "None"
        return model

    def get_transmission(self):
        try:
            selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(5) > div.info-show"
            container = self.soup.select(selector)[0].text
            tranmission = [text for text in container.split("\n") if text][0]
            replacer = {"Tự động": "automatic", "Số sàn": "manual", "Khác": "None"}
            tranmission = replace_all(replacer, tranmission)
        except BaseException:
            tranmission = "None"
        return tranmission

    def get_brand(self):
        try:
            brand_selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(1) > div.info-show"
            brand_container = self.soup.select(brand_selector)[0].text
            brand = [text for text in brand_container.split("\n") if text][0]
        except BaseException:
            brand = "None"
        return brand

    def get_price(self):
        try:
            price_selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > div.product-gab > div > span"
            price_container = self.soup.select(price_selector)[0].text
            price = int(price_container.split(" ")[0].replace(".", ""))
        except BaseException:
            price = "None"
        return price

    def get_year(self):
        try:
            year_selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(4) > div.info-show"
            year_container = self.soup.select(year_selector)[0].text
            year = int([text for text in year_container.split("\n") if text][0])
        except BaseException:
            year = "None"
        return year

    def get_km_driven(self):
        try:
            km_driven_container = "#so-km-da-di"
            km_driven = int(self.soup.select(km_driven_container)[0]["value"])
        except BaseException:
            km_driven = "None"
        return km_driven

    def get_fuels(self):
        try:
            fuels_selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(6) > div.info-show"
            fuels_container = self.soup.select(fuels_selector)[0].text
            fuels = [text for text in fuels_container.split("\n") if text][0]
            replacer = {
                "Xăng": "gasoline",
                "Dầu": "diesel",
                "Diesel": "diesel",
                "Hybrid": "hybrid",
                "Điện": "electric",
                "Khác": "NONE",
            }
            fuels = replace_all(replacer, fuels)
        except BaseException:
            fuels = "None"
        return fuels

    def get_origin(self):
        try:
            origin_selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(6) > div.info-show"
            origin_container = self.soup.select(origin_selector)[0].text
            origin = [text for text in origin_container.split("\n") if text][0]
            if origin.lower == "việt nam":
                origin = "domestic"
            else:
                origin = "imported"
        except BaseException:
            origin = "None"

        return origin

    def get_type(self):
        try:
            selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(8) > div.info-show"
            container = self.soup.select(selector)[0].text
            type = [text for text in container.split("\n") if text][0]
            replacer = {
                "Sedan": "sedan",
                "SUV / Cross over": "suv",
                "Hatchback": "hatchback",
                "Pick-up (bán tải)": "pickup",
                "Minivan (MPV)": "van",
                "Van": "van",
                "Coupe (2 cửa)": "coupe",
                "Mui trần": "NONE",
                "Kiểu dáng khác": "NONE",
            }
            type = replace_all(replacer, type)
        except BaseException:
            type = "None"
        return type

    def get_seats(self):
        try:
            selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(9) > div.info-show"
            container = self.soup.select(selector)[0].text
            seats = int([text for text in container.split("\n") if text][0])
        except BaseException:
            seats = "None"
        return seats

    def get_external_color(self):
        try:
            selector = "#main-content > div.product-detail.w-100.float-left > div > div.product-left > div.product-info.w-100.float-left > ul > li:nth-child(10) > div.info-show"
            container = self.soup.select(selector)[0].text
            color = [text for text in container.split("\n") if text][0]
        except BaseException:
            color = "None"
        return color

    def extract(self):
        car = {
            "name": self.get_name(),
            "brand": self.get_brand(),
            "model": self.get_model(),
            "type": self.get_type(),
            "source_url": self.url,
            "origin": self.get_origin(),
            "km_driven": self.get_km_driven(),
            "external_color": self.get_external_color(),
            "seats": self.get_seats(),
            "fuels": self.get_fuels(),
            "transmission": self.get_transmission(),
            "price": self.get_price(),
            "year": self.get_year(),
        }
        return car


def replace_all(replacer, value):
    for old, new in replacer.items():
        value = value.replace(old, new)
    return value


if __name__ == "__main__":
    print("main")
    XeTotCrawler().crawl(3)
