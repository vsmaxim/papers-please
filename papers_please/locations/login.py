import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from papers_please.locations.menu import MenuPage
from papers_please.locations.page import Page
from papers_please.parser import Location


class LoginPage(Page):
    COUNTRY_SELECT = Location(By.CSS_SELECTOR, "div.wrap:nth-child(2) > div:nth-child(2) > select:nth-child(1)")
    INSTANCE_SELECT = Location(By.CSS_SELECTOR, "div.wrap:nth-child(3) > div:nth-child(2) > select:nth-child(1)")
    EMAIL_INPUT = Location(By.ID, "Email")
    PASSWORD_INPUT = Location(By.ID, "Password")
    CAPTCHA_INPUT = Location(By.ID, "Captcha")

    def login(self, country: str, institution: str, email: str, password: str) -> MenuPage:
        print("logging in")
        next_page = MenuPage(self._d, self._c)
        self._d.open("https://q.midpass.ru/ru/Home/Index")

        if not self._d.wait_for(self.PASSWORD_INPUT):
            print("already signed in")
            return next_page

        self.accept_cookies()

        self._d.get_select(self.COUNTRY_SELECT).select_by_visible_text(country)
        self._d.get_select(self.INSTANCE_SELECT).select_by_visible_text(institution)
        self._d.get_input(self.EMAIL_INPUT).set_value(email)
        self._d.get_input(self.PASSWORD_INPUT).set_value(password)
        self._d.get_input(self.CAPTCHA_INPUT).set_value(self.solve_captcha())
        self._d.get_input(self.PASSWORD_INPUT).el.send_keys(Keys.RETURN)

        self._d.short_delay()
        return next_page
