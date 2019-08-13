#!/usr/bin/env python
# coding: utf-8

# <h1>Segmenting and Clustering Neighborhoods in Toronto<h>
# 
#     

# <h>In this assignment, you will be required to explore, segment, and cluster the neighborhoods in the city of Toronto <h>

# <h2>Step 1:Getting the data and create a dataframe<h2>

# In[12]:


# import libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

# getting data from wikipedia
wikipedia_link='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
raw_wikipedia_page= requests.get(wikipedia_link).text

# using beautiful soup to parse the HTML/XML codes.
data = []
columns = []
table = soup.find(class_='wikitable')
for index, tr in enumerate(table.find_all('tr')):
    section = []
    for td in tr.find_all(['th','td']):
        section.append(td.text.rstrip())
    
#First row of data is the header
    if (index == 0):
        columns = section
    else:
        data.append(section)

#create Pandas DataFrame
canada_df = pd.DataFrame(data = data,columns = columns)
canada_df.head()


# In[20]:


#Remove Boroughs that are 'Not assigned'
canada_df = canada_df[canada_df['Borough'] != 'Not assigned']
canada_df.head()

# More than one neighborhood can exist in one postal code area, combined these into one row with the neighborhoods separated with a comma
canada_df["Neighbourhood"] = canada_df.groupby("Postcode")["Neighbourhood"].transform(lambda neigh: ', '.join(neigh))

#remove duplicates and update index
canada_df = canada_df.drop_duplicates()

if(canada_df.index.name != 'Postcode'):
    canada_df = canada_df.set_index('Postcode')
    
canada_df.head()


# In[14]:


# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough
canada_df['Neighbourhood'].replace("Not assigned", canada_df["Borough"],inplace=True)
canada_df.head()


# In[15]:


canada_df.shape


# <h2>Step 2:Generate maps to visualize the neighborhoods and how they cluster together<h2>

# In[21]:


#Get data lat/long data from csv
lat_long_coord_df = pd.read_csv("http://cocl.us/Geospatial_data ")

#rename columns and set the index 
lat_long_coord_df.columns = ["Postcode", "Latitude", "Longitude"]
if(lat_long_coord_df.index.name != 'Postcode'):
    lat_long_coord_df = lat_long_coord_df.set_index('Postcode')
    
lat_long_coord_df.head()


# In[19]:


canada_df = canada_df.join(lat_long_coord_df)
canada_df.head(11)

