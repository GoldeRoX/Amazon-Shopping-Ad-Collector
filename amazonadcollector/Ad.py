from datetime import datetime
from appium.webdriver.webelement import WebElement

from dataclasses import dataclass
from abc import ABC


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

    def __init__(self, element: WebElement):
        self.width = element.size["width"]
        self.height = element.size["height"]
        self.location_x = element.location["x"]
        self.location_y = element.location["y"]
        self.text = element.get_attribute("text")
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class SearchedAdBottomBanner(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 1


class BrandsRelatedToYourSearch(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 2


class SearchedProductCarouselOfAds(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 4


class SearchedProductAd(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 5


class SearchedProductAdVideo(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 6


class SearchedProductSponsoredBrandTop(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 7
