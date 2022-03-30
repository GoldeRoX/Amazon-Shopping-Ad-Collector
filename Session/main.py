import os
import re
import time
import unittest

import cv2
import numpy as np
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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

        for i in range(13):
            try:
                time.sleep(1)
                self.driver.swipe(470, 1100, 470, 50, 400)
                time.sleep(1)
            except:
                pass

    def test_firstAddCollector(self):
        ts = time.strftime("%Y_%m_%d_%H%M%S")
        activityname = self.driver.current_activity
        filename = activityname + ts
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
            assert False

    def test_secondAddCollector(self):

        ts = time.strftime("%Y_%m_%d_%H%M%S")
        activityname = self.driver.current_activity
        filename = activityname + ts
        filename.replace(".", "_")

        temp_element_text = []
        temp_element_b = []

        try:
            element_node = self.driver.find_element(By.XPATH, "//*[@text='Brands related to your search']/parent::*")

            elements = element_node.find_elements(By.XPATH, "//*[@class='android.view.View']")

            for x in range(6, len(elements), 2):
                element = elements[x]

                text = element.get_attribute("text")
                print(element.location_in_view)
                #bounds = element.get_attribute("bounds").values()
                #print(bounds.mapping)
                #size = element.size
                #w = size['width']

                #print(w)
                temp_element_text.append(str(text))
                #element.screenshot(f"../ScreenshotsBrands related to your search/{filename}.png")

                self.driver.save_screenshot(f"../Screenshots/Brands related to your search/{filename}.png")
                image_path = f"../Screenshots/Brands related to your search/{filename}.png"

                time.sleep(2)
                img = cv2.imread(image_path)

                # Attribute
                # bounds : [44,1471][704,1977]
                cropped_image = img[1471:1977, 44:704]
                cv2.imwrite(f"../Screenshots/Brands related to your search/{filename}.png", cropped_image)



                #x = 400  /// y = 1700    | x = 800 /// y = 1700

                #self.driver.swipe(100, 1500, 500, 1500)
                #self.driver.execute_script('mobile: scroll', {"element": elements[x+1], "toVisible": True})
                action = TouchAction(self.driver)
                action.press(element).move_to(x=-353, y=0).release().perform()

            assert True
        except:
            print("error")

        #print(temp_element_b)
        print(temp_element_text)

    def tearDown(self) -> None:
        self.driver.close_app()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(MainActivity)
    unittest.TextTestRunner(verbosity=2).run(suite)
