from crawler import Crawler
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import *
from collections import defaultdict

DATA_PATH = "data/san_xe_hot"
PATH_TO_CARS = DATA_PATH + "/cars.csv"
PATH_TO_LINKS = DATA_PATH + "/links.csv"


class SanXeHotCrawler(Crawler):
    def crawl(self):
        """crawl cars data and save to csv file"""
        links = self.getLinks()
        cars = []
         
        for link in links:
            car_data = self.get_car_data(link)
            cars.append(car_data)

        cars_df = pd.DataFrame.from_records(cars)
        cars_df.to_csv(PATH_TO_CARS)

    def getLinks(self):
        try:
            links_df = pd.read_csv(PATH_TO_LINKS)
            links = links_df[0].values.tolist()
            if links:
                return links
        except:
            pass

        # feel free to refactor the code below
        links = {"link": [], "car_type": []}
        url_list = [
            "https://www.sanxehot.vn/mua-ban-xe/loai-xe-cu-pg" + str(i)
            for i in range(1, 2)
        ]

        for url in url_list:
            res = requests.get(url).text
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

        return links["link"]

    def get_car_data(self, link):

        """
        Args:
            link (str): link to the detail page of a car

        Returns:
            Car Data: a record of a car
        """
        car = {}

        url = 'https://www.sanxehot.vn/' + link
        res = requests.get(url).text
        soup = BeautifulSoup(res, "html.parser")

        brand = soup.find("h1", class_="name").find().text
        car["brand"] = brand
        
        name = soup.find("h1", class_="name").find().next_sibling.text
        car["name"] = name

        table = soup.find("table", class_="info")

        price = table.find_all("tr")[0].text
        car["price"] = price

        for tr in table.find_all("tr")[1:]:
            key = tr.find_all("td")[0].text
            value = tr.find_all("td")[1].text
            car[key] = value

        return car
