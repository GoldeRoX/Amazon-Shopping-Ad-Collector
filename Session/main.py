import os
import time
import unittest

import cv2  # import opencv-python	4.5.5.64
from appium import webdriver  # import Appium-Python-Client 2.2.0
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from TestData.config import TestData


class MainActivity(unittest.TestCase):

    def setUp(self) -> None:

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", TestData.APPIUM_DESC)

        self.driver.implicitly_wait(10)
        time.sleep(2)
        self.driver.find_element(By.ID, TestData.SKIP_REDIRECT_MARKETPLACE_ID).click()

        self.driver.implicitly_wait(10)
        time.sleep(2)
        self.driver.find_element(By.ID, TestData.SKIP_SIGN_IN_BUTTON_ID).click()

        """search item"""
        try:
            self.driver.implicitly_wait(10)
            self.driver.find_element(By.XPATH, TestData.SEARCH_ICON_AMAZON_XPATH).click()

            self.driver.implicitly_wait(10)
            self.driver.find_element(By.XPATH, TestData.SEARCH_AMAZON_SEND_TXT_XPATH).send_keys("oculus")
        except:
            self.driver.implicitly_wait(10)
            time.sleep(2)
            self.driver.find_element(By.XPATH, TestData.OCULUS_BUTTON_XPATH).click()

        try:
            self.driver.implicitly_wait(10)
            time.sleep(2)
            self.driver.find_element(By.XPATH, TestData.COOKIE_ACCEPT_XPATH).click()
        except:
            pass

        for i in range(11):
            try:
                time.sleep(2)
                self.driver.swipe(470, 1100, 470, 50, 400)
            except:
                pass

    def test_firstAddCollector(self):
        ts = time.strftime("%Y_%m_%d_%H%M%S")
        activity_name = self.driver.current_activity
        filename = activity_name + ts
        filename.replace(".", "_")

        try:
            self.driver.save_screenshot(f"../Screenshots/First Add/{filename}.png")
            image_path = f"../Screenshots/First Add/{filename}.png"

            time.sleep(2)
            img = cv2.imread(image_path)

            # Attribute
            # bounds : [0,820][1080,1166]
            cropped_image = img[820:1166, 0:1080]
            cv2.imwrite(f"../Screenshots/First Add/{filename}.png", cropped_image)

        except:
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
                ts = time.strftime("%Y_%m_%d_%H%M%S")
                activity_name = self.driver.current_activity
                filename = activity_name + ts
                filename.replace(".", "_")
                element = elements[x]

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

            assert True
        except:
            print("ERROR")
            pass
        print(temp_element_text)

    def tearDown(self) -> None:
        self.driver.close_app()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(MainActivity)
    unittest.TextTestRunner(verbosity=2).run(suite)
