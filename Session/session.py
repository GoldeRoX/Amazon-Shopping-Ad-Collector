import time

import cv2  # import opencv-python	4.5.5.64
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from database_connector import cursor, db_credentials
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
                #time.sleep(1)
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

            for element in ad:
                """informacje do bazy danych"""
                width = element.size["width"]
                height = element.size["height"]
                location_x = element.location["x"]
                location_y = element.location["y"]
                text = element.get_attribute("text")
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                filename = (self.driver.current_activity + timestamp).replace(".", "_")

                self.driver.save_screenshot(f"../Screenshots/First Ad/{filename}.png")
                image_path = f"../Screenshots/First Ad/{filename}.png"

                img = cv2.imread(image_path)

                cropped_image = img[
                                element.location_in_view["y"]:element.location_in_view["y"] + element.size["height"],
                                element.location_in_view["x"]:element.location_in_view["x"] + element.size["width"]]
                cv2.imwrite(f"../Screenshots/First Ad/{filename}.png", cropped_image)

                MainActivity().send_data_to_db("bottom_ad", filename, width, height, location_x, location_y, text,
                                               timestamp)

        except (NoSuchElementException, TimeoutException):
            print("ERROR-bottom_ad")

    def brands_related_to_your_search_Collector(self) -> None:
        try:
            #element_node = self.driver.find_elements(By.XPATH, "//*[@text='Brands related to your search']/parent::*")
            element_node = self.driver.find_element(By.XPATH, "//*[contains(@text, 'Brands related to your search')]/parent::*")
            print(element_node)
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
                        filename = (self.driver.current_activity + timestamp).replace(".", "_")

                        self.driver.save_screenshot(f"../Screenshots/Brands related to your search/{filename}.png")
                        image_path = f"../Screenshots/Brands related to your search/{filename}.png"
                        time.sleep(1)
                        img = cv2.imread(image_path)
                        cropped_image = img[
                                        element.location_in_view["y"]:element.location_in_view["y"] + element.size["height"],
                                        element.location_in_view["x"]:element.location_in_view["x"] + element.size["width"]]
                        cv2.imwrite(f"../Screenshots/Brands related to your search/{filename}.png", cropped_image)

                        MainActivity().send_data_to_db("brands_related_to_your_search", filename, width, height, location_x,
                                                       location_y, text, timestamp)

                        """scroll through ads"""
                        action = TouchAction(self.driver)
                        action.press(element).move_to(x=-element.size["width"] / 2, y=0).release().perform()
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        pass

        except NoSuchElementException:
            # TODO zamienic pass na konkret
            print("ERROR-brands_related_to_your_search_Collector")

    def related_inspiration(self) -> None:
        try:
            element = self.driver.find_element(By.XPATH, "(//*[@text='RELATED INSPIRATION See all']")
            print(element)

        except NoSuchElementException:
            print("ERROR-related_inspiration")

    def tearDown(self) -> None:
        self.driver.close_app()

    def send_data_to_db(self, table_name, filename, width, height, location_x, location_y, text, timestamp):
        query = f"""
                INSERT INTO 
                    {str(table_name)}
                    (filename, width, height, location_x, location_y, text, timestamp)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                ;"""

        with cursor(**db_credentials) as c:
            if not text:
                text = None

            c.execute(
                query,
                (filename, width, height, location_x, location_y, text, timestamp)
            )


if __name__ == "__main__":
    # TODO zorganizowac plynny system logiki
    while True:
        try:
            Amazon = MainActivity()
            Amazon.setUp()
            Amazon.brands_related_to_your_search_Collector()
            Amazon.bottom_ad()
            #Amazon.related_inspiration()
            Amazon.tearDown()
        except Exception as e:
            print(f'Excepion occured : {e}')
            pass