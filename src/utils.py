
import langid
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def detect_language(text):
    lang, _ = langid.classify(text)
    return lang
