import time

from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, \
    InvalidElementStateException, WebDriverException
from selenium.webdriver.common.by import By

from Ad import Ad
from locators_data import LocatorsData
from base import MyDriver


class AdHandler(object):

    def __init__(self, driver):
        self.driver = driver

    def execute_ad_1(self, ad_text_filter: [str], session_id: int) -> None:
        try:
            ads_list = self.collect_ads_1()
            for ad in ads_list:
                MyDriver.save_cropped_scr(self.driver, ad)
                ad.send_to_db(session_id)
                if ad.text.strip() is not None:
                    ad_text_filter.append(ad.text)
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
            pass

    def get_webelements_ads_2(self) -> [WebElement]:
        element_node = self.driver.find_element(By.XPATH, LocatorsData.brands_related_to_your_search_element_node_ENG)
        elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")
        webelements = []
        for element in elements:
            if element.get_attribute("clickable") == "true" and element.get_attribute("text").startswith(
                    "Sponsored ad from"):  # Sponsored ad from # Gesponserte Werbeanzeige von
                webelements.append(element)
        return webelements

    def execute_ad_2(self, ad_text_filter: [str], session_id: int) -> None:
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
                    ad_text_filter.append(ad.text)
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
            pass

    def get_webelements_ads_1(self) -> [WebElement]:
        webelements = []
        elements = self.driver.find_elements(By.XPATH, LocatorsData.BOTTOM_AD_ENG)

        for element in elements:
            if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
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
            elements = self.driver.find_elements(By.XPATH, LocatorsData.ad_4_node_ENG)
            return elements
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return []

    def get_webelements_ads_5(self) -> [WebElement]:
        try:
            elements = self.driver.find_elements(By.XPATH, LocatorsData.ad_5_node_ENG)
            return elements
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return []

    def execute_ad_4(self, ad_text_filter: [str], session_id: int):
        try:
            ads_webelements = self.get_webelements_ads_4()
            for element in ads_webelements:
                # TODO check if height can be replaced with other valid.
                if element.size["height"] > 870:
                    action = TouchAction(self.driver)
                    for i, web_element in enumerate(ads_webelements):
                        path = ".//child::*" + 3 * "/following-sibling::*"
                        text = web_element.find_element(By.XPATH, path).get_attribute("text")
                        if text not in ad_text_filter:
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
                            time.sleep(1.5)
                            if ad.text is not None:
                                ad_text_filter.append(ad.text)
                    break
        except (NoSuchElementException, TimeoutException, WebDriverException,
                StaleElementReferenceException, InvalidElementStateException):
            pass

    # TODO create a solution that will automate verification
    def execute_ad_5(self, ad_text_filter: [str], session_id: int):
        try:
            ads_webelements = self.get_webelements_ads_5()
            for webElement in ads_webelements:
                if webElement.size["height"] > 450:
                    elements = webElement.find_elements(By.XPATH, ".//*[@class='android.view.View']")
                    result_text = elements[4].get_attribute("text")
                    var1 = result_text.startswith("Sponsored")
                    var2 = elements[7].get_attribute("text") == "product-detail"
                    if var1 and var2 and result_text not in ad_text_filter:
                        """create ad object"""
                        ad = Ad(webElement, 5)
                        MyDriver.save_cropped_scr(self.driver, ad)
                        ad.text = result_text
                        ad.send_to_db(session_id)
                        if ad.text is not None:
                            ad_text_filter.append(ad.text)
        except (
                NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException,
                IndexError):
            pass

# for ads_with recording, for height(crop) add y of element_text + y of element with text "Sponsored"
