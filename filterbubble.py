import streamlit as st
import pandas as pd
import tldextract
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the history.csv file from the URL
url = 'https://bestofworlds.se/filterbubble/data/history.csv'
df = pd.read_csv(url, header=None, names=['date', 'url'])

# Extract base domains using tldextract
extract = tldextract.extract
df['domain'] = df['url'].apply(lambda x: extract(x).domain)

# Count domain occurrences
domain_counts = df['domain'].value_counts()

# Display a bar chart of the top 10 domains using Plotly
st.write('## Top 10 News Sources')
st.bar_chart(domain_counts.head(10))

# Generate a word cloud
st.write('## News Source Word Cloud')
wordcloud = WordCloud(width=800, height=400, max_words=50).generate(domain_counts.index.str.cat(sep=' '))
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)
