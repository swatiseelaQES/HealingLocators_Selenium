# coding=utf-8
import pytest

from pages.search_page import SearchPage
from tests.base_test import BaseTest
from pytest_bdd import scenarios, given, when, then

scenarios("../features/search.feature")

@given("I am on the search page")
def go_to_search_page(load_pages):
    pass

@then("the title should start with \"DuckDuckGo - \"")
def check_title(load_pages):
    load_pages.page.check_title("DuckDuckGo - ")
    assert load_pages.page.title.startswith("DuckDuckGo - "), "Title does not match expected value"

@when("I search for \"Selenium\"")
def search_for_selenium(load_pages):
    load_pages.page.make_a_search("Selenium")

@then("the search should be successful")
def verify_search_success(load_pages):
    assert load_pages.page.is_search_successful("Selenium"), "Search results are not as expected"

class TestSearch(BaseTest):
    @pytest.fixture
    def load_pages(self):
        self.page = SearchPage(self.driver, self.wait, self.healing_engine)
        self.page.go_to_search_page()

    def test_title(self, load_pages):
        self.page.check_title("DuckDuckGo - ")

    def test_search_with_healing_demo(self, load_pages):
        self.page.make_a_search("Selenium")