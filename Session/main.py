import re
import time
import unittest

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
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

        for i in range(16):
            try:
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
            image = self.driver.find_element(By.XPATH, TestData.FIRST_ADD_XPATH_1).screenshot(f"../Screenshots/First Add/{filename}.png")
        except:
            pass
        assert True

    def test_secondAddCollector(self):

        time.sleep(5)
        ts = time.strftime("%Y_%m_%d_%H%M%S")
        activityname = self.driver.current_activity
        filename = activityname + ts
        filename.replace(".", "_")

        temp_element_text = []



        try:
            element_node = self.driver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View[64]/android.view.View[3]/android.view.View")

            #element_node.screenshot(f"../Screenshots/Second Add/{filename}.png")
            #print(element_node.text)

            elements = element_node.find_elements(By.XPATH, "//*[@class='android.view.View']")

            for x in range(len(elements)):
                element = elements[x]

                text = element.get_attribute("text")
                if str(text) != "":
                    temp_element_text.append(str(text))
                    element.screenshot(f"../Screenshots/Second Add/{filename}.png")


            assert True
        except:
            print("no")



        print(temp_element_text)






    def tearDown(self) -> None:
        self.driver.close_app()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(MainActivity)
    unittest.TextTestRunner(verbosity=2).run(suite)

"""http://pentagonlabs.pl/logowanie4labswww/index.php"""