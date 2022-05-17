import time

from appium import webdriver  # import Appium-Python-Client 2.2.0
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC


class Search:

    def __init__(self):
        appium_desc = {
            "platformName": "Android",
            "appium:platformVersion": "9",
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": "com.amazon.mShop.android.shopping",
            "appium:appActivity": "com.amazon.mShop.home.HomeActivity",
            "appium:deviceName": "emulator-5554"
        }
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", appium_desc)

    #create interface that will choose id or xpath or other by.
    def if_exist_click(self):
        pass

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
                (By.XPATH,
                 '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView')))
        except (NoSuchElementException, TimeoutException):
            self.driver.find_element(By.XPATH,
                                     '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView').click()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text")))
            self.driver.find_element(By.ID, "com.amazon.mShop.android.shopping:id/rs_search_src_text").send_keys(
                "oculus oculus 2")
            self.driver.press_keycode(66)
        except (NoSuchElementException, TimeoutException):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]'
                                                    '/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View')))
                self.driver.find_element(By.XPATH,
                                         '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]'
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


test = Search()
test.setUp()
