from typing import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from papers_please.exceptions import NoSlotsAvailable
from papers_please.locations.accept import AcceptPage
from papers_please.locations.page import Page
from papers_please.parser import Location, ChromeDriver


class CalendarCell:
    PLACES_SPAN = Location(By.TAG_NAME, "span")
    DATE_SPAN = Location(By.TAG_NAME, "a")

    def __init__(self, el: WebElement, month: str):
        self.el = el
        self.month = month
        self._places_span = el.find_elements(*self.PLACES_SPAN)
        self._date_span = el.find_element(*self.DATE_SPAN)

    def is_available(self) -> bool:
        if len(self._places_span) == 0:
            return False
        places_span = self._places_span[0]
        if "/" not in places_span.text:
            return False
        available, _ = [int(part) for part in places_span.text.split("/")]
        return available > 0

    @property
    def date(self) -> str:
        return self._date_span.text

    def click(self, driver: ChromeDriver):
        driver.move_to(self.el)
        self.el.click()


class CalendarPage(Page):
    MONTH_SEARCH_DEPTH = 2
    NEXT_MONTH_BUTTON = Location(By.CLASS_NAME, "MonthNavNext")
    DATE_BOX_DIV = Location(By.CLASS_NAME, "DateBox")
    MONTH_NAME_DIV = Location(By.CLASS_NAME, "MonthName")

    def get_current_month(self) -> str:
        self._d.short_delay()
        return self._d.find(self.MONTH_NAME_DIV).text

    def next_month(self):
        next_month_btn = self._d.find(self.NEXT_MONTH_BUTTON)
        self._d.move_to(next_month_btn)
        next_month_btn.click()
        self._d.wait_for(self.DATE_BOX_DIV)
        self._d.wait_for(self.MONTH_NAME_DIV)
        self._d.short_delay()

    def slots(self) -> Iterable[CalendarCell]:
        for _ in range(self.MONTH_SEARCH_DEPTH):
            month = self.get_current_month()
            for element in self._d.find_many(self.DATE_BOX_DIV):
                cell = CalendarCell(element, month)
                print(f"Iterating cell {cell.date} {cell.month}")
                yield cell
            self.next_month()

    def find_first_available_slot(self) -> AcceptPage:
        print("finding available slot")
        try:
            available_slot = next(slot for slot in self.slots() if slot.is_available())
            available_slot.click(self._d)
            self._d.short_delay()
            return AcceptPage(self._d, self._c)
        except StopIteration:
            raise NoSlotsAvailable
