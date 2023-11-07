import os
import yaml


class Lang(object):

    __lang = None

    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), "../data/config.yaml"), "r") as file:
            __config = yaml.safe_load(file)

        if __config["APP"]["LANG"] == "DE":
            self.__lang = DE()
        elif __config["APP"]["LANG"] == "UK":
            self.__lang = UK()

    def get_lang(self):
        return self.__lang


class UK(object):
    main_page_carousel_of_ads = "//*[starts-with(@resource-id,'mobile-hero-order')]"
    main_page_banner_ad_id = "ape_gateway_atf_mshop_wrapper"
    search_icon = '(//android.widget.LinearLayout[@content-desc="Search"])[1]/' \
                  'android.widget.LinearLayout/android.widget.TextView '
    search_input = 'com.amazon.mShop.android.shopping:id/rs_search_src_text'
    ad_5_node = "//*[starts-with(@text, 'Sponsored')]/parent::*"
    ad_5_starts_with = "Sponsored"
    sponsored = "Sponsored"
    ad_video = "//*[starts-with(@text, 'Sponsored video')]/parent::*/parent::*"
    brands_related_to_your_search_element_node = "//*[@text='Brands related to your search']/parent::*"
    Items_related_to_your_search_element_node = "//*[@text='Items related to your search']/parent::*"
    ad_2_starts_with = "Sponsored ad from"
    # ad_4_starts_with = "Sponsored Ad –"
    ad_7 = "//*[starts-with(@text, 'Sponsored ad from')]/parent::*/parent::*"
    ad_7_text_starts_with = "Sponsored ad from"
    ad_1 = "//*[starts-with(@text, 'Sponsored ad from')]/parent::*/parent::*/parent::*/parent::*"
    ad_1_text_starts_with = "Sponsored ad from"
    accept_cookies = "//*[@text='Accept Cookies']"


class DE(object):
    main_page_carousel_of_ads = "//*[starts-with(@resource-id,'mobile-hero-order')]"
    main_page_banner_ad_id = "//*[@text='Feedback zu gesponserter Anzeige geben']/parent::*/parent::*/parent::*"
    search_icon = "//android.widget.LinearLayout[@content-desc='Suche']"
    search_input = "com.amazon.mShop.android.shopping:id/rs_search_src_text"
    BOTTOM_AD = "//*[@text='Feedback zur gesponserten Werbeanzeige geben']/parent::*/parent::*"
    BOTTOM_AD_TEXT_ELEMENT = "//*[@text='Feedback zur gesponserten Werbeanzeige geben']/parent::*"
    brands_related_to_your_search_element_node = "//*[ends-with(@text, 'mit Ihrer Suche')]/parent::*"
    Items_related_to_your_search_element_node = "//*[@text='Artikel im Zusammenhang mit Ihrer Suche']/parent::*"
    ad_4_node = "//*[starts-with(@text,'Gesponserte Anzeige –')]/parent::*"
    ad_5_node = "//*[starts-with(@text,'Gesponsert')]/parent::*"
    ad_5_starts_with = "Gesponsert"
    sponsored = "Gesponsert"
    ad_2_starts_with = "Gesponserte Werbeanzeige von"
    ad_video = "//*[starts-with(@text, 'Gesponsertes Video stummschalten')]/parent::*/parent::*"
    App_schlieBen = "android:id/aerr_close"
    ad_7 = "//*[starts-with(@text, 'Gesponserte Werbeanzeige von')]/parent::*/parent::*"
    ad_7_text_starts_with = "Gesponserte Werbeanzeige von"
    ad_1 = "//*[starts-with(@text, 'Gesponserte Werbeanzeige von')]/parent::*/parent::*/parent::*/parent::*"
    ad_1_text_starts_with = "Gesponserte Werbeanzeige von"
    accept_cookies = "//*[@text='Cookies akzeptieren']"
    searched_product_banner = "//*[@text='Feedback zu gesponserter Anzeige geben']/parent::*/parent::*"

