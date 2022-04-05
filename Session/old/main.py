import os
import time
import unittest

import cv2  # import opencv-python	4.5.5.64
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from TestData.config import TestData


class MainActivity(unittest.TestCase):

    def setUp(self) -> None:

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", TestData.APPIUM_DESC)

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, TestData.SKIP_REDIRECT_MARKETPLACE_ID)))
        except (NoSuchElementException, TimeoutException):
            pass
        self.driver.find_element(By.ID, TestData.SKIP_REDIRECT_MARKETPLACE_ID).click()

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, TestData.SKIP_SIGN_IN_BUTTON_ID)))
        except (NoSuchElementException, TimeoutException):
            pass
        self.driver.find_element(By.ID, TestData.SKIP_SIGN_IN_BUTTON_ID).click()

        """search item"""
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/chrome_action_bar_search_icon")))
        except (NoSuchElementException, TimeoutException):
            pass
            self.driver.find_element(By.XPATH, "//*[contains(@resource-id,'chrome_action_bar_search_icon')]").click()
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text")))
            self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text").send_keys("oculus")
            self.driver.press_keycode(66)
        except (NoSuchElementException, TimeoutException):
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, TestData.OCULUS_BUTTON_XPATH)))
                self.driver.find_element(By.XPATH, TestData.OCULUS_BUTTON_XPATH).click()
            except (NoSuchElementException, TimeoutException):
                pass


            """try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, TestData.COOKIE_ACCEPT_XPATH)))
            self.driver.find_element(By.XPATH, TestData.COOKIE_ACCEPT_XPATH).click()
        except NoSuchElementException:
            pass"""

        for i in range(11):
            time.sleep(2)
            self.driver.swipe(470, 1100, 470, 50, 400)

    def test_firstAddCollector(self):

        filename = (self.driver.current_activity + time.strftime("%Y_%m_%d_%H%M%S")).replace(".", "_")

        try:
            element_node = self.driver.find_element(By.XPATH, "//*[@text='Leave feedback on Sponsored ad']/parent::*")
            #element_node.screenshot("test.png")

            #com.amazon.mShop.android.shopping: id / chrome_action_bar_search_icon

            elements = element_node.find_elements(By.XPATH, "//*[@class='android.view.View']")
            element = elements[0]
            print(elements)
            print(len(elements))

            width = element.size["width"]
            height = element.size["height"]
            location_x = element.location["x"]
            location_y = element.location["y"]
            text = element.get_attribute("text")


            self.driver.save_screenshot(f"../Screenshots/First Add/{filename}.png")
            image_path = f"../Screenshots/First Add/{filename}.png"

            #time.sleep(2)
            img = cv2.imread(image_path)

            for i in range(len(elements)):
                filename = (self.driver.current_activity + time.strftime("%Y_%m_%d_%H%M%S")).replace(".", "_")
                element = elements[i]
                print("wysokosc - " + str(element.get_attribute("bounds")))


            self.driver.save_screenshot(f"../Screenshots/First Add/{filename}.png")
            image_path = f"../Screenshots/First Add/{filename}.png"

            time.sleep(2)
            img = cv2.imread(image_path)


                # Attribute
                # bounds : [0,820][1080,1166]
                #cropped_image = img[820:1166, 0:1080]


                #[0,396][1080,743]
            cropped_image = img[396:743, 0:1080]
            cv2.imwrite(f"../Screenshots/First Add/{filename}.png", cropped_image)

        except NoSuchElementException:
            pass
        if os.path.exists(f"../Screenshots/First Add/{filename}.png"):
            assert True
        else:
            print("ERROR")
            assert False

    def test_secondAddCollector(self):

        temp_element_text = []

        try:
            element_node = self.driver.find_element(By.XPATH, "//*[@text='Brands related to your search']/parent::*")

            elements = element_node.find_elements(By.XPATH, "//*[@class='android.view.View']")

            for x in range(6, len(elements), 2):
                filename = (self.driver.current_activity + time.strftime("%Y_%m_%d_%H%M%S")).replace(".", "_")
                element = elements[x]

                """informacje do bazy danych"""
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
                with open("../temp.txt", "a") as file:
                    file.writelines(str(text) + " - " + filename + ".png\n")

            assert True
        except NoSuchElementException:
            print("ERROR")
            pass
        print(temp_element_text)

    def tearDown(self) -> None:
        self.driver.close_app()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(MainActivity)
    unittest.TextTestRunner(verbosity=2).run(suite)