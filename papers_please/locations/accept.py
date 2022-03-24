import time

from selenium.webdriver.common.by import By

from papers_please.exceptions import NoSlotsAvailable
from papers_please.locations.information import InformationPage
from papers_please.locations.page import Page
from papers_please.parser import Location


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

class AcceptPage(Page):
    TIME_SLOT_DIV = Location(By.CLASS_NAME, "ui-state-default")
    CONFIRM_APPOINTMENT_BTN = Location(By.CSS_SELECTOR, ".l-btn-left")
    CAPTCHA_VALUE_INPUT = Location(By.ID, "captchaValue")

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

    def confirm_appointnment(self) -> InformationPage:
        print("confirming appointment")
        self._d.wait_for(self.TIME_SLOT_DIV)

        for time_slot in self._d.find_many(self.TIME_SLOT_DIV):
            klass = time_slot.get_attribute("class")

            if "available" in klass:
                self._d.move_to(time_slot)
                time_slot.click()
                self._d.get_input(self.CAPTCHA_VALUE_INPUT).set_value(self.solve_captcha())
                self._d.find(self.CONFIRM_APPOINTMENT_BTN).click()
                self._d.short_delay()
                return InformationPage(self._d, self._c)

        raise NoSlotsAvailable
