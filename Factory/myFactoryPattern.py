from abc import ABC, abstractmethod
from datetime import datetime
from appium.webdriver.webelement import WebElement
from Factory.database_connector import get_last_saved_id_from_db
from Factory.database_connector import send_data_to_db
from dataclasses import dataclass


class IAd(ABC):

    @abstractmethod
    def send_to_db(self):
        """Prepares separate ad data for exporting."""


@dataclass
class BottomAd(IAd):
    filename: str
    width: int
    height: int
    location_x: int
    location_y: int
    text: str
    timestamp: str
    ad_type: int = 1

    def __init__(self, element: WebElement):
        self.width = element.size["width"]
        self.height = element.size["height"]
        self.location_x = element.location["x"]
        self.location_y = element.location["y"]
        self.text = element.get_attribute("text")
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.filename = str(get_last_saved_id_from_db() + 1) + ".png"""
        self.ad_type = 1

    def send_to_db(self):
        send_data_to_db(self.filename, self.width, self.height, self.location_x,
                        self.location_y, self.text, self.timestamp, self.ad_type)


@dataclass
class BrandsRelatedToYourSearch(IAd):
    filename: str
    width: int
    height: int
    location_x: int
    location_y: int
    text: str
    timestamp: str
    ad_type: int = 2

    def __init__(self, element: WebElement):
        self.width = element.size["width"]
        self.height = element.size["height"]
        self.location_x = element.location["x"]
        self.location_y = element.location["y"]
        self.text = element.get_attribute("text")
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.filename = str(get_last_saved_id_from_db() + 1) + ".png"""
        self.ad_type = 2

    def send_to_db(self):
        send_data_to_db(self.filename, self.width, self.height, self.location_x,
                        self.location_y, self.text, self.timestamp, self.ad_type)

    """stworzyc slownik z samymi nullami
    kazda wywolana metoda zbierania metadanych nadpisuje nulla o dana wartosc"""

    """fabryka przyjmuje web element
    z niego wyciaga PO KOLEI kazdy atrybut w osobnej metodzie
    na koncu fabryka wypluwa slownik z meta_danymi"""

# TODO sprawdzenie w save_croped_scr() czy reklama zawiera same biae/czarne pixels TODO zmodyfikowanie
#  save_cropped_scr() by zwracal True/False -> jesli nie zapisze scr == nie wysyla danych do db fasada! web element na
#  wyjsciu reklama blackbox ukryc tworzenie obiektu oddzie;ic typy reklam od strony w jakim sposobie oddzielic
#  tworzenie reklamy osobno syllabic atrybuty do ukrytej classy TODO weryfikatory sprawdzajace czy sa widoczne
#   checkpointy / jesli nie skip, /// jesli tak, przeklikac / apka zapisze stan sesji
