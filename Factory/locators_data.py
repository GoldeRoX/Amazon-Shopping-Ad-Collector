class LocatorsData:

    search_icon_ENG = '(//android.widget.LinearLayout[@content-desc="Search"])[1]/android.widget.LinearLayout/android.widget.TextView'
    # search_icon_DE = '//android.widget.LinearLayout[@content-desc="Suche"]'

    search_input_ENG = 'com.amazon.mShop.android.shopping:id/rs_search_src_text'
    # search_input_DE = 'com.amazon.mShop.android.shopping:id/rs_search_src_text'

    BOTTOM_AD_ENG = "//*[@text='Leave feedback on Sponsored ad']/parent::*/following-sibling::*/child::*"
    # BOTTOM_AD_DE = "//*[@text='Feedback zur gesponserten Werbeanzeige geben']/parent::*/following-sibling::*/child::*"

    brands_related_to_your_search_element_node_ENG = "//*[contains(@text, 'Brands related to your search')]/parent::*"
    # brands_related_to_your_search_element_node_DE = "//*[contains(@text, 'Marken verwandt mit Ihrer Suche')]/parent::*"

    ad_4_node_ENG = "//*[starts-with(@text,'Sponsored Ad -')]/parent::*"