from pathlib import Path

from python_anticaptcha import AnticaptchaClient, ImageToTextTask


class CaptchaClient:
    def __init__(self, api_key: str):
        self._client = AnticaptchaClient(api_key)

    def solve(self, path: Path) -> str:
        with path.open("rb") as img:
            task = ImageToTextTask(img)
            job = self._client.createTask(task)
            job.join()
            return job.get_captcha_text()