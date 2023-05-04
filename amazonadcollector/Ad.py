from datetime import datetime
from appium.webdriver.webelement import WebElement
from dataclasses import dataclass

from amazonadcollector.database_connector import SQLAdManager
from amazonadcollector.base import save_cropped_scr


@dataclass
class Ad(object):
    """
    Represents a generic advertisement.
    """

    def __init__(self, element: WebElement):
        self.width: int = element.size["width"]
        self.height: int = element.size["height"]
        self.location_x: int = element.location["x"]
        self.location_y: int = element.location["y"]
        self.text: str = element.get_attribute("text")
        self.timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_cropped_scr(self, driver, filename):
        save_cropped_scr(driver, self, filename)


class SearchedAdBottomBanner(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 1

    def send_data_to_db(self, id_session, keyword_id, udid):
        SQLAdManager.send_data_to_db(SQLAdManager(), self.width, self.height, self.location_x, self.location_y,
                                     self.text, self.timestamp, self.ad_type, id_session, keyword_id, udid)


class BrandsRelatedToYourSearch(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 2

    def send_data_to_db(self, id_session, keyword_id, udid):
        SQLAdManager.send_data_to_db(SQLAdManager(), self.width, self.height, self.location_x, self.location_y,
                                     self.text, self.timestamp, self.ad_type, id_session, keyword_id, udid)


class SearchedProductCarouselOfAds(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 4

    def send_data_to_db(self, id_session, keyword_id, udid):
        SQLAdManager.send_data_to_db(SQLAdManager(), self.width, self.height, self.location_x, self.location_y,
                                     self.text, self.timestamp, self.ad_type, id_session, keyword_id, udid)


class SearchedProductAd(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 5

    def send_data_to_db(self, id_session, keyword_id, udid):
        SQLAdManager.send_data_to_db(SQLAdManager(), self.width, self.height, self.location_x, self.location_y,
                                     self.text, self.timestamp, self.ad_type, id_session, keyword_id, udid)


class SearchedProductAdVideo(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 6

    def send_data_to_db(self, id_session, keyword_id, udid):
        SQLAdManager.send_data_to_db(SQLAdManager(), self.width, self.height, self.location_x, self.location_y,
                                     self.text, self.timestamp, self.ad_type, id_session, keyword_id, udid)


class SearchedProductSponsoredBrandTop(Ad):
    def __init__(self, element: WebElement):
        super().__init__(element)
        self.ad_type: int = 7

    def send_data_to_db(self, id_session, keyword_id, udid):
        SQLAdManager.send_data_to_db(SQLAdManager(), self.width, self.height, self.location_x, self.location_y,
                                     self.text, self.timestamp, self.ad_type, id_session, keyword_id, udid)


class AdFactory(object):
    ...
