import random
import time
from typing import NamedTuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

class Input:
    def __init__(self, el: WebElement):
        self.el = el

    def set_value(self, value: str) -> "Input":
        self.el.clear()
        self.el.send_keys(value)
        return self


class Clickable:
    def __init__(self, el: WebElement):
        self.el = el

    def click(self, driver: "ChromeDriver"):
        driver.move_to(self.el)
        self.el.click()


class Location(NamedTuple):
    by: str
    value: str


class ChromeDriver:
    def __init__(self, headless: bool = False):
        options = Options()

        if headless:
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--remote-debugging-port=9222")

        self._d = webdriver.Chrome(options=options)
        self._d.set_window_size(1920, 1080)
        self._timeout = 10

    def __enter__(self) -> "ChromeDriver":
        return self

    def __exit__(self, *exc_info):
        self._d.close()

    @staticmethod
    def short_delay():
        time.sleep(random.randint(3, 7))

    @staticmethod
    def long_delay():
        time.sleep(random.randint(40, 70))

    def open(self, url: str):
        self._d.get(url)

    def find(self, location: Location) -> WebElement:
        return self._d.find_element(*location)

    def find_many(self, location: Location) -> list[WebElement]:
        return self._d.find_elements(*location)

    def wait_for(self, location: Location) -> bool:
        try:
            self.short_delay()
            WebDriverWait(self._d, self._timeout).until(EC.presence_of_element_located(location))
            return True
        except TimeoutException:
            return False

    def move_to(self, element: WebElement):
        actions = ActionChains(self._d)
        actions.move_to_element(element)

    def get_select(self, location: Location) -> Select:
        return Select(self.find(location))

    def get_input(self, location: Location) -> Input:
        return Input(self.find(location))



# def login(
#     driver: WebDriver,
#     captcha_client: CaptchaClient,
#     country: str,
#     institution: str,
#     email: str,
#     password: str,
# ):
#     print("logging in")
#     driver.get("https://q.midpass.ru/ru/Home/Index")
#
#     try:
#         _wait_for_element(driver, By.ID, "Password")
#     except TimeoutException:
#         print("already signed in")
#         return
#
#     accept_cookies(driver)
#
#     country_el = driver.find_element(By.CSS_SELECTOR, "div.wrap:nth-child(2) > div:nth-child(2) > select:nth-child(1)")
#     country_select = Select(country_el)
#     country_select.select_by_visible_text(country)
#
#     inst_el = driver.find_element(By.CSS_SELECTOR, "div.wrap:nth-child(3) > div:nth-child(2) > select:nth-child(1)")
#     inst_select = Select(inst_el)
#     inst_select.select_by_visible_text(institution)
#
#     set_input_value(driver.find_element(By.ID, "Email"), email)
#     set_input_value(driver.find_element(By.ID, "Password"), password)
#     set_input_value(driver.find_element(By.ID, "Captcha"), _solve_captcha(driver, captcha_client))
#
#     driver.find_element(By.ID, "Password").send_keys(Keys.RETURN)
#     time.sleep(1)
#
#
# def _move_to_element(driver: WebDriver, element: WebElement):
#     actions = ActionChains(driver)
#     actions.move_to_element(element)
#
#
# def select_service(driver: WebDriver, service_number: int):
#     print("selecting service")
#     _wait_for_element(driver, By.CLASS_NAME, "servicebutton")
#     services = driver.find_elements(By.CLASS_NAME, "servicebutton")
#     service = services[service_number - 1]
#     _move_to_element(driver, service)
#     service.click()
#
#
# def select_available_dates(driver: WebDriver, captcha_client: CaptchaClient) -> tuple[bool, list[str]]:
#     print("searching for available slots")
#
#     def _search_and_select(reserve: bool = True) -> bool:
#         elements = driver.find_elements(By.CLASS_NAME, "DateBox")
#
#         for element in elements:
#             places_span = element.find_elements(By.TAG_NAME, "span")
#             date_span = element.find_element(By.TAG_NAME, "a")
#
#             if len(places_span) == 0:
#                 continue
#
#             places_span = places_span[0]
#
#             if "/" in places_span.text:
#                 available, _ = list(map(int, places_span.text.split("/")))
#
#                 if available == 0:
#                     continue
#
#                 _move_to_element(driver, element)
#
#                 if reserve:
#                     msg = f"Reserved a slot on {date_span.text} {month}"
#                     element.click()
#                     r = select_timeslot(driver, captcha_client)
#                     available_service_dates.append(msg)
#                     return r
#
#                 available_service_dates.append(f"{available} slots on {date_span.text} {month}")
#
#         return False
#
#     def _next_month():
#         nonlocal month
#         month_btn = driver.find_element(By.CLASS_NAME, "MonthNavNext")
#         _move_to_element(driver, month_btn)
#         month_btn.click()
#         _wait_for_element(driver, By.CLASS_NAME, "DateBox")
#         _wait_for_element(driver, By.CLASS_NAME, "MonthName")
#         month = driver.find_element(By.CLASS_NAME, "MonthName").text
#
#     available_service_dates = []
#
#     _wait_for_element(driver, By.CLASS_NAME, "DateBox")
#     month = driver.find_element(By.CLASS_NAME, "MonthName").text
#
#     reserved = _search_and_select()
#
#     # Look in the next month
#     if not reserved:
#         _next_month()
#         _search_and_select()
#
#     return reserved, available_service_dates
#
#
# def select_timeslot(driver: WebDriver, captcha_client: CaptchaClient) -> bool:
#     print("selecting timeslot")
#     _wait_for_element(driver, By.CLASS_NAME, "ui-state-default")
#
#     for element in driver.find_elements(By.CLASS_NAME, "ui-state-default"):
#         klass = element.get_attribute("class")
#
#         if "available" in klass:
#             _move_to_element(driver, element)
#             element.click()
#             _wait_for_element(driver, By.ID, "imgCaptcha")
#             set_input_value(driver.find_element(By.ID, "captchaValue"), _solve_captcha(driver, captcha_client))
#             driver.find_element(By.CSS_SELECTOR, ".l-btn-left").click()
#             print("return true")
#             return True
#
#     return False
