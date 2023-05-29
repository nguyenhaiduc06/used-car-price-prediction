from abc import ABC, abstractmethod


class Crawler(ABC):
    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def save(self):
        pass
