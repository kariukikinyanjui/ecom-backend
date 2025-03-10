import requests
from django.conf import settings
from rest_framework.exceptions import APIException


class EmailClient:
    '''
    Handles email sending via Testmail.app API
    Docs: https://testmail.app/docs/
    '''
    def __init__(self):
        self.api_key = settings.TESTMAIL_API_KEY
        self.namespace = settings.TESTMAIL_NAMESPACE
        self.base_url = 'https://api.testmail.app/api/json'

    def send_email(self, to_email, subject, text):
        '''
        Send transactional email with tracking
        Returns Testmail.app envelope ID for debugging
        '''
        try:
            response = requests.post(
                f"{self.base_url}?apikey={self.api_key}&namespace={self.namespace}",
                json={
                    "to": [to_email],
                    "subject": subject,
                    "text": text,
                    "html": f"<p>{text}</p>",
                    "tags": ["transactional"]
                }
            )
            response.raise_for_status()
            return response.json()['envelopeId']
        except (requests.RequestException, KeyError) as e:
            raise APIException(f"Email sending failed: {str(e)}")
