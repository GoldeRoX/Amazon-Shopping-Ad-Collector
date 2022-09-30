import subprocess
import shlex
import sys

from selenium.common.exceptions import InvalidSessionIdException

from AmazonShoppingProject.ads_logic import *
from AmazonShoppingProject.database_connector import get_random_keyword

from AmazonShoppingProject.base import *


def main(udid: int):
    pars_emulator = shlex.split(f"./emulator -avd Amazon-{udid} -http-proxy http://151.236.15.140:3128 -port {udid}")
    process_emulator = subprocess.Popen(pars_emulator, cwd="/home/krzysztof/android-sdk/emulator")
    time.sleep(10)
    start_time = time.time()

    try:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid))
    except (WebDriverException, InvalidSessionIdException):
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid),
                           skip_device_initialization=False, skip_server_installation=False, no_reset=False)

    close = session.driver.find_elements(By.ID, "android:id/aerr_close")
    try:
        close[0].click()
    except:
        pass

    session.config_start()
    session.first_launch()
    session.change_lang_from_eng_to_de()

    session_id = SQLAdManager().get_last_saved_session_id_from_db() + 1

    ad_handler = AdHandler(session.driver, lang=DE)

    keyword = get_random_keyword()
    keyword_id = keyword["id"]

    session.get_page(keyword["keyword"])

    try:

        """scroll down through app Y and collect ads"""
        is_end_of_page = False
        previous_page_source = session.driver.page_source

        while not is_end_of_page:
            try:
                close[0].click()
            except:
                pass
            session.cookies_click()
            ad_handler.collect_video_ad(session_id, keyword_id)
            # ad_handler.collect_ad_type_4(session_id, keyword_id)
            ad_handler.collect_ad_type_5(session_id, keyword_id)
            # TODO
            # naprawic problem z brakiem txt
            # ad_handler.collect_ad_type_1(session_id, keyword_id)

            session.scroll_down()

            is_end_of_page = previous_page_source == session.driver.page_source
            previous_page_source = session.driver.page_source

        # ad_handler.collect_ad_type_1(session_id, keyword_id)
        # ad_handler.collect_ad_type_2(session_id, keyword_id)
    except KeyboardInterrupt:
        print("KeyboardInterrupt exception")
        sys.exit()
    finally:
        session.driver.quit()
        process_emulator.terminate()
        print(f"end of session {session_id} : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("--- %s seconds running ---" % (time.time() - start_time))
