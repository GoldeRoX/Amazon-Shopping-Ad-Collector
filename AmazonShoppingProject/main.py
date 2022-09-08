import subprocess
import shlex
import sys

from selenium.common.exceptions import InvalidSessionIdException

from AmazonShoppingProject.ads_logic import *
from AmazonShoppingProject.database_connector import get_random_keyword

from AmazonShoppingProject.base import *


def main(udid: int):
    pars = shlex.split(f"./emulator -avd Amazon-{udid} -http-proxy http://151.236.15.140:3128 -port {udid}")

    p = subprocess.Popen(pars, cwd="/home/krzysztof/android-sdk/emulator")
    time.sleep(15)
    start_time = time.time()

    try:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid))
        session.config_start()
        session.first_launch()
        print("przed1")
        session.change_lang_from_eng_to_de()
        print("po1")
    except (WebDriverException, InvalidSessionIdException):
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid),
                           skip_device_initialization=False, skip_server_installation=False, no_reset=False)
        session.config_start()
        session.first_launch()
        time.sleep(5)
        session.cookies_click()
        print("przed2")
        session.change_lang_from_eng_to_de()
        print("po2")

    session_id = SQLAdManager().get_last_saved_session_id_from_db() + 1

    ad_handler = AdHandler(session.driver, lang=DE)

    try:

        keyword = get_random_keyword()
        keyword_id = keyword["id"]

        session.get_page(keyword["keyword"])

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
        p.terminate()
        print(f"end of session {session_id} : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("--- %s seconds running ---" % (time.time() - start_time))
