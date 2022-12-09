#!/usr/bin/env python
# coding: utf-8

# In[69]:


# Name: Bhavana Nelakuditi
# UIN: 667225823

from tkinter import *
import pickle
import string
import nltk
import re
import numpy as np
from collections import Counter
import math
import webbrowser
#from ipynb.fs.full.Website_PreProcessing import tokenize_text


# In[35]:


pickle_directory = "PickleFiles/"
pickle_pages_lens = open(pickle_directory+"pages_lens.pickle","rb")
pages_lens = pickle.load(pickle_pages_lens)

pickle_idf = open(pickle_directory+"idf.pickle","rb")
idf = pickle.load(pickle_idf)

pickle_tf_idf = open(pickle_directory+"tf_idf.pickle","rb")
tf_idf = pickle.load(pickle_tf_idf)

pickle_url = open(pickle_directory + 'pages_crawled.pickle', 'rb')
urls = pickle.load(pickle_url) 


# In[7]:


f = open("stopwords.txt", 'r')
stopwords=f.read()
stopwords = stopwords.split("\n")


# In[68]:


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


# In[26]:


def cosine_similarity(query, doc_lens):
    similarity_scores = {}
    query_len = 0
    query_weights = {}
    
    query_dict = Counter(query)
    
    for token in query_dict.keys():
        token_tf = query_dict[token] / query_dict.most_common(1)[0][1]
        query_weights[token] = token_tf * idf.get(token,0)
        query_len += query_weights[token] ** 2
    
    query_len = math.sqrt(query_len)

    for token in query:
        token_weight = query_weights.get(token)
        if token_weight:
            for page in tf_idf[token].keys():
                similarity_scores[page] = similarity_scores.get(page,0) + (tf_idf[token][page] * token_weight)
   
    for page in similarity_scores:
        similarity_scores[page] = similarity_scores[page] / (doc_lens[page] * query_len)
    return similarity_scores


# In[45]:


def display_pages(count,webpages):
    url_list = []
    for i in range(count, count+10):
        try:
            url_no = int(webpages[i][0])
            
        except Exception as e: 
            print("\n No more results found !!")
            break
        if urls.get(url_no, None):
            url_list.append(urls.get(url_no))
            #print(i+1,urls.get(url_no))
    return url_list


# In[65]:


count = 0
current_result = []
def callback(event):
    webbrowser.open_new(event.widget.cget('text'))

def searched():
    children = window.winfo_children()
    for child in children:
        if str(type(child)) == "<class 'tkinter.Frame'>":
            child.destroy()
    frame = Frame(window)
    
    query = txt.get()
    query_tokens = []
    processed_query = tokenize_text(query)
    for i in processed_query:
            if len(i) > 2 and i not in stopwords:
                stemmed_word = implement_stemmer(i)
                if stemmed_word not in stopwords:
                    query_tokens.append(stemmed_word)
    print("Query tokens ", query_tokens)

    similar_pages = cosine_similarity(query_tokens, pages_lens)
    sorted_pages = sorted(similar_pages.items(), key= lambda x: x[1], reverse=True)
    global current_result
    current_result = sorted_pages
    links = display_pages(count,sorted_pages)
    
    print(sorted_pages[:10])
    
    if len(links) == 0:
        link = Label(frame, text="There are no results for this query.")
        link.pack()
    else:
        page_limit = 10
        if len(links) < 10:
            page_limit = len(links)
        current_result = current_result[page_limit:]
        for i in range(page_limit):
            link = Label(frame, text=(links[i]), fg='blue', cursor='hand2')
            link.pack()
            link.bind("<Button-1>", callback)
    frame.pack()


# In[66]:


def more_results():
    children = window.winfo_children()
    for child in children:
        if str(type(child)) == "<class 'tkinter.Frame'>":
            child.destroy()
    frame = Frame(window)
    global current_result
    links = display_pages(0,current_result)
    if len(current_result) < 10:
        link = Label(frame, text="There are no results for this query.")
        link.pack()
    else:
        page_limit = 10
        if len(current_result) < page_limit:
            page_limit = len(links)
        current_result = current_result[page_limit:]
        for i in range(page_limit):
            link = Label(frame, text=(links[i]), fg='blue', cursor='hand2')
            link.pack()
            link.bind("<Button-1>", callback)
    frame.pack()


# In[ ]:


window = Tk()
window.title("Web Search Engine for UIC Domain")
window.geometry('800x800')

welcome = Label(window, text="Welcome to UIC Search Engine, Enter your query below")
welcome.pack()

txt = Entry(window, width=60)
txt.pack()
btn = Button(window, text='Search', command=searched)
btn.pack()

btn = Button(window, text="More results", command=more_results)
btn.pack()

window.mainloop()


# In[ ]:




