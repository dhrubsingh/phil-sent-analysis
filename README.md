# Sentiment Analysis Project 

This is a sentiment analysis project that I have built examining four classic Chinese texts: Tao Te Ching, Art of War, the Analects, Dream of the Red Chamber, and Chuang Tzu Mystic, Moralist, and Social Reformer.

The website is live via this link: https://dhrubsingh-phil-sent-analysis-app-0mw0n9.streamlit.app/

The key steps to replicate this project for other analysis can be as follows:
1. Collect the source text link for any book that you want to perform sentimental analysis on. In my case, I found all of my texts on Project Gutenberg, an online library with free access to ancient texts.
2. Add into the urls dictionary in *analyze.py*, this will then take that link and perform the sentimental analysis on it. It will update the results into the *sentiment_analysis_results.json* file
3. After that step, the code in *app.py* will handle the rest of the displaying and comparison graphs. The resulting graphs and charts will then be hosted in the Streamlit app, which you can run locally or host on the Streamlit platform itself.

If you are interested in my particular research methodolgy and data collection choices, the published website has an entire page dedicated to explaining my selection. Please contact me if you have any questions!