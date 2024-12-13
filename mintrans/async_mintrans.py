import aiohttp
import re
import time
import random
import asyncio
from functools import wraps
from .mintrans import RateLimitException, _CHROME_VERSION

async def get_random_user_agent_async():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://fingerprints.bablosoft.com/preview?tags=Desktop,' + random.choice(['Firefox', 'Chrome', 'Safari'])) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['ua']
                raise Exception("Failed to fetch user agent")
    except:
        return f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{_CHROME_VERSION} Safari/537.36'

def async_retry_on_rate_limit(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except RateLimitException:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    await asyncio.sleep(delay)
            return None
        return wrapper
    return decorator

class AsyncBingTranslator:
    def __init__(self):
        self.session = None
        self.headers = None

    async def _get_session(self):
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': await get_random_user_agent_async(),
                'Referer': 'https://www.bing.com/translator'
            }
            async with session.get('https://www.bing.com/translator', headers=headers) as response:
                content = await response.text()
                params_pattern = re.compile(r'params_AbusePreventionHelper\s*=\s*(\[.*?\]);', re.DOTALL)
                match = params_pattern.search(content)
                if match:
                    params = match.group(1)
                    key, token, _ = [p.strip('"').replace('[', '').replace(']', '') for p in params.split(',')]
                    headers.update({'key': key, 'token': token})
                match = re.search(r'IG:"(\w+)"', content)
                if match:
                    ig_value = match.group(1)
                    headers.update({'IG': ig_value})
                return headers

    @async_retry_on_rate_limit(max_attempts=3)
    async def translate(self, text, from_lang, to_lang):
        if not self.headers:
            self.headers = await self._get_session()

        url = f'https://www.bing.com/ttranslatev3?isVertical=1&&IG={self.headers.get("IG")}&IID=translator.{random.randint(5019, 5026)}.{random.randint(1, 3)}'
        data = {
            '': '',
            'fromLang': from_lang,
            'text': text,
            'to': to_lang,
            'token': self.headers.get('token'),
            'key': self.headers.get('key')
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=self.headers) as response:
                response_json = await response.json()
                if isinstance(response_json, dict):
                    if 'ShowCaptcha' in response_json:
                        self.headers = await self._get_session()
                        raise RateLimitException('Bing Translate rate limit reached (Captcha)!')
                    elif 'statusCode' in response_json:
                        if response_json['statusCode'] == 400:
                            response_json['errorMessage'] = f'1000 characters limit! You send {len(text)} characters.'
                        elif response_json['statusCode'] == 429:
                            raise RateLimitException('Bing Translate rate limit reached!')
                else:
                    return response_json[0]
                return response_json

class AsyncDeepLTranslator:
    def __init__(self):
        pass

    @async_retry_on_rate_limit(max_attempts=3)
    async def translate(self, text, from_lang, to_lang):
        json_data = {
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

        headers = {'User-Agent': await get_random_user_agent_async()}
        async with aiohttp.ClientSession() as session:
            async with session.post('https://www2.deepl.com/jsonrpc?method=LMT_handle_jobs', json=json_data, headers=headers) as response:
                response_json = await response.json()
                try:
                    translated_text = response_json['result']
                    return translated_text
                except KeyError:
                    if 'many requests' in response_json['error']['message']:
                        raise RateLimitException('Rate limit error!')
                    raise KeyError

class AsyncGoogleTranslator:
    def __init__(self):
        pass

    @async_retry_on_rate_limit(max_attempts=3)
    async def translate(self, text, from_lang, to_lang):
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

        headers = {'User-Agent': await get_random_user_agent_async()}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 429:
                    raise RateLimitException('Google Translate rate limit reached!')
                return await response.json()
