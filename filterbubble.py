import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from urllib.parse import urlparse

# Hämta history.csv från URL
url = 'https://bestofworlds.se/filterbubble/data/history.csv'
df = pd.read_csv(url, header=None, names=['date', 'domain'])

# Funktion för att extrahera domännamn
def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.hostname
    # Filtrera bort subdomäner (t.ex. www)
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

# Extrahera domäner
valid_domains = df['domain'].dropna().apply(extract_domain)

# Filtrera bort tomma strängar och subdomäner
valid_domains = valid_domains[valid_domains != '']
valid_domains = valid_domains.apply(lambda x: re.sub(r'^www\.', '', x))

# Räkna förekomster av domännamn
domain_counts = valid_domains.value_counts()

# Visa stapeldiagram med Plotly
st.write('## Topp 10 Domäner')
st.bar_chart(domain_counts.head(10))

# Wordcloud (endast om tillräckligt med data)
if len(valid_domains) > 0:
  st.write('## Wordcloud av domäner')

  # Filtrera bort korta ord
  valid_domains_filtered = valid_domains[valid_domains.apply(lambda x: len(x.split('.')) > 1)]

  # Skapa wordcloud
  if len(valid_domains_filtered) > 0:
    wordcloud = WordCloud(width=800, height=400, max_words=50).generate(' '.join(valid_domains_filtered))
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
  else:
    st.write("Inte tillräckligt med data för att skapa en wordcloud.")
else:
  st.write('## Wordcloud av domäner')
  st.write("Inte tillräckligt med data för att skapa en wordcloud.")
