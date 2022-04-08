import os
import time

import cv2  # import opencv-python	4.5.5.64
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from TestData.config import TestData

#testu
class MainActivity:

    def __init__(self, driver):
        self.driver = driver

    def setUp(self) -> None:

        # self.driver = webdriver.Remote("http://localhost:4723/wd/hub", TestData.APPIUM_DESC)

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

        """search item"""
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.ID, "com.amazon.mShop.android.shopping:id/chrome_action_bar_search_icon")))
        except (NoSuchElementException, TimeoutException):
            pass
            self.driver.find_element(By.XPATH, "//*[contains(@resource-id,'chrome_action_bar_search_icon')]").click()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text")))
            self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text").send_keys(
                "oculus")
            self.driver.press_keycode(66)
        except (NoSuchElementException, TimeoutException):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, TestData.OCULUS_BUTTON_XPATH)))
                self.driver.find_element(By.XPATH, TestData.OCULUS_BUTTON_XPATH).click()
            except (NoSuchElementException, TimeoutException):
                pass

            """try: WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, 
            TestData.COOKIE_ACCEPT_XPATH))) self.driver.find_element(By.XPATH, TestData.COOKIE_ACCEPT_XPATH).click() 
            except NoSuchElementException: pass """

        for i in range(11):
            time.sleep(1)
            self.driver.swipe(470, 1100, 470, 50, 400)

    def firstAddCollector(self) -> None:

        global filename

        try:
            sponsored_ads = self.driver.find_elements(By.XPATH, "//*[@text='Leave feedback on Sponsored ad']/parent::*/preceding-sibling::*")

            ad = []
            for x in sponsored_ads:
                if x.size["height"] > 100:
                    ad.append(x)

            for element in ad:

                """info do bazy danych"""
                filename = (self.driver.current_activity + time.strftime("%Y_%m_%d_%H%M%S")).replace(".", "_")
                width = element.size["width"]
                height = element.size["height"]
                location_x = element.location["x"]
                location_y = element.location["y"]
                text = element.get_attribute("text")
                """timestamp = datetime.now()"""

                self.driver.save_screenshot(f"../Screenshots/First Add/{filename}.png")
                image_path = f"../Screenshots/First Add/{filename}.png"

                img = cv2.imread(image_path)

                cropped_image = img[
                                element.location_in_view["y"]:element.location_in_view["y"] + element.size["height"],
                                element.location_in_view["x"]:element.location_in_view["x"] + element.size["width"]]
                cv2.imwrite(f"../Screenshots/First Add/{filename}.png", cropped_image)

        except NoSuchElementException:
            pass
        if os.path.exists(f"../Screenshots/First Add/{filename}.png"):
            print("ok")
        else:
            print("ERROR")

    def secondAddCollector(self) -> None:

        temp_element_text = []

        try:
            element_node = self.driver.find_element(By.XPATH, "//*[@text='Brands related to your search']/parent::*")

            elements = element_node.find_elements(By.XPATH, "//*[@class='android.view.View']")

            for x in range(6, len(elements), 2):
                element = elements[x]

                """info do bazy danych"""
                filename = (self.driver.current_activity + time.strftime("%Y_%m_%d_%H%M%S")).replace(".", "_")
                width = element.size["width"]
                height = element.size["height"]
                location_x = element.location["x"]
                location_y = element.location["y"]
                text = element.get_attribute("text")
                temp_element_text.append(str(text))

                self.driver.save_screenshot(f"../Screenshots/Brands related to your search/{filename}.png")
                image_path = f"../Screenshots/Brands related to your search/{filename}.png"

                time.sleep(2)
                img = cv2.imread(image_path)

                cropped_image = img[
                                element.location_in_view["y"]:element.location_in_view["y"] + element.size["height"],
                                element.location_in_view["x"]:element.location_in_view["x"] + element.size["width"]]
                cv2.imwrite(f"../Screenshots/Brands related to your search/{filename}.png", cropped_image)

                action = TouchAction(self.driver)
                action.press(element).move_to(x=-element.size["width"] / 2, y=0).release().perform()
                time.sleep(2)

                """open a temp file to store data"""
                with open("temp.txt", "a") as file:
                    file.writelines(str(text) + " - " + filename + ".png\n")

        except NoSuchElementException:
            print("ERROR")
            pass
        # print(temp_element_text)

    def tearDown(self) -> None:
        self.driver.close_app()

    #TODO zrobic uniwersalna funkcje do pobierania wszytskich danych z konkretnego obiektu. Funkcja powinna miec argument nazwy folderu + tabeli DB
    def collectData(self):
        pass
    """funkcja do zbierania/wysylania danych reklamowych"""




if __name__ == "__main__":
    Amazon = MainActivity(webdriver.Remote("http://localhost:4723/wd/hub", TestData.APPIUM_DESC))
    Amazon.setUp()
    Amazon.firstAddCollector()
    Amazon.secondAddCollector()
    # time.sleep(100000)
    Amazon.tearDown()
