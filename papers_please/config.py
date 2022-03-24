import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
COUNTRY = os.getenv("COUNTRY")
INSTITUTION = os.getenv("INSTITUTION")
SERVICE_NUMBER = int(os.getenv("SERVICE_NUMBER"))
CAPTCHA_TOkEN = os.getenv("CAPTCHA_TOKEN")
FIRST_NAME = os.getenv("FIRST_NAME")
LAST_NAME = os.getenv("LAST_NAME")
PATRONYMIC = os.getenv("PATRONYMIC")
CONTACT_PHONE = os.getenv("CONTACT_PHONE")
