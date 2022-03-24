import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By

from papers_please.captcha import CaptchaClient
from papers_please.parser import Location, ChromeDriver, Clickable
from papers_please.util import temporary_file


class Page:
    CAPTCHA_LOCATION = Location(By.ID, "imgCaptcha")
    COOKIE_ACCEPT = Location(By.CLASS_NAME, "cookieAccept")

    def __init__(self, driver: ChromeDriver, captcha: CaptchaClient):
        self._d = driver
        self._c = captcha

    def accept_cookies(self):
        try:
            if len(elements := self._d.find_many(self.COOKIE_ACCEPT)) == 1:
                Clickable(elements[0]).click(self._d)
        except ElementNotInteractableException:
            pass

    def solve_captcha(self) -> str:
        element = self._d.find(self.CAPTCHA_LOCATION)
        self._d.short_delay()

        with temporary_file() as captcha:
            with captcha.open("wb") as captcha_handle:
                captcha_handle.write(element.screenshot_as_png)
            return self._c.solve(captcha)