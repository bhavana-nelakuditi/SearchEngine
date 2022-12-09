#!/usr/bin/env python
# coding: utf-8

# In[16]:


# Name: Bhavana Nelakuditi
# UIN: 667225823

import pickle
from collections import Counter
import copy
import math


# In[57]:


pickle_directory = "PickleFiles/"
pickle_inverted_index = open(pickle_directory+"inverted_index.pickle","rb")
inverted_index = pickle.load(pickle_inverted_index)

pickle_word_dict = open(pickle_directory+"word_dict.pickle","rb")
word_dict = pickle.load(pickle_word_dict)

pickle_document_list = open(pickle_directory+"document_list_tokens.pickle","rb")
document_list = pickle.load(pickle_document_list)


# In[58]:


index_number = 6001

frequency = {}
tf_idf = {}


# In[59]:


#Calculating IDF
idf = {}

for key in inverted_index.keys():
    df = len(inverted_index[key].keys())
    idf[key] = math.log2(index_number/df)
    
for page in word_dict:
    frequency[page] = Counter(word_dict[page]).most_common(1)[0][1]


# In[60]:


tf_idf = copy.deepcopy(inverted_index)

for token in tf_idf:
    for page in tf_idf[token]:
        tf = tf_idf[token][page] / max_freq[page]
        tf_idf[token][page] = tf * idf[token]
tf_idf


# In[61]:


def document_length(doc, doc_tokens):
    doc_len = 0
    for token in set(doc_tokens):
        doc_len += tf_idf[token][doc] ** 2
    doc_len = math.sqrt(doc_len)
    return doc_len

def page_document_length(list_of_tokens):
    doc_lens = {}
    for page in list_of_tokens:
        doc_lens[page] = document_length(page, list_of_tokens[page])
    return doc_lens


# In[62]:


pages_lens = page_document_length(word_dict)


# In[55]:


with open(pickle_directory + 'pages_lens.pickle', 'wb') as f:
    pickle.dump(pages_lens,f)
with open(pickle_directory + 'idf.pickle', 'wb') as f:
    pickle.dump(idf,f)
with open(pickle_directory + 'tf_idf.pickle', 'wb') as f:
    pickle.dump(tf_idf,f)


# In[ ]:




