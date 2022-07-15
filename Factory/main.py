import sys
import random

from database_connector import get_last_saved_session_id_from_db
from ads_logic import *

from base import *


# TODO implement that tactic
"""
could query the current list of visible elements in between each swipe, 
then compare the current list against the last list. If the list is the same, 
the swipe had no effect, and app is at the bottom
"""


def scroll_down(driver) -> None:
    """scroll down through app Y"""
    try:
        driver.swipe(start_x=470, start_y=1100, end_x=470, end_y=500, duration=400)
    except WebDriverException:
        pass


def main():
    session = MyDriver()
    _driver = session.driver

    session_id = get_last_saved_session_id_from_db() + 1

    ad_text_filter = []

    ad_handler = AdHandler()

    try:
        """list of keywords will be added externally"""
        list_of_keywords = ["Laptops", "Monitors", "LG", "Oculus", "Meta"]
        try:
            session.get_page(_driver, list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])
        except NoSuchElementException:
            session.first_launch(_driver)
            session.get_page(_driver, list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])

        """scroll down through app Y and collect ads"""
        for i in range(26):
            if i == 0:
                time.sleep(2)
            else:
                scroll_down(_driver)

            ad_handler.execute_ad_4(_driver, ad_text_filter, session_id)
            ad_handler.execute_ad_5(_driver, ad_text_filter, session_id)

        ad_handler.execute_ad_1(_driver, ad_text_filter, session_id)
        ad_handler.execute_ad_2(_driver, ad_text_filter, session_id)
        ad_text_filter.clear()
    except KeyboardInterrupt:
        print("KeyboardInterrupt exception")
        sys.exit()
    finally:
        print(f"end of session {session_id} : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        _driver.close_app()


if __name__ == "__main__":
    while True:
        main()
