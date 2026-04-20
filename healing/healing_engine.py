import os
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class HealingEngine:
    def __init__(self, driver, wait, reporter=None, screenshot_on_heal=True):
        self.driver = driver
        self.wait = wait
        self.reporter = reporter
        self.screenshot_on_heal = screenshot_on_heal

    def _capture_screenshot(self, element_name):
        os.makedirs("results", exist_ok=True)
        file_name = f"results/healed_{element_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
        self.driver.save_screenshot(file_name)
        return file_name

    def find(self, element_name, primary_locator, fallback_locators=None, condition="visible"):
        fallback_locators = fallback_locators or []

        def resolve(locator):
            if condition == "visible":
                return self.wait.until(EC.visibility_of_element_located(locator))
            if condition == "clickable":
                return self.wait.until(EC.element_to_be_clickable(locator))
            if condition == "present":
                return self.wait.until(EC.presence_of_element_located(locator))
            raise ValueError(f"Unsupported condition: {condition}")

        try:
            element = resolve(primary_locator)
            if self.reporter:
                self.reporter.record_success(
                    element_name=element_name,
                    locator=primary_locator,
                    healed=False
                )
            return element

        except TimeoutException:
            print(f"[HEALING] Primary locator failed for '{element_name}': {primary_locator}")

            for fallback in fallback_locators:
                try:
                    element = resolve(fallback)
                    screenshot = None
                    if self.screenshot_on_heal:
                        screenshot = self._capture_screenshot(element_name)

                    print(f"[HEALING] Fallback worked for '{element_name}': {fallback}")

                    if self.reporter:
                        self.reporter.record_success(
                            element_name=element_name,
                            locator=primary_locator,
                            healed=True,
                            fallback_locator=fallback,
                            screenshot=screenshot,
                        )
                    return element

                except TimeoutException:
                    print(f"[HEALING] Fallback failed for '{element_name}': {fallback}")
                    continue

            print(f"[HEALING] All locator attempts failed for '{element_name}'")
            if self.reporter:
                self.reporter.record_failure(
                    element_name=element_name,
                    locator=primary_locator,
                    fallback_locators=fallback_locators,
                )
            raise Exception(
                f"Element '{element_name}' not found with primary or fallback locators"
            )