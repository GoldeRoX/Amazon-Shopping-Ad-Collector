import re
import time
import unittest

from appium import webdriver
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
        """self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, TestData.SEARCH_ICON_AMAZON_XPATH).click()

        self.driver.implicitly_wait(10)
        self.driver.find_element(By.XPATH, TestData.SEARCH_AMAZON_SEND_TXT_XPATH).send_keys("oculus")"""
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
                self.driver.swipe(470, 1100, 470, 50, 400)
                time.sleep(1)
            except:
                pass

    def test_firstAddCollector(self):

        ts = time.strftime("%Y_%m_%d_%H%M%S")
        activityname = self.driver.current_activity
        filename = activityname + ts
        filename.replace(".", "_")


        """try:
            element = self.driver.find_element(By.XPATH, '//android.view.View[contains(@text, "Next→")]').
            x = re.findall('[0-9]+', element.)
            if self.driver.find_element(By.XPATH, TestData.NEXT_BUTTON_SHOP_XPATH + f'[{i}]/android.view.View[3]/android.view.View').text == 'Leave feedback on Sponsored ad':
                pass
                #y = re.findall('[0-9]', TestData.NEXT_BUTTON_SHOP_XPATH)
                #print(y)
                #numbers = y[2]+y[3]
                #print(numbers)
                #self.driver.find_element(By.XPATH, ).text == 'Next→'
            self.driver.find_element(By.XPATH, TestData.FIRST_ADD_XPATH_1+f'[{number-1}]/android.view.View[1]').screenshot(f"../Screenshots/First Add/{filename}.png")
            assert True
        except NoSuchElementException:
            pass
        assert False"""
        #---------------------
        """ts = time.strftime("%Y_%m_%d_%H%M%S")
        activityname = self.driver.current_activity
        filename = activityname + ts
        filename.replace(".", "_")
        try:
            time.sleep(1)
            image = self.driver.find_element(By.XPATH, TestData.FIRST_ADD_XPATH_2).screenshot(f"../Screenshots/First Add/{filename}.png")
            #image = self.driver.find_element(By.ID, 'c620bb10-288e-42b2-9a4b-c1afba471868').screenshot(f"../Screenshots/First Add/{filename}.png")
            assert True
        except NoSuchElementException:
            pass
        assert False
        """

    def tearDown(self) -> None:
        self.driver.close_app()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(MainActivity)
    unittest.TextTestRunner(verbosity=2).run(suite)

"""http://pentagonlabs.pl/logowanie4labswww/index.php"""