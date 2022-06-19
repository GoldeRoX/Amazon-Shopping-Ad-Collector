import os.path
import random
import time
from datetime import datetime
import cv2  # import opencv-python	4.5.5.64

from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium import webdriver  # import Appium-Python-Client 2.2.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Factory.database_connector import get_last_saved_id_from_db

from AdFactory import BrandsRelatedToYourSearch, BottomAd, IAd


class Search(object):

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

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", __desired_caps)

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

    def set_up(self, phrase_to_search: str) -> None:

        time.sleep(3)
        Search.click_element(self, By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel")
        time.sleep(3)
        Search.click_element(self, By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button")
        time.sleep(1)

        """search item"""
        Search.click_element(self, By.XPATH, '(//android.widget.LinearLayout[@content-desc="Search"])[1]'
                                             '/android.widget.LinearLayout/android.widget.TextView')

        Search.send_text(self, By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text", phrase_to_search)

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
            element = self.driver.find_element(By.XPATH, "//*[@text='Leave feedback on Sponsored ad']"
                                                         "/parent::*/following-sibling::*/child::*")

            if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
                """create an object of ad"""
                ad: IAd
                ad = BottomAd(element)
                self.save_cropped_scr(element)
                ad.send_to_db()
        except NoSuchElementException:
            pass

    def execute_ad_2(self) -> None:
        try:
            element_node = self.driver.find_element(By.XPATH,
                                                    "//*[contains(@text, 'Brands related to your search')]/parent::*")
            elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")

            for x in range(len(elements)):
                element = elements[x]
                if element.get_attribute("clickable") == "true":
                    try:
                        """create an object of ad"""
                        ad: IAd
                        ad = BrandsRelatedToYourSearch(element)

                        self.save_cropped_scr(element)
                        ad.send_to_db()

                        """scroll through ads"""
                        action = TouchAction(self.driver)
                        action.press(element).move_to(x=-element.size["width"] / 2, y=0).release().perform()

                    except Exception as e:
                        print(f'Exception occurred : {e}')

        except (NoSuchElementException, TimeoutException):
            pass


if __name__ == "__main__":
    Amazon = Search()
    Amazon.set_up("Oculus")
    Amazon.bottom_ad()
    Amazon.execute_ad_2()
    while True:
        try:
            Amazon = Search()
            list_of_brands = ["Oculus", "Hp", "Laptops", "Monitors"]
            Amazon.set_up(list_of_brands[random.randint(0, len(list_of_brands)-1)])
            Amazon.bottom_ad()
            Amazon.execute_ad_2()
            time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(3)
