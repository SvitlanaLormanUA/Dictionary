
from langdetect import detect
import nltk

nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def detect_language(text):
    try:
        return detect(text)
    except Exception:
        return "en"  
