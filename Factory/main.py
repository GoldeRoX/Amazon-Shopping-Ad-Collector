import sys
import random

from ads_logic import *

from base import *


def main():
    start_time = time.time()
    try:
        session = MyDriver()
    except WebDriverException:
        session = MyDriver(skip_device_initialization=False, skip_server_installation=False, no_reset=False)
        session.config_start()
        session.first_launch()
        time.sleep(10)
        session.cookies_click()

    session_id = SQLAdManager().get_last_saved_session_id_from_db() + 1

    ad_handler = AdHandler(session.driver, lang=DE)

    try:
        """list of keywords will be added externally"""
        list_of_keywords = ["Laptops", "Monitors", "LG", "Oculus", "Meta"]
        session.get_page(list_of_keywords[random.randint(0, len(list_of_keywords) - 1)])

        """scroll down through app Y and collect ads"""
        is_end_of_page = False
        previous_page_source = session.driver.page_source

        while not is_end_of_page:
            ad_handler.execute_ad_4(session_id)
            ad_handler.execute_ad_5(session_id)
            session.scroll_down()
            is_end_of_page = previous_page_source == session.driver.page_source

            previous_page_source = session.driver.page_source

        ad_handler.execute_ad_1(session_id)
        ad_handler.execute_ad_2(session_id)
    except KeyboardInterrupt:
        print("KeyboardInterrupt exception")
        sys.exit()
    finally:
        print(f"end of session {session_id} : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("--- %s seconds running---" % (time.time() - start_time))
        session.driver.close_app()


if __name__ == "__main__":
    while True:
        main()
