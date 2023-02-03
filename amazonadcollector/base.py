import os
import time

import yaml
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, \
    StaleElementReferenceException
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import cv2  # import opencv-python	4.5.5.64
from amazonadcollector.Ad import Ad

from amazonadcollector.locators_data import *


class MyDriver(object):
    # new android 12.0 and model Pixel 4a

    """"platformName": "Android",
    "appium:platformVersion": "12",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.amazon.mShop.android.shopping",
    "appium:appActivity": "com.amazon.mShop.home.HomeActivity",
    "appium:deviceName": "emulator-5554",
    "uiautomator2ServerLaunchTimeout": 40000,
    "iosInstallPause": 8000,
    "wdaStartupRetryInterval": 200000,
    "newCommandTimeout": 20000,
    "skipDeviceInitialization": true,
    "skipServerInstallation": true,
    "noReset": true,
    "normalizeTagNames": true"""

    def __init__(self, platform_name="Android", platform_version="12",
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
            "normalizeTagNames": normalize_tag_names,
            "app": os.path.join(os.path.dirname(__file__),
                                "../amazon_apk/com.amazon.mShop.android.shopping_26.1.2.100.apk")
        }
        self.driver = webdriver.Remote(command_executor="http://localhost:4723/wd/hub",
                                       desired_capabilities=desired_caps)


class BaseMethods(object):

    def __init__(self, driver):
        self.driver: WebDriver = driver

    def get_element_when_located(self, by_type, path: str, time_to_wait: int = 5) -> WebElement:
        return WebDriverWait(self.driver, time_to_wait).until(
            EC.presence_of_element_located((by_type, path)))

    def send_text(self, by_type, path: str, text_to_send: str) -> None:
        try:
            self.get_element_when_located(by_type, path).send_keys(text_to_send)
        except (NoSuchElementException, TimeoutException):
            print('No "Search Input" field')

    def first_launch(self) -> None:
        """this method will be executed when the emulator had a reset or is a new one"""
        try:
            self.get_element_when_located(AppiumBy.ID, "com.amazon.mShop.android.shopping:id/btn_cancel").click()
        except (NoSuchElementException, TimeoutException):
            pass
        try:
            self.get_element_when_located(AppiumBy.ID,
                                          "com.amazon.mShop.android.shopping:id/skip_sign_in_button").click()
        except (NoSuchElementException, TimeoutException):
            pass

    def change_lang_if_must(self):
        self.get_element_when_located(AppiumBy.XPATH,
                                      '//android.widget.ImageView[@content-desc='
                                      '"Menu. Contains your orders, your account, '
                                      'shop by department, programs and features, settings,'
                                      ' and customer service Tab 4 of 4"]').click()

    def get_page(self, phrase_to_search: str) -> None:
        """search item phrase on the app"""
        try:
            self.get_element_when_located(AppiumBy.XPATH, DE.search_icon, time_to_wait=30).click()
        except (NoSuchElementException, TimeoutException):
            try:
                self.get_element_when_located(AppiumBy.XPATH, ENG.search_icon)
                self.driver.find_element(AppiumBy.XPATH, ENG.search_icon).click()
            except (NoSuchElementException, TimeoutException):
                self.get_element_when_located(AppiumBy.ID,
                                              "com.amazon.mShop.android.shopping:id/"
                                              "chrome_action_bar_search_icon").click()

        self.send_text(AppiumBy.ID, 'com.amazon.mShop.android.shopping:id/rs_search_src_text', phrase_to_search)

        """press enter"""
        self.driver.press_keycode(66)

    def amazon_not_responding_close(self):
        try:
            close = self.driver.find_elements(AppiumBy.ID, "android:id/aerr_close")
            close[0].click()
        except (IndexError, WebDriverException):
            pass

    def scroll_down(self, y: int = 600) -> None:
        """scroll down through app Y axis
        *default value is y=600
        """
        try:
            self.driver.swipe(start_x=0, start_y=1100, end_x=0, end_y=1100 - y, duration=400)
        except WebDriverException:
            pass

    def config_start(self) -> None:
        # TODO change xpath for multi lang (config)
        xpath = "//*[@text='Land/Region: Vereinigte Staaten (United States)']"
        try:
            self.get_element_when_located(AppiumBy.XPATH, xpath, time_to_wait=15).click()
            time.sleep(4)
            TouchAction(self.driver).tap(None, 500, 500, 1).perform()
            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Fertig']", time_to_wait=8).click()
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            pass

    def cookies_click(self) -> None:
        try:
            xpath = "//*[@text='Cookies akzeptieren']"
            self.driver.find_element(AppiumBy.XPATH, xpath).click()

        except NoSuchElementException:
            try:
                web_elements2 = self.driver.find_elements(AppiumBy.XPATH, "//*[starts-with(@text, 'Cookie')]")

                web_elements2[-2].click()
            except (NoSuchElementException, IndexError, WebDriverException):
                pass

    def change_lang_from_eng_to_de(self):
        try:
            self.get_element_when_located(AppiumBy.XPATH, '//android.widget.ImageView[@content-desc='
                                                          '"Menu. Contains your orders, your account,'
                                                          ' shop by department, programs and features,'
                                                          ' settings, and customer service Tab 4 of 4"]', 15).click()

            try:
                self.get_element_when_located(AppiumBy.XPATH,
                                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                              "android.widget.FrameLayout/android.view.ViewGroup/"
                                              "android.widget.FrameLayout[2]/android.widget.FrameLayout/"
                                              "android.widget.ViewSwitcher/android.widget.FrameLayout/"
                                              "android.view.ViewGroup/android.widget.ScrollView/"
                                              "android.view.ViewGroup/android.widget.ScrollView/"
                                              "android.view.ViewGroup/android.view.ViewGroup[2]/"
                                              "android.view.ViewGroup/android.view.ViewGroup/"
                                              "android.widget.Button", 20).click()

                self.get_element_when_located(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/"
                                                              "android.widget.LinearLayout/android.widget.FrameLayout/"
                                                              "android.view.ViewGroup/android.widget.FrameLayout[2]/"
                                                              "android.widget.FrameLayout/android.widget.ViewSwitcher/"
                                                              "android.widget.FrameLayout/android.view.ViewGroup/"
                                                              "android.widget.ScrollView/android.view.ViewGroup/"
                                                              "android.widget.ScrollView/android.view.ViewGroup/"
                                                              "android.view.ViewGroup[2]/android.view.ViewGroup/"
                                                              "android.view.ViewGroup/android.view.ViewGroup/"
                                                              "android.view.View[1]/android.view.ViewGroup/"
                                                              "android.widget.TextView", 10).click()
            except Exception as e:
                self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Settings']").click()
                self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Country & Language']").click()

            time.sleep(5)
            self.get_element_when_located(AppiumBy.XPATH, "//*[starts-with(@text, 'Country/Region:')]").click()
            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Germany (Deutschland)']").click()

            try:
                self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Language: English']").click()
                self.get_element_when_located(AppiumBy.XPATH, "//*[@text='German']").click()
            except NoSuchElementException:
                self.driver.find_element(AppiumBy.XPATH, "//*[starts-with(@text, 'Sprache:')]").click()
                self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Deutsch']").click()

            self.get_element_when_located(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/"
                                                          "android.widget.LinearLayout/android.widget.FrameLayout/"
                                                          "android.view.ViewGroup/android.widget.FrameLayout[2]/"
                                                          "android.widget.FrameLayout/android.widget.RelativeLayout/"
                                                          "android.widget.RelativeLayout/android.webkit.WebView/"
                                                          "android.webkit.WebView/android.view.View/android.view.View/"
                                                          "android.view.View/android.view.View[10]/"
                                                          "android.widget.Button").click()
            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='€ - EUR - Euro']", 5).click()

            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Fertig']", 5).click()

            time.sleep(20)

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            pass


def save_cropped_scr(driver, ad: Ad, filename: str) -> None:
    PATH = os.path.join(os.path.dirname(__file__), "../data/config.yaml")
    with open(PATH, "r") as file:
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
