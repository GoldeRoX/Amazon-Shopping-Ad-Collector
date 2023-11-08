import os
import time
import cv2

import yaml
from appium import webdriver
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, \
    StaleElementReferenceException, InvalidSessionIdException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from typing import Tuple
from appium.webdriver.webdriver import WebDriver

from amazonadcollector.locators_data import Lang


class MyDriver(object):

    def __init__(self, platform_name="Android", platform_version="9",
                 automation_name="UiAutomator2", app_package="com.amazon.mShop.android.shopping",
                 app_activity="com.amazon.mShop.home.HomeActivity", device_name="emulator-5554",
                 uiautomator_2_server_launch_timeout=40000, ios_install_pause=8000,
                 wda_startup_retry_interval=20000, new_command_timeout=20000, skip_device_initialization=True,
                 skip_server_installation=True, no_reset=True, normalize_tag_names=True, udid="emulator-5554"):
        desired_caps = {
            "platformName": platform_name,
            "udid": udid,
            "appium:platformVersion": platform_version,
            "appium:automationName": automation_name,
            "appium:appPackage": app_package,
            "appium:appActivity": app_activity,
            "appium:deviceName": device_name,
            "uiautomator2ServerLaunchTimeout": uiautomator_2_server_launch_timeout,
            "iosInstallPause": ios_install_pause,
            "wdaStartupRetryInterval": wda_startup_retry_interval,
            "newCommandTimeout": new_command_timeout,
            "skipDeviceInitialization": skip_device_initialization,
            "skipServerInstallation": skip_server_installation,
            "noReset": no_reset,
            "normalizeTagNames": normalize_tag_names,
            "videoCodec": 'libx264',
            "app": os.path.join(os.path.dirname(__file__), "../amazon_apk/amazon.apk")
        }
        self.driver = webdriver.Remote(command_executor="http://localhost:4723/wd/hub",
                                       desired_capabilities=desired_caps)


class BaseMethods(object):

    def __init__(self, driver):
        self.__driver: WebDriver = driver
        self.__lang = Lang().get_lang()

    def config_app_settings(self):

        if self.__lang.__class__.__name__ == "DE":
            pass
            # TODO refactor for the new Amazon auto-update
            self.change_setting_to_de()
        elif self.__lang.__class__.__name__ == "UK":
            pass
            # TODO refactor for the new Amazon auto-update
            # base_methods.change_setting_to_uk()

    def get_element_when_located(self, by_type, path: str, time_to_wait: int = 5) -> WebElement:
        try:
            return WebDriverWait(self.__driver, time_to_wait).until(
                EC.presence_of_element_located((by_type, path)))
        except InvalidSessionIdException:
            pass

    def send_text(self, by_type, path: str, text_to_send: str) -> None:
        try:
            self.get_element_when_located(by_type, path).send_keys(text_to_send)
        except (NoSuchElementException, TimeoutException):
            print('No "Search Input" field')

    def first_launch(self) -> None:
        """this method will be executed when the emulator had a reset or is a new one"""
        try:
            self.get_element_when_located(AppiumBy.ID, "com.amazon.mShop.android.shopping:id/btn_cancel").click()
        except (NoSuchElementException, TimeoutException):
            pass
        try:
            self.get_element_when_located(AppiumBy.ID,
                                          "com.amazon.mShop.android.shopping:id/skip_sign_in_button").click()
        except (NoSuchElementException, TimeoutException):
            pass

    def get_page(self, phrase_to_search: str) -> None:
        """

                Args:
                    phrase_to_search: phrase used for going to next page

                Returns:
                    None

                """""

        try:
            self.get_element_when_located(AppiumBy.XPATH, self.__lang.search_icon, time_to_wait=10).click()
        except (NoSuchElementException, TimeoutException, AttributeError):
            try:
                self.get_element_when_located(AppiumBy.ID,
                                              "com.amazon.mShop.android.shopping:id/"
                                              "chrome_action_bar_search_icon").click()
            except Exception as e:
                print(e)

        self.send_text(AppiumBy.ID, 'com.amazon.mShop.android.shopping:id/rs_search_src_text', phrase_to_search)

        """press enter"""
        self.__driver.press_keycode(66)

    def amazon_not_responding_close(self):
        try:
            close = self.__driver.find_elements(AppiumBy.ID, "android:id/aerr_close")
            close[0].click()
        except (IndexError, WebDriverException):
            pass

    def config_start(self) -> None:
        # TODO change xpath for multi lang (config)
        xpath = "//*[@text='Land/Region: Vereinigte Staaten (United States)']"
        try:
            self.get_element_when_located(AppiumBy.XPATH, xpath, time_to_wait=15).click()
            time.sleep(4)
            TouchAction(self.__driver).tap(None, 500, 500, 1).perform()
            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Fertig']", time_to_wait=8).click()
        except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
            pass

    def cookies_click(self) -> None:
        try:
            self.__driver.find_element(AppiumBy.ID, "cc-banner-accept").click()
            return
        except NoSuchElementException:
            try:
                self.__driver.find_element(AppiumBy.XPATH, self.__lang.accept_cookies).click()
                return
            except NoSuchElementException:
                return

    def change_setting_to_uk(self):
        self.get_element_when_located(AppiumBy.ACCESSIBILITY_ID, "Menu. Contains your orders, your account, shop by"
                                                                 " department, programs and features, settings,"
                                                                 " and customer service Tab 4 of 4").click()

        time.sleep(10)
        while True:
            try:
                self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Settings']", time_to_wait=1).click()
                break
            except (NoSuchElementException, TimeoutException):
                Scroll(self.__driver).scroll_down()

        Scroll(self.__driver).scroll_down()
        self.get_element_when_located(AppiumBy.XPATH, "//*[starts-with(@text,'Country')]", time_to_wait=10).click()

        try:
            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Country/Region: United States']",
                                          time_to_wait=10).click()
        except (NoSuchElementException, TimeoutException):
            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Done']").click()
            return
        TouchAction(self.__driver).tap(x=403, y=330).perform()

        for i in range(8):
            Scroll(self.__driver).scroll_down()
        TouchAction(self.__driver).tap(x=403, y=330).perform()
        time.sleep(3)

        self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Currency: US$ - USD - US Dollar']").click()
        time.sleep(3)
        TouchAction(self.__driver).tap(x=354, y=603).perform()

        self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Done']").click()
        return

    def change_setting_to_de(self) -> None:
        try:
            self.get_element_when_located(AppiumBy.ACCESSIBILITY_ID, "Menu. Contains your orders, your account, shop by"
                                                                     " department, programs and features, settings,"
                                                                     " and customer service Tab 4 of 4").click()

            self.get_element_when_located(AppiumBy.ACCESSIBILITY_ID, "Settings menu header. Tap to expand and hear "
                                                                     "list of settings", 60).click()
            self.get_element_when_located(AppiumBy.ACCESSIBILITY_ID, "Country and Language selector").click()

            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Country/Region: United States']").click()
            self.get_element_when_located(AppiumBy.XPATH, "//*[starts-with(@text,'Germany')]").click()

            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Language: English']").click()
            self.get_element_when_located(AppiumBy.XPATH, "//*[starts-with(@text,'German')]").click()

            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Währung: $ - USD - US-Dollar']").click()
            try:
                self.get_element_when_located(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/"
                                                              "android.widget.LinearLayout/android.widget.FrameLayout/"
                                                              "android.view.ViewGroup/android.widget.FrameLayout[2]/"
                                                              "android.widget.FrameLayout/android.widget"
                                                              ".RelativeLayout/"
                                                              "android.widget.RelativeLayout/android.webkit.WebView/"
                                                              "android.webkit.WebView/android.view.View[1]/"
                                                              "android.view.View/android.view.View[7]/"
                                                              "android.widget.RadioButton[3]").click()
            except NoSuchElementException:
                self.get_element_when_located(AppiumBy.XPATH, "//*[@text='€ - EUR - Euro']").click()

            self.get_element_when_located(AppiumBy.XPATH, "//*[@text='Fertig']").click()
        except (NoSuchElementException, TimeoutException):
            return


def save_cropped_scr(driver: WebDriver, ad, filename: str) -> None:
    config_path = os.path.join(os.path.dirname(__file__), "../data/config.yaml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    date_folder_name = datetime.now().strftime("%Y-%m-%d")

    save_path = config["COMPUTER"]["SAVE_PATH"]

    if not os.path.exists(f"{save_path}/DE"):
        os.mkdir(f"{save_path}/DE")

    if not os.path.exists(f"{save_path}/UK"):
        os.mkdir(f"{save_path}/UK")

    if not os.path.exists(f"{save_path}/{config['APP']['LANG']}/{date_folder_name}"):
        os.mkdir(f"{save_path}/{config['APP']['LANG']}/{date_folder_name}")

    img_name = filename

    image_path = f"{save_path}/{config['APP']['LANG']}/{date_folder_name}/{str(img_name)}.png"
    driver.save_screenshot(image_path)
    img = cv2.imread(image_path)

    cropped_image = img[
                    ad.location_y:ad.location_y + ad.height,
                    ad.location_x:ad.location_x + ad.width
                    ]
    try:
        cv2.imwrite(image_path, cropped_image)
        return
    except cv2.error as error:
        print(error)
        return


class Scroll(object):
    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.actions = ActionChains(self.driver)

    def scroll_down(self, y: int = 600) -> None:
        """
            scroll down through app Y axis

            default: value is y=600
        """
        self.press_and_move_to_location(start_location=(0, 1100), end_location=(0, 1100 - y))

    def press_and_move_to_location(self,
                                   start_location: Tuple[int, int],
                                   end_location: Tuple[int, int],
                                   ):
        x1, y1 = start_location
        x2, y2 = end_location

        self.actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        self.actions.w3c_actions.pointer_action.move_to_location(x1, y1)
        self.actions.w3c_actions.pointer_action.pointer_down()
        self.actions.w3c_actions.pointer_action.move_to_location(x2, y2)
        self.actions.w3c_actions.pointer_action.pointer_up()
        self.actions.perform()
