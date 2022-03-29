
class TestData:
    APPIUM_DESC = {
      "platformName": "Android",
      "appium:platformVersion": "9",
      "appium:automationName": "UiAutomator2",
      "appium:appPackage": "com.amazon.mShop.android.shopping",
      "appium:appActivity": "com.amazon.mShop.home.HomeActivity",
      "appium:deviceName": "emulator-5554"
    }

    SKIP_SIGN_IN_BUTTON_ID = 'com.amazon.mShop.android.shopping:id/skip_sign_in_button'

    REDIRECT_MARKETPLACE_ID = 'com.amazon.mShop.android.shopping:id/btn_redirect_marketplace'

    SKIP_REDIRECT_MARKETPLACE_ID = 'com.amazon.mShop.android.shopping:id/btn_cancel'

    OCULUS_BUTTON_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View'


    SEARCH_ICON_AMAZON_XPATH = '(//android.widget.LinearLayout[@content-desc="Szukaj"])[2]/android.widget.ImageView'

    SEARCH_AMAZON_SEND_TXT_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.EditText'

    COOKIE_ACCEPT_XPATH = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View/android.view.View[3]/android.view.View/android.widget.Button"
    #--------------------#

    FIRST_ADD_XPATH_1 = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View[63]/android.view.View[1]'
    FIRST_ADD_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View[63]/android.view.View[1]/android.view.View'

    BOTTOM_ADDS_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[1]/android.view.View/android.view.View[61]'