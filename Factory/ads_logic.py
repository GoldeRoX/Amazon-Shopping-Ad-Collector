from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, \
    InvalidElementStateException, WebDriverException
from selenium.webdriver.common.by import By

from Ad import Ad
from base import MyDriver


class AdHandler(object):

    def __init__(self, lang):
        self.driver = MyDriver().driver
        self.ad_text_filter = []
        self.lang = lang

    def is_ad_used(self, ad: Ad) -> bool:
        text = ad.text.strip()
        if text not in self.ad_text_filter:
            return False
        else:
            return True

    def execute_ad_1(self, session_id: int) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            ads_list = self.collect_ads_1()
            for ad in ads_list:
                MyDriver.save_cropped_scr(self.driver, ad)
                ad.send_to_db(session_id)
                if ad.text.strip() is not None:
                    self.ad_text_filter.append(ad.text)
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
            pass

    def get_webelements_ads_2(self) -> [WebElement]:
        element_node = self.driver.find_element(By.XPATH, self.lang.brands_related_to_your_search_element_node)
        elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")
        webelements = []
        for element in elements:
            if element.get_attribute("clickable") == "true" and element.get_attribute("text").startswith(
                    self.lang.ad_2_starts_with):
                webelements.append(element)
        return webelements

    def execute_ad_2(self, session_id: int) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            ads_webelements = self.get_webelements_ads_2()
            action = TouchAction(self.driver)
            for i, web_element in enumerate(ads_webelements):
                """scroll through web_elements ads"""
                if i == 0:
                    pass
                else:
                    action.press(ads_webelements[i]).move_to(ads_webelements[i - 1]).wait(ms=2000).release().perform()

                """create an object of ad"""
                ad = Ad(web_element, 2)
                MyDriver.save_cropped_scr(self.driver, ad)
                ad.send_to_db(session_id)
                if ad.text.strip() is not None:
                    self.ad_text_filter.append(ad.text)
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
            pass

    def get_webelements_ads_1(self) -> [WebElement]:
        webelements = []
        elements = self.driver.find_elements(By.XPATH, self.lang.BOTTOM_AD)

        for element in elements:
            if element.size["height"] > 300:
                webelements.append(element)
        return webelements

    def collect_ads_1(self) -> [Ad]:
        ads = []
        webelements = self.get_webelements_ads_1()

        for webElement in webelements:
            """create an object of ad"""
            ad = Ad(webElement, 1)
            ads.append(ad)
        return ads

    def collect_ads_2(self) -> [Ad]:
        ads = []
        ads_webelements = self.get_webelements_ads_2()
        for web_element in ads_webelements:
            """create an object of ad"""
            ad = Ad(web_element, 2)
            ads.append(ad)
        return ads

    def get_webelements_ads_4(self) -> [WebElement]:
        try:
            elements = self.driver.find_elements(By.XPATH, self.lang.ad_4_node)
            return elements
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return []

    def get_webelements_ads_5(self) -> [WebElement]:
        try:
            elements = self.driver.find_elements(By.XPATH, self.lang.ad_5_node)
            return elements
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return []

    def execute_ad_4(self, session_id: int):
        """Create, send to DB and save scr of ad"""
        try:
            ads_webelements = self.get_webelements_ads_4()
            for element in ads_webelements:
                if element.size["height"] > 870:
                    action = TouchAction(self.driver)
                    for i, web_element in enumerate(ads_webelements):
                        path = ".//child::*" + 3 * "/following-sibling::*"
                        text = web_element.find_element(By.XPATH, path).get_attribute("text")
                        if text not in self.ad_text_filter:
                            """scroll through web_elements ads"""
                            if i == 0:
                                pass
                            else:
                                par = (ads_webelements[i].size["width"] - ads_webelements[i].size["width"] / 2)
                                action.press(ads_webelements[i]).move_to(ads_webelements[i - 1], x=par, y=0).wait(
                                    ms=2000).release().perform()

                            """create an object of ad"""
                            ad = Ad(web_element, 4)
                            MyDriver.save_cropped_scr(self.driver, ad)

                            ad.text = text
                            ad.send_to_db(session_id)
                            if ad.text is not None:
                                self.ad_text_filter.append(ad.text)
                    break
        except (NoSuchElementException, TimeoutException, WebDriverException,
                StaleElementReferenceException, InvalidElementStateException):
            pass

    def execute_ad_5(self, session_id: int):
        """Create, send to DB and save scr of ad"""
        try:
            ads_webelements = self.get_webelements_ads_5()
            for webElement in ads_webelements:
                if webElement.size["height"] > 450:
                    elements = webElement.find_elements(By.XPATH, ".//*[@class='android.view.View']")
                    result_text = elements[4].get_attribute("text")
                    var1 = result_text.startswith(self.lang.ad_5_starts_with)
                    var2 = elements[7].get_attribute("text") == "product-detail"
                    if var1 and var2 and result_text not in self.ad_text_filter:
                        """create ad object"""
                        ad = Ad(webElement, 5)
                        MyDriver.save_cropped_scr(self.driver, ad)
                        ad.text = result_text
                        ad.send_to_db(session_id)
                        if ad.text is not None:
                            self.ad_text_filter.append(ad.text)
        except (
                NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException,
                IndexError):
            pass
