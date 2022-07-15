import sys
import random

from database_connector import get_last_saved_session_id_from_db
from ads_logic import *

from base import *


def main():
    session = MyDriver()
    _driver = session.driver

    session_id = get_last_saved_session_id_from_db() + 1

    ad_text_filter = []

    ad_handler = AdHandler(session.driver)

    try:
        """list of keywords will be added externally"""
        list_of_keywords = ["Laptops", "Monitors", "LG", "Oculus", "Meta"]
        try:
            session.get_page(list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])
        except NoSuchElementException:
            session.first_launch()
            session.get_page(list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])

        """scroll down through app Y and collect ads"""
        for i in range(26):
            if i == 0:
                time.sleep(2)
            else:
                session.scroll_down()

            ad_handler.execute_ad_4(ad_text_filter, session_id)
            ad_handler.execute_ad_5(ad_text_filter, session_id)

        ad_handler.execute_ad_1(ad_text_filter, session_id)
        ad_handler.execute_ad_2(ad_text_filter, session_id)
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
