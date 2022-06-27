from appium import webdriver  # import Appium-Python-Client 2.2.0
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriver(object):
    __platformName = "Android"
    __platformVersion = "9"
    __automationName = "UiAutomator2"
    __appPackage = "com.amazon.mShop.android.shopping"
    __appActivity = "com.amazon.mShop.home.HomeActivity"
    __deviceName = "emulator-5554"
    __uiautomator2ServerLaunchTimeout = "40000"
    __iosInstallPause = "8000"
    __wdaStartupRetryInterval = "20000"
    __newCommandTimeout = "20000"
    __skipDeviceInitialization = "True"
    __skipServerInstallation = "True"
    __noReset = "True"

    def __init__(self, platform_name=__platformName, platform_version=__platformVersion,
                 automation_name=__automationName, app_package=__appPackage, app_activity=__appActivity,
                 device_name=__deviceName, uiautomator_2_server_launch_timeout=__uiautomator2ServerLaunchTimeout,
                 ios_install_pause=__iosInstallPause, wda_startup_retry_interval=__wdaStartupRetryInterval,
                 new_command_timeout=__newCommandTimeout, skip_device_initialization=__skipDeviceInitialization,
                 skip_server_installation=__skipServerInstallation, no_reset=__noReset):
        __desired_caps = {
            "platformName": platform_name,
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
            "noReset": no_reset
        }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", __desired_caps)


class Base(object):

    def send_text(self, by_type, path: str, text_to_send: str) -> None:
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((by_type, path)))
            self.driver.find_element(by_type, path).send_keys(text_to_send)
        except (NoSuchElementException, TimeoutException):
            print("No such Input field")


driver = WebDriver().driver
