import os
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from healing.locator_memory import LocatorMemory


class HealingEngine:
    def __init__(
        self,
        driver,
        wait,
        reporter=None,
        screenshot_on_heal=True,
        memory=None,
        memory_enabled=True,
    ):
        self.driver = driver
        self.wait = wait
        self.reporter = reporter
        self.screenshot_on_heal = screenshot_on_heal
        self.memory_enabled = memory_enabled
        self.memory = memory or LocatorMemory()

    def _capture_screenshot(self, element_name):
        os.makedirs("results", exist_ok=True)
        file_name = (
            f"results/healed_{element_name}_"
            f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
        )
        self.driver.save_screenshot(file_name)
        return file_name

    def _resolve(self, locator, condition):
        if condition == "visible":
            return self.wait.until(EC.visibility_of_element_located(locator))
        if condition == "clickable":
            return self.wait.until(EC.element_to_be_clickable(locator))
        if condition == "present":
            return self.wait.until(EC.presence_of_element_located(locator))
        raise ValueError(f"Unsupported condition: {condition}")

    def find(self, element_name, primary_locator, fallback_locators=None, condition="visible"):
        fallback_locators = fallback_locators or []

        try:
            element = self._resolve(primary_locator, condition)

            if self.memory_enabled:
                self.memory.remember(
                    element_name=element_name,
                    locator=primary_locator,
                    source="primary",
                )

            if self.reporter:
                self.reporter.record_success(
                    element_name=element_name,
                    locator=primary_locator,
                    healed=False,
                )
            return element

        except TimeoutException:
            print(f"[HEALING] Primary locator failed for '{element_name}': {primary_locator}")

        for fallback in fallback_locators:
            try:
                element = self._resolve(fallback, condition)
                screenshot = self._capture_screenshot(element_name) if self.screenshot_on_heal else None

                print(f"[HEALING] Fallback worked for '{element_name}': {fallback}")

                if self.memory_enabled:
                    self.memory.remember(
                        element_name=element_name,
                        locator=fallback,
                        source="fallback",
                    )

                if self.reporter:
                    self.reporter.record_success(
                        element_name=element_name,
                        locator=primary_locator,
                        healed=True,
                        fallback_locator=fallback,
                        screenshot=screenshot,
                        heal_source="fallback",
                    )
                return element

            except TimeoutException:
                print(f"[HEALING] Fallback failed for '{element_name}': {fallback}")

        remembered_locators = []
        if self.memory_enabled:
            remembered_locators = self.memory.get_locators(element_name)

        for remembered in remembered_locators:
            if remembered == primary_locator or remembered in fallback_locators:
                continue

            try:
                element = self._resolve(remembered, condition)
                screenshot = self._capture_screenshot(element_name) if self.screenshot_on_heal else None

                print(f"[HEALING] Memory locator worked for '{element_name}': {remembered}")

                self.memory.remember(
                    element_name=element_name,
                    locator=remembered,
                    source="memory",
                )

                if self.reporter:
                    self.reporter.record_success(
                        element_name=element_name,
                        locator=primary_locator,
                        healed=True,
                        fallback_locator=remembered,
                        screenshot=screenshot,
                        heal_source="memory",
                    )
                return element

            except TimeoutException:
                print(f"[HEALING] Memory locator failed for '{element_name}': {remembered}")

        print(f"[HEALING] All locator attempts failed for '{element_name}'")

        if self.reporter:
            self.reporter.record_failure(
                element_name=element_name,
                locator=primary_locator,
                fallback_locators=fallback_locators + remembered_locators,
            )

        raise Exception(
            f"Element '{element_name}' not found with primary, fallback, or memory locators"
        )