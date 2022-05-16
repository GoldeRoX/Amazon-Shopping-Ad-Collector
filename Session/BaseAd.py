from telnetlib import EC
from traceback import print_stack

from abc import ABCMeta, abstractmethod, abstractstaticmethod

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



class IAd(metaclass=ABCMeta):

    @abstractstaticmethod
    def adMethod():
        """ Interface Method """

class Ad(IAd):

    def __int__(self):
        self.name = "Basic Ad Name"

    def adMethod(self):
        print("I am an ad")

ad1 = Ad()

ad1.adMethod()