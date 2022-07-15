import os
import time

from appium import webdriver  # import Appium-Python-Client 2.2.0
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import cv2  # import opencv-python	4.5.5.64
from Ad import Ad

from database_connector import get_last_saved_id_from_db
from locators_data import LocatorsData


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
        # self.driver = webdriver.Remote("http://149.154.159.160:3128/wd/hub", desired_caps)
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    @staticmethod
    def save_cropped_scr(driver, ad: Ad) -> None:
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

    def wait_for_element(self, by_type, path) -> None:
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((by_type, path)))

    def send_text(self, by_type, path: str, text_to_send: str) -> None:
        try:
            self.wait_for_element(by_type, path)
            self.driver.find_element(by_type, path).send_keys(text_to_send)
        except (NoSuchElementException, TimeoutException):
            print("No such Input field")

    # TODO refactor this method
    def first_launch(self) -> None:
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
        """search item"""
        self.driver.find_element(By.XPATH, LocatorsData.search_icon_ENG).click()
        self.send_text(By.ID, LocatorsData.search_input_ENG, phrase_to_search)

        """press enter"""
        self.driver.press_keycode(66)

    # TODO implement that tactic
    """
    could query the current list of visible elements in between each swipe, 
    then compare the current list against the last list. If the list is the same, 
    the swipe had no effect, and app is at the bottom
    """

    def scroll_down(self) -> None:
        """scroll down through app Y"""
        try:
            self.driver.swipe(start_x=470, start_y=1100, end_x=470, end_y=500, duration=400)
        except WebDriverException:
            pass

    def is_bottom(self) -> bool:
        end_of_page = False
        previous_page_source = self.driver.page_source

        while not end_of_page:
            self.scroll_down()
            end_of_page = previous_page_source == self.driver.page_source
            previous_page_source = self.driver.page_source
        return True
