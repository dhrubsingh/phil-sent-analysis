
"""Further functionality I want to add: keep track of multiple texts, compare each one's scores on multiple graphs and visualizations

Other classical texts:

Art of War
Tao Te Ching
Analects
Chuang Tzu Mystic, Moralist, and Social Reformer


"""

import streamlit as st
from textblob import TextBlob
import requests
from collections import Counter
import nltk
from nltk.corpus import stopwords


# Function to perform sentiment analysis
def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    word_count = len(blob.words)
    sentence_count = len(blob.sentences)
    return polarity, subjectivity, word_count, sentence_count

# The Tao Teh King text
url = "https://www.gutenberg.org/cache/epub/216/pg216.txt"
response = requests.get(url)

tao_teh_king = response.content.decode('utf-8')
print(tao_teh_king)

# Perform sentiment analysis on The Tao Teh King
polarity, subjectivity, word_count, sentence_count = perform_sentiment_analysis(tao_teh_king)

# Extract most common interesting words
words = TextBlob(tao_teh_king).words
stop_words = stopwords.words('english')
interesting_words = [word.lower() for word in words if word.lower() not in stop_words and len(word) > 3]
common_words = Counter(interesting_words).most_common(5)
most_common_word, count = common_words[0]

# Create the streamlit app
st.title("Sentiment Analysis of The Tao Teh King")

st.write("The Tao Teh King is a Chinese classic text written by Lao Tzu. "
         "Let's perform sentiment analysis on the text to see how positive or negative it is.")

st.write("Polarity Score: ", polarity)

if polarity > 0:
    st.write("The text is generally positive.")
elif polarity < 0:
    st.write("The text is generally negative.")
else:
    st.write("The text is neutral.")

st.write("Subjectivity Score: ", subjectivity)

st.write("Word Count: ", word_count)

st.write("Sentence Count: ", sentence_count)

st.write("Average Words Per Sentence: ", round(word_count / sentence_count, 2))

st.write("Most Common Interesting Word: ", most_common_word)
st.write("Count: ", count)