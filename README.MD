# mintrans

A simple Python wrapper for Bing, DeepL, and Google Translate.

This library allows you to use these translation services without official API keys by utilizing their web interfaces/public endpoints.

**Note:** Since this relies on scraping or undocumented endpoints, stability depends on the providers not changing their frontend or blocking requests. DeepL is particularly strict with rate limiting.

## Installation

```bash
pip install mintrans
```

## Usage

Basic usage for all three supported engines.

```python
from mintrans import BingTranslator, DeepLTranslator, GoogleTranslator
from mintrans import RateLimitException

text = 'Hello World'
source = 'en'
target = 'fr'

# 1. Bing
bing = BingTranslator()
print("Bing:", bing.translate(text, source, target))

# 2. Google
google = GoogleTranslator()
print("Google:", google.translate(text, source, target))

# 3. DeepL
# DeepL is more prone to IP blocks and rate limits.
deepl = DeepLTranslator()

try:
    result = deepl.translate(text, source, target)
    print("DeepL:", result)
except RateLimitException:
    print("DeepL rate limit reached.")
except Exception as e:
    print(f"DeepL error: {e}")
```

## Supported Engines

*   **Bing**: Generally stable.
*   **Google**: Standard web translation.
*   **DeepL**: High quality, but very low tolerance for repeated requests from the same IP.

## Notes

*   Language codes follow standard ISO 639-1 format (e.g., `en`, `fr`, `es`, `ja`).
*   Not recommended for high-volume production use due to the lack of official API guarantees.
