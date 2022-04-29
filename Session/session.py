import os.path
import time

import cv2  # import opencv-python	4.5.5.64
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from os.path import exists
from os import remove
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from database_connector import get_last_saved_id_from_db
from database_connector import send_data_to_db
from TestData.config import TestData


class MainActivity:

    def __init__(self):
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", TestData.APPIUM_DESC)

    def setUp(self) -> None:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, TestData.SKIP_REDIRECT_MARKETPLACE_ID)))
        except (NoSuchElementException, TimeoutException):
            pass
        self.driver.find_element(By.ID, TestData.SKIP_REDIRECT_MARKETPLACE_ID).click()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, TestData.SKIP_SIGN_IN_BUTTON_ID)))
        except (NoSuchElementException, TimeoutException):
            pass
        self.driver.find_element(By.ID, TestData.SKIP_SIGN_IN_BUTTON_ID).click()

        #TODO skonfigurowac wyszukiwanie przez search bar w celu dowolnosci wyszukiwania
        """search item"""
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView')))
        except (NoSuchElementException, TimeoutException):
            self.driver.find_element(By.XPATH, '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView').click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text")))
            self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text").send_keys(
                "oculus oculus 2")
            self.driver.press_keycode(66)
        except (NoSuchElementException, TimeoutException):
            """try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, TestData.LAPTOP_BUTTON_XPATH)))
                self.driver.find_element(By.XPATH, TestData.LAPTOP_BUTTON_XPATH).click()
            except (NoSuchElementException, TimeoutException):
                pass"""
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, TestData.OCULUS_BUTTON_XPATH)))
                self.driver.find_element(By.XPATH, TestData.OCULUS_BUTTON_XPATH).click()
            except (NoSuchElementException, TimeoutException):
                pass

        """scroll through app Y"""
        for i in range(14):
            try:
                self.driver.swipe(470, 1100, 470, 50, 400)
            except:
                pass

    def bottom_ad(self) -> None:
        try:
            sponsored_ads = self.driver.find_elements(By.XPATH, "//*[@text='Sponsored']/parent::*")

            ad = []
            for x in sponsored_ads:
                elements = x.find_elements(By.XPATH, ".//*[@class='android.view.View']")
                for element in elements:
                    if element.size["height"] > 100 and element.get_attribute("scrollable") == "true":
                        ad.append(element)
                print("len(ad) = "+str(len(ad)))

            ads_meta_data = []

            for element in ad:
                """informacje do bazy danych"""
                width = element.size["width"]
                height = element.size["height"]
                location_x = element.location["x"]
                location_y = element.location["y"]
                text = element.get_attribute("text")
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                filename = (self.driver.current_activity + timestamp).replace(".", "_")

                ads_meta_data.append([filename, width, height, location_x, location_y, text, timestamp])

                MainActivity.save_croped_scr(self, element)

            for ad in ads_meta_data:
                send_data_to_db(ad[0], ad[1], ad[2], ad[3], ad[4], ad[5], ad[6], 1)



        except NoSuchElementException:
            print("ERROR-bottom_ad")

    def brands_related_to_your_search_Collector(self):
        try:
            element_node = self.driver.find_element(By.XPATH, "//*[contains(@text, 'Brands related to your search')]/parent::*")
            elements = element_node.find_elements(By.XPATH, ".//*[@class='android.view.View']")

            ads_meta_data = []
            for x in range(len(elements)):
                element = elements[x]
                if element.get_attribute("clickable") == "true":
                    print(element)
                    try:
                        """informacje do bazy danych"""
                        width = element.size["width"]
                        height = element.size["height"]
                        location_x = element.location["x"]
                        location_y = element.location["y"]
                        text = element.get_attribute("text")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        filename = (self.driver.current_activity + timestamp).replace(".", "_")

                        ads_meta_data.append([filename, width, height, location_x, location_y, text, timestamp])

                        MainActivity.save_croped_scr(self, element)

                        """scroll through ads"""
                        action = TouchAction(self.driver)
                        action.press(element).move_to(x=-element.size["width"] / 2, y=0).release().perform()

                    except Exception as e:
                        print(f'Excepion occured : {e}')

            for ad in ads_meta_data:
                try:
                    if os.path.exists(f"../Screenshots/Brands related to your search/{ad[0]}.png"):

                        send_data_to_db(ad[0], ad[1], ad[2], ad[3], ad[4], ad[5], ad[6], 2)

                except Exception as e:
                    print(f'Excepion occured in sending meta_data to DB: {e}')
                    remove(f"../Screenshots/Brands related to your search/{ad[0]}.png")

        except Exception as e:
            # TODO zamienic pass na konkret
            print(f'Excepion occured : {e}')

    def related_inspiration(self) -> None:
        try:
            ads_block = self.driver.find_elements(By.XPATH, "//*[@text='RELATED INSPIRATION']/parent::*/following-sibling::*[2]/child::*/child::*/child::*")

            print(ads_block)
            print(len(ads_block))

            ads_meta_data = []
            x = 0
            for ad1 in ads_block:
                ads_block_crc = ad1.find_elements(By.XPATH, ".//*[@class='android.view.View']")
                for ad in ads_block_crc:
                    if str(ad.get_attribute("text")).startswith("Follow the brand"):
                        x+=1

                        """informacje do bazy danych"""
                        width = ad.size["width"]
                        height = ad.size["height"]
                        location_x = ad.location["x"]
                        location_y = ad.location["y"]
                        text = ad.get_attribute("text")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        filename = (self.driver.current_activity + timestamp).replace(".", "_")

                        #tutaj ify i na koncu zweryfikowac scr -> wyslac do bd

                        ad_img = ad.find_element(By.XPATH, "child::*/child::*/child::*")

                        MainActivity.save_croped_scr(self, ad_img)

                        """scroll through ads"""
                        action = TouchAction(self.driver)
                            #z prawej strony na lewo
                            #action.press(ad_img).move_to(x=-ad_img.size["width"] / 2, y=0).release().perform()
                            #location_y+(height/2)
                        #action.press(x=location_x+width, y=0).move_to(x=location_x+(width/2), y=0).release().perform()
                        self.driver.execute_script('mobile: scroll', {"element": ad_img, "toVisible": True})

                        """
                        int centerX = element.getLocation().getX() + (element.getSize().getWidth()/2)
                        driver.swipe(centerX, bottomY, centerX, topY, duration);
                        """


                        ads_meta_data.append([filename, width, height, location_x, location_y, text, timestamp, str(x)]) #testowe



            print(ads_meta_data)

            """ads = element.find_elements(By.XPATH, ".//*[@class='android.view.View']")

            print(len(ads))
            for ad in ads:
                print(ad)"""

        except Exception as e:
            print(f'Excepion occured %%%%%%%%%: {e}')

    def save_croped_scr(self, object_to_save) -> None:

        date_folder_name = datetime.now().strftime("%Y-%m-%d")

        if not os.path.exists(f"../Screenshots/{date_folder_name}"):
            os.mkdir(f"../Screenshots/{date_folder_name}")

        img_name = int(get_last_saved_id_from_db())+1

        image_path = f"../Screenshots/{date_folder_name}/{str(img_name)}.png"
        self.driver.save_screenshot(image_path)
        img = cv2.imread(image_path)

        cropped_image = img[
                        object_to_save.location_in_view["y"]:object_to_save.location_in_view["y"] + object_to_save.size[
                            "height"],
                        object_to_save.location_in_view["x"]:object_to_save.location_in_view["x"] + object_to_save.size[
                            "width"]]
        cv2.imwrite(image_path, cropped_image)

    def tearDown(self) -> None:
        self.driver.close_app()

if __name__ == "__main__":
    while True:
        Amazon = MainActivity()
        try:
            Amazon.setUp()
            Amazon.bottom_ad()
            #Amazon.brands_related_to_your_search_Collector()
            #Amazon.related_inspiration()
        except Exception as e:
            print(f'Excepion occured : {e}')
        finally:
            Amazon.tearDown()
    #TODO przetestowac zmiany zawarte w metodzie brands_related_to_your_search_Collector() | zmiany polegaja na modyfikacji wysylania do DB
    #TODO stworzyc jedna metode do wysylania wszytskich reklam do jednej tabeli. (zmodyfikowac istniejaca)


    #TODO kazda "sesja" MUSI wysylac cropowane scr. to folderow o nazwie rok-mies-dzien | sprawdza czy folder istnieje jak nie to stworzy