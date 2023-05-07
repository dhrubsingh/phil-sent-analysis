import streamlit as st
from textblob import TextBlob
import requests
from collections import Counter
import nltk
from nltk.corpus import stopwords
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


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


# The Tao Teh King text
url = "https://www.gutenberg.org/cache/epub/216/pg216.txt"
response = requests.get(url)
tao_teh_king = response.content.decode('utf-8')

# Perform sentiment analysis on The Tao Teh King
polarity, subjectivity, sentiment, words, blob = perform_sentiment_analysis(tao_teh_king, nouns_only=True)

# Exclude words related to Project Gutenberg
exclude_words = ['gutenberg', 'gutenberg-tm', 'project', 'ebook', 'www', 'http', 'org', 'etext', 'edition', 'file', 'files', 'online', 'pg']
interesting_words = [word for word in words if word not in exclude_words]

# Extract most common interesting words
common_words = Counter(interesting_words).most_common(10)

# Create a list of tuples containing the word and its frequency
word_freq = [(word, freq) for word, freq in common_words]

# Create a Pandas dataframe from the list of tuples
df = pd.DataFrame(word_freq, columns=['Word', 'Frequency'])

# Create a heatmap using Seaborn
sns.set()
fig, ax = plt.subplots(figsize=(10, 6))
heatmap = sns.heatmap(df.pivot_table(index='Word', columns='Frequency', aggfunc=len), cmap="YlGnBu", annot=True, fmt=".1f", ax=ax, linewidths=0.5, linecolor='black')

# Set the title and axis labels
ax.set_title("Most Common Interesting Nouns in The Tao Teh King", fontsize=16)
ax.set_xlabel("Frequency", fontsize=12)
ax.set_ylabel("Words", fontsize=12)

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

st.write("Word Count: ", len(words))

st.write("Average Words Per Sentence: ", round(len(words) / len(TextBlob(tao_teh_king).sentences), 2))

st.write("Most Common Interesting Nouns: ")
st.pyplot(fig)
