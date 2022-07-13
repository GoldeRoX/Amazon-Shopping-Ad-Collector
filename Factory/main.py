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


def scroll_down(driver):

    """scroll down through app Y"""
    try:
        driver.swipe(start_x=470, start_y=1100, end_x=470, end_y=500, duration=400)
    except WebDriverException:
        pass


def main():
    session = MyDriver()
    _driver = session.driver

    ad_text_filter = []

    try:
        """list of keywords will be added externally"""
        list_of_keywords = ["Laptops", "Monitors", "LG"]
        try:
            get_page(_driver, list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])
        except NoSuchElementException:
            first_launch(_driver)
            get_page(_driver, list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])

        """scroll down through app Y and collect ads"""
        for i in range(26):
            if i == 0:
                time.sleep(2)
                pass
            else:
                scroll_down(_driver)

            execute_ad_4(_driver, ad_text_filter)
            execute_ad_5(_driver, ad_text_filter)

        execute_ad_1(_driver, ad_text_filter)
        execute_ad_2(_driver, ad_text_filter)
        print(ad_text_filter)
        ad_text_filter.clear()
        print(ad_text_filter)
    except KeyboardInterrupt:
        sys.exit()
    finally:
        _driver.close_app()


if __name__ == "__main__":
    while True:
        main()

# TODO after adding ad_type_5 give every session an ID (+DB)
