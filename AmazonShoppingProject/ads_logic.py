import base64
import math
import os
import time

import cv2
import yaml
from datetime import datetime
from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, \
    InvalidElementStateException, WebDriverException
from selenium.webdriver.common.by import By

from Ad import Ad
from base import save_cropped_scr
from database_connector import SQLAdManager


class AdHandler(object):

    def __init__(self, driver, lang):
        self.driver: WebDriver = driver
        self.ad_text_filter = []
        self.lang = lang

    @staticmethod
    def save_ad(driver, session_id: int, ad: Ad):
        Manager = SQLAdManager()
        Manager.send_data_to_db(ad.width, ad.height, ad.location_x, ad.location_y, ad.text, ad.timestamp,
                                ad.ad_type, session_id)
        save_cropped_scr(driver, ad, str(Manager.get_last_saved_id_from_db()))

    def collect_ad_type_1(self, session_id: int) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            ads_list = self.collect_ads_1()
            for ad in ads_list:
                print("collecting ad \033[1;31;40mtype 1\033[0;0m ...")
                self.save_ad(self.driver, session_id, ad)
                if ad.text.strip() is not None:
                    self.ad_text_filter.append(ad.text)
                print("ad \033[1;31;40mtype 1\033[0;0m \033[1;32;40mcollected\033[0;0m")
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
            pass

    def get_webelements_ads_2(self) -> [WebElement]:
        element_node = self.driver.find_element(By.XPATH, self.lang.brands_related_to_your_search_element_node)
        elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")
        webelements = []
        for element in elements:
            if element.get_attribute("clickable") == "true" and element.get_attribute("text").startswith(
                    self.lang.ad_2_starts_with):
                webelements.append(element)
        return webelements

    def collect_ad_type_2(self, session_id: int) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            ads_webelements = self.get_webelements_ads_2()
            action = TouchAction(self.driver)
            for i, web_element in enumerate(ads_webelements):
                """scroll through web_elements ads"""
                print("collecting ad \033[1;31;40mtype 2\033[0;0m ...")
                if i == 0:
                    pass
                else:
                    action.press(ads_webelements[i]).move_to(ads_webelements[i - 1]).wait(ms=2000).release().perform()
                    time.sleep(2)

                """create an object of ad"""
                if web_element.get_attribute("text") not in self.ad_text_filter:
                    ad = Ad(web_element, 2)
                    self.save_ad(self.driver, session_id, ad)
                    print("ad \033[1;31;40mtype 2\033[0;0m \033[1;32;40mcollected\033[0;0m")
                    if ad.text.strip() is not None:
                        self.ad_text_filter.append(ad.text)
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
            pass

    def get_webelements_ads_1(self) -> [WebElement]:
        webelements = []
        elements = self.driver.find_elements(By.XPATH, self.lang.BOTTOM_AD)

        for element in elements:
            text_element_node = self.driver.find_element(By.XPATH, self.lang.BOTTOM_AD_TEXT_ELEMENT)
            if element.size["height"] > 300 and text_element_node.size["width"] > 500:
                webelements.append(element)
        return webelements

    def collect_ads_1(self) -> [Ad]:
        ads = []
        webelements = self.get_webelements_ads_1()

        for webElement in webelements:
            """create an object of ad"""
            ad = Ad(webElement, 1)
            ads.append(ad)
        return ads

    def collect_ads_2(self) -> [Ad]:
        ads = []
        ads_webelements = self.get_webelements_ads_2()
        for web_element in ads_webelements:
            """create an object of ad"""
            ad = Ad(web_element, 2)
            ads.append(ad)
        return ads

    def get_webelements_ads_4(self) -> [WebElement]:
        try:
            elements = self.driver.find_elements(By.XPATH, self.lang.ad_4_node)
            return elements
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return []

    def get_webelements_ads_5(self) -> [WebElement]:
        try:
            elements = self.driver.find_elements(By.XPATH, self.lang.ad_5_node)
            return elements
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            return []

    def collect_ad_type_4(self, session_id: int):
        """Create, send to DB and save scr of ad"""
        try:
            ads_webelements = self.get_webelements_ads_4()
            for element in ads_webelements:
                if element.size["height"] > 50:
                    action = TouchAction(self.driver)
                    for i, web_element in enumerate(ads_webelements):
                        path = ".//child::*" + 3 * "/following-sibling::*"
                        text = web_element.find_element(By.XPATH, path).get_attribute("text")
                        if text not in self.ad_text_filter and text != "product-detail":
                            """scroll through web_elements ads"""
                            print("collecting ad \033[1;31;40mtype 4\033[0;0m ...")
                            if i == 0:
                                AdjustAd(self.driver).match_ad_visibility(element)
                            else:
                                par = (ads_webelements[i].size["width"] - ads_webelements[i].size["width"] / 2)
                                action.press(ads_webelements[i]).move_to(ads_webelements[i - 1], x=par, y=0).wait(
                                    ms=2000).release().perform()
                                AdjustAd(self.driver).match_ad_visibility(element)
                            """create an object of ad"""
                            ad = Ad(web_element, 4)
                            ad.text = text
                            if ad.width > 300 and ad.height > 300:
                                self.save_ad(self.driver, session_id, ad)
                                print("ad \033[1;31;40mtype 4\033[0;0m \033[1;32;40mcollected\033[0;0m")
                                if ad.text is not None:
                                    self.ad_text_filter.append(ad.text)
                    break
        except (NoSuchElementException, TimeoutException, WebDriverException,
                StaleElementReferenceException, InvalidElementStateException):
            pass

    def collect_ad_type_5(self, session_id: int):
        """Create, send to DB and save scr of ad"""
        try:
            ads_webelements = self.get_webelements_ads_5()
            for webElement in ads_webelements:
                if webElement.size["height"] > 10:
                    elements = webElement.find_elements(By.XPATH, ".//*[@class='android.view.View']")
                    result_text = elements[4].get_attribute("text")
                    var1 = result_text.startswith(self.lang.ad_5_starts_with)
                    var2 = elements[7].get_attribute("text") == "product-detail"
                    if var1 and var2 and result_text not in self.ad_text_filter:
                        """create ad object"""
                        AdjustAd(self.driver).match_ad_visibility(webElement)
                        print("collecting ad \033[1;31;40mtype 5\033[0;0m ...")
                        ad = Ad(webElement, 5)
                        ad.text = result_text
                        self.save_ad(self.driver, session_id, ad)
                        print("ad \033[1;31;40mtype 5\033[0;0m \033[1;32;40mcollected\033[0;0m")
                        if ad.text is not None:
                            self.ad_text_filter.append(ad.text)

        except (
                NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException,
                IndexError):
            pass

    def save_cropped_scr_for_videos(self, ad: Ad, filename: str) -> None:
        with open("../data/config.yaml", "r") as file:
            config = yaml.safe_load(file)
        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        path = config["COMPUTER"]["SAVE_PATH"]
        if not os.path.exists(f"{path}/{date_folder_name}"):
            os.mkdir(f"{path}/{date_folder_name}")

        img_name = filename

        image_path = f"{path}/{date_folder_name}/{str(img_name)}_thumb.png"
        self.driver.save_screenshot(image_path)
        img = cv2.imread(image_path)

        cropped_image = img[
                        ad.location_y:ad.location_y + ad.height,
                        ad.location_x:ad.location_x + ad.width
                        ]

        cv2.imwrite(image_path, cropped_image)

        image_path = f"{path}/{date_folder_name}/{str(img_name)}.png"
        video_element_ad_web_element = self.driver.find_element(By.XPATH, self.lang.ad_video)
        path = ".//child::*/following-sibling::*"
        video_element = video_element_ad_web_element.find_element(By.XPATH, path)
        self.driver.save_screenshot(image_path)
        new_img = cv2.imread(image_path)

        test = cv2.rectangle(new_img, (video_element.location["x"], video_element.location["y"]),
                             (video_element.location["x"]+video_element.size["width"],
                              video_element.location["y"]+video_element.size["height"]), (0, 0, 0), -1)
        cropped_image = test[
                        ad.location_y:ad.location_y + ad.height,
                        ad.location_x:ad.location_x + ad.width
                        ]

        try:
            cv2.imwrite(image_path, cropped_image)
        except cv2.error:
            pass

    def create_and_crop_video(self, video_ad_web_element: WebElement, db_id: int):
        with open("../data/config.yaml", "r") as file:
            config = yaml.safe_load(file)
        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        path = config["COMPUTER"]["SAVE_PATH"]
        if not os.path.exists(f"{path}/{date_folder_name}"):
            os.mkdir(f"{path}/{date_folder_name}")
        self.driver.start_recording_screen()
        time.sleep(60)
        video_rawdata = self.driver.stop_recording_screen()
        video_name = str(db_id)
        filepath = os.path.join(f"{path}/{date_folder_name}", "test_" + video_name + ".mp4")

        with open(filepath, "wb+") as vd:
            vd.write(base64.b64decode(video_rawdata))

        os.system(
            f'ffmpeg -i {path}/{date_folder_name}/test_{video_name}.mp4 -vf "crop={video_ad_web_element.size["width"]}:'
            f'{video_ad_web_element.size["height"]}:{video_ad_web_element.location["x"]}:'
            f'{video_ad_web_element.location["y"]}" {path}/{date_folder_name}/{video_name}.mp4')
        os.system(f"unlink {path}/{date_folder_name}/test_{video_name}.mp4")

    def collect_video_ad(self, session_id: int):
        """Collecting video, scr and modified scr for ad of type 6 - video_ad"""
        try:
            video_ad_web_element = self.driver.find_element(By.XPATH, self.lang.ad_video)
            if video_ad_web_element.size["height"] > 10:
                print("adjusting video ad ...")
                AdjustAd(self.driver).match_ad_visibility(video_ad_web_element)

                path = ".//child::*" + 7 * "/following-sibling::*"
                text = video_ad_web_element.find_element(By.XPATH, path).get_attribute("text")

                if text not in self.ad_text_filter:
                    """create ad object"""
                    print("collecting ad \033[1;31;40mvideo type 6\033[0;0m ...")
                    ad = Ad(video_ad_web_element, 6)
                    ad.text = text

                    Manager = SQLAdManager()
                    Manager.send_data_to_db(ad.width, ad.height, ad.location_x, ad.location_y, ad.text, ad.timestamp,
                                            ad.ad_type, session_id)

                    self.save_cropped_scr_for_videos(ad, str(Manager.get_last_saved_id_from_db()))
                    self.ad_text_filter.append(video_ad_web_element.id)
                    self.create_and_crop_video(video_ad_web_element, Manager.data_set_id)
                    print("ad \033[1;31;40mvideo\033[0;0m \033[1;32;40mcollected\033[0;0m")
                    if ad.text is not None:
                        self.ad_text_filter.append(ad.text)

        except (NoSuchElementException, TimeoutException, StaleElementReferenceException, WebDriverException):
            pass


class AdjustAd(object):

    def __init__(self, driver):
        self.driver = driver

    # samsung s20
    # TODO remake and repair match_ad_visibility(). It must adjust with windowed architecture of the site
    def match_ad_visibility(self, web_element: WebElement):
        if web_element.size["height"] > 10 and web_element.size["width"] > 10:
            previous_height: int = web_element.size["height"]
            self.driver.swipe(start_x=10, start_y=1100, end_x=10, end_y=1000, duration=400)
            next_height: int = web_element.size["height"]

            while True:

                if math.isclose(previous_height, next_height, abs_tol=1) and web_element.size["height"] > 100:
                    return

                if next_height > previous_height:
                    """case if element is on the bottom"""
                    previous_height = web_element.size["height"]
                    self.driver.swipe(start_x=10, start_y=1100, end_x=10, end_y=1000, duration=400)
                    next_height = web_element.size["height"]

                else:
                    """case if element is on the top"""
                    previous_height = web_element.size["height"]
                    self.driver.swipe(start_x=10, start_y=1000, end_x=10, end_y=1500, duration=400)
                    next_height = web_element.size["height"]
