import time

from selenium.webdriver.common.by import By

from papers_please.locations.page import Page
from papers_please.parser import Location


class InformationPage(Page):
    AGREEMENT_CHECKBOX = Location(By.ID, "warningCheckbox")
    LAST_NAME_INPUT = Location(By.CLASS_NAME, "surname")
    FIRST_NAME_INPUT = Location(By.CLASS_NAME, "_name")
    PATRONYMIC_INPUT = Location(By.CLASS_NAME, "patronymic")
    CONTACT_PHONE_INPUT = Location(By.CLASS_NAME, "phone-number")
    SAVE_BUTTON = Location(By.CLASS_NAME, "saveButton")

    def fill_info(
        self,
        first_name: str,
        last_name: str,
        patronymic: str,
        contact_phone: str,
    ):
        print("filling additional info")
        self._d.short_delay()
        self._d.find(self.AGREEMENT_CHECKBOX).click()
        self._d.get_input(self.FIRST_NAME_INPUT).set_value(first_name)
        self._d.get_input(self.LAST_NAME_INPUT).set_value(last_name)
        self._d.get_input(self.PATRONYMIC_INPUT).set_value(patronymic)
        self._d.get_input(self.CONTACT_PHONE_INPUT).set_value(contact_phone)
        btn = self._d.find(self.SAVE_BUTTON)
        self._d.move_to(btn)
        self._d.short_delay()
        btn.click()


