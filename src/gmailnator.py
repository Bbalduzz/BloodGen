import requests
import json, re
from urllib.parse import unquote
from random import choice

class GmailNator:
    def __init__(self):
        self.s = requests.Session()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'content-type': 'application/json'
        }
        self.xsrf_token = ''

    def generate(self, use_custom_domain=False, use_plus=False, use_point=True):
        page = self.s.get('https://www.emailnator.com/')
        self.xsrf_token = unquote(self.s.cookies.get('XSRF-TOKEN'))
        data = ['','','dotGmail']
        payload = json.dumps({'email': [i for i, k in zip(data, [use_custom_domain, use_plus, use_point]) if k]})
        r = self.s.post('https://www.emailnator.com/generate-email',
                          headers={**self.headers, 'x-xsrf-token': self.xsrf_token}, data=payload)
        if r.status_code == 200:
            return r.json()['email'][0]

    def inbox(self, email):
        payload = json.dumps({'email': email})
        r = self.s.post('https://www.emailnator.com/message-list',
                         headers={**self.headers, 'x-xsrf-token': self.xsrf_token}, data=payload)
        if r.status_code == 200:
            inboxes = [_letter for _letter in r.json()['messageData'] if 'ADSVPN' not in _letter['messageID']]
            return inboxes

    def get_message(self, msgID, email):
        payload = {'email': email, 'messageID': msgID}
        r = self.s.post('https://www.emailnator.com/message-list', 
                         headers={**self.headers, 'x-xsrf-token': self.xsrf_token}, json=payload)
        if r.status_code == 200:
            return re.findall(r'\b\d{5}\b', r.text)[0]