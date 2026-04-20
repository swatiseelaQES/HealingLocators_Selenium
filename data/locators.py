from selenium.webdriver.common.by import By


class SearchPageLocators:
    # Intentionally broken for demo
    SEARCH_INPUT = (By.ID, "searchbox_input_broken")
    SEARCH_INPUT_FALLBACKS = []

    """SEARCH_INPUT_FALLBACKS = [
        (By.NAME, "q"),
        (By.CSS_SELECTOR, "input[placeholder*='Search']"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ]
    """

    SEARCH_BUTTON = (By.XPATH, "//*[@id='searchbox_homepage']//*[@type='submit']")
    SEARCH_BUTTON_FALLBACKS = [
        (By.CSS_SELECTOR, "#searchbox_homepage button[type='submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
    ]

    RESULTS = (By.XPATH, "//*[@data-testid='mainline']//*[@data-testid='result']")