import json

from conftest import element_utils
from tests.android.common.element_utils import ElementUtils
from tests.android.common.element_selectors import ElementSelectors


class BookmarkUtils:
    def __init__(self, element_utils: ElementUtils) -> None:
        self.element_utils = element_utils
        with open("tests/android/standalone/test_bookmarks/elements.json") as json_file:
            launch_elm = json.load(json_file)
        self.element_selectors = ElementSelectors(launch_elm)

    def bookmark_article(self):
        selectors = self.element_selectors
        self.element_utils.click_first_list_view_items_by_id(selectors.getSelector('feed_list'),
                                                             selectors.getName('feed_list'))
        self.element_utils.click_by_accessibility_id(selectors.getSelector('bookmark_button'),
                                       selectors.getName('bookmark_button'))
        # go back to feed
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('back_to_feed_button'),
                                       selectors.getName('back_to_feed_button'))

    def open_bookmarks(self):
        selectors = self.element_selectors
        self.element_utils.click_by_id(selectors.getSelector('bookmark_tab'),
                                       selectors.getName('bookmark_tab'))

    def validate_bookmarked(self) -> bool:
        selectors = self.element_selectors
        return self.element_utils.list_element_has_at_least_one_element(selectors.getSelector('feed_list'))

    def remove_from_bookmark(self):
        # click first element
        selectors = self.element_selectors
        self.element_utils.click_first_list_view_items_by_id(selectors.getSelector('feed_list'),
                                                             selectors.getName('feed_list'))

        # click to remove bookmark
        self.element_utils.click_by_accessibility_id(selectors.getSelector('bookmark_remove_button'),
                                       selectors.getName('bookmark_remove_button'))
        # go back to feed
        self.element_utils.click_by_ANDROID_UIAUTOMATOR(selectors.getSelector('back_from_read_button'),
                                                        selectors.getName('back_from_read_button'))

