import sys
import random

from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException

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
    for i in range(14):
        try:
            driver.swipe(470, 1100, 470, 50, 400)
        except WebDriverException:
            pass


def execute_ad_1(driver) -> None:
    try:
        ads_list = collect_ads_1(driver)
        for ad in ads_list:
            save_cropped_scr(driver, ad)
            ad.send_to_db()
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        pass


def get_webelements_ads_2(driver):
    element_node = driver.find_element(By.XPATH, LocatorsData.brands_related_to_your_search_element_node)
    elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")
    webelements = []
    for element in elements:
        if element.get_attribute("clickable") == "true" and element.get_attribute("text").startswith(
                "Sponsored ad from"):
            webelements.append(element)
    return webelements


def execute_ad_2(driver) -> None:
    ads_webelements = get_webelements_ads_2(driver)
    action = TouchAction(driver)
    for i, web_element in enumerate(ads_webelements):
        """scroll through web_elements ads"""
        if i == 0:
            pass
        else:
            action.press(ads_webelements[i]).move_to(ads_webelements[i - 1]).wait(ms=1000).release().perform()
        """create an object of ad"""
        ad = Ad(web_element, 2)
        save_cropped_scr(driver, ad)
        ad.send_to_db()


def collect_ads_1(driver) -> [Ad]:
    ads = []
    elements = driver.find_elements(By.XPATH, LocatorsData.BOTTOM_AD)

    for element in elements:
        if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
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


def main():
    session = MyDriver()

    _driver = session.driver
    try:
        # first_launch(_driver)

        list_of_brands = ["Oculus", "Hp", "Laptops", "Monitors"]
        set_up(_driver, list_of_brands[random.randint(0, len(list_of_brands) - 1)])
        execute_ad_1(_driver)
        execute_ad_2(_driver)
    except KeyboardInterrupt:
        sys.exit()
    finally:
        _driver.close_app()
        _driver.close()


if __name__ == "__main__":
    main()
