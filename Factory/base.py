import os
import time

from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import cv2  # import opencv-python	4.5.5.64
from Ad import Ad

from database_connector import get_last_saved_id_from_db
from locators_data import *


class MyDriver(object):

    def __init__(self, platform_name="Android", platform_version="9",
                 automation_name="UiAutomator2", app_package="com.amazon.mShop.android.shopping",
                 app_activity="com.amazon.mShop.home.HomeActivity", device_name="emulator-5554",
                 uiautomator_2_server_launch_timeout=40000, ios_install_pause=8000,
                 wda_startup_retry_interval=20000, new_command_timeout=20000, skip_device_initialization=True,
                 skip_server_installation=True, no_reset=True, normalize_tag_names=True):

        desired_caps = {
            "platformName": platform_name,
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

    @staticmethod
    def save_cropped_scr(driver, ad: Ad) -> None:
        # self.create_scr_folders_if_not_exist()
        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        if not os.path.exists(f"/nfsshare/Screenshots/{date_folder_name}"):
            os.mkdir(f"/nfsshare/Screenshots/{date_folder_name}")

        img_name = int(get_last_saved_id_from_db()) + 1

        image_path = f"/nfsshare/Screenshots/{date_folder_name}/{str(img_name)}.png"
        driver.save_screenshot(image_path)
        img = cv2.imread(image_path)

        cropped_image = img[
                        ad.location_y:ad.location_y + ad.height,
                        ad.location_x:ad.location_x + ad.width
                        ]
        cv2.imwrite(image_path, cropped_image)

    @staticmethod
    def create_scr_folders_if_not_exist():
        if not os.path.exists("/nfs/Screenshots"):
            os.makedirs("/nfs/Screenshots")

    def wait_for_element(self, by_type, path) -> None:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((by_type, path)))

    def send_text(self, by_type, path: str, text_to_send: str) -> None:
        try:
            self.wait_for_element(by_type, path)
            self.driver.find_element(by_type, path).send_keys(text_to_send)
        except (NoSuchElementException, TimeoutException):
            print('No "Search Input" field')

    # TODO change xpath for multi lang (config)
    def first_launch(self) -> None:
        """this method will be executed when the emulator had a reset or is a new one"""
        try:
            self.wait_for_element(By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel")
            self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel").click()
        except (NoSuchElementException, TimeoutException):
            pass
        time.sleep(5)
        try:
            self.wait_for_element(By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button")
            self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button").click()
        except (NoSuchElementException, TimeoutException):
            pass

    def get_page(self, phrase_to_search: str) -> None:
        """search item on the app"""
        try:
            self.driver.find_element(By.XPATH, DE.search_icon).click()
        except NoSuchElementException:
            self.driver.find_element(By.XPATH, ENG.search_icon).click()
        self.send_text(By.ID, 'com.amazon.mShop.android.shopping:id/rs_search_src_text', phrase_to_search)

        """press enter"""
        self.driver.press_keycode(66)

    def scroll_down(self) -> None:
        """scroll down through app Y"""
        try:
            self.driver.swipe(start_x=470, start_y=1100, end_x=470, end_y=500, duration=400)
        except WebDriverException:
            pass

    def config_start(self) -> None:
        # TODO change xpath for multi lang (config)
        xpath = "//*[@text='Land/Region: Vereinigte Staaten (United States)']"
        try:
            self.wait_for_element(By.XPATH, xpath)
            self.driver.find_element(By.XPATH, xpath).click()

            TouchAction(self.driver).tap(None, 500, 500, 1).perform()

            xpath_button = "//*[@text='Fertig']"
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
                for element in web_elements2:
                    print(element.text)

                web_elements2[-2].click()
            except (NoSuchElementException, IndexError):
                pass
