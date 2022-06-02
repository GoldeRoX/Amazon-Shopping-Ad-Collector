import os.path
import time

import cv2  # import opencv-python	4.5.5.64
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from database_connector import get_last_saved_id_from_db
from database_connector import send_data_to_db

class MainActivity:

    def __init__(self, driver):
        self.driver = driver

    def setUp(self) -> None:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel")))
        except (NoSuchElementException, TimeoutException):
            pass
        self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/btn_cancel").click()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'com.amazon.mShop.android.shopping:id/skip_sign_in_button')))
        except (NoSuchElementException, TimeoutException):
            pass
        self.driver.find_element(By.ID, 'com.amazon.mShop.android.shopping:id/skip_sign_in_button').click()

        """search item"""
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView')))
        except (NoSuchElementException, TimeoutException):
            self.driver.find_element(By.XPATH, '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView').click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '(//android.widget.LinearLayout[@content-desc="Search"])[2]/android.widget.ImageView')))
                #EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text")))
            self.driver.find_element(By.XPATH, '(//android.widget.LinearLayout[@content-desc="Search"])[2]/android.widget.ImageView').click()
            self.driver.find_element(By.XPATH, 'com.amazon.mShop.android.shopping:id/rs_search_src_text').send_keys(
                "oculus oculus 2")
            self.driver.press_keycode(66)
        except (NoSuchElementException, TimeoutException):
            print("nie znalazlo 'search' input")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]'
                                                              '/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View')))
                self.driver.find_element(By.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]'
                                                   '/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View').click()
            except (NoSuchElementException, TimeoutException):
                pass

        """scroll through app Y"""
        for i in range(14):
            try:
                self.driver.swipe(470, 1100, 470, 50, 400)
                time.sleep(1)
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
                    send_data_to_db(ad[0], ad[1], ad[2], ad[3], ad[4], ad[5], ad[6], 2)


        except Exception as e:
            print(f'Excepion occured : {e}')

    def related_inspiration(self) -> None:
        try:
            ads_block = self.driver.find_elements(By.XPATH, "//*[@text='RELATED INSPIRATION']/parent::*/following-sibling::*[2]/child::*/child::*/child::*")

            x = 0
            for ad1 in ads_block:
                ads_block_crc = ad1.find_elements(By.XPATH, ".//*[@class='android.view.View']")
                for ad in ads_block_crc:
                    if str(ad.get_attribute("text")).startswith("Follow the brand"):

                        """informacje do bazy danych"""
                        width = ad.size["width"]
                        height = ad.size["height"]
                        location_x = ad.location["x"]
                        location_y = ad.location["y"]
                        text = ad.get_attribute("text")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        filename = (self.driver.current_activity + timestamp).replace(".", "_")

                        """scroll through ads | send data to db"""
                        if ads_block_crc[x]:
                            send_data_to_db(filename, width, height, location_x, location_y, text, timestamp, 3)
                            self.driver.swipe(location_x + (width/2), location_y + (height/2),
                                              ads_block_crc[x].size["width"]/2, ads_block_crc[x].location["y"]+
                                              (ads_block_crc[x].size["height"]/2))
                            time.sleep(2)
                            MainActivity.save_croped_scr(self, ad)
                            time.sleep(2)
                            x += 1

        except Exception as e:
            print(f'Excepion occured retade_ins: {e}')

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

    def tearDown(self) -> None:
        self.driver.close_app()

if __name__ == "__main__":
    while True:
        APPIUM_DESC = {
            "platformName": "Android",
            "appium:platformVersion": "9",
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": "com.amazon.mShop.android.shopping",
            "appium:appActivity": "com.amazon.mShop.home.HomeActivity",
            "appium:deviceName": "emulator-5554"
        }
        Amazon = MainActivity(webdriver.Remote("http://localhost:4723/wd/hub", APPIUM_DESC))
        try:
            Amazon.setUp()
            Amazon.bottom_ad()
            Amazon.brands_related_to_your_search_Collector()
            Amazon.related_inspiration()
        except Exception as e:
            print(f'Excepion occured : ***')
        finally:
            Amazon.tearDown()