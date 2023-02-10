import subprocess
import shlex
import sys
import time

from selenium.common.exceptions import WebDriverException
from datetime import datetime

from amazonadcollector.ads_logic import SQLAdManager, AdHandler
from amazonadcollector.database_connector import get_random_keyword
from amazonadcollector.base import MyDriver, BaseMethods
from amazonadcollector.locators_data import DE


def main(udid: int):
    pars_emulator = shlex.split(f"./emulator -avd Amazon-{udid} -http-proxy http://81.169.186.225:3128 -port {udid}")
    process_emulator = subprocess.Popen(pars_emulator, cwd="/home/krzysztof/android-sdk/emulator")
    time.sleep(30)
    start_time = time.time()

    try:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid))
    except WebDriverException:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid),
                           skip_device_initialization=False, skip_server_installation=False, no_reset=False)

    base_methods = BaseMethods(session.driver)
    base_methods.amazon_not_responding_close()
    base_methods.first_launch()
    base_methods.change_lang_from_eng_to_de()

    session_id = SQLAdManager().get_last_saved_session_id_from_db() + 1

    ad_handler = AdHandler(session.driver, lang=DE)

    keyword = get_random_keyword()
    keyword_id = keyword["id"]

    base_methods.get_page("Minecraft")
    # base_methods.get_page(keyword["keyword"])
    try:
        new_udid = 1

        base_methods.amazon_not_responding_close()
        time.sleep(2)
        base_methods.cookies_click()
        time.sleep(4)
        """scroll down through app Y and collect ads"""
        is_end_of_page = False
        previous_page_source = session.driver.page_source
        ad_handler.collect_ad_type_7_top(session_id, keyword_id, new_udid)
        """ad_handler.collect_ad_type_9(session_id, keyword_id, new_udid)
        ad_handler.collect_ad_type_9_alternative(session_id, keyword_id, new_udid)"""

        """test_1 = ad_handler.get_all_node_web_elements()
        print(len(test_1))
        test = ad_handler.get_filtered_complex_web_elements()
        print(len(test))
        print(test)"""

        while not is_end_of_page:
            base_methods.scroll_down()
            base_methods.amazon_not_responding_close()
            # ad_handler.collect_ad_type_1(session_id, keyword_id, new_udid)
            ad_handler.collect_video_ad(session_id, keyword_id, new_udid)
            # ad_handler.collect_video_ad_alternative(session_id, keyword_id, new_udid)
            ad_handler.collect_ad_type_7_mid(session_id, keyword_id, new_udid)
            ad_handler.collect_ad_type_5(session_id, keyword_id, new_udid)
            """ad_handler.collect_ad_type_2(session_id, keyword_id, new_udid)"""
            # ad_handler.collect_ad_type_2(session_id, keyword_id, new_udid)
            # ad_handler.collect_ad_type_1()

            is_end_of_page = previous_page_source == session.driver.page_source
            previous_page_source = session.driver.page_source

    except KeyboardInterrupt:
        print("KeyboardInterrupt exception")
        sys.exit()
    finally:
        session.driver.quit()
        process_emulator.terminate()
        print(f"end of session {session_id} : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("--- %s seconds running ---" % (time.time() - start_time))
