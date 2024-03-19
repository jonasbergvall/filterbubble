import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the history.csv file from the URL
url = 'https://bestofworlds.se/filterbubble/data/history.csv'
df = pd.read_csv(url, header=None, names=['date', 'domain'])

# Filter out non-string values and empty strings in the 'domain' column
valid_domains = df['domain'].dropna().astype(str)
valid_domains = valid_domains[valid_domains != '']

# Count domain occurrences
domain_counts = valid_domains.value_counts()

# Display a bar chart of the top 10 domains using Plotly
st.write('## Top 10 News Sources')
st.bar_chart(domain_counts.head(10))

# Generate a word cloud only if there are valid words
if len(valid_domains) > 0:
    st.write('## News Source Word Cloud')
    wordcloud = WordCloud(width=800, height=400, max_words=50).generate(' '.join(valid_domains))
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.write('## News Source Word Cloud')
    st.write('Not enough valid words to create a word cloud.')
