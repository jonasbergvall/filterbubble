import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tldextract
import re

# Hämta history.csv från URL
url = 'https://bestofworlds.se/filterbubble/data/history.csv'
df = pd.read_csv(url, header=None, names=['date', 'domain'])

# Funktion för att extrahera domän och protokoll
def extract_domain(url):
    try:
        parsed = tldextract.extract(url)
        protocol = parsed.scheme
        domain = f"{parsed.domain}.{parsed.suffix}"
        return f"{protocol}//{domain}" if parsed.subdomain else f"{protocol}//{parsed.domain}"
    except Exception as e:
        print(f"Error processing URL: {url} - {e}")
        return url  # Return the original URL if parsing fails


# Extrahera domäner med protokoll
valid_domains = df['domain'].dropna().apply(extract_domain)

# Filtrera bort tomma strängar och subdomäner
valid_domains = valid_domains[valid_domains != '']
valid_domains = valid_domains.apply(lambda x: re.sub(r'^www\.', '', x))

# Räkna förekomster av protokoll
protocol_counts = valid_domains.value_counts()

# Visa stapeldiagram med Plotly
st.write('## Fördelning av http och https')
st.bar_chart(protocol_counts)

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
