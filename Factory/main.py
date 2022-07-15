import sys
import random

from database_connector import get_last_saved_session_id_from_db
from ads_logic import *

from base import *


def main():
    start_time = time.time()
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
        end_of_page = False
        previous_page_source = _driver.page_source

        while not end_of_page:
            ad_handler.execute_ad_5(ad_text_filter, session_id)
            ad_handler.execute_ad_4(ad_text_filter, session_id)
            session.scroll_down()
            end_of_page = previous_page_source == _driver.page_source
            previous_page_source = _driver.page_source

        ad_handler.execute_ad_1(ad_text_filter, session_id)
        ad_handler.execute_ad_2(ad_text_filter, session_id)
        ad_text_filter.clear()
    except KeyboardInterrupt:
        print("KeyboardInterrupt exception")
        sys.exit()
    finally:
        print(f"end of session {session_id} : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("--- %s seconds running---" % (time.time() - start_time))
        _driver.close_app()
        _driver.quit()


if __name__ == "__main__":
    while True:
        main()
