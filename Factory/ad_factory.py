import os.path
import time
from datetime import datetime
import cv2  # import opencv-python	4.5.5.64

from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium import webdriver  # import Appium-Python-Client 2.2.0
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Session.database_connector import get_last_saved_id_from_db
from Session.database_connector import send_data_to_db

from BrandsRelatedToYourSearch import BrandsRelatedToYourSearch


class Search(object):

    def __init__(self):
        appium_desc = {
            "platformName": "Android",
            "appium:platformVersion": "9",
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": "com.amazon.mShop.android.shopping",
            "appium:appActivity": "com.amazon.mShop.home.HomeActivity",
            "appium:deviceName": "emulator-5554"
        }
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", appium_desc)

    def save_croped_scr(self, object_to_save) -> None:
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

    def click_element(self, by_type, path: str, time_to_wait=10) -> None:
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

        Search.click_element(self, By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel")
        Search.click_element(self, By.ID, "com.amazon.mShop.android.shopping:id/skip_sign_in_button")
        time.sleep(1)

        """search item"""
        Search.click_element(self, By.XPATH, '(//android.widget.LinearLayout[@content-desc="Search"])[1]'
                                             '/android.widget.LinearLayout/android.widget.TextView')

        Search.send_text(self, By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text", phrase_to_search)

        """press enter"""
        self.driver.press_keycode(66)

        """scroll through app Y"""
        for i in range(14):
            try:
                self.driver.swipe(470, 1100, 470, 50, 400)
                time.sleep(1)
            except:
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
                        """informacje do bazy danych"""
                        width = element.size["width"]
                        height = element.size["height"]
                        location_x = element.location["x"]
                        location_y = element.location["y"]
                        text = element.get_attribute("text")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        filename = str(get_last_saved_id_from_db() + 1) + ".png"

                        """create an object of ad"""
                        ad = BrandsRelatedToYourSearch(filename, width, height, location_x, location_y, text, timestamp)

                        self.save_croped_scr(element)
                        send_data_to_db(ad.filename, ad.width, ad.height, ad.location_x,
                                        ad.location_y, ad.text, ad.timestamp, 2)

                        """scroll through ads"""
                        action = TouchAction(self.driver)
                        action.press(element).move_to(x=-element.size["width"] / 2, y=0).release().perform()

                    except Exception as e:
                        print(f'Excepion occured : {e}')

        except (NoSuchElementException, TimeoutException):
            pass


if __name__ == "__main__":
    bottomAd = Search()
    bottomAd.set_up("Oculus set")
    bottomAd.execute_ad_2()
    bottomAd.driver.close_app()
