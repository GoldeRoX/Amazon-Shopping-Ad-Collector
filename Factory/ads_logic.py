import time

from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, \
    InvalidElementStateException
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

    for webElement in webelements:
        """create an object of ad"""
        ad = Ad(webElement, 1)
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


def get_webelements_ads_4(driver) -> [WebElement]:
    try:
        elements = driver.find_elements(By.XPATH, LocatorsData.ad_4_node_ENG)
        return elements
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        return []


def get_webelements_ads_5(driver) -> [WebElement]:
    try:
        elements = driver.find_elements(By.XPATH, LocatorsData.ad_5_node_ENG)
        return elements
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        return []


def execute_ad_4(driver, ads_text_filer: [str]):
    try:
        ads_webelements = get_webelements_ads_4(driver)
        for element in ads_webelements:
            if element.size["height"] > 870:
                action = TouchAction(driver)
                for i, web_element in enumerate(ads_webelements):
                    path = ".//child::*" + 2 * "/following-sibling::*"
                    text = web_element.find_element(By.XPATH, path).get_attribute("text")
                    if text not in ads_text_filer:
                        """scroll through web_elements ads"""
                        if i == 0:
                            pass
                        else:
                            par = (ads_webelements[i].size["width"] - ads_webelements[i].size["width"] / 2)
                            action.press(ads_webelements[i]).move_to(ads_webelements[i - 1], x=par, y=0).wait(
                                ms=2000).release().perform()

                        """create an object of ad"""
                        ad = Ad(web_element, 4)
                        save_cropped_scr(driver, ad)

                        ad.text = text
                        ad.send_to_db()
                        time.sleep(1.5)
                        ads_text_filer.append(text)
                break
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException, InvalidElementStateException):
        pass


def execute_ad_5(driver, ad_text_filter: [str]):
    try:
        ads_webelements = get_webelements_ads_5(driver)
        for webElement in ads_webelements:
            if webElement.get_attribute("text").startswith('Sponsored Ad -'):
                continue
            print("ad type 5 in view")
            text_path = ".//child::*" + 3 * "/following-sibling::*"
            text = webElement.find_element(By.XPATH, text_path).get_attribute("text")
            price_path = ".//child::*" + 4 * "/following-sibling::*"
            price = webElement.find_element(By.XPATH, price_path).get_attribute("text")
            if text not in ad_text_filter:
                """create ad"""
                ad = Ad(webElement, 5)
                ad.text = text
                ad.price = price
                save_cropped_scr(driver, ad)
                ad.send_to_db()
                ad_text_filter.append(ad.text)

    except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
        print("error ad5")
