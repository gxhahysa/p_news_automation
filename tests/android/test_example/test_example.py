import time
import pytest
from .launch_utils import LaunchUtils

@pytest.fixture(scope="session")
def launch_utils(element_utils):
    launch_utils = LaunchUtils(
        element_utils
    )
    yield launch_utils

@pytest.mark.dependency()
def test_app_launch(driver, launch_utils):
    time.sleep(5)  # Wait for the app to load
    assert driver.current_activity is not None, "App failed to launch!"
    launch_utils.click_standalone_on_lunch()
    time.sleep(2)
