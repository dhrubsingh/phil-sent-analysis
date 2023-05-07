import json
import requests
from collections import Counter
from nltk.corpus import stopwords
from textblob import TextBlob
import os

def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    sentiment = blob.sentiment
    return polarity, subjectivity, sentiment, blob

def write_sentiment_to_json(title, polarity, subjectivity, sentiment, common_words, output_file):
    data = {
        'title': title,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'sentiment': sentiment,
        'common_words': common_words
    }
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            data_list = json.load(f)
    else:
        data_list = []
    data_list.append(data)
    with open(output_file, 'w') as f:
        json.dump(data_list, f, indent=4)

# Prompt user to input book title and output file name
title = "Ta"
output_file = input("Enter the output file name: ")

# Download book text from URL and perform sentiment analysis
url = "https://www.gutenberg.org/cache/epub/216/pg216.txt"
response = requests.get(url)
text = response.content.decode('utf-8')
polarity, subjectivity, sentiment, blob = perform_sentiment_analysis(text)

# Extract most common interesting words and write results to JSON file
words = blob.words
stop_words = stopwords.words('english')
interesting_words = [word.lower() for word in words if word.lower() not in stop_words and len(word) > 3]
common_words = Counter(interesting_words).most_common(5)
write_sentiment_to_json(title, polarity, subjectivity, str(sentiment), common_words, output_file)

print("Sentiment analysis results written to", output_file)
