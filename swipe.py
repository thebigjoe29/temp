#!/usr/bin/env python
# coding: utf-8

# In[15]:


#Importing libraries
from pymongo import MongoClient


# In[14]:


# Establishing database connection
client = MongoClient('mongodb+srv://pjt123:pjt12345678@profile.ifhh9x7.mongodb.net')
db = client.recommendation_system
swipe_collection = db.swipe 

