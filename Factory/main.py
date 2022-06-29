import random
import time

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from appium.webdriver.webelement import WebElement

from Factory.locators_data import LocatorsData
from base import *

from Ad import Ad


def set_up(driver, phrase_to_search: str) -> None:
    """search item"""
    driver.find_element(By.XPATH, LocatorsData.search_icon).click()
    send_text(driver, By.ID, LocatorsData.search_input, phrase_to_search)

    """press enter"""
    driver.press_keycode(66)

    """scroll through app Y"""
    for i in range(16):
        try:
            driver.swipe(470, 1100, 470, 50, 400)
            time.sleep(1)
        except:
            pass


"""def get_ads_1(driver) -> [WebElement]:
    elements = driver.find_elements(By.XPATH, LocatorsData.BOTTOM_AD)
    ads = []
    for element in elements:
        if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
            ads.append(element)
    return ads"""


def bottom_ad(driver) -> None:
    try:
        element = driver.find_element(By.XPATH, LocatorsData.BOTTOM_AD)

        if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
            """create an object of ad"""
            ad = Ad(element, 1)
            save_cropped_scr(driver, ad)
            ad.send_to_db()

    except NoSuchElementException:
        pass


def get_webelements_ads_2(driver):
    element_node = driver.find_element(By.XPATH, LocatorsData.brands_related_to_your_search_element_node)
    elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")
    ads = []
    for x in range(len(elements)):
        if elements[x].get_attribute("clickable") == "true" and elements[x].get_attribute("text").startswith(
                "Sponsored ad from"):
            ads.append(elements[x])
    return ads


def execute_ad_2(driver) -> None:
    try:
        ads_webelements = get_webelements_ads_2(driver)

        # reklamy_tet = []
        for x in range(len(ads_webelements)):
            web_element = ads_webelements[x]
            try:
                """create an object of ad"""
                ad = Ad(web_element, 2)

                # reklamy_tet.append(ad)

                save_cropped_scr(driver, ad)
                ad.send_to_db()
                # TODO remake scroll
                """scroll through web_elements ads"""
                action = TouchAction(driver)
                action.press(web_element).move_to(x=-web_element.size["width"] / 2, y=0).release().perform()

            except Exception as e:
                print(f'Exception occurred : {e}')

    except (NoSuchElementException, TimeoutException):
        pass


def collect_ads_1(driver) -> [Ad]:
    try:
        ads = []
        elements = driver.find_elements(By.XPATH, LocatorsData.BOTTOM_AD)

        for element in elements:
            if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
                """create an object of ad"""
                ad = Ad(element, 1)
                ads.append(ad)
        return ads
    except NoSuchElementException:
        pass


def collect_ads_2(driver) -> [Ad]:
    ads = []
    ads_webelements = get_webelements_ads_2(driver)
    for x in range(len(ads_webelements)):
        web_element = ads_webelements[x]
        """create an object of ad"""
        ad = Ad(web_element, 2)
        ads.append(ad)

    return ads


if __name__ == "__main__":
    session = MyDriver()

    _driver = session.driver
    while True:
        try:
            list_of_brands = ["Oculus", "Hp", "Laptops", "Monitors"]
            set_up(_driver, list_of_brands[random.randint(0, len(list_of_brands) - 1)])
            print(collect_ads_1(_driver))
            print(collect_ads_2(_driver))
            #bottom_ad(_driver)
            #execute_ad_2(_driver)
        except:
            pass
        """finally:
            _driver.close()"""
