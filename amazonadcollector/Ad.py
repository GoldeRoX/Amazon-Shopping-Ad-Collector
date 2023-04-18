from datetime import datetime
from appium.webdriver.webelement import WebElement

from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Ad(ABC):
    filename: str
    width: int
    height: int
    location_x: int
    location_y: int
    text: str
    timestamp: str
    ad_type: int
    emulator: int
    host_ip: str

    def __init__(self, element: WebElement, ad_type: int):
        self.width = element.size["width"]
        self.height = element.size["height"]
        self.location_x = element.location["x"]
        self.location_y = element.location["y"]
        self.text = element.get_attribute("text")
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ad_type = ad_type


class SearchedAdBottomBanner(Ad):
    ...


class BrandsRelatedToYourSearch(Ad):
    ...


class SearchedProductCarouselOfAds(Ad):
    ...


class SearchedProductAd(Ad):
    ...


class SearchedProductAdVideo(Ad):
    ...


class SearchedProductSponsoredBrandTop(Ad):
    ...


