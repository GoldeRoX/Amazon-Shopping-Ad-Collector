import os
import time

from appium import webdriver  # import Appium-Python-Client 2.2.0
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import cv2  # import opencv-python	4.5.5.64
from Factory.Ad import Ad

from Factory.database_connector import get_last_saved_id_from_db


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

        # self.driver = webdriver.Remote("http://85.214.87.200:3128/wd/hub", desired_caps)
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)


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


def wait_for_element(driver, by_type, path) -> None:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((by_type, path)))


def send_text(driver, by_type, path: str, text_to_send: str) -> None:
    try:
        wait_for_element(driver, by_type, path)
        driver.find_element(by_type, path).send_keys(text_to_send)
    except (NoSuchElementException, TimeoutException):
        print("No such Input field")


# TODO create logic, that will NOT wait 10s in case of not locating elements

def first_launch(driver) -> None:
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel")))
        driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel").click()
    except (NoSuchElementException, TimeoutException):
        pass
    time.sleep(5)
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button")))
        driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button").click()
    except (NoSuchElementException, TimeoutException):
        pass
