import base64
import math
import os
import time

import cv2
import yaml
from datetime import datetime
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from amazonadcollector.Ad import Ad
from amazonadcollector.base import save_cropped_scr, Scroll
from amazonadcollector.database_connector import SQLAdManager


class AdHandler(object):

    def __init__(self, driver, lang):
        self.driver: WebDriver = driver
        self.scroll = Scroll(self.driver)
        self.ad_text_filter = []
        self.lang = lang

    def save_ad(self, session_id: int, ad: Ad, keyword_id, udid: int) -> None:
        Manager = SQLAdManager()
        Manager.send_data_to_db(ad.width, ad.height, ad.location_x, ad.location_y, ad.text, ad.timestamp,
                                ad.ad_type, session_id, keyword_id, udid)
        save_cropped_scr(self.driver, ad, str(Manager.get_last_saved_id_from_db()))

    def collect_ad_type_1(self, session_id: int, keyword_id: int, udid: int) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            ads_list: [Ad] = self.collect_ads_1()
            for ad in ads_list:
                print("collecting ad \033[1;31;40mtype 1\033[0;0m ...")
                self.save_ad(session_id, ad, keyword_id, udid)
                if ad.text.strip() is not None:
                    self.ad_text_filter.append(ad.text)
                print("ad \033[1;31;40mtype 1\033[0;0m \033[1;32;40mcollected\033[0;0m")
        except WebDriverException:
            pass

    def get_webelements_ads_2(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.brands_related_to_your_search_element_node)

    def get_webelements_ads_7(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_7)

    def collect_ad_type_2(self, session_id: int, keyword_id: int, udid: int) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            webelements: list[WebElement] = [element for element in self.get_webelements_ads_2()
                                             if element.size["height"] > 10
                                             for web_element in
                                             element.find_elements(AppiumBy.XPATH, ".//*[@class='android.view.View']")
                                             if web_element.get_attribute("clickable") == "true"
                                             and web_element.get_attribute("text").startswith(
                                             self.lang.ad_2_starts_with)
                                             and web_element.get_attribute("text") not in self.ad_text_filter]

            for index, web_element in enumerate(webelements):
                """scroll through web_elements ads"""
                print("collecting ad \033[1;31;40mtype 2\033[0;0m ...")
                if index == 0:
                    print(webelements)
                    print("adjusting ad type 2 ...")
                    AdjustAd(self.driver).match_ad_visibility(webelements[0])
                else:
                    action = TouchAction(self.driver)
                    # self.scroll.press_and_move_to_location(start_location=[])
                    action.press(webelements[index]) \
                        .move_to(webelements[index - 1]) \
                        .wait(ms=2000) \
                        .release() \
                        .perform()
                    time.sleep(2.5)

                """create an object of ad"""
                if web_element.get_attribute("text") not in self.ad_text_filter:
                    ad = Ad(web_element, 2)
                    self.save_ad(session_id, ad, keyword_id, udid)
                    print("ad \033[1;31;40mtype 2\033[0;0m \033[1;32;40mcollected\033[0;0m")
                    if ad.text.strip() is not None:
                        self.ad_text_filter.append(ad.text)
        except (NoSuchElementException, IndexError):
            return

    def collect_ad_type_7(self, session_id: int, keyword_id: int, udid: int) -> None:
        """Create, send data to DB and save scr of ad"""
        ads_webelements = self.get_webelements_ads_7()
        for webElement in ads_webelements:
            if webElement.size["height"] > 10 and webElement.get_attribute("resource-id") != "search":
                result_text: str = self.driver.find_element(AppiumBy.XPATH, "//*[starts-with(@text, 'Gesponserte "
                                                                            "Werbeanzeige von')]").get_attribute("text")
                """create ad object"""
                print("collecting ad \033[1;31;40mtype 7\033[0;0m ...")
                ad = Ad(webElement, 7)
                ad.text = result_text
                self.save_ad(session_id, ad, keyword_id, udid)
                print("ad \033[1;31;40mtype 7\033[0;0m \033[1;32;40mcollected\033[0;0m")
                if ad.text is not None:
                    self.ad_text_filter.append(ad.text)
                return

    def get_webelements_ads_10(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_10)

    def collect_ad_type_10(self, session_id: int, keyword_id: int, udid: int) -> None:
        """Create, send data to DB and save scr of ad"""
        ads_webelements = self.get_webelements_ads_10()
        for webElement in ads_webelements:
            if webElement.size["height"] > 10 and webElement.get_attribute("resource-id") != "search":
                elements: [WebElement] = webElement.find_elements(AppiumBy.XPATH, "//*[@class='android.view.View']")

                result_text: str = elements[2].get_attribute("content-desc")
                valid: str = elements[len(elements) - 1].get_attribute("content-desc")

                if valid.__contains__("Jetzt"):
                    """create ad object"""
                    print("collecting ad \033[1;31;40mtype 10\033[0;0m ...")
                    ad = Ad(webElement, 7)
                    ad.text = result_text
                    self.save_ad(session_id, ad, keyword_id, udid)
                    print("ad \033[1;31;40mtype 10\033[0;0m \033[1;32;40mcollected\033[0;0m")
            else:
                return

    def get_webelements_ads_8(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_8)

    def collect_ad_type_8(self, session_id: int, keyword_id: int, udid: int) -> None:
        """Create ad type 8 | the same type of ad type 7 (type 7 is only for TOP presenting),
        send to DB and save scr of ad"""

        print("start type_8")
        ads_webelements = self.get_webelements_ads_8()
        for webElement in ads_webelements:

            result_text: str = webElement.get_attribute('content-desc')
            print(result_text)

            element_1_gesponsert: WebElement = webElement.find_element(AppiumBy.XPATH,
                                                                       ".//following-sibling::*/following-sibling::*")
            element_1_gesponsert_text: str = element_1_gesponsert.get_attribute("text")
            print(element_1_gesponsert_text)

            element_2_Jetzt_einkaufen: WebElement = element_1_gesponsert.find_element(
                ".//following-sibling::*/following-sibling::*/child::*/following-sibling::*/child::*")
            element_2_Jetzt_einkaufen_text: str = element_2_Jetzt_einkaufen.get_attribute('content-desc')
            print(element_2_Jetzt_einkaufen_text)

            if webElement.size["height"] > 10 and result_text not in self.ad_text_filter:

                """create ad object"""
                print("collecting ad \033[1;31;40mtype 7\033[0;0m ...")
                ad = Ad(webElement, 7)
                ad.text = result_text
                self.save_ad(session_id, ad, keyword_id, udid)
                print("ad \033[1;31;40mtype 7\033[0;0m \033[1;32;40mcollected\033[0;0m")
                if ad.text is not None:
                    self.ad_text_filter.append(ad.text)

    def get_webelements_ads_8_alt(self):
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_8_alt)

    def get_webelements_ads_9(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_9)

    def collect_ad_type_9(self, session_id: int, keyword_id: int, udid: int) -> None:
        """Create ad type 9 | the same type of ad type 7 (type 7 is only for TOP presenting),
        send to DB and save scr of ad"""

        ads_webelements: [WebElement] = self.get_webelements_ads_9()
        for webElement in ads_webelements:
            if webElement.size["height"] > 40:

                elements: [WebElement] = webElement.find_elements(AppiumBy.XPATH, "//*[@class='android.view.View']")

                try:
                    result_text: str = elements[1].get_attribute("text")
                    element_with_gesponsert: str = elements[1].get_attribute("text").strip()
                    element_wit_Jetzt_einkaufen: str = elements[7].get_attribute("text").strip()
                except IndexError:
                    return

                element_with_gesponsert_validation: bool = element_with_gesponsert.__contains__("Gesponsert")
                element_wit_Jetzt_einkaufen_validation: bool = element_wit_Jetzt_einkaufen.startswith("Jetzt")

                if result_text not in self.ad_text_filter \
                        and element_with_gesponsert_validation \
                        and element_wit_Jetzt_einkaufen_validation:

                    """create ad object"""
                    print("collecting ad \033[1;31;40mtype 9\033[0;0m ...")
                    ad = Ad(webElement, 7)
                    ad.text = result_text
                    self.save_ad(session_id, ad, keyword_id, udid)
                    print("ad \033[1;31;40mtype 9\033[0;0m \033[1;32;40mcollected\033[0;0m")
                    if ad.text is not None:
                        self.ad_text_filter.append(ad.text)
                    return

    def get_webelements_ads_9_alt(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_9_alt)

    def collect_ad_type_9_alternative(self, session_id: int, keyword_id: int, udid: int) -> None:
        """Create ad type 9 | the same type of ad type 7 (type 7 is only for TOP presenting),
        send to DB and save scr of ad"""

        ads_webelements: [WebElement] = self.get_webelements_ads_9_alt()
        for webElement in ads_webelements:
            if webElement.size["height"] > 40:

                elements: list[WebElement] = webElement.find_elements(AppiumBy.XPATH, "//*[@class='android.view.View']")

                try:
                    result_text: str = elements[1].get_attribute("content-desc")
                    element_with_gesponsert: str = elements[1].get_attribute("content-desc").strip()
                    element_wit_Jetzt_einkaufen: str = elements[4].get_attribute("content-desc").strip()
                except IndexError:
                    return

                element_with_gesponsert_validation: bool = element_with_gesponsert.__contains__("Gesponsert")
                element_wit_Jetzt_einkaufen_validation: bool = element_wit_Jetzt_einkaufen.startswith("Jetzt")

                if result_text not in self.ad_text_filter \
                        and element_with_gesponsert_validation \
                        and element_wit_Jetzt_einkaufen_validation:

                    """create ad object"""
                    print("collecting ad \033[1;31;40mtype 9_alt\033[0;0m ...")
                    ad = Ad(webElement, 7)
                    ad.text = result_text
                    self.save_ad(session_id, ad, keyword_id, udid)
                    print("ad \033[1;31;40mtype 9_alt\033[0;0m \033[1;32;40mcollected\033[0;0m")
                    if ad.text is not None:
                        self.ad_text_filter.append(ad.text)
                    return

    def get_webelements_ads_1(self) -> [WebElement]:
        webelements = []
        elements = self.driver.find_elements(AppiumBy.XPATH, self.lang.BOTTOM_AD)

        for element in elements:
            text_element_node = self.driver.find_element(AppiumBy.XPATH, self.lang.BOTTOM_AD_TEXT_ELEMENT)
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
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_4_node)

    def get_webelements_ads_5(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_5_node)

    def collect_ad_type_5(self, session_id: int, keyword_id: int, udid: int) -> None:
        """
        Collect and save ad of type 5 with the given session, keyword, and user device IDs.
        """
        try:
            ad_elements: list[WebElement] = self.get_webelements_ads_5()
            for ad_element in ad_elements:
                if ad_element.size["height"] <= 10:
                    continue

                text_elements: list[WebElement] = ad_element.find_elements(AppiumBy.XPATH,
                                                                           ".//*[@class='android.view.View']")
                if len(text_elements) < 8:
                    continue

                result_text: str = text_elements[4].get_attribute("text")
                if not result_text.startswith(self.lang.ad_5_starts_with):
                    continue

                if text_elements[7].get_attribute("text") != "product-detail":
                    continue

                if result_text in self.ad_text_filter:
                    continue

                print("Adjusting ad type 5...")
                AdjustAd(self.driver).match_ad_visibility(ad_element)
                print("Collecting ad type 5...")
                ad = Ad(ad_element, 5)
                ad.text = result_text
                self.save_ad(session_id, ad, keyword_id, udid)
                self.ad_text_filter.append(ad.text)
                print("Ad type 5 collected.")
        except (NoSuchElementException, IndexError):
            pass

    def save_cropped_scr_for_videos(self, ad: Ad, filename: str) -> None:
        PATH: str = os.path.join(os.path.dirname(__file__), "../data/config.yaml")
        with open(PATH, "r") as file:
            config = yaml.safe_load(file)
        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        path = config["COMPUTER"]["SAVE_PATH"]
        if not os.path.exists(f"{path}/{date_folder_name}"):
            os.mkdir(f"{path}/{date_folder_name}")

        img_name = filename

        image_path: str = f"{path}/{date_folder_name}/{str(img_name)}_thumb.png"
        self.driver.save_screenshot(image_path)
        img = cv2.imread(image_path)

        cropped_image = img[
                        ad.location_y:ad.location_y + ad.height,
                        ad.location_x:ad.location_x + ad.width
                        ]

        cv2.imwrite(image_path, cropped_image)

        image_path = f"{path}/{date_folder_name}/{str(img_name)}.png"
        video_element_ad_web_element = self.driver.find_element(AppiumBy.XPATH, self.lang.ad_video)
        path = ".//child::*/following-sibling::*"
        video_element = video_element_ad_web_element.find_element(AppiumBy.XPATH, path)
        self.driver.save_screenshot(image_path)
        new_img = cv2.imread(image_path)

        test = cv2.rectangle(new_img, (video_element.location["x"], video_element.location["y"]),
                             (video_element.location["x"] + video_element.size["width"],
                              video_element.location["y"] + video_element.size["height"]), (0, 0, 0), -1)
        cropped_image = test[
                        ad.location_y:ad.location_y + ad.height,
                        ad.location_x:ad.location_x + ad.width
                        ]

        try:
            cv2.imwrite(image_path, cropped_image)
        except cv2.error:
            pass

    def create_and_crop_video(self, video_ad_web_element: WebElement, db_id: int):

        PATH = os.path.join(os.path.dirname(__file__), "../data/config.yaml")
        with open(PATH, "r") as file:
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

    def collect_video_ad(self, session_id: int, keyword_id: int, udid: int):
        """Collecting video, scr and modified scr for ad of type 6 - video_ad"""
        try:
            video_ad_web_element = self.driver.find_element(AppiumBy.XPATH, self.lang.ad_video)
            path: str = ".//child::*" + 7 * "/following-sibling::*"
            text: str = video_ad_web_element.find_element(AppiumBy.XPATH, path).get_attribute("text")
            if video_ad_web_element.size["height"] > 10 and text not in self.ad_text_filter:

                print("adjusting video ad ...")
                AdjustAd(self.driver).match_ad_visibility(video_ad_web_element)

                """create ad object"""
                print("collecting ad \033[1;31;40mvideo type 6\033[0;0m ...")
                ad = Ad(video_ad_web_element, 6)
                ad.text = text

                Manager = SQLAdManager()
                Manager.send_data_to_db(ad.width, ad.height, ad.location_x, ad.location_y, ad.text, ad.timestamp,
                                        ad.ad_type, session_id, keyword_id, udid)

                self.save_cropped_scr_for_videos(ad, str(Manager.get_last_saved_id_from_db()))

                if ad.text is not None:
                    self.ad_text_filter.append(ad.text)
                """In case of error in recording screen, save ad info and continue"""

                self.create_and_crop_video(video_ad_web_element, Manager.data_set_id)
                print("ad \033[1;31;40mvideo\033[0;0m \033[1;32;40mcollected\033[0;0m")

        except NoSuchElementException:
            pass

    def collect_video_ad_alternative(self, session_id: int, keyword_id: int, udid: int):
        """Collecting video, scr and modified scr for ad of type 6 - video_ad"""
        try:
            video_ad_web_element = self.driver.find_element(AppiumBy.XPATH, self.lang.ad_video)

            path: str = ".//child::*" + 7 * "/following-sibling::*"
            text: str = video_ad_web_element.find_element(AppiumBy.XPATH, path).get_attribute("text")
            if video_ad_web_element.size["height"] > 10 and text not in self.ad_text_filter:

                print("adjusting video ad ...")
                AdjustAd(self.driver).match_ad_visibility(video_ad_web_element)

                """create ad object"""
                print("collecting ad \033[1;31;40mvideo type 6\033[0;0m ...")
                ad = Ad(video_ad_web_element, 6)
                ad.text = text

                Manager = SQLAdManager()
                Manager.send_data_to_db(ad.width, ad.height, ad.location_x, ad.location_y, ad.text, ad.timestamp,
                                        ad.ad_type, session_id, keyword_id, udid)

                self.save_cropped_scr_for_videos(ad, str(Manager.get_last_saved_id_from_db()))

                if ad.text is not None:
                    self.ad_text_filter.append(ad.text)
                """In case of error in recording screen, save ad info and continue"""

                self.create_and_crop_video(video_ad_web_element, Manager.data_set_id)
                print("ad \033[1;31;40mvideo\033[0;0m \033[1;32;40mcollected\033[0;0m")

        except NoSuchElementException:
            pass


class AdjustAd(object):

    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.scroll = Scroll(self.driver)
        self.test_element = self.driver.find_element(AppiumBy.XPATH,
                                        "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/"
                                        "android.widget.FrameLayout/android.view.ViewGroup/"
                                        "android.widget.FrameLayout[2]/android.widget.FrameLayout/"
                                        "android.widget.RelativeLayout/android.widget.RelativeLayout/"
                                        "android.webkit.WebView/android.webkit.WebView/android.view.View[1]/"
                                        "android.view.View")

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

    def match_ad_visibility_test(self, web_element: WebElement):
        if web_element.size["height"] > 10 and web_element.size["width"] > 10:
            previous_height: int = web_element.size["height"]
            self.scroll.press_and_move_to_location(start_location=(10, 1100), end_location=(10, 1000))
            # self.driver.swipe(start_x=10, start_y=1100, end_x=10, end_y=1000, duration=400)
            next_height: int = web_element.size["height"]

            wait = WebDriverWait(self.driver, timeout=30)

            while True:
                if math.isclose(previous_height, next_height, abs_tol=1) and web_element.size["height"] > 100:
                    return

                if next_height > previous_height:
                    """case if element is on the bottom"""
                    previous_height = web_element.size["height"]
                    self.scroll.press_and_move_to_location(start_location=(10, 1100), end_location=(10, 1000))
                    # self.driver.swipe(start_x=10, start_y=1100, end_x=10, end_y=1000, duration=400)
                    next_height = web_element.size["height"]

                else:
                    """case if element is on the top"""
                    previous_height = web_element.size["height"]
                    self.scroll.press_and_move_to_location(start_location=(10, 1000), end_location=(10, 1500))
                    # self.driver.swipe(start_x=10, start_y=1000, end_x=10, end_y=1500, duration=400)
                    next_height = web_element.size["height"]

                # Wait for the element to become visible
                wait.until(EC.visibility_of_element_located((AppiumBy.ID, web_element.id)))

    def is_fully_visible(self, element: WebElement) -> bool:
        # Get the element's location and size
        location = element.location
        size = element.size

        # Get the size of the viewport
        viewport_size = self.driver.get_window_size()

        # Calculate the position and size of the viewport in the coordinate system of the element
        viewport_position = self.driver.get_window_rect()
        viewport_position['x'] = location['x'] + viewport_size['width'] / 2
        viewport_size_in_element = {
            'width': viewport_size['width'],
            'height': viewport_size['height'] - viewport_position['y']
        }

        # Check if the viewport is fully contained within the element
        return (location['x'] <= viewport_position['x']
                and location['y'] <= viewport_position['y']
                and location['x'] + size['width'] >= viewport_position['x'] + viewport_size_in_element['width']
                and location['y'] + size['height'] >= viewport_position['y'] + viewport_size_in_element['height'])

    def custom_scroll_to_element(self, target_element: WebElement) -> None:
        # Get the size of the viewport
        viewport_size = self.driver.get_window_size()

        # Get the location and size of the target element
        target_location = target_element.location
        target_size = target_element.size

        # Calculate the center point of the target element
        target_center = {
            'x': target_location['x'] + target_size['width'] / 2,
            'y': target_location['y'] + target_size['height'] / 2
        }

        # Calculate the destination point for the scroll action
        destination = {
            'x': target_center['x'],
            'y': target_center['y'] - viewport_size['height'] / 3
        }

        # Create a TouchAction instance and perform the scroll action
        actions = TouchAction(self.driver)
        actions.press(x=viewport_size['width'] / 2, y=viewport_size['height'] - 1)
        actions.wait(200)
        actions.move_to(x=destination['x'], y=destination['y'])
        actions.release()
        actions.perform()

        # Wait until the target element is visible
        WebDriverWait(self.driver, 10).until(EC.visibility_of(target_element))
