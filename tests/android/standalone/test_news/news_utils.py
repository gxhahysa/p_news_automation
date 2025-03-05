import json

from conftest import element_utils
from tests.android.common.element_utils import ElementUtils
from tests.android.common.element_selectors import ElementSelectors


class NewsUtils:
    def __init__(self, element_utils: ElementUtils) -> None:
        self.element_utils = element_utils
        with open("tests/android/standalone/test_news/elements.json") as json_file:
            launch_elm = json.load(json_file)
        self.element_selectors = ElementSelectors(launch_elm)


    def open_main_news_feed(self):
        selectors = self.element_selectors
        self.element_utils.click_by_id(selectors.getSelector('news_feed_button'),
                                       selectors.getName('news_feed_button'))


    def feed_list_is_available(self) -> bool:
        selectors = self.element_selectors
        # return (self.element_utils.wait_and_validate_element_displayed_by_id
        #         (selectors.getSelector('feed_list'),
        #         selectors.getName('feed_list'), 10))
        return self.element_utils.list_element_has_at_least_one_element(selectors.getSelector('feed_list'))