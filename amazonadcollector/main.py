import subprocess
import shlex
import sys
import time

from datetime import datetime

from selenium.common.exceptions import WebDriverException
from amazonadcollector.ads_logic import SQLAdManager, AdFactory
from amazonadcollector.base import MyDriver, BaseMethods, Scroll
from amazonadcollector.locators_data import Lang


def main(udid: int):

    sql_manager = SQLAdManager()

    pars_emulator = shlex.split(f"./emulator -avd Amazon-{udid} -gpu host -accel on -http-proxy http://{sql_manager.get_proxy_address(udid).strip()}:{int(sql_manager.get_proxy_port(udid))} -port {udid}")
    process_emulator = subprocess.Popen(pars_emulator, cwd="/home/krzysztof/android-sdk/emulator")

    # time to cold boot emulator
    time.sleep(15)

    start_time = time.time()

    try:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid))
    except WebDriverException:
        session = MyDriver(udid="emulator-" + str(udid), device_name="emulator-" + str(udid),
                           skip_device_initialization=False, skip_server_installation=False, no_reset=False)

    # time to start app
    time.sleep(5)

    base_methods = BaseMethods(session.driver)
    base_methods.amazon_not_responding_close()
    base_methods.first_launch()
    base_methods.cookies_click()

    base_methods.config_app_settings()

    new_udid = 1

    ad_factory = AdFactory(session.driver, sql_ad_manager=sql_manager, udid=new_udid)
    scroll = Scroll(session.driver)

    for i in range(30):

        base_methods.get_page("Laptops")
        # Apple
        # base_methods.get_page(keyword["keyword"])

        base_methods.amazon_not_responding_close()
        time.sleep(2)
        base_methods.cookies_click()
        time.sleep(4)

        try:
            is_end_of_page = False
            previous_page_source = session.driver.page_source

            ad_factory.create_and_save_top_ads()

            while not is_end_of_page:
                base_methods.amazon_not_responding_close()
                base_methods.cookies_click()

                ad_factory.create_and_save_mid_ads()

                scroll.scroll_down()

                is_end_of_page = previous_page_source == session.driver.page_source
                previous_page_source = session.driver.page_source

        except KeyboardInterrupt:
            print("KeyboardInterrupt exception")
            sys.exit()
        finally:
            session.driver.quit()
            process_emulator.terminate()
            print(f"end of session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("--- %s seconds running ---" % (time.time() - start_time))
