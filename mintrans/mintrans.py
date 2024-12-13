import requests
import re
import time
import random
from functools import wraps

class RateLimitException(Exception):
    pass

_CHROME_VERSION = None
def get_google_latest_version():
    global _CHROME_VERSION
    if _CHROME_VERSION is None:
        try:
            data = requests.get('https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json').json()
            _CHROME_VERSION = data['channels']['Stable']['version']
        except:
            _CHROME_VERSION = '131.0.6778.139'
    return _CHROME_VERSION

def get_random_user_agent():
    try:
        return requests.get('https://fingerprints.bablosoft.com/preview?tags=Desktop,' + random.choice(['Firefox', 'Chrome', 'Safari'])).json()['ua']
    except:
        return f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{get_google_latest_version()} Safari/537.36'

def retry_on_rate_limit(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except RateLimitException:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class BingTranslator:
    def __init__(self):
        self.session = self._get_session()

    def _get_session(self):
        session = requests.Session()
        headers = {
            'User-Agent': get_random_user_agent(),
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

    @retry_on_rate_limit(max_attempts=3)
    def translate(self, text, from_lang, to_lang):
        url = f'https://www.bing.com/ttranslatev3?isVertical=1&&IG={self.session.headers.get("IG")}&IID=translator.{random.randint(5019, 5026)}.{random.randint(1, 3)}'
        data = {'': '', 'fromLang': from_lang, 'text': text, 'to': to_lang, 'token': self.session.headers.get('token'), 'key': self.session.headers.get('key')}
        response = self.session.post(url, data=data).json()
        if type(response) is dict:
            if 'ShowCaptcha' in response.keys():
                self.session = self._get_session()
                raise RateLimitException('Bing Translate rate limit reached (Captcha)!')
            elif 'statusCode' in response.keys():
                if response['statusCode'] == 400:
                    response['errorMessage'] = f'1000 characters limit! You send {len(text)} characters.'
                elif response['statusCode'] == 429:
                    raise RateLimitException('Bing Translate rate limit reached!')
        else:
            return response[0]
        return response

class DeepLTranslator:
    def __init__(self):
        pass

    @retry_on_rate_limit(max_attempts=3)
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
                    "quality": "normal",
                    "mode": "translate",
                    "browserType": 1,
                    "textType": "plaintext",
                },
                "timestamp": round(time.time())
            },
            "id": random.randint(88720004, 100000000)
        }
        headers = {'User-Agent': get_random_user_agent()}
        r = requests.post('https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs', json=json, headers=headers)
        print(r.json())
        try:
            translated_text = r.json()['result']
            return translated_text
        except KeyError:
            if 'many requests' in r.json()['error']['message']:
                raise RateLimitException('Rate limit error!')
            raise KeyError

class GoogleTranslator:
    def __init__(self):
        pass

    @retry_on_rate_limit(max_attempts=3)
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

        headers = {'User-Agent': get_random_user_agent()}
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 429:
            raise RateLimitException('Google Translate rate limit reached!')
        return response.json()
