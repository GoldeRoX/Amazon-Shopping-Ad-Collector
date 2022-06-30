from datetime import datetime
from appium.webdriver.webelement import WebElement
from Factory.database_connector import get_last_saved_id_from_db
from Factory.database_connector import send_data_to_db
from dataclasses import dataclass


@dataclass
class Ad(object):
    filename: str
    width: int
    height: int
    location_x: int
    location_y: int
    text: str
    timestamp: str
    ad_type: int

    def __init__(self, element: WebElement, ad_type: int):
        self.width = element.size["width"]
        self.height = element.size["height"]
        self.location_x = element.location["x"]
        self.location_y = element.location["y"]
        self.text = element.get_attribute("text")
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.filename = str(get_last_saved_id_from_db() + 1) + ".png"""
        self.ad_type = ad_type

    def send_to_db(self):
        send_data_to_db(self.filename, self.width, self.height, self.location_x,
                        self.location_y, self.text, self.timestamp, self.ad_type)
