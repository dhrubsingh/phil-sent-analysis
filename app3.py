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


# Read sentiment analysis results from JSON file
with open('sentiment_analysis_results.json', 'r') as f:
    results = json.load(f)

# Define the book titles and sentiment analysis results
book_titles = list(results.keys())
book_data = list(results.values())

# Set the page title and choose the initial book to display
st.set_page_config(page_title="Sentiment Analysis")
book_index = st.sidebar.selectbox("Select a book", range(len(book_titles)), format_func=lambda i: book_titles[i])
book = book_data[book_index]

# Display the sentiment analysis results for the selected book
st.title(book_titles[book_index])
st.write("Polarity Score: ", book["polarity"])

if book["polarity"] > 0:
    st.write("The text is generally positive.")
elif book["polarity"] < 0:
    st.write("The text is generally negative.")
else:
    st.write("The text is neutral.")

st.write("Subjectivity Score: ", book["subjectivity"])
st.write("Word Count: ", book["word_count"])
st.write("Average Words Per Sentence: ", book["average_words_per_sentence"])

# Extract most common interesting words
common_words = book["word_freq"]

# Create a list of tuples containing the word and its frequency
word_freq = [(word, freq) for word, freq in common_words]

# Create a Pandas dataframe from the list of tuples
df = pd.DataFrame(word_freq, columns=['Word', 'Frequency'])

# Create a heatmap using Seaborn
sns.set()
fig, ax = plt.subplots(figsize=(10, 6))
heatmap = sns.heatmap(df.pivot_table(index='Word', columns='Frequency', aggfunc=len), cmap="YlGnBu", annot=True,
                      fmt=".1f", ax=ax, linewidths=0.5, linecolor='black')

# Set the title and axis labels
ax.set_title(f"Most Common Interesting Nouns in {book_titles[book_index]}", fontsize=16)
ax.set_xlabel("Frequency", fontsize=12)
ax.set_ylabel("Words", fontsize=12)

st.write("Most Common Interesting Nouns: ")
st.pyplot(fig)
