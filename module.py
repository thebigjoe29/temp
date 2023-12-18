#!/usr/bin/env python
# coding: utf-8

# ## Importing data manipulation libraries 

# In[30]:


import pandas as pd
import numpy as np
import bcrypt
from pymongo import MongoClient


# ## Establishing server connection - MongodB

# In[31]:


try:
    # Connect to the MongoDB server
    client = MongoClient('mongodb+srv://pjt123:pjt12345678@profile.ifhh9x7.mongodb.net')
    db = client.recommendation_system
    collection = db.profiles
    print("Connected to MongoDB successfully!")
    
except Exception as e:
      print(f"Error connecting to MongoDB: {e}")


# ## Establishing database connection - MongoDb 

# In[32]:


#Function to connect to database
def update_data():
    global data
    data = pd.DataFrame(list(collection.find()))
    #data


# In[33]:


update_data()


# ## Defining profile creation and login functions 

# In[34]:


#Function to encrypt password with hashing
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


# In[35]:


def check_password(email, password):
    user = collection.find_one({"Email": email})
    
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        print("Successful login!")

        global user_name, actual_interests, actual_collaborations
        user_name = user['Name']

        # Extract interests and collaborations from the data DataFrame
        user_data = data[data['Name'] == user_name]
        if not user_data.empty:
            actual_interests = set(user_data['interest'].values[0].split(','))
            actual_collaborations = set(user_data['collaboration'].values[0].split(','))
        else:
            print(f"Warning: No data found for user {user_name}")
        return {
            'authentication': True,
            'currentUser':user_name
        }
    else:
        return {
            'authentication': False
        }

# In[36]:


#Funtion to create profile and update database
def create_profile():
    print("Let's create your profile")
    print(" ")
    
    email=str(input("Enter your Email "))
    query = {"Email": email}
    result = collection.find_one(query)
    if(result):
        print("Email already exists")
        print("")
        create_profile()
    password=str(input("Enter your password"))
    password2=str(input("Repeat your password"))
    if(password!=password2):
        print("Passwords did not match")
        print("")
        create_profile()
    password=hash_password(password)
    name=str(input("Enter your name "))
    profession=str(input("Enter your profession "))
    year=str(input("Enter your year of study - if student "))
    interest=str(input("What are you interested to do? "))
    collaboration=str(input("Who do you want to collaborate with? "))
    topic=str(input("Enter topic of interest "))
    skills=str(input("Enter your skills "))
    experience=str(input("Enter your experience - if professional "))
    
    dict={"Name":name,"Email":email,"profession":profession,"Year":year,"interest":interest,"collaboration":collaboration,"Topic":topic,"Skills":skills,"experience":experience,"password":password}
    x = collection.insert_one(dict)
    print("Profile created successfully")


# In[37]:


#Function to authenticate user login
def user_login():
    email=str(input("Enter your Email "))
    password=str(input("Enter your password"))
    check_password(email, password)


# ## Executing authentication and profile creation 

# In[38]:



# ## Importing NLP libraries 

# In[40]:


import nltk
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


# In[41]:


#Listing out stopwords in english
x=stopwords.words('english')


# ## Text prepocessing 

# In[46]:


#Cleaning topic column and appending to list

topic_processed=[]
for i in range(len(data)):
    topic=data.loc[i, 'Topic']
    topic=re.sub('[^a-zA-Z]',' ',topic)
    topic=topic.lower()
    topic=topic.split()
    ps=PorterStemmer()
    topic=[ps.stem(word) for word in topic if not word in set(stopwords.words('english'))]
    topic=' '.join(topic)
    topic_processed.append(topic)


# In[49]:


#Cleaning skills column and appending to list
skills_processed=[]
for i in range(len(data)):
    skills=data.loc[i, 'Skills']
    skills=re.sub('[^a-zA-Z]',' ',skills)
    skills=skills.lower()
    skills=skills.split()
    ps=PorterStemmer()
    skills=[ps.stem(word) for word in skills if not word in set(stopwords.words('english'))]
    skills=' '.join(skills)
    skills_processed.append(skills)


# ## Building a recommendation system 

# In[50]:


#TF-IDF vectorization
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(topic_processed)
cosine_similarities = linear_kernel(matrix,matrix)
name=(data['Name'])
interest=(data['interest'])
collaboration=(data['collaboration'])
indices = pd.Series(data.index, index=data['Name'])


# In[51]:


#Taking into consideration collaboration interests
df = pd.DataFrame({'name': name,'interest':interest, 'collaboration':collaboration})


# In[52]:


#Defining a recommender function
def profile_recommender(name):
    idx = indices[name]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:5] 
    name_indices = [i[0] for i in sim_scores]
    
    #Recommended profiles based on NLP performed on skills
    recom_profiles=df.iloc[name_indices]
    
    #Considering interests and collaborations specified by the user
    input_interests = set(df.loc[df['name'] == name, 'interest'].values[0].split(','))
    input_collaborations = set(df.loc[df['name'] == name, 'collaboration'].values[0].split(','))
    
    #Filterting recommended profiles who have common interests and collaborations
    common_interests = recom_profiles[recom_profiles['interest'].apply(lambda x: any(item in input_interests for item in x.split(',')))]
    common_collaborations = recom_profiles[recom_profiles['collaboration'].apply(lambda x: any(item in input_collaborations for item in x.split(',')))]
    
    #Merging the filtered data
    merged_recommendations = pd.merge(common_interests, common_collaborations, on='name', how='inner')
    
    return merged_recommendations
    


# ## Recommending names 

# In[53]:




# In[ ]:




