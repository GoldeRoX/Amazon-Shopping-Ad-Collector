import base64
import math
import os
import time
import cv2
import yaml

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from amazonadcollector.Ad import *
from amazonadcollector.base import Scroll
from amazonadcollector.database_connector import SQLAdManager
from amazonadcollector.locators_data import Lang


class AdFactory(object):

    def __init__(self, driver: WebDriver, sql_ad_manager: SQLAdManager, random_keyword: {str: int}):
        self.__dict_of_ads_top: {WebElement: int} = {}
        self.__dict_of_ads_mid: {WebElement: int} = {}
        self.__lang = Lang().get_lang()
        self.__driver = driver
        self.__ad_collector = AdCollector(self.__driver, self.__lang)
        self.__ad_handler = AdHandler(driver, self.__lang, sql_ad_manager.get_session_id(), sql_ad_manager,
                                      sql_ad_manager.get_udid(), random_keyword["id"])
        self.__keyword = random_keyword["keyword"]

    def collect_ads_top(self) -> {WebElement: int}:
        self.__dict_of_ads_top.clear()

        for ad in self.__ad_collector.get_webelements_ads_1():
            self.__dict_of_ads_top.update({ad: 1})

        for ad in self.__ad_collector.get_webelements_ads_7():
            self.__dict_of_ads_top.update({ad: 7})

        return self.__dict_of_ads_top

    def collect_ads_mid(self) -> {WebElement: int}:
        self.__dict_of_ads_mid.clear()

        for ad in self.__ad_collector.get_webelements_ads_2():
            self.__dict_of_ads_mid.update({ad: 2})

        for ad in self.__ad_collector.get_webelements_ads_2_alt():
            self.__dict_of_ads_mid.update({ad: 2})

        for ad in self.__ad_collector.get_webelements_ads_7():
            self.__dict_of_ads_mid.update({ad: 3})

        """for ad in self.ad_collector.get_webelements_ads_4():
            print(ad)
            self.dict_of_ads_mid.update({ad: 4})"""

        for ad in self.__ad_collector.get_webelements_ads_5():
            self.__dict_of_ads_mid.update({ad: 5})

        for ad in self.__ad_collector.get_webelements_ads_6():
            self.__dict_of_ads_mid.update({ad: 6})

        for ad in self.__ad_collector.get_webelements_ads_1():
            self.__dict_of_ads_mid.update({ad: 8})

        return self.__dict_of_ads_mid

    def create_and_save_main_page_ads(self) -> None:
        self.__ad_handler.collect_main_page_top_carousel_of_ads()
        # self.__ad_handler.collect_main_page_banner_ad()

    def create_and_save_top_ads(self) -> None:
        """
        Creates and saves an Ad object from top sector of app
        based on the type of advertisement element passed to it.
        """
        self.collect_ads_top()

        for web_element, ad_type in self.__dict_of_ads_top.items():
            match ad_type:
                case 1:
                    print("test_1")
                    self.__ad_handler.collect_ad_type_1(web_element)
                case 7:
                    self.__ad_handler.collect_ad_type_7(web_element)
                case _:
                    raise ValueError(f"Invalid ad type '{ad_type}'")

    def create_and_save_mid_ads(self) -> None:
        """
        Creates and saves an Ad object from middle sector of app
        based on the type of advertisement element passed to it.
        """
        self.collect_ads_mid()

        for web_element, ad_type in self.__dict_of_ads_mid.items():
            match ad_type:
                case 2:
                    self.__ad_handler.collect_ad_type_2(web_element)
                case 3:
                    self.__ad_handler.collect_ad_type_3(web_element)
                # case 4:
                # self.__ad_handler.collect_ad_type_4(web_element)
                case 5:
                    self.__ad_handler.collect_ad_type_5(web_element)
                case 6:
                    self.__ad_handler.collect_video_ad()
                case 8:
                    self.__ad_handler.collect_ad_type_8(web_element)
                case _:
                    raise ValueError(f"Invalid ad type '{ad_type}'")


class AdCollector(object):
    def __init__(self, driver: WebDriver, lang):
        self.__driver = driver
        self.__lang = lang

    def get_webelements_ads_1(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_1)

    def get_webelements_ads_2(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.brands_related_to_your_search_element_node)

    def get_webelements_ads_2_alt(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.Items_related_to_your_search_element_node)

    """def get_webelements_ads_4(self) -> [WebElement]:
        element = self.driver.find_elements(AppiumBy.XPATH, self.lang.ad_4_locator)
        print(element)
        return element"""

    def get_webelements_ads_5(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_5_node)

    def get_webelements_ads_7(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_7)

    def get_webelements_ads_8(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_8)

    def get_webelements_ads_8_alt(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_8_alt)

    def get_webelements_ads_9(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_9)

    def get_webelements_ads_6(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_video)

    def get_webelements_ads_9_alt(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_9_alt)

    def get_webelements_ads_10(self) -> [WebElement]:
        return self.__driver.find_elements(AppiumBy.XPATH, self.__lang.ad_10)


class AdHandler(object):
    def __init__(self, driver: WebDriver, lang, session_id, sql_ad_manager: SQLAdManager, udid: int, keyword_id: int):
        self.__sql_ad_manager: SQLAdManager = sql_ad_manager
        self.__driver: WebDriver = driver
        self.__lang = lang
        self.__session_id = session_id
        self.__keyword_id = keyword_id
        self.__udid = udid
        self.__scroll = Scroll(self.__driver)
        self.__ad_text_filter: [str] = []
        self.__ad_text_video_filter: [str] = []
        self.__main_carousel_ads: [str] = []

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
                   and web_element.get_attribute("text").startswith(self.__lang.ad_2_starts_with)
                   and web_element.get_attribute("text") not in self.__ad_text_filter
            ]

            for index, web_element in enumerate(ad_web_elements):
                """scroll through web_elements ads"""
                print("collecting ad type 2 ...")
                if index == 0:
                    print("adjusting ad type 2 ...")
                    AdjustAd(self.__driver).match_ad_visibility(web_element)
                else:
                    x, y, width, height = web_element.rect["x"], web_element.rect["y"], \
                        web_element.rect["width"], web_element.rect["height"]

                    self.__scroll.press_and_move_to_location(
                        start_location=(x, (height / 2) + y),
                        end_location=(ad_web_elements[index - 1].rect["x"], (height / 2) + y)
                    )
                    time.sleep(3)

                """create an object of ad"""
                ad = BrandsRelatedToYourSearch(web_element, self.__sql_ad_manager)
                ad.save_ad(self.__driver, self.__keyword_id)
                print("ad type 2 collected")
                if ad.text.strip() is not None:
                    self.__ad_text_filter.append(ad.text)
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            return

    def collect_ad_type_2(self, ad_web_element: WebElement) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            ad_web_elements: list[WebElement] = [
                web_element
                for web_element in ad_web_element.find_elements(AppiumBy.XPATH, ".//*[@class='android.view.View']")
                if web_element.size["height"] > 10
                   and web_element.get_attribute("clickable") == "true"
                   and web_element.get_attribute("text").startswith(self.__lang.ad_2_starts_with)
                   and web_element.get_attribute("text") not in self.__ad_text_filter
            ]

            for index, web_element in enumerate(ad_web_elements):
                """scroll through web_elements ads"""
                print("collecting ad type 2 ...")
                if index == 0:
                    print("adjusting ad type 2 ...")
                    AdjustAd(self.__driver).match_ad_visibility(web_element)
                else:
                    x, y, height = web_element.rect["x"], web_element.rect["y"], web_element.rect["height"]

                    self.__scroll.press_and_move_to_location(
                        start_location=(x, (height / 2) + y),
                        end_location=(ad_web_elements[index - 1].rect["x"], (height / 2) + y)
                    )
                    time.sleep(1.5)

                """create an object of ad"""
                ad = BrandsRelatedToYourSearch(web_element, self.__sql_ad_manager)
                ad.save_ad(self.__driver, self.__keyword_id)
                print("ad type 2 collected")
                if ad.text.strip() is not None:
                    self.__ad_text_filter.append(ad.text)
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
        try:
            if ad_web_element.size["height"] > 50 and ad_web_element.get_attribute("resource-id") != "search" \
                    and ad_web_element.find_elements(AppiumBy.XPATH, "//*[@class='android.view.View']")[-2] \
                    .get_attribute("text") == self.__lang.sponsored:
                result_text: str = self.__driver.find_element(AppiumBy.XPATH, f"//*[starts-with(@text, '"
                                                                              f"{self.__lang.ad_7_text_starts_with}')]") \
                    .get_attribute("text")

                """create ad object"""
                print("collecting ad type 7 ...")
                ad = SearchedProductSponsoredBrandTop(ad_web_element, self.__sql_ad_manager)
                ad.text = result_text
                ad.save_ad(self.__driver, self.__keyword_id)
                print("ad type 7 collected")
                return
        except StaleElementReferenceException:
            return

    # TODO test
    def collect_ad_type_3(self, ad_web_element: WebElement) -> None:
        """Create and send data to DB, then save scr of ad"""
        try:
            if ad_web_element.size["height"] > 50 and ad_web_element.get_attribute("resource-id") != "search" \
                    and ad_web_element.find_elements(AppiumBy.XPATH, "//*[@class='android.view.View']")[-2] \
                    .get_attribute("text") == self.__lang.sponsored:

                try:
                    ad_web_element.find_element(AppiumBy.XPATH, "./preceding-sibling::*[2]")
                except NoSuchElementException:
                    return

                result_text: str = self.__driver.find_element(AppiumBy.XPATH, f"//*[starts-with(@text, '"
                                                                              f"{self.__lang.ad_7_text_starts_with}')]") \
                    .get_attribute("text")

                if result_text in self.__ad_text_filter or result_text is None:
                    return

                print("Adjusting ad type 3...")
                AdjustAd(self.__driver).match_ad_visibility(ad_web_element)
                """create ad object"""
                print("collecting ad type 3 ...")
                ad = SearchedProductSponsoredBrandMid(ad_web_element, self.__sql_ad_manager)
                ad.text = result_text
                ad.save_ad(self.__driver, self.__keyword_id)
                print("ad type 3 collected")

                if ad.text.strip() is not None:
                    self.__ad_text_filter.append(ad.text)

                return
        except StaleElementReferenceException:
            return

    def collect_ad_type_8(self, ad_web_element: WebElement) -> None:
        """Create and send data to DB, then save scr of ad"""
        try:
            if ad_web_element.size["height"] > 100 and ad_web_element.get_attribute("resource-id") not in (
                    "search", "a-page") and ad_web_element.get_attribute("text").strip() is None:
                result_text: str = self.__driver.find_element(AppiumBy.XPATH, f"//*[starts-with(@text, '"
                                                                              f"{self.__lang.ad_1_text_starts_with}')]") \
                    .get_attribute("text")

                if result_text in self.__ad_text_filter or result_text is None:
                    return
                print("Adjusting ad type 8...")
                AdjustAd(self.__driver).match_ad_visibility(ad_web_element)
                """create ad object"""
                print("collecting ad type 8 ...")
                ad = SearchedProductSponsoredBrandTop(ad_web_element, self.__sql_ad_manager)
                ad.text = result_text
                ad.save_ad(self.__driver, self.__keyword_id)
                print("ad type 8 collected")

                if ad.text.strip() is not None:
                    self.__ad_text_filter.append(ad.text)

                return
        except StaleElementReferenceException:
            return

    # TODO test
    def collect_ad_type_1(self, ad_web_element: WebElement) -> None:
        """Create and send data to DB, then save scr of ad"""
        try:
            print(ad_web_element.size["height"])
            print(ad_web_element.get_attribute("resource-id"))
            print(ad_web_element.get_attribute("text").strip())

            if ad_web_element.size["height"] < 600 and ad_web_element.get_attribute("resource-id") not in (
                    "search", "a-page") and ad_web_element.get_attribute("text").strip() is None:
                print("testu")
                result_text: str = self.__driver.find_element(AppiumBy.XPATH, f"//*[starts-with(@text, '"
                                                                              f"{self.__lang.ad_1_text_starts_with}')]") \
                    .get_attribute("text")
                print("passed")
                try:
                    ad_web_element.find_element(AppiumBy.XPATH, "./preceding-sibling::*[2]")
                except NoSuchElementException:
                    return

                """create ad object"""
                print("collecting ad type 1 ...")
                ad = SearchedProductSponsoredBrandMid(ad_web_element, self.__sql_ad_manager)
                ad.text = result_text
                ad.save_ad(self.__driver, self.__keyword_id)
                print("ad type 1 collected")

                if ad.text.strip() is not None:
                    self.__ad_text_filter.append(ad.text)
                return
        except StaleElementReferenceException:
            return

    '''def collect_ad_type_10(self, ad_web_element: WebElement) -> None:
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
            return'''

    '''def get_webelements_ads_1(self) -> [WebElement]:
        webelements = []
        elements = self.driver.find_elements(AppiumBy.XPATH, self.lang.BOTTOM_AD)

        for element in elements:
            text_element_node = self.driver.find_element(AppiumBy.XPATH, self.lang.BOTTOM_AD_TEXT_ELEMENT)
            if element.size["height"] > 300 and text_element_node.size["width"] > 500:
                webelements.append(element)
        return webelements'''

    '''def collect_ads_1(self) -> [SearchedAdBottomBanner]:
        ads = []
        webelements = self.get_webelements_ads_1()

        for webElement in webelements:
            """create an object of ad"""
            ad = SearchedAdBottomBanner(webElement)
            ads.append(ad)
        return ads'''

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
            if not result_text.startswith(self.__lang.ad_5_starts_with):
                return

            if result_text in self.__ad_text_filter or result_text is None:
                return

            print("Adjusting ad type 5...")
            AdjustAd(self.__driver).match_ad_visibility(ad_web_element)
            print("Collecting ad type 5...")
            ad = SearchedProductAd(ad_web_element, self.__sql_ad_manager)
            ad.text = result_text
            ad.save_ad(self.__driver, self.__keyword_id)
            self.__ad_text_filter.append(ad.text)
            print("Ad type 5 collected.")
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            return

    def __save_cropped_scr_for_videos(self, ad: Ad, filename: str) -> None:
        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        save_path = self.config["COMPUTER"]["SAVE_PATH"]

        if not os.path.exists(f"{save_path}/DE"):
            os.mkdir(f"{save_path}/DE")

        if not os.path.exists(f"{save_path}/UK"):
            os.mkdir(f"{save_path}/UK")

        if not os.path.exists(f"{save_path}/{self.config['APP']['LANG']}/{date_folder_name}"):
            os.mkdir(f"{save_path}/{self.config['APP']['LANG']}/{date_folder_name}")

        img_name = filename

        image_path: str = f"{save_path}/{self.config['APP']['LANG']}/{date_folder_name}/{str(img_name)}_thumb.png"
        self.__driver.save_screenshot(image_path)
        img = cv2.imread(image_path)

        cropped_image = img[
                        ad.get_location_y():ad.get_location_y() + ad.get_height(),
                        ad.get_location_x():ad.get_location_x() + ad.get_width()
                        ]

        cv2.imwrite(image_path, cropped_image)

        image_path = f"{save_path}/{self.config['APP']['LANG']}/{date_folder_name}/{str(img_name)}.png"
        video_element_ad_web_element = self.__driver.find_element(AppiumBy.XPATH, self.__lang.ad_video)
        path = ".//child::*/following-sibling::*"
        video_element = video_element_ad_web_element.find_element(AppiumBy.XPATH, path)
        self.__driver.save_screenshot(image_path)
        new_img = cv2.imread(image_path)

        test = cv2.rectangle(new_img, (video_element.location["x"], video_element.location["y"]),
                             (video_element.location["x"] + video_element.size["width"],
                              video_element.location["y"] + video_element.size["height"]), (0, 0, 0), -1)

        cropped_image = test[
                        ad.get_location_y():ad.get_location_y() + ad.get_height(),
                        ad.get_location_x():ad.get_location_x() + ad.get_width()
                        ]

        try:
            cv2.imwrite(image_path, cropped_image)
        except cv2.error:
            pass

    def __create_and_crop_video(self, video_ad_web_element: WebElement) -> None:
        date_folder_name: str = datetime.now().strftime("%Y-%m-%d")

        path: str = self.config["COMPUTER"]["SAVE_PATH"]

        if not os.path.exists(f"{path}/DE"):
            os.mkdir(f"{path}/DE")

        if not os.path.exists(f"{path}/UK"):
            os.mkdir(f"{path}/UK")

        if not os.path.exists(f"{path}//{self.config['APP']['LANG']}/{date_folder_name}"):
            os.mkdir(f"{path}/{self.config['APP']['LANG']}/{date_folder_name}")

        self.__driver.start_recording_screen()
        time.sleep(60)
        video_rawdata = self.__driver.stop_recording_screen()

        video_name = str(self.__sql_ad_manager.get_last_saved_id_from_db())
        filepath = os.path.join(f"{path}/{self.config['APP']['LANG']}/{date_folder_name}",
                                "test_" + video_name + ".mp4")
        with open(filepath, "wb+") as vd:
            vd.write(base64.b64decode(video_rawdata))
        os.system(
            f'ffmpeg -i {path}/{self.config["APP"]["LANG"]}/{date_folder_name}/test_{video_name}.mp4 -vf "crop={video_ad_web_element.size["width"]}:'
            f'{video_ad_web_element.size["height"]}:{video_ad_web_element.location["x"]}:'
            f'{video_ad_web_element.location["y"]}" {path}/{self.config["APP"]["LANG"]}/{date_folder_name}/{video_name}.mp4')
        os.system(f"unlink {path}/{self.config['APP']['LANG']}/{date_folder_name}/test_{video_name}.mp4")

    def collect_video_ad(self) -> None:
        """Collecting video, scr and modified scr for ad of type 6 - video_ad"""
        try:
            video_ad_web_element: WebElement = self.__driver.find_element(AppiumBy.XPATH, self.__lang.ad_video)

            path: str = ".//child::*" + 4 * "/following-sibling::*"
            element: WebElement = video_ad_web_element.find_element(AppiumBy.XPATH, path)
            text_element: WebElement = element.find_element(AppiumBy.XPATH, ".//child::*" + 3 * "/following-sibling::*")
            text: str = text_element.get_attribute("text")

            if video_ad_web_element.size["height"] > 10 and text is not None \
                    and text not in self.__ad_text_video_filter:

                print("adjusting video ad ...")
                AdjustAd(self.__driver).match_ad_visibility(video_ad_web_element)

                """create ad object"""
                print("collecting ad video type 6 ...")
                ad = SearchedProductAdVideo(video_ad_web_element, self.__sql_ad_manager)
                ad.__text = text

                self.__sql_ad_manager.send_data_to_db(ad.get_width(), ad.get_height(), ad.get_location_x(),
                                                      ad.get_location_y(), ad.text, ad.get_timestamp(), ad.ad_type,
                                                      self.__keyword_id, )

                self.__save_cropped_scr_for_videos(ad, str(self.__sql_ad_manager.get_last_saved_id_from_db()))

                if ad.text.strip() is not None:
                    self.__ad_text_video_filter.append(ad.text)

                self.__create_and_crop_video(video_ad_web_element)
                print("ad video collected")
                return

        except (NoSuchElementException, StaleElementReferenceException):
            return

    def collect_main_page_banner_ad(self) -> None:
        """Create, send to DB and save scr of ad"""
        try:
            web_element: WebElement = self.__driver.find_element(AppiumBy.XPATH, self.__lang.main_page_banner_ad_id)
            if web_element.size["height"] <= 10:
                return

            print("Adjusting ad type 1...")
            AdjustAd(self.__driver).match_ad_visibility(web_element)
            print("Collecting ad type 1...")
            ad = MainPageBannerAd(web_element, self.__sql_ad_manager)
            ad.save_ad(self.__driver, self.__keyword_id)
            self.__ad_text_filter.append(ad.text)
            print("Ad type 1 collected.")
        except (NoSuchElementException, IndexError, StaleElementReferenceException):
            return

    def collect_main_page_top_carousel_of_ads(self, max_attempts: int = 150) -> None:
        """Create, send to DB and save scr of ad"""
        attempts = 0
        while attempts < max_attempts:
            try:
                carousel_elements = self.__driver.find_elements(AppiumBy.XPATH,
                                                                self.__lang.main_page_carousel_of_ads)

                ads_saved = 0

                for element in carousel_elements:
                    if element.size["width"] <= 10:
                        continue

                    try:
                        web_elements = self.__driver.find_elements(AppiumBy.XPATH,
                                                                   self.__lang.main_page_carousel_of_ads)

                        for i in range(len(web_elements)):
                            ad_text = web_elements[i].get_attribute("text")
                            if web_elements[i].size["width"] <= 10 or ad_text in self.__main_carousel_ads:
                                continue

                            ad = MainPageBannerAd(web_elements[i], self.__sql_ad_manager)
                            ad.save_ad(self.__driver, self.__keyword_id)
                            self.__main_carousel_ads.append(ad_text)
                            ads_saved += 1

                            if ads_saved >= max_attempts:
                                break

                    except (NoSuchElementException, StaleElementReferenceException):
                        pass

                if ads_saved >= max_attempts:
                    break

            except Exception as e:
                print(e)

            attempts += 1


class AdjustAd(object):

    def __init__(self, driver: WebDriver):
        self.__scroll = Scroll(driver)

    def match_ad_visibility(self, web_element: WebElement) -> None:
        if web_element.size["height"] > 10 and web_element.size["width"] > 10:
            previous_height: int = web_element.size["height"]
            self.__scroll.press_and_move_to_location(start_location=(10, 1100), end_location=(10, 1000))
            next_height: int = web_element.size["height"]

            while True:
                if math.isclose(previous_height, next_height, abs_tol=1) and web_element.size["height"] > 100:
                    return

                if next_height > previous_height:
                    """case if element is on the bottom"""
                    previous_height = web_element.size["height"]
                    self.__scroll.press_and_move_to_location(start_location=(10, 1100), end_location=(10, 1000))
                    next_height = web_element.size["height"]

                else:
                    """case if element is on the top"""
                    previous_height = web_element.size["height"]
                    self.__scroll.press_and_move_to_location(start_location=(10, 1000), end_location=(10, 1500))
                    next_height = web_element.size["height"]
