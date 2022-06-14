from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractAdFactory(ABC):

    @abstractmethod
    def create_ad_type_1(self):
        pass

    @abstractmethod
    def create_ad_type_2(self):
        pass