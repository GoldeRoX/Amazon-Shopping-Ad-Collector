from abc import ABC, abstractmethod


class AdExporter(ABC):

    @abstractmethod
    def prepere_export(self, element):
        """Prepares seprate ad data for exporting."""

    @abstractmethod
    def do_export_to_db(self):
        """sends ad to db"""

    @abstractmethod
    def extract_element_width(self, element):
        """extract size width"""

    @abstractmethod
    def extract_element_height(self, element):
        """extract size height"""

    @abstractmethod
    def extract_element_location_x(self, element):
        """extract location_x"""

    @abstractmethod
    def extract_element_location_y(self, element):
        """extract location_y"""

    @abstractmethod
    def extract_element_text(self, element):
        """extract text"""


class BottomAd(AdExporter):
    def prepere_export(self, element):
        print("wywolywanie meta_danych")



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