import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tldextract
import re

# Read the history.csv file from the URL
url = 'https://bestofworlds.se/filterbubble/data/history.csv'
df = pd.read_csv(url, header=None, names=['date', 'domain'])

# Extract domain names from the 'domain' column
def extract_domain(url):
    parsed = tldextract.extract(url)
    domain = f"{parsed.domain}.{parsed.suffix}"
    return domain if parsed.subdomain else parsed.domain

valid_domains = df['domain'].dropna().apply(extract_domain)

# Filter out empty strings and subdomains
valid_domains = valid_domains[valid_domains != '']
valid_domains = valid_domains.apply(lambda x: re.sub(r'^www\.', '', x))

# Count domain occurrences
domain_counts = valid_domains.value_counts()

# Display a bar chart of the top 10 domains using Plotly
st.write('## Top 10 News Sources')
st.bar_chart(domain_counts.head(10))

# Generate a word cloud only if there are valid words
if len(valid_domains) > 0:
    st.write('## News Source Word Cloud')

    # Filter out short words (like "com", "se", etc.) from the word cloud
    valid_domains_filtered = valid_domains[valid_domains.apply(lambda x: len(x.split('.')) > 1)]

    # Check if there are any valid domains after filtering
    if len(valid_domains_filtered) > 0:
        # Remove protocols like 'http' and 'https' from the domains
        valid_domains_filtered = valid_domains_filtered.apply(lambda x: re.sub(r'^https?\://', '', x))

        wordcloud = WordCloud(width=800, height=400, max_words=50).generate(' '.join(valid_domains_filtered))
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.write("Not enough valid domains to create a word cloud.")
else:
    st.write('## News Source Word Cloud')
    st.write('Not enough valid words to create a word cloud.')
