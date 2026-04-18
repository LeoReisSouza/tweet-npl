import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob


nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

STOPWORDS = set(stopwords.words('english') + stopwords.words('portuguese'))


def clean_text(text: str) -> str:
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'@\w+|#\w+', '', text)
    text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)
    text = text.lower().strip()
    return text


def remove_stopwords(text: str) -> str:
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in STOPWORDS]
    return ' '.join(tokens)


def get_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    return {
        'polarity': blob.sentiment.polarity,
        'subjectivity': blob.sentiment.subjectivity,
        'sentiment': 'positive' if blob.sentiment.polarity > 0 else 'negative' if blob.sentiment.polarity < 0 else 'neutral'
    }


def preprocess_tweet(text: str) -> dict:
    cleaned = clean_text(text)
    no_stop = remove_stopwords(cleaned)
    sentiment = get_sentiment(cleaned)
    return {
        'original': text,
        'cleaned': cleaned,
        'no_stopwords': no_stop,
        'sentiment': sentiment
    }