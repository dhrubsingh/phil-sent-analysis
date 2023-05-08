import streamlit as st
from collections import Counter
from nltk.corpus import stopwords
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json
from wordcloud import WordCloud
import plotly.express as px


# Define the methodology page

def methodlogoy():
    st.title("Methodology")
    st.write("This is a sentiment analysis project examining several classical Chinese texts, namely the Tao Te Ching, Art of War, the Analects, Dream of the Red Chamber, and Chuang Tzu Mystic, Moralist, and Social Reformer.")
    st.write("In particular, I examine several key metrics for sentiment analysis, namely polarity, subjectivity, sentiment, word count, and word frequencies.")
    st.write("Firstly, I chose to examine polarity because this is the metric that would help classify whether a text is positive, negative, or neutral. This is important in the context of this exploration as it helps illuminate some insight into each author's perspective and general themese throughout the text.")
    st.write("Secondly, I chose to examine the subjecitivty of each text because I wanted to take into consideration potentiall biases from the author. It is important to highlight bias in order to effectively contextualize each text in its time period.")
    st.write("Additionally, it's also important to keep track of sentiment as this helps us idenitfy emotional content of the passage, which can help us understand the philosophical arguments in some of these texts better. Understanding the sentimental context may give us better insight into their philosophical arguments.")
    st.write("Furthermore, it's also important to keep track of the word count because it provides inisight into the complexity of a text: the longer the word count the more this implies that the texts may contain more nuanced ideas.")
    st.write("Finally, it's also important to keep track of the word frequencies so that we can see what are the most common themes, ideas, and concepts for each text.")
    st.write("This entire project was built using Python. I used TextBlob and Natural Language Toolkit to parse through each text and extract the sentiment analysis metrics. I used plotting and data science libarires like Pandas, Seaborn, WordCloud, and Matplotlib to display my results. I used Streamlit to publish my findings. For source code and potential research replication, visit this Github link:")

# Define the main page
def main_page():
    st.title("Sentiment Analysis")
    st.write("This app displays sentiment analysis results for four classic Chinese texts: Tao Te Ching, Art of War, the Analects, Dream of the Red Chamber, and Chuang Tzu Mystic, Moralist, and Social Reformer.")

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
    chart1.set_ylim(0, 1)  # Set the y-axis limits to 0 and 1

    st.write("Polarity Scores:")
    st.pyplot(fig1)

    # Create a bar chart for subjectivity scores using Seaborn
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    chart2 = sns.barplot(x='Book', y='Subjectivity Score', data=df, ax=ax2)
    chart2.set_title("Subjectivity Scores for Classic Chinese Texts", fontsize=16)
    chart2.set_xlabel("Book Titles", fontsize=12)
    chart2.set_ylabel("Subjectivity Score", fontsize=12)
    chart2.set_ylim(0, 1)  # Set the y-axis limits to 0 and 1

    st.write("Subjectivity Scores:")
    st.pyplot(fig2)

    # Create a heatmap of word frequencies using WordCloud
    word_freq = Counter()
    for book_data in results.values():
        for word, freq in book_data['word_freq']:
            word_freq[word] += freq

    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.write("Word Frequencies:")
    st.pyplot()

    # Create a bubble chart of word frequencies using Plotly
    word_freq = Counter()
    for book_data in results.values():
        for word, freq in book_data['word_freq']:
            word_freq[word] += freq

    df_word_freq = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
    df_word_freq = df_word_freq[df_word_freq['Word'].apply(lambda x: len(x) > 2)]
    fig3 = px.scatter(df_word_freq, x='Word', y='Frequency', size='Frequency', size_max=50,
                 hover_data={'Word': True, 'Frequency': True}, title='Word Frequency in Classic Chinese Texts')
    fig3.update_layout(xaxis={'title': 'Word'}, yaxis={'title': 'Frequency'})
    st.write("Word Frequencies:")
    st.plotly_chart(fig3)



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
menu = ["Home", "Methodology"] + book_titles
choice = st.sidebar.selectbox("Select a page", menu)

# Display the selected page
if choice == "Home":
    main_page()
elif choice == "Methodology":
    methodlogoy()
else:
    book_index = book_titles.index(choice)
    book = book_data[book_index]
    book_title = book_titles[book_index]
    sentiment_analysis_page(book, book_title)
