#!/usr/bin/env python
# coding: utf-8

# ## SALES ANALYSIS PROJECT
# 
# ### Import Necessary Libraries

# In[1]:


pip install pandas


# In[17]:


import pandas as pd
import os


# ### Merging 12 Months of Data into a single file

# In[15]:


df = pd.read_csv ("/Users/mac/Desktop/projects/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/Sales_April_2019.csv")


# In[21]:


files = [file for file in os.listdir("/Users/mac/Desktop/projects/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data")]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv ("/Users/mac/Desktop/projects/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, df])

all_months_data.to_csv("all_data.csv", index=False)
    


# #### Read in updated dataframe

# In[64]:


all_data = pd.read_csv("/Users/mac/Desktop/projects/Pandas-Data-Science-Tasks-master/SalesAnalysis/Sales_Data/all_data.csv")
all_data.head()


# ### Clean the data

# #### Drop rows of NaN

# In[65]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()


# In[68]:


all_data = all_data.dropna(how='all')
nan_df.head()


# #### Find 'Or' and delete it

# In[75]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']


# #### Convert columns to the correct type

# In[79]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered']) # Make int
all_data['Price Each'] = pd.to_numeric(all_data['Price Each']) # Make float


# ### Augment data with Additional Columns

# #### Add month column

# In[76]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# #### Add a sales column

# In[80]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# #### Add a city column

# In[98]:


# Using the .apply method to split the purchase address to get the different cities
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")

all_data.head()


# In[ ]:





# ###  Calculate sales by month and visualize what month has the most sales 

# In[84]:


# Showing sales volume by months
results = all_data.groupby('Month').sum()
results.head()


# In[86]:


# Plot a bar chart showing sales volume by months
import matplotlib.pyplot as plt

months = range(1,13)

plt.bar(months,results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')

plt.show


# ### What US city has the highest number of sales?

# In[99]:


# Separating the city from the Address data type and parsing into a new column
results = all_data.groupby('City').sum()
results


# In[109]:


# Plot bar chart showing sales by city
import matplotlib.pyplot as plt

cities = [city for city, df in all_data.groupby('City')]

plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City name')

plt.show


# ### When should we display advertisement to maximize patronage?

# #### Change 'Order Date' to a date time data type

# In[111]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# #### Create columns to show the hours and minutes from the Order Date column

# In[114]:


# Seperate the hours and minutes data from the Order date type and parse them into new columns
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data.head()


# In[120]:


# Plot the graph that shows the relationship between different times of the day and sales
hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby(['Hour']).count())
all_data.groupby(['Hour']).count()

plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()

plt.show

# My recommendation is to advertise between 10-11am and 6-7pm


# ### What products are often sold together?

# In[130]:


# This is going to help group at least two products that were sold to the same customer i.e bought together
df = all_data[all_data['Order ID'].duplicated(keep=False)]

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))

df = df[['Order ID', 'Grouped']].drop_duplicates()
df.head(10)


# In[135]:


# This is going to further group and then assign the products sold together to their Order IDs
from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))
    
for key, value in count.most_common(10):
    print(key, value)


# ### What product sold the most and why?

# In[151]:


# Plot graph showing the sales for each product 
product_group = all_data.groupby('Product')

quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]
plt.title('Quantity Ordered by Product')
plt.bar(products, quantity_ordered)
plt.ylabel("Quantity Ordered")
plt.xlabel('Product')
plt.xticks(products, rotation='vertical', size=8)
plt.show()


# In[150]:


# Plot the graph with a sub axis showing price
prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='y')
ax2.plot(products, prices, 'g-')
plt.title('Quantity Ordered by Product by Price')
ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='y')
ax2.set_ylabel('Price($)', color='g')
ax1.set_xticklabels(products, rotation='vertical', size=8)

plt.show()


# In[ ]:





# In[ ]:




