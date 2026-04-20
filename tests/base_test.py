import os
import warnings
from pathlib import Path

import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ServiceChrome
from selenium.webdriver.firefox.service import Service as ServiceFirefox
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from healing.healing_engine import HealingEngine
from healing.healing_reporter import HealingReporter

os.environ["WDM_LOG_LEVEL"] = "0"

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


def config():
    path = Path(__file__).parent / "../data/config.yaml"
    with open(path) as config_file:
        return yaml.safe_load(config_file)


def build_chrome_options(headless: bool):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return options


def build_firefox_options(headless: bool):
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", user_agent)
    if headless:
        options.add_argument("--headless")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    return options


class BaseTest:
    @pytest.fixture(autouse=True)
    def init_driver(self):
        warnings.simplefilter("ignore", ResourceWarning)

        cfg = config()
        browser = cfg.get("browser", "chrome")
        headless = cfg.get("headless", True)
        wait_timeout = cfg.get("wait_timeout", 10)

        healing_cfg = cfg.get("healing", {})
        report_path = healing_cfg.get("report_path", "results/healing_report.json")
        screenshot_on_heal = healing_cfg.get("screenshot_on_heal", True)

        if browser == "chrome":
            options = build_chrome_options(headless)
            self.driver = webdriver.Chrome(
                service=ServiceChrome(ChromeDriverManager().install()),
                options=options,
            )
        elif browser == "firefox":
            options = build_firefox_options(headless)
            self.driver = webdriver.Firefox(
                service=ServiceFirefox(GeckoDriverManager().install()),
                options=options,
            )
        else:
            raise Exception("Incorrect Browser")

        self.wait = WebDriverWait(self.driver, wait_timeout)
        self.healing_reporter = HealingReporter(report_path=report_path)
        self.healing_engine = HealingEngine(
            driver=self.driver,
            wait=self.wait,
            reporter=self.healing_reporter,
            screenshot_on_heal=screenshot_on_heal,
        )

        yield self.wait, self.driver

        self.healing_reporter.write_report()

        if self.driver is not None:
            self.driver.quit()