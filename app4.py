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


# Define the main page
def main_page():
    st.title("Coming Soon")
    st.write("This app will display sentiment analysis results for classic Chinese texts.")


# Define the sentiment analysis page
def sentiment_analysis_page(book):
    st.title(book["title"])
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
    ax.set_title(f"Most Common Interesting Nouns in {book['title']}", fontsize=16)
    ax.set_xlabel("Frequency", fontsize=12)
    ax.set_ylabel("Words", fontsize=12)

    st.write("Most Common Interesting Nouns: ")
    st.pyplot(fig)


# Read sentiment analysis results from JSON file
with open('sentiment_analysis_results.json', 'r') as f:
    results = json.load(f)

# Define the book titles and sentiment analysis results
book_titles = list(results.keys())
book_data = list(results.values())

# Set the page title
st.set_page_config(page_title="Sentiment Analysis")

# Create a sidebar with a navigation menu
menu = ["Home"] + book_titles
choice = st.sidebar.selectbox("Select a page", menu)

# Display the selected page
if choice == "Home":
    main_page()
else:
    book_index = book_titles.index(choice)
    book = book_data[book_index]
    sentiment_analysis_page(book)
