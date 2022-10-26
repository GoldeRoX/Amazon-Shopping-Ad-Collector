class ENG:
    search_icon = '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView '
    search_input = 'com.amazon.mShop.android.shopping:id/rs_search_src_text'
    BOTTOM_AD = "//*[@text='Leave feedback on Sponsored ad']/parent::*/parent::*"
    BOTTOM_AD_TEXT_ELEMENT = "//*[@text='Leave feedback on Sponsored ad']"
    brands_related_to_your_search_element_node = "//*[contains(@text, 'Brands related to your search')]/parent::*"
    ad_4_node = "//*[starts-with(@text,'Sponsored Ad -')]/parent::*"
    ad_5_node = "//*[starts-with(@text,'Sponsored')]/parent::*"
    ad_5_starts_with = "Sponsored"
    ad_2_starts_with = "Sponsored ad from"
    ad_7 = "//*[starts-with(@text, 'Sponsored ad from')]/parent::*/parent::*"
    # ad_video = "//*[starts-with(@text, 'Gesponsertes Video stummschalten')]"
    App_close = "android:id/aerr_close"


class DE:
    search_icon = '//android.widget.LinearLayout[@content-desc="Suche"]'
    search_input = 'com.amazon.mShop.android.shopping:id/rs_search_src_text'
    BOTTOM_AD = "//*[@text='Feedback zur gesponserten Werbeanzeige geben']/parent::*/parent::*"
    BOTTOM_AD_TEXT_ELEMENT = "//*[@text='Feedback zur gesponserten Werbeanzeige geben']/parent::*"
    brands_related_to_your_search_element_node = "//*[contains(@text, 'Marken verwandt mit Ihrer Suche')]/parent::*"
    ad_4_node = "//*[starts-with(@text,'Gesponserte Anzeige –')]/parent::*"
    ad_5_node = "//*[starts-with(@text,'Gesponsert')]/parent::*"
    ad_5_starts_with = "Gesponsert"
    ad_2_starts_with = "Gesponserte Werbeanzeige von"
    ad_video = "//*[starts-with(@text, 'Gesponsertes Video stummschalten')]/parent::*/parent::*"
    App_schlieBen = "android:id/aerr_close"
    ad_7 = "//*[starts-with(@text, 'Gesponserte Werbeanzeige von')]/parent::*/parent::*"



