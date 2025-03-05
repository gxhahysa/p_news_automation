import pytest
import os
from tests import logger
from dotenv import load_dotenv
from appium import webdriver
from appium.options.android import UiAutomator2Options
from tests.android.common.element_utils import ElementUtils
from tests.config import RSS_FEEDS

# Load environment variables from .env file
load_dotenv()
# Override config values with environment variables if provided
if os.getenv('DEFAULT_RSS_FEED'):
    RSS_FEEDS['default'] = os.getenv('DEFAULT_RSS_FEED')
if os.getenv('NEWS_RSS_FEED'):
    RSS_FEEDS['news'] = os.getenv('NEWS_RSS_FEED')


@pytest.fixture(scope="session", autouse=True)
def driver():
    # Debugging
    logger.debug("\n[DEBUG] Loading environment variables...")
    logger.info(f"PLATFORM_NAME: {os.getenv('ANDROID_APP_PATH')}")
    logger.info(f"DEVICE_NAME: {os.getenv('ANDROID_DEVICE_NAME')}")
    logger.info(f"APP_PATH: {os.getenv('ANDROID_APP_PATH')}")

    # fail in case
    assert os.getenv("ANDROID_PLATFORM_NAME"), "[ERROR] PLATFORM_NAME is not set in .env"
    assert os.getenv("ANDROID_DEVICE_NAME"), "[ERROR] DEVICE_NAME is not set in .env"
    assert os.getenv("ANDROID_APP_PATH"), "[ERROR] APP_PATH is not set in .env"

    logger.debug("\n[DEBUG] Environment variables loaded successfully!")  # Debugging

    # Setup Appium desired capabilities
    desired_caps = {
        "automationName": "UiAutomator2",
        "platformName": os.getenv('ANDROID_PLATFORM_NAME'),
        "platformVersion": os.getenv('ANDROID_DEVICE_PLATFORM_VERSION'),
        "app": os.getenv('ANDROID_APP_PATH'),
        "deviceName": os.getenv('ANDROID_DEVICE_NAME'),
        "isRealMobile": False
    }

    logger.info("Desired capabilities:", desired_caps)

    # Initialize Appium driver
    appium_server = os.getenv("APPIUM_SERVER_URL")
    driver = webdriver.Remote(appium_server, options=UiAutomator2Options().load_capabilities(desired_caps))

    logger.debug("\n[DEBUG] Appium driver initialized successfully!")  # Debugging

    # Yield the driver for use in tests
    yield driver
    # Cleanup: Quit the Appium driver after tests
    logger.debug("\n[DEBUG] Quitting Appium driver...")  # Debugging
    # claenup/ session teardown can be done here
    driver.quit()

@pytest.fixture(scope="session", autouse=True)
def element_utils(driver):
    return ElementUtils(driver)

@pytest.fixture(scope="session")
def rss_feeds():
    # provide access to FEEDS url
    return RSS_FEEDS
