import pytest
from .news_utils import NewsUtils


@pytest.fixture(scope="session")
def news_utils(element_utils):
    news_utils = NewsUtils(
        element_utils
    )
    yield news_utils

@pytest.mark.dependency(depends=["test_read_feed_content_dissapears_check"])
def test_news_view(news_utils):
    news_utils.open_main_news_feed()
    assert news_utils.feed_list_is_available(), "Feed list isnt shown on main feed"
