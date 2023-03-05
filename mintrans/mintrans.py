import requests
import re
import random

class BingTranslator:
    def __init__(self):
        self.session = self._get_session()

    def _get_session(self):
        session = requests.Session()
        headers = {
            'User-Agent': '',
            'Referer': 'https://www.bing.com/translator'
        }
        session.headers.update(headers)
        response = session.get('https://www.bing.com/translator')
        content = response.text
        params_pattern = re.compile(r'params_AbusePreventionHelper\s*=\s*(\[.*?\]);', re.DOTALL)
        match = params_pattern.search(content)
        if match:
            params = match.group(1)
            key, token, time = [p.strip('"').replace('[', '').replace(']', '') for p in params.split(',')]
            session.headers.update({'key': key, 'token': token})
        match = re.search(r'IG:"(\w+)"', content)
        if match:
            ig_value = match.group(1)
            session.headers.update({'IG': ig_value})
        return session

    def translate(self, text, from_lang, to_lang):
        url = f'https://www.bing.com/ttranslatev3?isVertical=1&&IG={self.session.headers.get("IG")}&IID=translator.{random.randint(5019, 5026)}.{random.randint(1, 3)}'
        data = {'': '', 'fromLang': from_lang, 'text': text, 'to': to_lang, 'token': self.session.headers.get('token'), 'key': self.session.headers.get('key')}
        response = self.session.post(url, data=data).json()
        if type(response) is dict:
            if 'ShowCaptcha' in response.keys():
                self.session = self._get_session()
                return self.translate(text, from_lang, to_lang)
            elif 'statusCode' in response.keys():
                if response['statusCode'] == 400:
                    response['errorMessage'] = f'1000 characters limit! You send {len(text)} characters.'
        else:
            return response[0]
        return response