#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Name: Bhavana Nelakuditi
# UIN: 667225823

get_ipython().run_line_magic('pip', 'install numpy')
get_ipython().run_line_magic('pip', 'install nltk')
import os
import string
import nltk
import re
import numpy as np
from bs4 import BeautifulSoup
from bs4.element import Comment


# In[1]:


get_ipython().system('python -V')


# In[3]:


directory = "CrawledPages/"


# In[4]:


# Adding the stopwords to a list
f = open("stopwords.txt", 'r')
stopwords=f.read()
stopwords = stopwords.split("\n")
stopwords


# In[5]:


# Pre-Processing methods
def filter_text(website):
    soup = BeautifulSoup(website, features ="lxml")
    content = soup.find_all(text=True)
    textual_content = []
    for text in content:
        if not (text.parent.name in ['style', 'script', 'head', 'meta', '[document]']) and not (isinstance(text, Comment)) and not (re.match(r"[\s\r\n]+",str(text))):
            textual_content.append(text)
            
    return " ".join(term.strip() for term in textual_content)
    

def tokenize_text(data):
    
    #Removing SGML tags
    data = re.sub(r'<.*?>','',data)
    #remove punctuation, turns it to lower case
    data = removePunctuation(data)
    data = data.lower()
    data = data.strip()
    
    # Removing numbers
    data = re.sub(re.compile('[0-9]'), '', data)
    
    
    #used split fucntion to tokenise the data on whitespace
    tokens = data.split()   
    return tokens

def removePunctuation(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# Stemming each word
def implement_stemmer(token):
    sno = nltk.stem.SnowballStemmer('english')
    return sno.stem(token)


# In[6]:


# include a function that tokenizes the text
NumberOfWords = 0
word_dict = {}
document_list = []
document_count =0
inverted_index = {}
os.getcwd()
for filename in os.listdir(directory):
        word_list =[]
        file=directory+'/'+filename
        f = open(file, 'r', encoding="utf8")
        document_count+=1
        website=f.read()
        data = filter_text(website)
        tokens = tokenize_text(data)
        
        # What is the total number of words in the collection?
        #NumberOfWords = NumberOfWords + len(tokens)
        
        # What is the vocabulary size?
        for i in tokens:
            if len(i) > 2 and i not in stopwords:
                stemmed_word = implement_stemmer(i)
                if stemmed_word not in stopwords:
                    word_list.append(stemmed_word)
                    NumberOfWords+=1
        document_list.append(word_list)
        word_dict[filename] = word_list
        for token in word_list:
            freq = inverted_index.setdefault(token,{}).get(filename,0)
            inverted_index.setdefault(token,{})[filename] = freq  + 1 


# In[13]:


print(NumberOfWords,
document_list[:10],
document_count)


# In[14]:


import pickle
pickle_directory = "PickleFiles/"
os.makedirs(pickle_directory, exist_ok=True)
with open(pickle_directory + 'inverted_index.pickle', 'wb') as f:
    pickle.dump(inverted_index,f)
    
with open(pickle_directory + 'word_dict.pickle', 'wb') as f:
    pickle.dump(word_dict,f)


# In[15]:


with open(pickle_directory + 'document_list_tokens.pickle', 'wb') as f:
    pickle.dump(document_list,f)


# In[ ]:




