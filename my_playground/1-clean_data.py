# -*- coding: utf-8 -*-

# Web scraping, pickle imports
import requests
from bs4 import BeautifulSoup
import pickle

# Scrapes transcript data from scrapsfromtheloft.com
def url_to_transcript(url):
    '''Returns transcript data specifically from scrapsfromtheloft.com.'''
    page = requests.get(url).text
    soup = BeautifulSoup(page)
    text = [p.text for p in soup.find_all('p')]
    print(url)
    return text

urls=[
"https://ascopubs.org/doi/abs/10.1200/JCO.2018.36.15_suppl.9045"
]

# load data from web first
# transcripts = {}
# for x in urls:
# 	print(url_to_transcript(x))
# 	data.update({'nsclc':url_to_transcript(x)})
# with open("transcripts/" + "nsclc" + ".txt", "wb") as file:
#     pickle.dump(transcripts['nsclc'], file)

data = {}
with open("transcripts/" + "nsclc" + ".txt", "rb") as file:
    data['nsclc'] = pickle.load(file)

print("------data------")
print(data)

##########################################################################################################
def combine_text(list_of_text):
    '''Takes a list of text and combines them into one large chunk of text.'''
    combined_text = ' '.join(list_of_text)
    return combined_text

# Combine it!
data_combined = {key: [combine_text(value)] for (key, value) in data.items()}

print("------data_combined------")
print(data_combined)

##########################################################################################################
import pandas as pd
pd.set_option('max_colwidth',150)
data_df = pd.DataFrame.from_dict(data_combined).transpose()
data_df.columns = ['transcript']
data_df = data_df.sort_index()
print("------data_df------")
print(data_df)

##########################################################################################################
# Apply a first round of text cleaning techniques
import re
import string

def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\n', '', text)
    text = re.sub('\d*', '', text)
    text = re.sub(' p ', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    return text

round1 = lambda x: clean_text_round1(x)
# Let's take a look at the updated text
data_clean = pd.DataFrame(data_df.transcript.apply(round1))
print("------data_clean------")
print(data_clean.transcript.loc['nsclc'])

#############################################################################################################

# Let's add the comedians' full names as well
full_names = ['nsclc']

data_df['full_name'] = full_names
print(data_df)

# Let's pickle it for later use
data_df.to_pickle("corpus.pkl")

############################################################################################################
# We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(stop_words='english')
data_cv = cv.fit_transform(data_clean.transcript)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = data_clean.index
print("-----data_dtm------")
print(data_dtm)

# Let's pickle it for later use
data_dtm.to_pickle("dtm.pkl")

# Let's also pickle the cleaned data (before we put it in document-term matrix format) and the CountVectorizer object
data_clean.to_pickle('data_clean.pkl')
pickle.dump(cv, open("cv.pkl", "wb"))

