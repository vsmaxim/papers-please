from papers_please.captcha import CaptchaClient
from papers_please.locations.login import LoginPage
from papers_please.parser import ChromeDriver
from papers_please import config

captcha_client = CaptchaClient(config.CAPTCHA_TOkEN)

# TODO: Telegram notification
with ChromeDriver(headless=False) as driver:
    reserved = False

    while not reserved:
        try:
            (
                LoginPage(driver, captcha_client)
                .login(config.COUNTRY, config.INSTITUTION, config.EMAIL, config.PASSWORD)
                .select_service(config.SERVICE_NUMBER)
                .find_first_available_slot()
                .confirm_appointnment()
                .fill_info(config.FIRST_NAME, config.LAST_NAME, config.PATRONYMIC, config.CONTACT_PHONE)
            )
            reserved = True
        except Exception as e:
            print(e.with_traceback(None))
            driver.long_delay()
