import requests
import re
import time
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

class RateLimitException(Exception):
    pass

class DeepLTranslator:
    def __init__(self):
        pass

    def translate(self, text, from_lang, to_lang):
        json = {
    "jsonrpc": "2.0",
    "method": "LMT_handle_jobs",
    "params": {
        "jobs": [{
            "kind": "default",
            "sentences": [{
                "text": text,
                "id": 1,
                "prefix": ""
            }],
            "raw_en_context_before": [],
            "raw_en_context_after": [],
            "preferred_num_beams": 4
        }],
        "lang": {
            "target_lang": to_lang.upper(),
            "preference": {
                "weight": {},
                "default": "default"
            },
            "source_lang_computed": from_lang.upper()
        },
        "priority": 1,
        "commonJobParams": {
            "regionalVariant": "en-US",
            "mode": "translate",
            "textType": "plaintext",
            "browserType": 1
        },
        "timestamp": round(time.time() * 1.5)
    },
    "id": random.randint(100000000, 9999999999)
}
        r = requests.post('https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs', json=json)
        try:
            translated_text = r.json()['result']['translations'][-1]['beams'][-1]['sentences'][-1]['text']
            return translated_text
        except KeyError:
            raise RateLimitException('Rate limit error!')

class GoogleTranslator:
    def __init__(self):
        pass

    def translate(self, text, from_lang, to_lang):
        url = 'https://translate.googleapis.com/translate_a/single'

        params = {
        'client': 'gtx',
        'sl': 'auto',
        'tl': to_lang,
        'hl': from_lang,
        'dt': ['t', 'bd'],
        'dj': '1',
        'source': 'popup5',
        'q': text
        }

        return requests.get(url, params=params).json()