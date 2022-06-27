import os.path
import random
import time
from datetime import datetime
import cv2  # import opencv-python	4.5.5.64

from threading import Lock
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium import webdriver  # import Appium-Python-Client 2.2.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Factory.locators_data import LocatorsData
from Factory.database_connector import get_last_saved_id_from_db

from Ad import Ad

from base import Base

"""class WebDriverMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class WebDriver(metaclass=WebDriverMeta):
    # TODO dac parametry jako atrybuty osobne
    def __init__(self):
        __desired_caps = {
            "platformName": "Android",
            "appium:platformVersion": "9",
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": "com.amazon.mShop.android.shopping",
            "appium:appActivity": "com.amazon.mShop.home.HomeActivity",
            "appium:deviceName": "emulator-5554",
            "uiautomator2ServerLaunchTimeout": "40000",
            "iosInstallPause": "8000",
            "wdaStartupRetryInterval": "20000",
            "newCommandTimeout": "20000",
            "skipDeviceInitialization": "True",
            "skipServerInstallation": "True",
            "noReset": "True"
        }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", __desired_caps)"""


class Search(object):

    driver = Base().driver

    def save_cropped_scr(self, object_to_save) -> None:
        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        if not os.path.exists(f"../Screenshots/{date_folder_name}"):
            os.mkdir(f"../Screenshots/{date_folder_name}")

        img_name = int(get_last_saved_id_from_db()) + 1

        image_path = f"../Screenshots/{date_folder_name}/{str(img_name)}.png"
        self.driver.save_screenshot(image_path)
        img = cv2.imread(image_path)

        cropped_image = img[
                        object_to_save.location["y"]:object_to_save.location["y"] + object_to_save.size[
                            "height"],
                        object_to_save.location["x"]:object_to_save.location["x"] + object_to_save.size[
                            "width"]]
        cv2.imwrite(image_path, cropped_image)

    def click_element(self, by_type, path: str, time_to_wait=5) -> None:
        try:
            WebDriverWait(self.driver, time_to_wait).until(
                EC.presence_of_element_located((by_type, path)))
            self.driver.find_element(by_type, path).click()
        except (NoSuchElementException, TimeoutException):
            pass

    def send_text(self, by_type, path: str, text_to_send: str) -> None:
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((by_type, path)))
            self.driver.find_element(by_type, path).send_keys(text_to_send)
        except (NoSuchElementException, TimeoutException):
            print("No such Input field")

    """def first_launch(self) -> None:
        time.sleep(3)
        if self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel").is_displayed():
            Search.click_element(self, By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel")
        if self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button").is_displayed():
            Search.click_element(self, By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button")"""

    def set_up(self, phrase_to_search: str) -> None:
        """search item"""
        Search.click_element(self, By.XPATH, LocatorsData.search_icon)

        Search.send_text(self, By.ID, LocatorsData.search_input, phrase_to_search)

        """press enter"""
        self.driver.press_keycode(66)

        """scroll through app Y"""
        for i in range(16):
            try:
                self.driver.swipe(470, 1100, 470, 50, 400)
                time.sleep(1)
            except:
                pass

    def bottom_ad(self) -> None:

        try:
            element = self.driver.find_element(By.XPATH, LocatorsData.BOTTOM_AD)

            if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
                """create an object of ad"""
                ad = Ad(element, 1)
                self.save_cropped_scr(element)
                ad.send_to_db()

        except NoSuchElementException:
            pass

    def execute_ad_2(self) -> None:
        try:
            element_node = self.driver.find_element(By.XPATH, LocatorsData.brands_related_to_your_search_element_node)
            elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")
            ads = []
            for x in range(len(elements)):
                if elements[x].get_attribute("clickable") == "true" and elements[x].get_attribute("text").startswith("Sponsored ad from"):
                    ads.append(elements[x])

            for x in range(len(ads)):
                element = ads[x]
                try:
                    """create an object of ad"""
                    ad = Ad(element, 2)

                    self.save_cropped_scr(element)
                    ad.send_to_db()
                    # TODO zmodyfikowac tym sposobem scroll
                    """scroll through ads"""
                    """first_ad = ads[x]
                    print(f" z {x} = {element}")
                    next_ad = ads[x+1]
                    print(f"do {x+1} = {ads[x+1]}")
                    self.driver.scroll(first_ad, next_ad)"""

                    """scroll through ads"""
                    action = TouchAction(self.driver)
                    action.press(element).move_to(x=-element.size["width"] / 2, y=0).release().perform()

                except Exception as e:
                    print(f'Exception occurred : {e}')

        except (NoSuchElementException, TimeoutException):
            pass


if __name__ == "__main__":
    while True:
        try:
            Amazon = Search()
            list_of_brands = ["Oculus", "Hp", "Laptops", "Monitors"]
            Amazon.set_up(list_of_brands[random.randint(0, len(list_of_brands) - 1)])
            Amazon.bottom_ad()
            Amazon.execute_ad_2()
        except Exception as e:
            print(e)
