import logging
import time

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ElementUtils:
    def __init__(self, driver: webdriver, default_timeout= 10):
        self.driver = driver
        self.logger = logging
        self.default_timeout = default_timeout


    def find_by_id(self, id: str):
        element = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located((AppiumBy.ID, id))
        )
        return element

    def click_by_id(self, id: str, name: str):
        click_action = self.find_by_id(id).click()
        self.logger.info(f"Element {name} was clicked")
        return click_action

    def wait_and_validate_element_displayed_by_id(self, id: str, name: str, timeout) -> bool:
        try:
            # Set up WebDriverWait
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((AppiumBy.ID, id))
            )
            self.logger.info(f'Element with ID {name} is displayed')
            return True  # Return the element if found and visible
        except Exception as e:
            print(f"Error: Element with ID '{name}' not found within {timeout} seconds.")
            raise e

    def click_by_element_containing_text(self, text: str):
        element = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")')))
        element.click()

    def wait_and_validate_element_displayed_by_text(self, text: str, timeout) -> bool:
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text}")')
                )
            )
            self.logger.info(f"Element containing text '{text}' is visible!")
            return True
        except Exception as e:
            self.logger.info(f"Timeout: Element containing text '{text}' was not found within 10 seconds.")
            raise e

    def send_keys_to_textbox_by_id(self, id: str, name: str, text: str):
        textbox = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located((AppiumBy.ID, id)))
        textbox.send_keys(text)
        self.logger.info(f"Send keys {text} to element {name}")

    def clear_then_send_keys_to_textbox_by_id(self, id: str, name: str, text: str):
        textbox = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located((AppiumBy.ID, id)))

        textbox.click()
        textbox.clear()
        textbox.send_keys(text)
        self.logger.info(f"Send keys {text} to element {name}")

    def click_by_ANDROID_UIAUTOMATOR(self, path: str, name: str):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, path)))
        element.click()
        self.logger.info(f"Clicked {name}")

    def scroll_for_refresh(self):
        size = self.driver.get_window_size()
        # Get the start and end points for the swipe
        start_x = size['width'] / 2
        start_y = size['height'] * 0.2  # Starting near the top of the screen
        end_y = size['height'] * 0.8  # Ending near the bottom of the screen

        self.driver.swipe(start_x,start_y,end_y,3000)

    def scroll_for_refresh_mobile_actions(self):
        # Get screen dimensions
        size = self.driver.get_window_size()
        center_x = size['width'] / 2
        start_y = size['height'] * 0.2  # Start near the top of the screen
        end_y = size['height'] * 0.7  # Pull down to about 70% of the screen height

        try:
            # Create pointer action
            actions = self.driver.action()

            # Create action sequence for pull-to-refresh
            actions.pointer_action.move_to_location(center_x, start_y)
            actions.pointer_action.pointer_down()
            actions.pointer_action.pause(300)  # Small pause after pressing down
            actions.pointer_action.move_to_location(center_x, end_y)
            actions.pointer_action.pause(600)  # Hold briefly at the bottom to trigger refresh
            actions.pointer_action.release()
            actions.perform()

            # Wait briefly for refresh animation
            time.sleep(1)

            self.logger.info("Performed pull-to-refresh gesture using W3C Actions")
        except Exception as e:
            self.logger.error(f"Error performing pull-to-refresh: {e}")
            # Fallback to legacy method if W3C actions fail
            self.driver.swipe(center_x, start_y, center_x, end_y, 2500)
            self.logger.info("Performed pull-to-refresh using legacy swipe")

    def count_elements_in_layout_by_uiselector(self, uiselector_value: str, child_type: str = None) -> int:
        try:
            # Find the layout using UiSelector
            layout = WebDriverWait(self.driver, self.default_timeout).until(
                EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, uiselector_value))
            )

            # Get the resource-id of the found element (if any)
            resource_id = layout.get_attribute("resource-id")
            content_desc = layout.get_attribute("content-desc")
            self.logger.info(f"Found layout with resource-id: {resource_id}, content-desc: {content_desc}")

            # Find all children
            if child_type:
                # Count only specific types of children
                children = layout.find_elements(AppiumBy.CLASS_NAME, child_type)
            else:
                # Count all direct children using XPath
                children = layout.find_elements(AppiumBy.XPATH, "./*")

            count = len(children)
            self.logger.info(f"Found {count} elements in layout")

            # Optionally log details about the children
            for i, child in enumerate(children):
                try:
                    child_class = child.get_attribute("className")
                    child_text = child.text if child.text else "[No text]"
                    self.logger.info(f"  Child {i + 1}: {child_class} - '{child_text}'")
                except:
                    self.logger.info(f"  Child {i + 1}: [Could not get details]")

            return count

        except Exception as e:
            self.logger.error(f"Error counting elements in layout by UiSelector: {e}")
            return 0

    def search_for_text_on_page(self, search_text: str)-> bool:

        try:
            elements = self.driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().textContains("{search_text}")'
                # This will find any element containing the specified text
            )
            self.logger.info(f"Element containing text '{search_text}' is visible!")
            return True
        except Exception as e:
            self.logger.info(f"Timeout: Element containing text '{search_text}' was not found within 10 seconds.")
            raise e

    def click_by_automator_value(self, automator_value: str, name: str):
        elm = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, automator_value))
        )
        elm.click()
        self.logger.info(f"Clicked {name}")

    def search_text_on_page_by_XPATH(self, search_text: str) -> bool:
        try:
            # Find the text element anywhere on the screen
            element = WebDriverWait(self.driver, self.default_timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, f"//*[contains(@text, '{search_text}')]"))
            )
            self.logger.info(f"Text found: {element.text}")
            return True
        except:
            self.logger.info("Text not found on the current screen.")
            return False

    def click_first_list_view_items_by_id(self, id: str, name: str):
        recycler_view = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located((AppiumBy.ID, id))
        )
        # Now, locate all the child elements inside the RecyclerView (e.g., list items)
        list_items = recycler_view.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        # Click on first list item
        if list_items:
            first_item = list_items[0]
            first_item.click()
            self.logger.info(f"First item clicked! {name} item contents are --- {first_item}")

            return True
        self.logger.info("No items found.")
        return False

    def click_by_accessibility_id(self, value: str, name: str):
        try:
            elm = WebDriverWait(self.driver, self.default_timeout).until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, value))
            )
            elm.click()
            self.logger.info(f"Element {name} clicked successfully!")
        except Exception as e:
            self.logger.info(f"Error occurred while clicking the element: {e}")

    def list_element_has_at_least_one_element(self, id: str) -> bool:
        try:
            recycler_view = self.driver.find_element(by=AppiumBy.ID,
                                                value=id)

            # Get the child elements (list items) within the RecyclerView
            list_items = recycler_view.find_elements(by=AppiumBy.CLASS_NAME,
                                                     value="android.widget.TextView")

            # Return True if the list has at least one element
            if len(list_items) > 0:
                return True
            else:
                return False
        except Exception as e:
            self.logger.info(f"Error occurred: {e}")
            return False

    def is_text_duplicated_on_screen(self, text: str) -> bool:
        try:
            # Find all elements containing the specified text
            elements = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().textContains("{text}")'
            )
            # Count how many times the text appears
            count = len(elements)

            # Log the result
            if count == 0:
                self.logger.info(f"Text '{text}' not found on screen")
            elif count == 1:
                self.logger.info(f"Text '{text}' appears once on screen")
            else:
                self.logger.info(f"Text '{text}' appears {count} times on screen")

            # Return True if the text appears more than once
            return count > 1

        except Exception as e:
            self.logger.error(f"Error checking for duplicate text: {e}")
            return False