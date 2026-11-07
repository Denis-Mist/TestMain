"""Run Selenium IDE .side projects in headless Chrome."""

import fnmatch
import json
import sys
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

KEY_MAP = {
    "${KEY_ENTER}": Keys.ENTER,
    "${KEY_TAB}": Keys.TAB,
    "${KEY_ESCAPE}": Keys.ESCAPE,
}


def make_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1400,1000")
    return webdriver.Chrome(options=options)


class Runner:
    def __init__(self, driver, side_path: Path):
        self.driver = driver
        self.side_path = side_path
        self.variables = {}
        self.skip_stack = []
        self.branch_stack = []

    def expand(self, text):
        if text is None:
            return ""
        result = str(text)
        for name, value in self.variables.items():
            result = result.replace("${" + name + "}", value)
        return result

    def skipping(self):
        return any(self.skip_stack)

    def locator(self, target):
        target = self.expand(target)
        if target.startswith("id="):
            return By.ID, target[3:]
        if target.startswith("css="):
            return By.CSS_SELECTOR, target[4:]
        if target.startswith("xpath="):
            return By.XPATH, target[6:]
        if target.startswith("name="):
            return By.NAME, target[5:]
        if target.startswith("linkText="):
            return By.LINK_TEXT, target[9:]
        if target.startswith("//"):
            return By.XPATH, target
        return By.CSS_SELECTOR, target

    def wait(self, seconds):
        return WebDriverWait(self.driver, seconds)

    def find(self, target, timeout=10, visible=False):
        loc = self.locator(target)
        condition = EC.visibility_of_element_located(loc) if visible else EC.presence_of_element_located(loc)
        return self.wait(timeout).until(condition)

    def matches(self, expected, actual):
        expected = self.expand(expected).strip()
        actual = (actual or "").strip()
        if any(ch in expected for ch in "*?"):
            return fnmatch.fnmatch(actual, expected)
        return actual == expected

    def element_present(self, target):
        try:
            self.driver.find_element(*self.locator(target))
            return True
        except Exception:
            return False

    def condition(self, target):
        target = self.expand(target).strip()
        if target.startswith("elementPresent="):
            return self.element_present(target.split("=", 1)[1])
        return bool(target)

    def shot(self, test_name, failed=False):
        folder = self.side_path.parent / "screenshots"
        folder.mkdir(parents=True, exist_ok=True)
        safe = "".join(ch if ch.isalnum() else "-" for ch in test_name).strip("-")
        suffix = "-failed" if failed else ""
        path = folder / f"{safe}{suffix}.png"
        self.driver.save_screenshot(str(path))
        print(f"screenshot {path}")

    def run_command(self, command):
        name = command["command"]
        target = command.get("target") or ""
        value = command.get("value") or ""
        if name == "if":
            if self.skipping():
                self.skip_stack.append(True)
                self.branch_stack.append("dead")
            else:
                cond = self.condition(target)
                self.skip_stack.append(not cond)
                self.branch_stack.append("then" if cond else "else")
            return
        if name == "else":
            state = self.branch_stack[-1] if self.branch_stack else "dead"
            if state == "then":
                self.skip_stack[-1] = True
            elif state == "else":
                self.skip_stack[-1] = False
            return
        if name == "end":
            if self.skip_stack:
                self.skip_stack.pop()
            if self.branch_stack:
                self.branch_stack.pop()
            return
        if self.skipping():
            return
        if name == "open":
            self.driver.get(self.expand(target))
            return
        if name == "type":
            element = self.find(target)
            element.clear()
            element.send_keys(self.expand(value))
            return
        if name == "sendKeys":
            element = self.find(target)
            token = value.strip()
            element.send_keys(KEY_MAP.get(token, self.expand(value)))
            return
        if name == "click":
            self.find(target).click()
            return
        if name == "mouseOver":
            ActionChains(self.driver).move_to_element(self.find(target)).perform()
            return
        if name == "executeScript":
            self.driver.execute_script(self.expand(target))
            return
        if name == "store":
            self.variables[value] = self.expand(target)
            return
        if name == "storeText":
            self.variables[value] = self.find(target).text
            return
        if name == "echo":
            print("echo", self.expand(target))
            return
        if name == "assertTitle":
            actual = self.driver.title
            if not self.matches(target, actual):
                raise AssertionError(f"title {actual!r} != {self.expand(target)!r}")
            return
        if name == "assertElementPresent":
            self.find(target)
            return
        if name == "assertText":
            actual = self.find(target).text
            if not self.matches(value, actual):
                raise AssertionError(f"text {actual!r} != {self.expand(value)!r}")
            return
        if name == "waitForElementPresent":
            timeout = int(value) / 1000 if str(value).isdigit() else 10
            self.find(target, timeout=timeout)
            return
        if name == "waitForElementVisible":
            timeout = int(value) / 1000 if str(value).isdigit() else 10
            self.find(target, timeout=timeout, visible=True)
            return
        if name == "waitForText":
            timeout = 10
            expected = self.expand(value)

            def _has_text(driver):
                try:
                    return self.matches(expected, driver.find_element(*self.locator(target)).text)
                except Exception:
                    return False

            if not self.wait(timeout).until(_has_text):
                raise AssertionError(f"text {expected!r} did not appear")
            return
        if name in ("pause", "comment"):
            return
        raise AssertionError(f"unsupported command {name}")

    def run_test(self, test):
        self.variables = {}
        self.skip_stack = []
        self.branch_stack = []
        print(f"TEST {test['name']}")
        try:
            for command in test["commands"]:
                self.run_command(command)
        except (AssertionError, TimeoutException, Exception) as error:
            print(f"FAILED {test['name']}: {error}")
            self.shot(test["name"], failed=True)
            return False
        print(f"PASSED {test['name']}")
        self.shot(test["name"])
        return True


def tests_in_order(project):
    by_id = {test["id"]: test for test in project["tests"]}
    if project.get("suites"):
        ordered = []
        for test_id in project["suites"][0].get("tests", []):
            if test_id in by_id:
                ordered.append(by_id[test_id])
        if ordered:
            return ordered
    return project["tests"]


def main(paths):
    failed = 0
    driver = make_driver()
    try:
        for raw in paths:
            path = Path(raw)
            project = json.loads(path.read_text(encoding="utf-8"))
            print(f"PROJECT {project.get('name', path.name)}")
            runner = Runner(driver, path)
            for test in tests_in_order(project):
                if not runner.run_test(test):
                    failed += 1
                driver.delete_all_cookies()
    finally:
        driver.quit()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
