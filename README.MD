# 🗺️ mintrans - A translation API wrapper 🗺️

mintrans is a free API wrapper that utilizes Bing, DeepL, and Google Translate for translation purposes. 🤖

## 💡 How to use 💡

```python 
from mintrans import BingTranslator, DeepLTranslator, GoogleTranslator
from mintrans import RateLimitException

text = 'Hello World!'
from_lang = 'en'  
to_lang = 'fr'

# Bing Translator
bing_translator = BingTranslator()  
bing_translation = bing_translator.translate(text, from_lang, to_lang)
print(bing_translation)

# DeepL Translator  
deepl_translator = DeepLTranslator()
try:
	deepl_translation = deepl_translator.translate(text, from_lang, to_lang)
	print(deepl_translation)
except RateLimitException:
	print('Limit of DeepL Translator reached!')

# Google Translator
google_translator = GoogleTranslator()  
google_translation = google_translator.translate(text, from_lang, to_lang)
print(google_translation)
```

## 🔑 Features 🔑

- Bing, DeepL and Google translators for more translation options!
- Easy switching between translators.
- Supports 100+ languages across translators. 🌍

## 🏆 Examples 🏆

```python
text = 'This is a longer text to test the translation.'

bing_translation = bing_translator.translate(text, 'en', 'es') 

deepl_translation = deepl_translator.translate(text, 'en', 'de')

google_translation = google_translator.translate(text, 'en', 'fr')  
```