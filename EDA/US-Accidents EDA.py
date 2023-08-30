#!/usr/bin/env python
# coding: utf-8

# # US Accidents Exploratory Data Analysis
# Explore the vast landscape of US Accidents data through insightful visualizations and statistical analysis, gaining valuable insights into the factors influencing road safety and traffic incidents
# 
# * **Source** : Kaggle
# * **Dataset**: 4.2 Million+ records
# * New York Accidents Data is not recorded.

# ### Data Loading

# In[80]:


import opendatasets as od

download_url='https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents'
od.download(download_url)


# In[3]:


data_filename='./us-accidents/US_Accidents_March23.csv'


# ## Data Preparation and Cleaning

# In[1]:


import pandas as pd


# In[4]:


df=pd.read_csv(data_filename)


# In[5]:


df.info()


# In[6]:


df.describe()


# In[7]:


#count of numeric columns only

numerics=['int16','int32','int64','float16','float32','float64']
numeric_df=df.select_dtypes(include=numerics)

len(numeric_df.columns)


# In[11]:


#percentage of missing values per column 

missing_percentages= df.isna().sum().sort_values(ascending=False)/len(df)
missing_percentages


# In[60]:


#Plotting missing percentages

m=missing_percentages[missing_percentages != 0].plot(kind='barh', color='skyblue')
m.grid(False)


# **You can remove useless columns or select useful columns only.**

# ## Exploratory Analysis and Visualization

# **Columns Selection**
# * City
# * Start_Time
# * Start_Lat and Start_Lng
# * Temperature
# * Weather condition

# ### City

# In[14]:


# US-Cities are around 19K while in this dataset around 14k is used.

cities_data=df.City.unique()
len(cities_data) 


# In[15]:


# No.of unique values in column City

cities_by_accident=df.City.value_counts()
cities_by_accident[:20]


# In[16]:


# No.of states in US is 50 and few terrorities it all sum up to 52

'NY' in df.State 


# **New York State data is not included in dataset.**

# In[59]:


# Plotting City-by-accident data

c=cities_by_accident[:20].plot(kind='barh', color='skyblue')
c.grid(False)


# In[41]:


import seaborn as sns 
sns.set_style('whitegrid')
sns.set_palette("Set2")
import matplotlib.pyplot as plt


# In[42]:


# In order to see distribution of data

sns.histplot(cities_by_accident,log_scale=True) 

plt.title("Distribution of Accidents")
plt.grid(True, alpha=0.3)


# In[43]:


# Cities and no.of accidents occurences

cities_by_accident[cities_by_accident==1]


# ### Start Time

# In[44]:


df.Start_Time


# In[45]:


df.Start_Time=pd.to_datetime(df.Start_Time)


# In[46]:


# Figuring out accidents by hour in percentages 

sns.distplot(df.Start_Time.dt.hour, bins=24, kde=False, norm_hist=True)

plt.title("Distribution of Accidents by Hour")
plt.grid(True, alpha=0.3)


# In[51]:


# Figuring out accidents by day of week in percentages 

sns.distplot(df.Start_Time.dt.dayofweek, bins=7, kde=False ,norm_hist=True)

plt.xticks(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.title("Distribution of Accidents by Week Days")
plt.grid(True, alpha=0.3)


# **Is the distribution of accidents by hour is same on weekends as on weekdays?**
# ON weekends peak occurs in afternoon unlike weekdays.

# In[50]:


# Plotting weekend accident occurences with reect to Time

Sundays_Start_Time=df.Start_Time[df.Start_Time.dt.dayofweek==6 ]

sns.distplot(Sundays_Start_Time.dt.hour, bins=24, kde=False, norm_hist=True)

plt.title("Distribution of Accidents by Weekend")
plt.grid(True, alpha=0.3)


# **ON weekends peak occurs in afternoon unlike weekdays.**

# In[49]:


# Figuring out accidents by months in percentages 

sns.distplot(df.Start_Time.dt.month, bins=12, kde=False, norm_hist=True)

plt.title("Distribution of Accidents by Months")
plt.grid(True, alpha=0.3)


# **Highest number of accidents at end of year BUT**
#  * Whey are there more accidents in Winter? Because of icy roads etc (Inspect further)
#  * Is there something to do with sources of data? Inspect

# In[52]:


# Data sources column analysis due to unusual patterns

df.Source


# In[53]:


df.Source.value_counts().plot(kind='pie')

plt.title("Sources Data")
plt.grid(True, alpha=0.3)


# In[55]:


# Checkibg year vise data and sources

df_2016=df[df.Start_Time.dt.year==2016]
df_2016_Source=df_2016[df_2016.Source=='Source2']


# In[56]:


#Plotting distribution by year

sns.distplot(df_2016_Source.Start_Time.dt.month, bins=12, kde=False, norm_hist=True)

plt.title("Distribution of Accidents by Year")
plt.grid(True, alpha=0.3)


# **Years data is pretty much balanced BUT**
# * Much data is missing from 2016,2017.Thus,source 2 seems to have missing data.
# * Consider removing it coz that may lead to inaccurate conclusions.

# ### Start-lat and Start_lng 

# In[57]:


# Plotting longitude and lattitude

sns.scatterplot(x=df.Start_Lng,y=df.Start_Lat,size=0.001)

plt.title(" Location of Accidents by Latittude & Longitude")
plt.grid(True, alpha=0.3)


# In[114]:


get_ipython().system('pip install folium --quiet')
import folium
from folium.plugins import HeatMap


# In[116]:


# Turns lat and long into list of pairs and zip them up for heat map data

(zip(list(df.Start_Lng),list(df.Start_Lng)))


# In[61]:


# Taking sample from data for plotting heat map

sample_df=df.sample(int(0.01*len(df)))
lat_lon_pairs=list(zip(list(df.Start_Lng),list(df.Start_Lng)))


# In[ ]:


# Heat Map (due to large amount of data ,memory run out ....) 

map=folium.Map()
HeatMap(lat_lon_pairs[:100]).add_to(map)
map


# # Summary and Conclusion
# 
# ### Insights
# * No data for NY
# * Less than (5%) cities have more than nearly 1000 accidents
# * More than 1000 cities have reported just one accident
# * No.of accidents per city decreases  exponentianlly
# * Higher % of accidents between 6am to 8am (traffic,office hour) next highest % is 3pm to 6pm.
# 

# ### Questions
# 
# * Which state has the highest number of accidents?
# * Are there more accidents in warmer areas or colder areas?
# * Accidents per capita
# * Why does new york not show up in data? if yes why is the count lower as it is most populated in US?
# * Among top 100 cities in number of accidents which states do they belong to most frequently?
# * What time of day are accidents more frequent in?
# * Which days of the week have the most accidents?
# * Which months have the most accident?
# * What is the trend of accidents year over year(decr,inc)?
