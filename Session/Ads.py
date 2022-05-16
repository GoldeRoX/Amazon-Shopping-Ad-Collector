import os.path
import time
from traceback import print_stack

import cv2  # import opencv-python	4.5.5.64
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException, \
    ElementNotSelectableException
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from BaseAd import *

from database_connector import get_last_saved_id_from_db
from database_connector import send_data_to_db

class Bottom_ad():

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def is_element_present_with_xpath(self, xpath, time_to_wait):
        try:
            WebDriverWait(self.driver, time_to_wait).until(EC.presence_of_element_located(
                (By.XPATH,
                 xpath)))
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def find_all_bot_ads(self, elements_collection):
        ad = []
        for x in elements_collection:
            elements = x.find_elements(By.XPATH, ".//*[@class='android.view.View']")
            for element in elements:
                if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
                    ad.append(element)
        return ad

    def save_data_from_ad(self, ads):
        ads_meta_data = []
        for element in ads:
            """informacje do bazy danych"""
            width = element.size["width"]
            height = element.size["height"]
            location_x = element.location["x"]
            location_y = element.location["y"]
            text = element.get_attribute("text")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = (self.driver.current_activity + timestamp).replace(".", "_")

            ads_meta_data.append([filename, width, height, location_x, location_y, text, timestamp])
        return ads_meta_data

    def save_croped_scr(self, object_to_save) -> None:

        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        if not os.path.exists(f"../Screenshots/{date_folder_name}"):
            os.mkdir(f"../Screenshots/{date_folder_name}")

        img_name = int(get_last_saved_id_from_db())+1

        image_path = f"../Screenshots/{date_folder_name}/{str(img_name)}.png"
        self.driver.save_screenshot(image_path)
        img = cv2.imread(image_path)

        cropped_image = img[
                        object_to_save.location["y"]:object_to_save.location["y"] + object_to_save.size[
                            "height"],
                        object_to_save.location["x"]:object_to_save.location["x"] + object_to_save.size[
                            "width"]]
        cv2.imwrite(image_path, cropped_image)

    def send_data_to_db(self, ads_meta_data) -> None:
        for ad in ads_meta_data:
            send_data_to_db(ad[0], ad[1], ad[2], ad[3], ad[4], ad[5], ad[6], 1)

    def run_script(self):

        global sponsored_ads
        if self.is_element_present_with_xpath("//*[@text='Sponsored']/parent::*", 10):
            sponsored_ads = self.driver.find_elements(By.XPATH, "//*[@text='Sponsored']/parent::*")
        ads =self.find_all_bot_ads(sponsored_ads)
        self.save_data_from_ad(ads)


