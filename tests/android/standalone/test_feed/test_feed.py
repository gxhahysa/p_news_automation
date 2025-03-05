import time
import pytest
from .launch_utils import LaunchUtils
from tests.android.common.feed_fetcher import FeedFetcher


@pytest.fixture(scope="session")
def launch_utils(element_utils):
    launch_utils = LaunchUtils(
        element_utils
    )
    yield launch_utils


# tests/android/standalone/test_feed/test_feed.py
@pytest.fixture
def feed_fetcher(rss_feeds):
    """Create a feed fetcher using the default RSS feed."""
    fetcher = FeedFetcher("default")  # Use the key from RSS_FEEDS
    success = fetcher.fetch_feed()
    if not success:
        pytest.fail("Failed to fetch the RSS feed after multiple retries.")
    return fetcher

@pytest.fixture
def podcast_feed_fetcher(rss_feeds):
    """Create a feed fetcher using the tech RSS feed."""
    fetcher = FeedFetcher("podcasts")
    success = fetcher.fetch_feed()
    if not success:
        pytest.fail("Failed to fetch the tech RSS feed after multiple retries.")
    return fetcher



@pytest.mark.dependency()
def test_app_launch(driver, launch_utils):
    time.sleep(5)  # Let's just wait a bit for the app to load
    assert driver.current_activity is not None, "App failed to launch!"
    launch_utils.click_standalone_on_lunch()
    result = launch_utils.wait_for_empty_landing_page()
    assert result, "Landing page not available!"
    launch_utils.click_on_feed()
    assert launch_utils.lookup_feed_upload_OPML_available(), "OPML feed upload not available"
    assert launch_utils.lookup_RSS_feed_upload_plus_button_available(), "RSS feed upload not available"
    launch_utils.click_import_OPML()
    assert launch_utils.wait_for_sample_file(), "OPML sample file not available"
    assert launch_utils.upload_sample_file()

@pytest.mark.dependency()
def test_rss_upload(driver, launch_utils):
    assert launch_utils.click_upload_rss_feed(), "Add rss feed didnt work"
    launch_utils.upload_rss_feed()
    assert launch_utils.rss_upload_check(), "Rss upload failed"

@pytest.mark.dependency(depends=["test_rss_upload"])
def test_rss_delete(driver, launch_utils):
    launch_utils.delete_feed()
    assert not launch_utils.read_feed_content_check('WirelessMoves'), "Deletion did not work"

@pytest.mark.dependency()
#@pytest.mark.skip # WIP podcast upload is not stable thats why skip
def test_rss_podcast_upload(driver, launch_utils, podcast_feed_fetcher):
    assert launch_utils.click_upload_rss_feed(), "Add rss feed didnt work"
    launch_utils.upload_rss_podcast()
    assert launch_utils.podcast_upload_check(), "PODCAST upload failed"
    launch_utils.open_podcast_feed()
    launch_utils.refresh_page()
    launch_utils.open_feed_tile(podcast_feed_fetcher.get_first_entry_title())
    assert launch_utils.feed_content_displayed(podcast_feed_fetcher.get_first_entry_title())
    assert launch_utils.feed_is_downloadable()
    launch_utils.back_from_feed_read_view()
    launch_utils.exit_podcast_feed()

@pytest.mark.dependency(depends=["test_app_launch"])
def test_feed_result(driver, launch_utils, feed_fetcher):
    launch_utils.open_feed()
    assert launch_utils.feed_list_is_available(), "Feed didnt show up."
    launch_utils.open_feed_tile(feed_fetcher.get_first_entry_title())
    assert launch_utils.feed_content_displayed(feed_fetcher.get_first_entry_description()), "Feed content was not displayed"
    launch_utils.exit_back_from_read_view()

@pytest.mark.dependency(depends=["test_feed_result"])
def test_read_feed_content_dissapears_check(launch_utils, feed_fetcher):
    assert not launch_utils.read_feed_content_check(feed_fetcher.get_first_entry_title()), "Read feed is still displaying"

@pytest.mark.dependency(depends=["test_read_feed_content_dissapears_check"])
def test_read_feed_setting(launch_utils, feed_fetcher):
    launch_utils.click_feed_setting()
    launch_utils.activate_show_read_news()
    assert launch_utils.feed_content_displayed(feed_fetcher.get_first_entry_title()), "Read news didnt show up"
    launch_utils.exit_back_from_feed_list()

@pytest.mark.dependency()
def test_rename_setting(launch_utils):
    launch_utils.click_feed_setting_remame()
    launch_utils.click_rename()
    launch_utils.rename_feed()
    assert launch_utils.updated_name_persisted(), "Rename did not work"
    launch_utils.click_feed_setting_remame()
    launch_utils.click_rename()
    launch_utils.rename_feed_to_existing()
    assert not launch_utils.updated_is_already_existing(), "Updated name already exists on the list"

# bug 1 no exit from load from file
# bug 2 load button always there and just invisible
# rename allows 2 feeds with same name
