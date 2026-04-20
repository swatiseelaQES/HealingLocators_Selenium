from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from data.locators import SearchPageLocators


class SearchPage(BasePage):
    def __init__(self, driver, wait, healing_engine):
        self.url = "https://duckduckgo.com/"
        self.locator = SearchPageLocators
        self.healing = healing_engine
        super().__init__(driver, wait)

    def go_to_search_page(self):
        self.go_to_page(self.url)

    def check_title(self, title):
        self.wait.until(EC.title_contains(title))

    def make_a_search(self, input_text):
        search_input = self.healing.find(
            element_name="search_input",
            primary_locator=self.locator.SEARCH_INPUT,
            fallback_locators=self.locator.SEARCH_INPUT_FALLBACKS,
            condition="visible",
        )
        search_input.clear()
        search_input.send_keys(input_text)

        search_button = self.healing.find(
            element_name="search_button",
            primary_locator=self.locator.SEARCH_BUTTON,
            fallback_locators=self.locator.SEARCH_BUTTON_FALLBACKS,
            condition="clickable",
        )
        search_button.click()

        self.wait.until(
            EC.presence_of_all_elements_located(self.locator.RESULTS)
        )
        self.driver.save_screenshot("results/results.png")