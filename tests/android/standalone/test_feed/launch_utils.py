import json
import time

from conftest import element_utils
from tests.android.common.element_utils import ElementUtils
from tests.android.common.element_selectors import ElementSelectors


class LaunchUtils:
    def __init__(self, element_utils: ElementUtils) -> None:
        self.element_utils = element_utils
        with open("tests/android/standalone/test_feed/elements.json") as json_file:
            launch_elm = json.load(json_file)
        self.element_selectors = ElementSelectors(launch_elm)

    def click_standalone_on_lunch(self):
        selectors = self.element_selectors
        return self.element_utils.click_by_id(selectors.getSelector("button_standalone"),
                                              selectors.getName("button_standalone"))

    def wait_for_empty_landing_page(self) -> bool:
        selectors = self.element_selectors
        return self.element_utils.wait_and_validate_element_displayed_by_id(selectors.getSelector("message_empty_list"),
                                                                            selectors.getName("message_empty_list"), 10)

    def click_on_feed(self):
        selectors = self.element_selectors
        return self.element_utils.click_by_id(selectors.getSelector("feed_button"),
                                              selectors.getName("feed_button"))

    def lookup_feed_upload_OPML_available(self) -> bool:
        selectors = self.element_selectors
        return self.element_utils.wait_and_validate_element_displayed_by_id(selectors.getSelector("opml_button_upload"),
                                                                            selectors.getName("opml_button_upload"), 10)

    def lookup_RSS_feed_upload_plus_button_available(self) -> bool:
        selectors = self.element_selectors
        return self.element_utils.wait_and_validate_element_displayed_by_id(selectors.getSelector("rss_feed_button_upload"),
                                                                            selectors.getName("rss_feed_button_upload"), 10)
    def click_import_OPML(self):
        selectors = self.element_selectors
        return self.element_utils.click_by_id(selectors.getSelector("opml_button_upload"),
                                              selectors.getName("opml_button_upload"))

    def wait_for_sample_file(self):
        selectors = self.element_selectors
        return self.element_utils.wait_and_validate_element_displayed_by_id(selectors.getSelector("sample_file"),
                                                                            selectors.getName("sample_file"), 10)
    def upload_sample_file(self) -> bool:
        # first click on load sample
        selectors = self.element_selectors
        self.element_utils.click_by_element_containing_text('sample.opml')
        # make sure it loads

        count = self.element_utils.count_elements_in_layout_by_uiselector(selectors.getSelector('feed_linear_layout'),
                                                    selectors.getSelector('feed_layout_class'))
        print(f"count...............................................{count}")
        return self.element_utils.wait_and_validate_element_displayed_by_text('Nextcloud', 10)

    def click_upload_rss_feed(self):
        selectors = self.element_selectors
        self.element_utils.click_by_id(selectors.getSelector("rss_feed"),
                                              selectors.getName("rss_feed"))

        return self.element_utils.wait_and_validate_element_displayed_by_id(selectors.getSelector('feed_textbook')
                                                                            ,selectors.getName('feed_textbook'), 10)

    def upload_rss_feed(self, rss_link=None):
        if rss_link is None:
            from tests.config import RSS_FEEDS
            rss_link = RSS_FEEDS["news"]  # Use the news feed by default

        selectors = self.element_selectors
        self.element_utils.send_keys_to_textbox_by_id(
            selectors.getSelector("rss_feed_textbox"),
            selectors.getSelector("rss_feed_textbox"),
            rss_link
        )
        time.sleep(1)  # wait for ui complete
        self.element_utils.click_by_id(
            selectors.getSelector('add_rss_feed_button'),
            selectors.getName('add_rss_feed_button')
        )

    def upload_rss_podcast(self, rss_link=None):
        if rss_link is None:
            from tests.config import RSS_FEEDS
            rss_link = RSS_FEEDS["podcasts"]  # Use the podcast feed now

        selectors = self.element_selectors
        self.element_utils.send_keys_to_textbox_by_id(
            selectors.getSelector("rss_feed_textbox"),
            selectors.getSelector("rss_feed_textbox"),
            rss_link
        )
        time.sleep(1)  # wait for ui complete
        self.element_utils.click_by_id(
            selectors.getSelector('add_rss_feed_button'),
            selectors.getName('add_rss_feed_button')
        )

    def rss_upload_check(self) -> bool:
        return self.element_utils.wait_and_validate_element_displayed_by_text('Gesundheit und Medizin', 10)

    def podcast_upload_check(self)-> bool:
        return self.element_utils.wait_and_validate_element_displayed_by_text('Health Report - Full program podcast', 10)

    def delete_feed(self):
        selectors = self.element_selectors
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('wireless_moves_path'),
                                                 selectors.getName('wireless_moves_path'))
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('delete_wireless_moves'),
                                                        selectors.getName('delete_wireless_moves'))

    def deleted_feed_is_displayed(self) -> bool:
        print('delete wirelesss.............................')
        print(self.element_utils.
              wait_and_validate_element_displayed_by_text('WirelessMoves', 2))
        return self.element_utils.wait_and_validate_element_displayed_by_text('WirelessMoves', 2)

    def open_feed(self):
        self.element_utils.click_by_element_containing_text('Nextcloud')
        self.element_utils.scroll_for_refresh()

    def open_podcast_feed(self):
        self.element_utils.click_by_element_containing_text('Health Report - Full program podcast')

    def feed_list_is_available(self) -> bool:
        selectors = self.element_selectors
        return self.element_utils.wait_and_validate_element_displayed_by_id(selectors.getSelector('feed_list'),
                                                                     selectors.getName('feed_list'), 10)

    def open_feed_tile(self, title: str):
        self.element_utils.click_by_element_containing_text(title)

    def feed_content_displayed(self, descr: str) -> bool:
        return self.element_utils.search_for_text_on_page(descr)


    def exit_back_from_read_view(self):
        selectors = self.element_selectors
        self.element_utils.click_by_automator_value(selectors.getSelector('back_button_read'),
                                                    selectors.getName('back_button_read'))

    def read_feed_content_check(self, title: str):
       return self.element_utils.search_text_on_page_by_XPATH(title)

    def click_feed_setting(self):
        selectors = self.element_selectors
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('feed_settings'),
                                                        selectors.getName('feed_settings'))

    def activate_show_read_news(self):
        selectors = self.element_selectors
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('show_read_news'),
                                                        selectors.getName('show_read_news'))

    def exit_back_from_feed_list(self):
        selectors = self.element_selectors
        self.element_utils.click_by_automator_value(selectors.getSelector('exit_feed_list'),
                                                    selectors.getName('exit_feed_list'))

    def click_feed_setting_remame(self):
        selectors = self.element_selectors
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('feed_setting_for_rename'),
                                                        selectors.getName('feed_setting_for_rename'))

    def click_rename(self):
        selectors = self.element_selectors
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('rename_button'),
                                       selectors.getName('rename_button'))

    def rename_feed(self):
        selectors = self.element_selectors
        self.element_utils.clear_then_send_keys_to_textbox_by_id(
            selectors.getSelector('textfield_rename'),
            selectors.getName('textfield_rename'),
            'Community blog updated')
        self.element_utils.click_by_id(selectors.getSelector('rename_button_textfield'),
                                       selectors.getName('rename_button_textfield'))

    def rename_feed_to_existing(self):
        selectors = self.element_selectors
        self.element_utils.clear_then_send_keys_to_textbox_by_id(
            selectors.getSelector('textfield_rename'),
            selectors.getName('textfield_rename'),
            'Gesundheit und Medizin')
        self.element_utils.click_by_id(selectors.getSelector('rename_button_textfield'),
                                       selectors.getName('rename_button_textfield'))

    def updated_name_persisted(self) -> bool:
        selectors = self.element_selectors
        return self.element_utils.wait_and_validate_element_displayed_by_text('Community blog updated', 10)

    def updated_is_already_existing(self) -> bool:
        return self.element_utils.is_text_duplicated_on_screen('Gesundheit und Medizin')

    def open_podcast_feed(self):
        selectors = self.element_selectors
        self.element_utils.click_by_element_containing_text('Health Report - Full program podcast')

    def feed_is_downloadable(self) -> bool:
        selectors = self.element_selectors
        return self.element_utils.wait_and_validate_element_displayed_by_id(selectors.getSelector('podcast_download'),
                                                                     selectors.getName('podcast_download'),
                                                                     10)

    def refresh_page(self):
        self.element_utils.scroll_for_refresh()

    def back_from_feed_read_view(self):
        selectors = self.element_selectors
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('back_feed_read'),
                                                        selectors.getName('back_feed_read'))

    def exit_podcast_feed(self):
        selectors = self.element_selectors
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('exit_podcast_feed'),
                                                        selectors.getName('exit_podcast_feed'))



