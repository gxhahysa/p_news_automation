import pytest
from .bookmark_utils import BookmarkUtils


@pytest.fixture(scope="session")
def bookmark_utils(element_utils):
    bookmark_utils = BookmarkUtils(
        element_utils
    )
    yield bookmark_utils


@pytest.mark.dependency()
def test(bookmark_utils):
    bookmark_utils.bookmark_article()
    bookmark_utils.open_bookmarks()
    assert bookmark_utils.validate_bookmarked, "Bookmarking didnt work!"
    bookmark_utils.remove_from_bookmark()
    assert not bookmark_utils.validate_bookmarked(), "Bookmark was not removed"
