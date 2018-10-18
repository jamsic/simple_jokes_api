import requests
import logging


class GeekJokesApi:
    API_URL = 'https://geek-jokes.sameerkumar.website/api'
    OK_STATUS_CODE = 200
    RETRY_TIMES = 5

    def get_a_joke(self):
        for i in xrange(self.RETRY_TIMES):
            try:
                new_joke = requests.get(self.API_URL)
                if new_joke.status_code == self.OK_STATUS_CODE:
                    return new_joke.text.strip()
            except Exception as e:
                logging.error(e)

