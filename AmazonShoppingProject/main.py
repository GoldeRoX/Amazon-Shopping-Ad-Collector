import sys

from selenium.common.exceptions import InvalidSessionIdException

from ads_logic import *
from database_connector import get_random_keyword

from base import *

"""adb shell settings put global http_proxy 151.236.15.140:3128"""


def main():
    # os.system("cd ~/android-sdk/emulator ./emulator -avd Amazon")
    start_time = time.time()
    try:
        session = MyDriver()
        session.first_launch()
    except (WebDriverException, InvalidSessionIdException):
        session = MyDriver(skip_device_initialization=False, skip_server_installation=False, no_reset=False)
        session.config_start()
        session.first_launch()
        time.sleep(5)
        session.cookies_click()

    session_id = SQLAdManager().get_last_saved_session_id_from_db() + 1

    ad_handler = AdHandler(session.driver, lang=DE)

    try:

        keyword = get_random_keyword()
        # TODO add to db column keyword_id
        keyword_id = keyword["id"]

        session.get_page(keyword["keyword"])
        # session.get_page(random.choice(list(open('keywords_test.txt'))))
        # session.get_page("Monitors")

        """scroll down through app Y and collect ads"""
        is_end_of_page = False
        previous_page_source = session.driver.page_source

        while not is_end_of_page:
            session.cookies_click()
            ad_handler.collect_video_ad(session_id, keyword_id)
            ad_handler.collect_ad_type_4(session_id, keyword_id)
            ad_handler.collect_ad_type_5(session_id, keyword_id)

            session.scroll_down()

            is_end_of_page = previous_page_source == session.driver.page_source
            previous_page_source = session.driver.page_source

        ad_handler.collect_ad_type_1(session_id, keyword_id)
        ad_handler.collect_ad_type_2(session_id, keyword_id)
    except KeyboardInterrupt:
        print("KeyboardInterrupt exception")
        sys.exit()
    finally:
        print(f"end of session {session_id} : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("--- %s seconds running ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()

# TODO Disable gps location on first lunch to save settings .... the rest of runs, enable gps to secure session
