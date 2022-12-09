#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Name: Bhavana Nelakuditi
# UIN: 667225823

import requests
import os
import pickle
from bs4 import BeautifulSoup
from collections import deque


# In[ ]:


# Creating and deploying a web crawler
# Domain limitation for web agent
domain = "uic.edu"
start_url = "https://cs.uic.edu/"
# Index number for the crawler
crawl_index = 6000


# In[ ]:


# Directory to store the pages crawled
pages_folder = "./CrawledPages/"
error_file = "error.txt"


# In[ ]:


extensions = [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".css", ".js", ".aspx", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".mp4", ".avi", ".tar", ".gz", ".tgz", ".zip"]


# In[ ]:


# Queue to maintain the webpages list for breadth first search traversal
webpage_queue = deque()
webpage_queue.append(start_url)
crawl_urls = []
crawl_urls.append(start_url)
pages_crawled = {}
page_no = 0


# In[ ]:


while webpage_queue:

    try:
        # Get the url at index position
        url = webpage_queue.popleft()
        rqst = requests.get(url)

        if rqst.status_code == 200:
            soup = BeautifulSoup(rqst.text, "lxml")
            tags_extracted = soup.find_all("a")

            if len(tags_extracted) != 0:
                pages_crawled[page_no] = url
                output_file = pages_folder + str(page_no)

                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(rqst.text)
                file.close()

                for tag in tags_extracted:
                    link = tag.get("href")

                    if (
                        link is not None
                        and link.startswith("http")
                        and not any(ext in link.lower() for ext in extensions)
                    ):

                        link = link.lower()
                        link = link.split("#")[0]
                        link = link.split("?", maxsplit=1)[0]
                        link = link.rstrip("/")
                        link = link.strip()

                        if link not in crawl_urls and domain in link:
                            webpage_queue.append(link)
                            crawl_urls.append(link)

                if len(pages_crawled) > crawl_index:
                    break

                page_no += 1

    except Exception as e:
        with open(error_file, "a+") as log:
            log.write(f"Coonection Failed for  {url}")
            log.write(f"{e}\n\n")
        log.close()
        continue


# In[ ]:


pickle_directory = "./PickleFiles/"
os.makedirs(pickle_directory, exist_ok=True)
with open(pickle_directory + "crawled_pages.pickle", "wb") as f:
    pickle.dump(pages_crawled, f)

