import sys
import random

from selenium.common.exceptions import WebDriverException
from ads_logic import *

from Factory.locators_data import LocatorsData
from base import *


def get_page(driver, phrase_to_search: str) -> None:
    """search item"""
    driver.find_element(By.XPATH, LocatorsData.search_icon_ENG).click()
    send_text(driver, By.ID, LocatorsData.search_input_ENG, phrase_to_search)

    """press enter"""
    driver.press_keycode(66)


def scroll_to_bottom_and_collect_ads(driver):

    """scroll down through app Y"""
    for i in range(25):
        try:
            driver.swipe(start_x=470, start_y=1100, end_x=470, end_y=500, duration=400)
            webelements_list = get_webelements_ads_4(driver)

            for element in webelements_list:
                if element.size["height"] > 870:
                    execute_ad_4(driver)
                    break
        except WebDriverException:
            pass


def main():
    session = MyDriver()

    _driver = session.driver
    try:
        """list of keywords will be added externally"""
        list_of_keywords = ["Oculus", "Hp", "Laptops", "Monitors"]
        try:
            get_page(_driver, list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])
        except NoSuchElementException:
            first_launch(_driver)
            get_page(_driver, list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])

        """scroll down through app Y"""
        scroll_to_bottom_and_collect_ads(_driver)

        execute_ad_1(_driver)
        execute_ad_2(_driver)

    except KeyboardInterrupt:
        sys.exit()
    finally:
        _driver.close_app()


if __name__ == "__main__":
    main()

# TODO after adding ad_type_5 give every session an ID (+DB)
