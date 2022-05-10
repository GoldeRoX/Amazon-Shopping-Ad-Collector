from telnetlib import EC
from traceback import print_stack

from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class BaseAd:

    def __init__(self, driver):
        self.driver = driver
    
    def get_by_type(self, locator_type):
        locator_type = locator_type.lower()
        if locator_type == "accessibilityid":
            # iOS: accessibility-id
            # Android: content-desc
            return MobileBy.ACCESSIBILITY_ID
        elif locator_type == "classname":
            # iOS: full name of the XCUI element and begins with XCUIElementType
            # Android: full name of the UIAutomator2 class (e.g.: android.widget.TextView)
            return By.CLASS_NAME
        elif locator_type == "id":
            # Native element identifier. resource-id for android; name for iOS.
            return By.ID
        elif locator_type == "name":
            return By.NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "image":
            return MobileBy.IMAGE
        elif locator_type == "uiautomator":
            # UIAutomator2 only
            return MobileBy.ANDROID_UIAUTOMATOR
        elif locator_type == "viewtag":
            # Espresso only
            return MobileBy.ANDROID_VIEWTAG
        elif locator_type == "datamatcher":
            # Espresso only
            return MobileBy.ANDROID_DATA_MATCHER
        elif locator_type == "classchain":
            # iOS only
            return MobileBy.IOS_CLASS_CHAIN
        elif locator_type == "linktext":
            return By.LINK_TEXT
        else:
            print("Locator type not supported - or check the argument you passed in")
        return False

    def wait_for_element_to_appear(self, locator, locator_type="accessibilityid",
                                   timeout=10, pollFrequency=0.5):
        element = None
        try:
            by_type = self.get_by_type(locator_type)
            print("Waiting for element with locator: '" + locator + "' to appear")
            wait = WebDriverWait(self.driver, timeout=timeout,
                                 poll_frequency=pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            element = wait.until(EC.visibility_of_element_located((by_type, locator)))
        except:
            print_stack()
        return element

    def get_element(self, locator, locator_type="accessibilityid"):
        element = None
        try:
            element = self.wait_for_element_to_appear(locator=locator, locator_type=locator_type)
            print("Element found with locator: '" + locator + "'")
        except:
            print("Element not found with locator: '" + locator + "'")
        return element