
# Importing required libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import streamlit as st
from PIL import Image


# **loading dataset**
st.title('RunKeeper Analysis')
image = Image.open('runner_in_blue.jpg')
st.image(image, use_column_width=True)


dataset = pd.read_csv('cardioActivities.csv',parse_dates=True,index_col='Date')


# In[3]:


dataset.info()


# **We see that there are total 508 observations and 13 columns**

# In[4]:

st.markdown('## review raw data')
st.dataframe(dataset.head())


# ## Data Preprocessing

# **There are a few columns which we don't require for analysis like activity Id,Route Name ( becuase there's a sinlge route ), Friend's Tagged, Notes and GPX File so we need to remove these columns**

# In[5]:


cols = ['Activity Id','Route Name',"Friend's Tagged",'Notes','GPX File']


# dropping the unnecessary columns
dataset.drop(columns=cols, axis=1, inplace=True)

st.header('After preprocessing')
st.write(dataset)


st.markdown('## Activities')
plt.figure(figsize=(10,5))
sns.countplot(x=dataset.Type)
st.pyplot()
st.write("It seems that most of the people like running")

# counting missing values
st.header('Missing values')
st.bar_chart(dataset.isnull().sum(),height=400)
st.write("Average Heat Rate column has the great number of missing values")

st.write("before filling the missing values let's first check if we have the outliers, accordingly we will fill the missing values")
# boxplot to see outliers
sns.boxplot(x=dataset['Average Heart Rate (bpm)'])
st.pyplot()

st.write("As we know that mean() is sensitive to outliers that's why we will fill the missing values with median")
dataset['Average Heart Rate (bpm)'].fillna(dataset['Average Heart Rate (bpm)'].median(), inplace=True)
st.write(' Let us see if we have left missing values ')
st.write(dataset.isnull().mean())

# Plotting running data
st.header('Plotting running data')
dataset[dataset['Type']=='Running'].plot(subplots=True,
               sharex=False,
               figsize=(10,12),
               linestyle='none',
               marker='o',
               markersize=3,
              )
st.pyplot()


# Running statistics
st.header('Running statistics')
st.dataframe(dataset[dataset['Type']=='Running'].resample('A').mean())


# Questions
st.markdown('* What is your average distance?')
st.bar_chart(dataset.groupby(dataset['Type']=='Running')['Distance (km)'].mean())
st.markdown('* How fast do you run?')
st.bar_chart(dataset.groupby(dataset['Type']=='Running')['Average Speed (km/h)'].mean())
st.markdown('* Do you measure your heart rate?')
st.bar_chart(dataset.groupby(dataset['Type']=='Running')['Average Heart Rate (bpm)'].mean())



# weekly statistics average
st.markdown('**Weekly statistics average**')
st.dataframe(dataset[dataset['Type']=='Running'].resample('W').mean().mean())


# Visualization with averages
st.header('Visualization with averages')
st.markdown('**Calories burned per activity**')
st.bar_chart(dataset.groupby(['Type'])['Calories Burned'].mean())


# creating running activity dataset
running = dataset[dataset['Type']=='Running']


# running distance average
dist_avrg=running['Distance (km)'].mean()
# running heart rate average
heart_avrg=running['Average Heart Rate (bpm)'].mean()

# creating subplots
fig, (ax1,ax2) = plt.subplots(2, figsize=(8,8))

# plotting running distance
running['Distance (km)'].plot(ax=ax1, label= f'average {dist_avrg:.4f} km', color='tomato')
ax1.set(ylabel='Distance (km)', title='Historical data with averages')
ax1.axhline(running['Distance (km)'].mean(), color='black', linewidth=1, linestyle='-.')
ax1.legend()


# plotting heart rate
running['Average Heart Rate (bpm)'].plot(ax=ax2, label= f'average {heart_avrg:.4f} bpm', color='gray')
ax2.set(xlabel='Date', ylabel='Average Heart Rate (bpm)')
ax2.axhline(running['Average Heart Rate (bpm)'].mean(), color='red', linewidth=1, linestyle='-.')
ax2.legend()
st.pyplot()



# Did I reach my goals
st.header('Did I reach my goals')
goal=dataset.groupby(dataset['Type']=='Running')['Distance (km)'].resample('A').sum()

plt.figure(figsize=(12,8))
ax=goal.plot(marker='o', markersize=16, linewidth=0, color='white')
ax.set(ylim=[0, 1210],
       ylabel='Distance (km)',
       xlabel='Years',
       title='Annually covered distance')
plt.xticks(rotation=-8)
ax.axhspan(1000, 1210, color='gray', alpha=0.4)
ax.axhspan(800, 1000, color='red', alpha=0.3)
ax.axhspan(0, 800, color='blue', alpha=0.2)
st.pyplot()


# Am I progressing
st.header('Am I progressing')
st.line_chart(running['Distance (km)'].resample('W').bfill())

# Training Intensity
st.header('Training Intensity')
plt.figure(figsize=(8,5))
sns.scatterplot(x=running['Distance (km)'], y=running['Average Heart Rate (bpm)'])
plt.title('Training intensity', size=16)
st.pyplot()


# Detailed summary report
st.header('Detailed summary report')
summary = dataset.groupby('Type')['Distance (km)', 'Climb (m)', 'Average Speed (km/h)'].describe()
st.dataframe(summary.stack())
