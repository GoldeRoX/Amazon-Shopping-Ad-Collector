# Basic Ad exporter

from abc import ABC, abstractmethod

class AdExporter(ABC):

    @abstractmethod
    def prepere_export(self, ad_data):
        """Prepares ad data for exporting."""

    @abstractmethod
    def do_export_to_db(self):
        """sends ad to db"""


class BottomAd()




        """fabryka przyjmuje web element
        z niego wyciaga PO KOLEI kazdy atrybut w osobnej metodzie
        na koncu fabryka wypluwa slownik z meta_danymi"""