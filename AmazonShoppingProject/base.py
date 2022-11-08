import logging
import os
import time

import yaml
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver import WebElement
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import cv2  # import opencv-python	4.5.5.64
from AmazonShoppingProject.Ad import Ad

from AmazonShoppingProject.locators_data import *


class MyDriver(object):

    def __init__(self, platform_name="Android", platform_version="9",
                 automation_name="UiAutomator2", app_package="com.amazon.mShop.android.shopping",
                 app_activity="com.amazon.mShop.home.HomeActivity", device_name="emulator-5554",
                 uiautomator_2_server_launch_timeout=40000, ios_install_pause=8000,
                 wda_startup_retry_interval=20000, new_command_timeout=20000, skip_device_initialization=True,
                 skip_server_installation=True, no_reset=True, normalize_tag_names=True, udid="emulator-5554"):

        desired_caps = {
            "platformName": platform_name,
            "udid": udid,
            "appium:platformVersion": platform_version,
            "appium:automationName": automation_name,
            "appium:appPackage": app_package,
            "appium:appActivity": app_activity,
            "appium:deviceName": device_name,
            "uiautomator2ServerLaunchTimeout": uiautomator_2_server_launch_timeout,
            "iosInstallPause": ios_install_pause,
            "wdaStartupRetryInterval": wda_startup_retry_interval,
            "newCommandTimeout": new_command_timeout,
            "skipDeviceInitialization": skip_device_initialization,
            "skipServerInstallation": skip_server_installation,
            "noReset": no_reset,
            "normalizeTagNames": normalize_tag_names
        }
        self.driver = webdriver.Remote(command_executor="http://localhost:4723/wd/hub",
                                       desired_capabilities=desired_caps)

    def wait_for_element(self, by_type, path: str, time_to_wait: int = 5) -> None:
        WebDriverWait(self.driver, time_to_wait).until(
            EC.presence_of_element_located((by_type, path)))

    def send_text(self, by_type, path: str, text_to_send: str) -> None:
        try:
            self.wait_for_element(by_type, path)
            self.driver.find_element(by_type, path).send_keys(text_to_send)
        except (NoSuchElementException, TimeoutException):
            print('No "Search Input" field')

    def first_launch(self) -> None:
        """this method will be executed when the emulator had a reset or is a new one"""
        try:
            self.wait_for_element(By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel")
            self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel").click()
        except (NoSuchElementException, TimeoutException):
            pass
        try:
            self.wait_for_element(By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button")
            self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button").click()
        except (NoSuchElementException, TimeoutException):
            pass

    def change_lang_if_must(self):
        self.wait_for_element(By.XPATH,
                              '//android.widget.ImageView[@content-desc="Menu. Contains your orders, your account, '
                              'shop by department, programs and features, settings, and customer service Tab 4 of 4"]')
        self.driver.find_element(By.XPATH,
                                 '//android.widget.ImageView[@content-desc="Menu. Contains your orders, your account, '
                                 'shop by department, programs and features, settings, '
                                 'and customer service Tab 4 of 4"]').click()

    def get_page(self, phrase_to_search: str) -> None:
        """search item phrase on the app"""
        try:
            self.wait_for_element(By.XPATH, DE.search_icon, time_to_wait=30)
            self.driver.find_element(By.XPATH, DE.search_icon).click()
        except (NoSuchElementException, TimeoutException):
            try:
                self.wait_for_element(By.XPATH, ENG.search_icon)
                self.driver.find_element(By.XPATH, ENG.search_icon).click()
            except (NoSuchElementException, TimeoutException):
                self.wait_for_element(By.ID, "com.amazon.mShop.android.shopping:id/chrome_action_bar_search_icon")
                self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/chrome_action_bar_search_icon")

        self.send_text(By.ID, 'com.amazon.mShop.android.shopping:id/rs_search_src_text', phrase_to_search)

        """press enter"""
        self.driver.press_keycode(66)

    def amazon_not_responding_close(self):
        try:
            close = self.driver.find_elements(By.ID, "android:id/aerr_close")
            close[0].click()
        except IndexError:
            pass

    def scroll_down(self, y: int = 600) -> None:
        """scroll down through app Y axis
        *default value is y=600
        """
        try:
            self.driver.swipe(start_x=10, start_y=1100, end_x=10, end_y=1100 - y, duration=400)
        except WebDriverException:
            pass

    def config_start(self) -> None:
        # TODO change xpath for multi lang (config)
        xpath = "//*[@text='Land/Region: Vereinigte Staaten (United States)']"
        try:
            self.wait_for_element(By.XPATH, xpath, time_to_wait=15)
            self.driver.find_element(By.XPATH, xpath).click()
            time.sleep(4)
            TouchAction(self.driver).tap(None, 500, 500, 1).perform()
            # TODO change xpath for multi lang (config)
            xpath_button = "//*[@text='Fertig']"
            self.wait_for_element(By.XPATH, xpath_button, time_to_wait=8)
            self.driver.find_element(By.XPATH, xpath_button).click()
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            pass

    def cookies_click(self) -> None:
        try:
            xpath = "//*[@text='Cookies akzeptieren']"
            self.driver.find_element(By.XPATH, xpath).click()

        except NoSuchElementException:
            try:
                web_elements2 = self.driver.find_elements(By.XPATH, "//*[starts-with(@text, 'Cookie')]")

                web_elements2[-2].click()
            except (NoSuchElementException, IndexError, WebDriverException):
                pass

    def change_lang_from_eng_to_de(self):
        is_settings_in_use = False
        try:
            xpath_menu = '//android.widget.ImageView[@content-desc="Menu. Contains your orders, ' \
                         'your account, shop by department, programs and features, settings, and' \
                         ' customer service Tab 4 of 4"]'
            self.wait_for_element(By.XPATH, xpath_menu, time_to_wait=15)
            self.driver.find_element(By.XPATH, xpath_menu).click()
            is_settings_in_use = True
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            pass

        if is_settings_in_use:
            try:
                self.standard_config1()
            except WebDriverException:
                try:
                    self.standard_config2()
                except WebDriverException:
                    pass

    def standard_config2(self):
        try:
            # in case of a wrong currency ($) and correct lang

            xpath_prime = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/' \
                          'android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/' \
                          'android.widget.FrameLayout/android.widget.ViewSwitcher/android.widget.FrameLayout/' \
                          'android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/' \
                          'android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/' \
                          'android.view.ViewGroup[1]/android.view.ViewGroup/' \
                          'android.view.ViewGroup[2]/android.widget.TextView'

            self.wait_for_element(By.XPATH, xpath_prime, time_to_wait=60)
            prime = self.driver.find_element(By.XPATH, xpath_prime)

            if prime.get_attribute("text") == "Prime":
                is_end_of_page = False
                previous_page_source = self.driver.page_source
                while not is_end_of_page:
                    self.scroll_down()
                    is_end_of_page = previous_page_source == self.driver.page_source
                    previous_page_source = self.driver.page_source

                xpath_settings = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/' \
                                 'android.widget.FrameLayout/' \
                                 'android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/' \
                                 'android.widget.ViewSwitcher/android.widget.FrameLayout/android.view.ViewGroup/' \
                                 'android.widget.ScrollView/android.view.ViewGroup/android.widget.ScrollView/' \
                                 'android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/' \
                                 'android.view.ViewGroup/android.widget.Button'
                self.wait_for_element(By.XPATH, xpath_settings)
                self.driver.find_element(By.XPATH, xpath_settings).click()

                xpath_land_und_sprache = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/' \
                                         'android.widget.FrameLayout/android.view.ViewGroup/' \
                                         'android.widget.FrameLayout[2]/android.widget.FrameLayout/' \
                                         'android.widget.ViewSwitcher/android.widget.FrameLayout/' \
                                         'android.view.ViewGroup/android.widget.ScrollView/' \
                                         'android.view.ViewGroup/android.widget.ScrollView/' \
                                         'android.view.ViewGroup/android.view.ViewGroup[1]/' \
                                         'android.view.ViewGroup/android.view.ViewGroup/' \
                                         'android.view.ViewGroup/android.view.View[1]'
                self.wait_for_element(By.XPATH, xpath_land_und_sprache, time_to_wait=30)
                self.driver.find_element(By.XPATH, xpath_land_und_sprache).click()

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            self.standard_config1()

    def standard_config1(self):
        xpath_setting_bar = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/' \
                            'android.widget.FrameLayout/' \
                            'android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/' \
                            'android.widget.ViewSwitcher/android.widget.FrameLayout/android.view.ViewGroup/' \
                            'android.widget.ScrollView/android.view.ViewGroup/android.widget.ScrollView/' \
                            'android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/' \
                            'android.view.ViewGroup/android.widget.Button'
        self.wait_for_element(By.XPATH, xpath_setting_bar, time_to_wait=60)
        self.driver.find_element(By.XPATH, xpath_setting_bar).click()

        xpath_country_and_language = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/' \
                                     'android.widget.FrameLayout/' \
                                     'android.view.ViewGroup/android.widget.FrameLayout[' \
                                     '2]/android.widget.FrameLayout/' \
                                     'android.widget.ViewSwitcher/android.widget.FrameLayout/' \
                                     'android.view.ViewGroup/' \
                                     'android.widget.ScrollView/android.view.ViewGroup/' \
                                     'android.widget.ScrollView/' \
                                     'android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/' \
                                     'android.view.ViewGroup/android.view.ViewGroup/android.view.View[' \
                                     '1]'
        self.wait_for_element(By.XPATH, xpath_country_and_language, time_to_wait=60)
        self.driver.find_element(By.XPATH, xpath_country_and_language).click()

        country_region = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/' \
                         'android.widget.FrameLayout/' \
                         'android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/' \
                         'android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/' \
                         'android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/' \
                         'android.view.View[11]/android.view.View[1]/android.widget.Button'
        self.wait_for_element(By.XPATH, country_region, time_to_wait=30)
        country_and_region_button = self.driver.find_element(By.XPATH, country_region)
        country_and_region_button.click()

        try:
            self.wait_for_element(MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                                  "android.widget.FrameLayout/android.view.ViewGroup/"
                                                  "android.widget.FrameLayout[2]/android.widget.FrameLayout/"
                                                  "android.widget.RelativeLayout/android.widget.RelativeLayout/"
                                                  "android.webkit.WebView/android.webkit.WebView/android.view.View[1]/"
                                                  "android.view.View/android.view.View[7]/"
                                                  "android.widget.RadioButton[5]", time_to_wait=60)
            webElement_region_germany = self.driver.find_element(MobileBy.XPATH,
                                                                 "/hierarchy/android.widget.FrameLayout/"
                                                                 "android.widget.LinearLayout/"
                                                                 "android.widget.FrameLayout/"
                                                                 "android.view.ViewGroup/"
                                                                 "android.widget.FrameLayout[2]/"
                                                                 "android.widget.FrameLayout/"
                                                                 "android.widget.RelativeLayout/"
                                                                 "android.widget.RelativeLayout/"
                                                                 "android.webkit.WebView/"
                                                                 "android.webkit.WebView/"
                                                                 "android.view.View[1]/"
                                                                 "android.view.View/"
                                                                 "android.view.View[7]/"
                                                                 "android.widget.RadioButton[5]")
            webElement_region_germany.click()

        except WebDriverException:
            # TODO change to logs
            print("ERROR in the country/regions button settings (stage 1)!")

        xpath_language = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget' \
                         '.FrameLayout/' \
                         'android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/' \
                         'android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/' \
                         'android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/' \
                         'android.view.View[14]/android.view.View[1]/android.widget.Button'
        self.wait_for_element(MobileBy.XPATH, xpath_language, time_to_wait=60)
        language_button = self.driver.find_element(MobileBy.XPATH, xpath_language)
        language_button.click()

        """xpath_lang = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/' \
                     'android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/' \
                     'android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/' \
                     'android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/' \
                     'android.view.View[7]/android.widget.RadioButton[1]'"""

        xpath_lang = "//*[starts-with(@text,'German Deutsch')]"

        self.wait_for_element(MobileBy.XPATH, xpath_lang, time_to_wait=60)
        language_button: WebElement = self.driver.find_element(MobileBy.XPATH, xpath_lang)

        language_button.click()

        xpath_currency = '/hierarchy/android.widget.FrameLayout/' \
                         'android.widget.LinearLayout/android.widget.FrameLayout/' \
                         'android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/' \
                         'android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/' \
                         'android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View/' \
                         'android.view.View[17]/android.view.View[1]/android.widget.Button'
        self.wait_for_element(By.XPATH, xpath_currency, time_to_wait=60)
        currency_button = self.driver.find_element(By.XPATH, xpath_currency)
        if currency_button.get_attribute("text") == "€ - EUR - Euro":
            pass
        elif currency_button.get_attribute("text") == "Währung: $ - USD - US-Dollar":
            currency_button.click()

            self.wait_for_element(MobileBy.XPATH, "//*[starts-with(@text,'€ - EUR - Euro')]")
            webelement_currency_euro = self.driver.find_element(MobileBy.XPATH,
                                                                "//*[starts-with(@text,'€ - EUR - Euro')]")
            webelement_currency_euro.click()

        self.wait_for_element(MobileBy.XPATH, "//*[starts-with(@text,'Fertig')]")
        accept_button = self.driver.find_element(MobileBy.XPATH, "//*[starts-with(@text,'Fertig')]")
        accept_button.click()


def save_cropped_scr(driver, ad: Ad, filename: str) -> None:
    with open("../data/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    date_folder_name = datetime.now().strftime("%Y-%m-%d")

    path = config["COMPUTER"]["SAVE_PATH"]
    if not os.path.exists(f"{path}/{date_folder_name}"):
        os.mkdir(f"{path}/{date_folder_name}")

    img_name = filename

    image_path = f"{path}/{date_folder_name}/{str(img_name)}.png"
    driver.save_screenshot(image_path)
    img = cv2.imread(image_path)

    cropped_image = img[
                    ad.location_y:ad.location_y + ad.height,
                    ad.location_x:ad.location_x + ad.width
                    ]
    try:
        cv2.imwrite(image_path, cropped_image)
    except cv2.error:
        pass
