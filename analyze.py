import streamlit as st
from textblob import TextBlob
import requests
from collections import Counter
import nltk
from nltk.corpus import stopwords
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json

        
urls = {"Tao Te Ching": "https://www.gutenberg.org/cache/epub/216/pg216.txt" , "Art of War": "https://www.gutenberg.org/cache/epub/132/pg132.txt",
        "The Analects": "https://www.gutenberg.org/cache/epub/3330/pg3330.txt",  "Chuang Tzu Mystic, Moralist, and Social Reformer": "https://www.gutenberg.org/files/59709/59709-0.txt",
        "Dream of the Red Chamber:": "https://www.gutenberg.org/cache/epub/9603/pg9603.txt", 
}


# Function to perform sentiment analysis
def perform_sentiment_analysis(text, nouns_only=False):
    blob = TextBlob(text)
    if nouns_only:
        words = [word.lower() for (word, pos) in blob.tags if pos.startswith('NN') and len(word) > 3]
    else:
        words = blob.words
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    sentiment = blob.sentiment
    return polarity, subjectivity, sentiment, words, blob


results = {}

for title, url in urls.items():

    response = requests.get(url)
    tao_teh_king = response.content.decode('utf-8')

    # Perform sentiment analysis on The Tao Teh King
    polarity, subjectivity, sentiment, words, blob = perform_sentiment_analysis(tao_teh_king, nouns_only=True)
    word_count = len(words)
    average_words_per_sentence = round(len(words) / len(TextBlob(tao_teh_king).sentences), 2)

    # Exclude words related to Project Gutenberg
    exclude_words = ['gutenberg', 'gutenberg-tm', 'project', 'ebook', 'www', 'http', 'org', 'etext', 'edition', 'file', 'files', 'online', 'pg']
    interesting_words = [word for word in words if word not in exclude_words]

    # Extract most common interesting words
    common_words = Counter(interesting_words).most_common(10)

    # Create a list of tuples containing the word and its frequency
    word_freq = [(word, freq) for word, freq in common_words]

    results[title] = {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'sentiment': str(sentiment),
        'word_count': word_count,
        'average_words_per_sentence':average_words_per_sentence,
        'word_freq': word_freq
    }

with open('sentiment_analysis_results.json', 'w') as f:
    json.dump(results, f, indent=4)