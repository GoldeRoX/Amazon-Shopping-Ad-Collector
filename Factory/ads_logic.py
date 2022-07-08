import time

from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from Ad import Ad
from locators_data import LocatorsData
from base import save_cropped_scr


def execute_ad_1(driver) -> None:
    try:
        ads_list = collect_ads_1(driver)
        for ad in ads_list:
            save_cropped_scr(driver, ad)
            ad.send_to_db()
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        pass


def get_webelements_ads_2(driver) -> [WebElement]:
    element_node = driver.find_element(By.XPATH, LocatorsData.brands_related_to_your_search_element_node_ENG)
    elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")
    webelements = []
    for element in elements:
        if element.get_attribute("clickable") == "true" and element.get_attribute("text").startswith(
                "Sponsored ad from"):  # Sponsored ad from # Gesponserte Werbeanzeige von
            webelements.append(element)
    return webelements


def execute_ad_2(driver) -> None:
    try:
        ads_webelements = get_webelements_ads_2(driver)
        action = TouchAction(driver)
        for i, web_element in enumerate(ads_webelements):
            """scroll through web_elements ads"""
            if i == 0:
                pass
            else:
                action.press(ads_webelements[i]).move_to(ads_webelements[i - 1]).wait(ms=2000).release().perform()

            """create an object of ad"""
            ad = Ad(web_element, 2)
            save_cropped_scr(driver, ad)
            ad.send_to_db()
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        pass


def get_webelements_ads_1(driver) -> [WebElement]:
    webelements = []
    elements = driver.find_elements(By.XPATH, LocatorsData.BOTTOM_AD_ENG)

    for element in elements:
        if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
            webelements.append(element)
    return webelements


def collect_ads_1(driver) -> [Ad]:
    ads = []

    webelements = get_webelements_ads_1(driver)

    for element in webelements:
        """create an object of ad"""
        ad = Ad(element, 1)
        ads.append(ad)
    return ads


def collect_ads_2(driver) -> [Ad]:
    ads = []
    ads_webelements = get_webelements_ads_2(driver)
    for web_element in ads_webelements:
        """create an object of ad"""
        ad = Ad(web_element, 2)
        ads.append(ad)
    return ads


# TODO
def get_webelements_ads_4(driver) -> [Ad]:
    try:

        elements = driver.find_elements(By.XPATH, LocatorsData.ad_4_node_ENG)
        return elements
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        return []


def execute_ad_4(driver):
    try:
        ads_webelements = get_webelements_ads_4(driver)
        action = TouchAction(driver)
        for i, web_element in enumerate(ads_webelements):
            """scroll through web_elements ads"""
            if i == 0:
                pass
            else:
                # TODO upgrade scroll
                # (possible solution = change moving elements to next element by moving by width)
                action.press(ads_webelements[i]).move_to(ads_webelements[i - 1]).wait(ms=2000).release().perform()
                """if i == len(ads_webelements) - 2:
                    action.press(ads_webelements[i]).move_to(ads_webelements[i - 1]).wait(ms=2000).release().perform()"""

            """create an object of ad"""
            ad = Ad(web_element, 4)
            save_cropped_scr(driver, ad)
            path = ".//child::*/following-sibling::*/following-sibling::*"
            text = web_element.find_element(By.XPATH, path).get_attribute("text")
            ad.text = text
            ad.send_to_db()
            time.sleep(1.5)
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        pass
