import os

from appium import webdriver  # import Appium-Python-Client 2.2.0
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
                 uiautomator_2_server_launch_timeout="40000", ios_install_pause="8000",
                 wda_startup_retry_interval="20000", new_command_timeout="20000", skip_device_initialization="True",
                 skip_server_installation="True", no_reset="True"):
        __desired_caps = {
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
            "noReset": no_reset
        }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", __desired_caps)


def save_cropped_scr(driver, ad) -> None:
    date_folder_name = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(f"/nfsshare/Screenshots/{date_folder_name}"):
        os.mkdir(f"/nfsshare/Screenshots/{date_folder_name}")

    img_name = int(get_last_saved_id_from_db()) + 1

    image_path = f"/nfsshare/Screenshots/{date_folder_name}/{str(img_name)}.png"
    driver.save_screenshot(image_path)
    img = cv2.imread(image_path)

    """cropped_image = img[
                    ad.location_y:ad.location_y + ad.height,
                    ad.location_x:ad.location_x + ad.width]"""

    cropped_image = img[
                    ad.location["y"]:ad.location["y"] + ad.size["height"],
                    ad.location["x"]:ad.location["x"] + ad.size["width"]]
    cv2.imwrite(image_path, cropped_image)


def click_element(driver, by_type, path: str, time_to_wait=5) -> None:
    try:
        WebDriverWait(driver, time_to_wait).until(
            EC.presence_of_element_located((by_type, path)))
        driver.find_element(by_type, path).click()
    except (NoSuchElementException, TimeoutException):
        pass


def send_text(driver, by_type, path: str, text_to_send: str) -> None:
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((by_type, path)))
        driver.find_element(by_type, path).send_keys(text_to_send)
    except (NoSuchElementException, TimeoutException):
        print("No such Input field")


"""def first_launch(self) -> None:
    time.sleep(3)
    if self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel").is_displayed():
        Search.click_element(self, By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel")
    if self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button").is_displayed():
        Search.click_element(self, By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button")"""