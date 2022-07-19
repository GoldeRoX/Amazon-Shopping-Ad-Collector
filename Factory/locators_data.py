class LocatorsDataENG:

    search_icon = '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView'
    search_input = 'com.amazon.mShop.android.shopping:id/rs_search_src_text'
    BOTTOM_AD = "//*[@text='Leave feedback on Sponsored ad']/parent::*/parent::*"
    brands_related_to_your_search_element_node = "//*[contains(@text, 'Brands related to your search')]/parent::*"
    ad_4_node = "//*[starts-with(@text,'Sponsored Ad -')]/parent::*"
    ad_5_node = "//*[starts-with(@text,'Sponsored')]/parent::*"


class LocatorsDataDE:

    search_icon = '//android.widget.LinearLayout[@content-desc="Suche"]'
    search_input = 'com.amazon.mShop.android.shopping:id/rs_search_src_text'
    BOTTOM_AD = "//*[@text='Feedback zur gesponserten Werbeanzeige geben']/parent::*/parent::*"
    brands_related_to_your_search_element_node = "//*[contains(@text, 'Marken verwandt mit Ihrer Suche')]/parent::*"
    ad_4_node = "//*[starts-with(@text,'Gesponserte Anzeige –')]/parent::*"
    ad_5_node = "//*[starts-with(@text,'Gesponsert')]/parent::*"