import base64
import math
import os
import time
import cv2
import yaml

from datetime import datetime
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from amazonadcollector.Ad import Ad, SearchedProductSponsoredBrandTop, SearchedProductAd, SearchedProductAdVideo, \
    SearchedAdBottomBanner, BrandsRelatedToYourSearch, SearchedProductSponsoredBrandMid
from amazonadcollector.base import Scroll
from amazonadcollector.database_connector import SQLAdManager


class AdFactory(object):

    def __init__(self, driver: WebDriver, lang, session_id: int, keyword_id: int, udid: int):
        self.dict_of_ads_top: {WebElement: int} = {}
        self.dict_of_ads_mid: {WebElement: int} = {}
        self.driver = driver
        self.lang = lang
        self.session_id = session_id
        self.keyword_id = keyword_id
        self.udid = udid
        self.ad_collector = AdCollector(self.driver, self.lang)
        self.ad_handler = AdHandler(self.driver, self.lang, self.session_id, self.keyword_id, self.udid)

    def collect_ads_top(self) -> {WebElement: int}:
        self.dict_of_ads_top.clear()

        for ad in self.ad_collector.get_webelements_ads_1():
            self.dict_of_ads_top.update({ad: 1})

        for ad in self.ad_collector.get_webelements_ads_7():
            self.dict_of_ads_top.update({ad: 7})

        return self.dict_of_ads_top

    def collect_ads_mid(self) -> {WebElement: int}:
        self.dict_of_ads_mid.clear()

        for ad in self.ad_collector.get_webelements_ads_2():
            self.dict_of_ads_mid.update({ad: 2})

        for ad in self.ad_collector.get_webelements_ads_2_alt():
            self.dict_of_ads_mid.update({ad: 2})

        for ad in self.ad_collector.get_webelements_ads_7():
            self.dict_of_ads_mid.update({ad: 3})

        """for ad in self.ad_collector.get_webelements_ads_4():
            print(ad)
            self.dict_of_ads_mid.update({ad: 4})"""

        for ad in self.ad_collector.get_webelements_ads_5():
            self.dict_of_ads_mid.update({ad: 5})

        for ad in self.ad_collector.get_webelements_ads_6():
            self.dict_of_ads_mid.update({ad: 6})

        for ad in self.ad_collector.get_webelements_ads_1():
            self.dict_of_ads_mid.update({ad: 8})

        return self.dict_of_ads_mid

    def create_and_save_top_ads(self) -> None:
        """
        Creates and saves an Ad object from top sector of app
        based on the type of advertisement element passed to it.
        """
        self.collect_ads_top()

        for web_element, ad_type in self.dict_of_ads_top.items():
            match ad_type:
                case 1:
                    self.ad_handler.collect_ad_type_1(web_element)
                case 7:
                    self.ad_handler.collect_ad_type_7(web_element)
                case _:
                    raise ValueError(f"Invalid ad type '{ad_type}'")

    def create_and_save_mid_ads(self) -> None:
        """
        Creates and saves an Ad object from middle sector of app
        based on the type of advertisement element passed to it.
        """
        self.collect_ads_mid()

        for web_element, ad_type in self.dict_of_ads_mid.items():
            match ad_type:
                case 2:
                    self.ad_handler.collect_ad_type_2(web_element)
                case 3:
                    self.ad_handler.collect_ad_type_3(web_element)
                # case 4:
                # self.ad_handler.collect_ad_type_4(web_element)
                case 5:
                    self.ad_handler.collect_ad_type_5(web_element)
                case 6:
                    self.ad_handler.collect_video_ad()
                case 8:
                    self.ad_handler.collect_ad_type_8(web_element)
                case _:
                    raise ValueError(f"Invalid ad type '{ad_type}'")


class AdCollector(object):
    def __init__(self, driver: WebDriver, lang):
        self.driver = driver
        self.lang = lang

    def get_webelements_ads_1(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_1)

    def get_webelements_ads_2(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.brands_related_to_your_search_element_node)

    def get_webelements_ads_2_alt(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.Items_related_to_your_search_element_node)

    """def get_webelements_ads_4(self) -> [WebElement]:
        element = self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_4_locator)
        print(element)
        return element"""

    def get_webelements_ads_5(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_5_node)

    def get_webelements_ads_7(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_7)

    def get_webelements_ads_8(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_8)

    def get_webelements_ads_8_alt(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_8_alt)

    def get_webelements_ads_9(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_9)

    def get_webelements_ads_6(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_video)

    def get_webelements_ads_9_alt(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_9_alt)

    def get_webelements_ads_10(self) -> [WebElement]:
        return self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_10)


class AdHandler(object):
    def __init__(self, driver: WebDriver, lang, session_id: int, keyword_id: int, udid: int):
        self.driver: WebDriver = driver
        self.lang = lang
        self.session_id = session_id
        self.keyword_id = keyword_id
        self.udid = udid
        self.scroll = Scroll(self.driver)
        self.ad_text_filter = []
        self.ad_text_video_filter = []

        path: str = os.path.join(os.path.dirname(__file__), "../data/config.yaml")
        with open(path, "r") as file:
            self.config = yaml.safe_load(file)

    def collect_ad_type_2_alt(self, ad_web_element: WebElement) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            ad_web_elements: list[WebElement] = [
                web_element
                for web_element in ad_web_element.find_elements(AppiumBy.XPATH, ".//*[@class='android.view.View']")
                if web_element.size["height"] > 10
                and web_element.get_attribute("clickable") == "true"
                and web_element.get_attribute("text").startswith(self.lang.ad_2_starts_with)
                and web_element.get_attribute("text") not in self.ad_text_filter
            ]

            for index, web_element in enumerate(ad_web_elements):
                """scroll through web_elements ads"""
                print("collecting ad type 2 ...")
                if index == 0:
                    print("adjusting ad type 2 ...")
                    AdjustAd(self.driver).match_ad_visibility(web_element)
                else:
                    x, y, width, height = web_element.rect["x"], web_element.rect["y"], \
                        web_element.rect["width"], web_element.rect["height"]

                    self.scroll.press_and_move_to_location(
                        start_location=(x, (height / 2) + y),
                        end_location=(ad_web_elements[index - 1].rect["x"], (height / 2) + y)
                    )
                    time.sleep(3)

                """create an object of ad"""
                ad = BrandsRelatedToYourSearch(web_element)
                ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
                print("ad type 2 collected")
                if ad.text.strip() is not None:
                    self.ad_text_filter.append(ad.text)
        except (NoSuchElementException, IndexError):
            return

    def collect_ad_type_2(self, ad_web_element: WebElement) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            ad_web_elements: list[WebElement] = [
                web_element
                for web_element in ad_web_element.find_elements(AppiumBy.XPATH, ".//*[@class='android.view.View']")
                if web_element.size["height"] > 10
                and web_element.get_attribute("clickable") == "true"
                and web_element.get_attribute("text").startswith(self.lang.ad_2_starts_with)
                and web_element.get_attribute("text") not in self.ad_text_filter
            ]

            for index, web_element in enumerate(ad_web_elements):
                """scroll through web_elements ads"""
                print("collecting ad type 2 ...")
                if index == 0:
                    print("adjusting ad type 2 ...")
                    AdjustAd(self.driver).match_ad_visibility(web_element)
                else:
                    x, y, height = web_element.rect["x"], web_element.rect["y"], web_element.rect["height"]

                    self.scroll.press_and_move_to_location(
                        start_location=(x, (height / 2) + y),
                        end_location=(ad_web_elements[index - 1].rect["x"], (height / 2) + y)
                    )
                    time.sleep(1.5)

                """create an object of ad"""
                ad = BrandsRelatedToYourSearch(web_element)
                ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
                print("ad type 2 collected")
                if ad.text.strip() is not None:
                    self.ad_text_filter.append(ad.text)
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            return

    """def collect_ad_type_4(self, ad_web_element: WebElement) -> None:
        try:
            ad = HighlyRatedProductCarouselOfAds(ad_web_element)
            ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)

            ad_web_element = ad_web_element.find_element(AppiumBy.XPATH, ".//child::*/child::*")
            ad_web_elements: list[WebElement] = [
                web_element
                for web_element in ad_web_element.find_elements(AppiumBy.XPATH, ".//*[@class='android.view.View']")
                if web_element.size["height"] > 10
                and web_element.get_attribute("text").startswith(self.lang.ad_4_starts_with)
            ]

            for index, ad_element in enumerate(ad_web_elements):
                if index == 0:
                    print("adjusting ad type 4")
                    AdjustAd(self.driver).match_ad_visibility(ad_element)

                element_1: WebElement = ad_element.find_element(AppiumBy.XPATH, ".//child::*")
                text_1: str = element_1.text
                element_2: WebElement = element_1.find_element(AppiumBy.XPATH, ".//child::*")
                text_2: str = element_2.text
                text: str = " ".join([text_1, text_2])

                ad_element: WebElement = element_1.find_element(AppiumBy.XPATH, ".//parent::*")
                print("collecting ad type 4 ...")
                ad = HighlyRatedProductCarouselOfAds(ad_element)
                ad.text = text
                ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
                print("ad type 4 collected")

                if ad.text.strip() is not None:
                    self.ad_text_filter.append(ad.text)

        except Exception as e:
            print(e)"""

    def collect_ad_type_7(self, ad_web_element: WebElement) -> None:
        """Create and send data to DB, then save scr of ad"""
        if ad_web_element.size["height"] > 1000 and ad_web_element.get_attribute("resource-id") != "search" \
                and ad_web_element.find_elements(AppiumBy.XPATH, "//*[@class='android.view.View']")[-2] \
                .get_attribute("text") == "Sponsored":
            result_text: str = self.driver.find_element(AppiumBy.XPATH, f"//*[starts-with(@text, '"
                                                                        f"{self.lang.ad_7_text_starts_with}')]") \
                .get_attribute("text")

            """create ad object"""
            print("collecting ad type 7 ...")
            ad = SearchedProductSponsoredBrandTop(ad_web_element)
            ad.text = result_text
            ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
            print("ad type 7 collected")

            Scroll(self.driver).scroll_down(y=ad_web_element.size["height"] - (ad_web_element.size["height"] / 3))
            return

    def collect_ad_type_3(self, ad_web_element: WebElement) -> None:
        """Create and send data to DB, then save scr of ad"""
        if ad_web_element.size["height"] > 100 and ad_web_element.get_attribute("resource-id") != "search" \
                and ad_web_element.find_elements(AppiumBy.XPATH, "//*[@class='android.view.View']")[-2] \
                .get_attribute("text") == "Sponsored":
            result_text: str = self.driver.find_element(AppiumBy.XPATH, f"//*[starts-with(@text, '"
                                                                        f"{self.lang.ad_7_text_starts_with}')]") \
                                                                        .get_attribute("text")

            if result_text in self.ad_text_filter or result_text is None:
                return

            print("Adjusting ad type 3...")
            AdjustAd(self.driver).match_ad_visibility(ad_web_element)
            """create ad object"""
            print("collecting ad type 3 ...")
            ad = SearchedProductSponsoredBrandMid(ad_web_element)
            ad.text = result_text
            ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
            print("ad type 3 collected")

            if ad.text.strip() is not None:
                self.ad_text_filter.append(ad.text)

            return

    def collect_ad_type_8(self, ad_web_element: WebElement) -> None:
        """Create and send data to DB, then save scr of ad"""
        if ad_web_element.size["height"] > 100 and ad_web_element.get_attribute("resource-id") not in (
                "search", "a-page"):
            result_text: str = self.driver.find_element(AppiumBy.XPATH, f"//*[starts-with(@text, '"
                                                                        f"{self.lang.ad_1_text_starts_with}')]") \
                .get_attribute("text")

            if result_text in self.ad_text_filter or result_text is None:
                return
            print("Adjusting ad type 8...")
            AdjustAd(self.driver).match_ad_visibility(ad_web_element)
            """create ad object"""
            print("collecting ad type 8 ...")
            ad = SearchedProductSponsoredBrandTop(ad_web_element)
            ad.text = result_text
            ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
            print("ad type 8 collected")

            if ad.text.strip() is not None:
                self.ad_text_filter.append(ad.text)

            return None

    def collect_ad_type_1(self, ad_web_element: WebElement) -> None:
        """Create and send data to DB, then save scr of ad"""
        if ad_web_element.size["height"] > 600 and ad_web_element.get_attribute("resource-id") not in (
                "search", "a-page"):
            result_text: str = self.driver.find_element(AppiumBy.XPATH, f"//*[starts-with(@text, '"
                                                                        f"{self.lang.ad_1_text_starts_with}')]") \
                .get_attribute("text")

            """create ad object"""
            print("collecting ad type 1 ...")
            ad = SearchedProductSponsoredBrandTop(ad_web_element)
            ad.text = result_text
            ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
            print("ad type 1 collected")

            if ad.text.strip() is not None:
                self.ad_text_filter.append(ad.text)

            Scroll(self.driver).scroll_down(y=ad_web_element.size["height"] - (ad_web_element.size["height"] / 3))
            return None

    def collect_ad_type_10(self, ad_web_element: WebElement) -> None:
        """Create, send data to DB and save scr of ad"""
        # TODO this code works only for DE, change to multi lang config
        if ad_web_element.size["height"] > 10 and ad_web_element.get_attribute("resource-id") != "search":
            elements: [WebElement] = ad_web_element.find_elements(AppiumBy.XPATH, "//*[@class='android.view.View']")

            result_text: str = elements[2].get_attribute("content-desc")
            valid: str = elements[len(elements) - 1].get_attribute("content-desc")

            if valid.__contains__("Jetzt"):
                """create ad object"""
                print("collecting ad type 10 ...")
                ad = SearchedProductSponsoredBrandTop(ad_web_element)
                ad.text = result_text
                ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
                print("ad type 10 collected")
        else:
            return

    def get_webelements_ads_1(self) -> [WebElement]:
        webelements = []
        elements = self.driver.find_elements(AppiumBy.XPATH, self.lang.BOTTOM_AD)

        for element in elements:
            text_element_node = self.driver.find_element(AppiumBy.XPATH, self.lang.BOTTOM_AD_TEXT_ELEMENT)
            if element.size["height"] > 300 and text_element_node.size["width"] > 500:
                webelements.append(element)
        return webelements

    def collect_ads_1(self) -> [SearchedAdBottomBanner]:
        ads = []
        webelements = self.get_webelements_ads_1()

        for webElement in webelements:
            """create an object of ad"""
            ad = SearchedAdBottomBanner(webElement)
            ads.append(ad)
        return ads

    def collect_ad_type_5(self, ad_web_element: WebElement) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            if ad_web_element.size["height"] <= 10:
                return

            text_elements: list[WebElement] = ad_web_element.find_elements(AppiumBy.XPATH,
                                                                           ".//*[@class='android.view.View']")
            if len(text_elements) < 8:
                return

            result_text: str = text_elements[4].get_attribute("text")
            if not result_text.startswith(self.lang.ad_5_starts_with):
                return

            if result_text in self.ad_text_filter or result_text is None:
                return

            print("Adjusting ad type 5...")
            AdjustAd(self.driver).match_ad_visibility(ad_web_element)
            print("Collecting ad type 5...")
            ad = SearchedProductAd(ad_web_element)
            ad.text = result_text
            ad.save_ad(self.driver, self.session_id, self.keyword_id, self.udid)
            self.ad_text_filter.append(ad.text)
            print("Ad type 5 collected.")
        except (NoSuchElementException, IndexError):
            return

    def save_cropped_scr_for_videos(self, ad: Ad, filename: str) -> None:
        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        path = self.config["COMPUTER"]["SAVE_PATH"]
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

    def create_and_crop_video(self, video_ad_web_element: WebElement, db_id: int) -> None:
        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        path = self.config["COMPUTER"]["SAVE_PATH"]
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

    def collect_video_ad(self) -> None:
        """Collecting video, scr and modified scr for ad of type 6 - video_ad"""
        try:
            video_ad_web_element = self.driver.find_element(AppiumBy.XPATH, self.lang.ad_video)

            path = ".//child::*" + 4 * "/following-sibling::*"
            element = video_ad_web_element.find_element(AppiumBy.XPATH, path)
            text_element: WebElement = element.find_element(AppiumBy.XPATH, ".//child::*" + 3 * "/following-sibling::*")
            text: str = text_element.get_attribute("text")

            if video_ad_web_element.size["height"] > 10 and text is not None and text not in self.ad_text_video_filter:

                print("adjusting video ad ...")
                AdjustAd(self.driver).match_ad_visibility(video_ad_web_element)

                """create ad object"""
                print("collecting ad video type 6 ...")
                ad = SearchedProductAdVideo(video_ad_web_element)
                ad.text = text

                manager = SQLAdManager()
                manager.send_data_to_db(ad.width, ad.height, ad.location_x, ad.location_y, ad.text, ad.timestamp,
                                        ad.ad_type, self.session_id, self.keyword_id, self.udid)

                self.save_cropped_scr_for_videos(ad, str(manager.get_last_saved_id_from_db()))

                if ad.text.strip() is not None:
                    self.ad_text_video_filter.append(ad.text)

                self.create_and_crop_video(video_ad_web_element, manager.data_set_id)
                print("ad video collected")
                return None

        except NoSuchElementException:
            return None


class AdjustAd(object):

    def __init__(self, driver: WebDriver):
        self.driver: WebDriver = driver
        self.scroll = Scroll(self.driver)

    def match_ad_visibility(self, web_element: WebElement) -> None:
        if web_element.size["height"] > 10 and web_element.size["width"] > 10:
            previous_height: int = web_element.size["height"]
            self.scroll.press_and_move_to_location(start_location=(10, 1100), end_location=(10, 1000))
            next_height: int = web_element.size["height"]

            while True:
                if math.isclose(previous_height, next_height, abs_tol=1) and web_element.size["height"] > 100:
                    return

                if next_height > previous_height:
                    """case if element is on the bottom"""
                    previous_height = web_element.size["height"]
                    self.scroll.press_and_move_to_location(start_location=(10, 1100), end_location=(10, 1000))
                    next_height = web_element.size["height"]

                else:
                    """case if element is on the top"""
                    previous_height = web_element.size["height"]
                    self.scroll.press_and_move_to_location(start_location=(10, 1000), end_location=(10, 1500))
                    next_height = web_element.size["height"]
