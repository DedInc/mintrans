<h1 align="center">Mintrans is a free API wrapper that utilizes Bing Translator for translation purposes.</h1>

<br>

<h1 align="center"> -How to use- </h1>

```python
from mintrans import BingTranslator

text = 'Hello World!'
from_lang = 'en'
to_lang = 'de'

translator = BingTranslator()
translation = translator.translate(text, from_lang, to_lang)
print(translation)
```