from abc import ABC, abstractmethod
from datetime import datetime
from appium.webdriver.webelement import WebElement
from Session.database_connector import get_last_saved_id_from_db


class IAd(ABC):

    @abstractmethod
    def prepere_export(self, element):
        """Prepares seprate ad data for exporting."""


class BottomAd(IAd):

    """"width": element.size["width"],
    "height": element.size["height"],
    "location_x": element.location["x"],
    "location_y": element.location["y"],
    "text": element.get_attribute("text"),
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "filename": str(get_last_saved_id_from_db() + 1) + ".png"""

    def __init__(self, element: WebElement):
        self.width = element.size["width"]
        self.height = element.size["height"]
        self.location_x = element.location["x"]
        self.location_y = element.location["y"]
        self.text = element.get_attribute("text")
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.filename = str(get_last_saved_id_from_db() + 1) + ".png"""







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