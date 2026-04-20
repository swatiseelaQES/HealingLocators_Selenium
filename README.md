# HealingLocators_Selenium
This is a simple example with healing locators implemented without AI

**Self-Healing Selenium (No AI, No Docker)**

A lightweight proof of concept that shows: 
You don’t need AI or external services to repair broken locators.
You can build a simple, deterministic self-healing layer directly in your Selenium framework.

**🚀 What this project demonstrates**

This repository extends a basic Selenium + Pytest framework with a self-healing locator layer that:

Detects when a locator fails
Tries predefined fallback locators
Recovers test execution when possible
Logs healing behavior
Generates a simple healing report

**Setup:**
Assuming python, pip and venv are installed correctly:

Download or clone this repository
Open a terminal
Go to the project root directory "/selenium-python-example/".
Create a virtual environment:
(UBUNTU): python3 -m venv .venv
(WINDOWS): py -m venv venv
Activate the virtual environment executing the following script:
(UBUNTU): source .venv/bin/activate
(WINDOWS): .\venv\Scripts\activate
Execute the following command to download the necessary libraries: pip install -r requirements.txt


**🧪 Running the tests**
1. Install dependencies
pip install -r requirements.txt
2. Run tests
pytest -v --html=results/report.html


**🔍 Demo: See self-healing in action**
Step 1 — Normal run
Use valid locator:
SEARCH_INPUT = (By.ID, "searchbox_input")
Run tests → ✅ Pass

Step 2 — Break the locator
SEARCH_INPUT = (By.ID, "searchbox_input_broken")
Run tests again → ✅ Still Pass (via fallback)

Step 3 — Check outputs
Console logs show healing steps
results/healing_report.json shows what was healed
Screenshot captured for healed elements

**You can achieve meaningful self-healing without AI.**

**🧭 Future improvements**
Add confidence scoring for locators
Auto-promote successful fallback locators
HTML report for healing events
Optional AI-assisted locator suggestions

**✍️ Author**
Swati Seela
Quality Engineering Sense

