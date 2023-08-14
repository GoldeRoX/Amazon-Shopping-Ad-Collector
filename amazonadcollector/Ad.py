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

    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        self.width: int = element.size["width"]
        self.height: int = element.size["height"]
        self.location_x: int = element.location["x"]
        self.location_y: int = element.location["y"]
        self.text: str = element.get_attribute("text")
        self.__timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sql_ad_manager: SQLAdManager = sql_ad_manager
        self.ad_type = None

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_location_x(self) -> int:
        return self.location_x

    def get_location_y(self) -> int:
        return self.location_y

    def get_timestamp(self) -> str:
        return self.__timestamp

    def send_data_to_db(self, keyword_id: int) -> int:
        """
        Returns:
            data_set_id: int
        """
        return SQLAdManager.send_data_to_db(self.sql_ad_manager, self.width, self.height, self.location_x,
                                            self.location_y, self.text, self.__timestamp, self.ad_type, keyword_id)

    def save_cropped_scr(self, driver, data_set_id: int):
        save_cropped_scr(driver, self, str(data_set_id))

    def save_ad(self, driver, keyword_id: int):
        self.save_cropped_scr(driver, self.send_data_to_db(keyword_id))


class MainPageBannerAd(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 1


class BrandsRelatedToYourSearch(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 2


class HighlyRatedProductCarouselOfAds(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 4


class SearchedProductCarouselOfAds(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 4


class SearchedProductAd(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 5


class SearchedProductAdVideo(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 6


class SearchedProductSponsoredBrandTop(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 7


class SearchedProductSponsoredBrandMid(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 3


class MainPageCarouselOfAds(Ad):
    def __init__(self, element: WebElement, sql_ad_manager: SQLAdManager):
        super().__init__(element, sql_ad_manager)
        self.ad_type: int = 8
