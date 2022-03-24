import time

from selenium.webdriver.common.by import By

from papers_please.locations.calendar import CalendarPage
from papers_please.locations.page import Page
from papers_please.parser import Location, Clickable


class MenuPage(Page):
    MENU_OPTION_DIV = Location(By.CLASS_NAME, "servicebutton")

    def select_service(self, number: int) -> CalendarPage:
        print("selecting option in menu")
        self._d.wait_for(self.MENU_OPTION_DIV)
        services = [Clickable(el) for el in self._d.find_many(self.MENU_OPTION_DIV)]

        if number < 1 or number > 8:
            raise ValueError("Number should be between 1 and 8")

        services[number - 1].click(self._d)
        self._d.short_delay()
        return CalendarPage(self._d, self._c)
