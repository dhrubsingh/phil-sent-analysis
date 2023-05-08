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
    st.title("Sentiment Analysis")
    st.write("This app displays sentiment analysis results for classic Chinese texts.")

    # Read sentiment analysis results from JSON file
    with open('sentiment_analysis_results.json', 'r') as f:
        results = json.load(f)

    # Define the book titles, polarity scores, and subjectivity scores
    book_titles = list(results.keys())
    polarity_scores = [book_data['polarity'] for book_data in results.values()]
    subjectivity_scores = [book_data['subjectivity'] for book_data in results.values()]

    # Shorten book titles with more than three words
    short_titles = []
    for title in book_titles:
        if len(title.split()) > 3:
            short_title = ' '.join(title.split()[:3]) + '...'
        else:
            short_title = title
        short_titles.append(short_title)

    # Create a Pandas dataframe from the polarity and subjectivity scores and shortened book titles
    df = pd.DataFrame({'Book': short_titles, 'Polarity Score': polarity_scores, 'Subjectivity Score': subjectivity_scores})

    # Create a bar chart for polarity scores using Seaborn
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    chart1 = sns.barplot(x='Book', y='Polarity Score', data=df, ax=ax1)
    chart1.set_title("Polarity Scores for Classic Chinese Texts", fontsize=16)
    chart1.set_xlabel("Book Titles", fontsize=12)
    chart1.set_ylabel("Polarity Score", fontsize=12)
    #chart1.set_ylim(0, 1)  # Set the y-axis limits to 0 and 1

    st.write("Polarity Scores:")
    st.pyplot(fig1)

    # Create a bar chart for subjectivity scores using Seaborn
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    chart2 = sns.barplot(x='Book', y='Subjectivity Score', data=df, ax=ax2)
    chart2.set_title("Subjectivity Scores for Classic Chinese Texts", fontsize=16)
    chart2.set_xlabel("Book Titles", fontsize=12)
    chart2.set_ylabel("Subjectivity Score", fontsize=12)
    #chart2.set_ylim(0, 1)  # Set the y-axis limits to 0 and 1

    st.write("Subjectivity Scores:")
    st.pyplot(fig2)




# Define the sentiment analysis page
def sentiment_analysis_page(book, book_title):
    st.title(book_title)
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
    ax.set_title(f"Most Common Interesting Nouns in {book_title}", fontsize=16)
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
    book_title = book_titles[book_index]
    sentiment_analysis_page(book, book_title)
