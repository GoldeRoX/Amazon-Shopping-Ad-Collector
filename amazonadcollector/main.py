import subprocess
import shlex
import sys
import time

from datetime import datetime

from selenium.common.exceptions import WebDriverException
from amazonadcollector.ads_logic import SQLAdManager, AdHandler
from amazonadcollector.base import MyDriver, BaseMethods, Scroll
from amazonadcollector.locators_data import DE, UK


def main(udid: int):

    sql_manager = SQLAdManager()


    pars_emulator = shlex.split(f"./emulator -avd Amazon-{udid} -gpu host -accel on -http-proxy http://{sql_manager.get_proxy_address(udid)}:{sql_manager.get_proxy_port(udid)} -port {udid}") # UK
    process_emulator = subprocess.Popen(pars_emulator, cwd="/home/krzysztof/android-sdk/emulator")

    # time to start an emulator
    time.sleep(15)

    start_time = time.time()

    try:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid))
    except WebDriverException:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid),
                           skip_device_initialization=False, skip_server_installation=False, no_reset=False)

    time.sleep(5)

    base_methods = BaseMethods(session.driver, lang=UK)
    base_methods.amazon_not_responding_close()
    base_methods.first_launch()
    base_methods.cookies_click()

    # base_methods.change_lang_from_eng_to_de()
    # base_methods.change_setting_to_uk()

    session_id = SQLAdManager().get_last_saved_session_id_from_db() + 1

    keyword = sql_manager.get_random_keyword()
    keyword_id = keyword["id"]
    new_udid = 1

    ad_handler = AdHandler(session.driver, lang=UK, session_id=session_id, keyword_id=keyword_id, udid=new_udid)

    for i in range(30):

        base_methods.get_page(keyword["keyword"])

        try:
            base_methods.amazon_not_responding_close()
            time.sleep(2)
            base_methods.cookies_click()
            time.sleep(4)

            """scroll down through app Y and collect ads"""
            scroll = Scroll(session.driver)

            is_end_of_page = False
            previous_page_source = session.driver.page_source

            ad_handler.collect_ad_type_7()  # works
            # ad_handler.collect_ad_type_9()
            # ad_handler.collect_ad_type_9_alternative()
            # ad_handler.collect_ad_type_10()

            while not is_end_of_page:
                base_methods.amazon_not_responding_close()
                base_methods.cookies_click()

                ad_handler.collect_video_ad()  # works
                ad_handler.collect_ad_type_5()  # works
                ad_handler.collect_ad_type_2()
                ad_handler.collect_ad_type_2_alt()
                # ad_handler.collect_ad_type_8()

                scroll.scroll_down()

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
