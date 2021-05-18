#!/usr/bin/env python
# coding: utf-8

# <center><h1> Investment Analysis Assignment </h1></center>

# # Reading Data

# In[301]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as tick


# In[302]:


companies_df = pd.read_csv('companies.txt', sep='\t',  encoding="iso-8859-1")
rounds_df = pd.read_csv('rounds2.csv',  encoding="iso-8859-1")


# In[303]:


companies_df.head()


# In[304]:


rounds_df.head()


# # Checkpoint 1: Data Cleaning 1

# ## 1. How many unique companies are present in rounds2?

# In[305]:


companies_df.permalink = companies_df.permalink.str.lower()
rounds_df.company_permalink = rounds_df.company_permalink.str.lower()
companies_df.name = companies_df.name.str.lower()


# In[306]:


temp = pd.merge(companies_df, rounds_df, left_on= 'permalink', right_on = 'company_permalink', how = 'inner')
temp.describe(include = 'all')


# ## 2. How many unique companies are present in companies?

# In[307]:


companies_df.describe(include = 'all')


# ## 3. In the companies data frame, which column can be used as the unique key for each company?

# In[308]:


companies_df[['permalink', 'name']].drop_duplicates().count()


# ## 4. Are there any companies in the rounds2 file which are not present in companies? Answer yes or no: Y/N

# In[309]:


set(rounds_df.company_permalink.unique()).difference(companies_df.permalink.unique())


# ## 5. Merge the two data frames so that all variables (columns) in the companies frame are added to the rounds2 data frame. Name the merged frame master_frame. How many observations are present in master_frame?

# In[310]:


master_frame = pd.merge(rounds_df, companies_df, left_on= 'company_permalink', right_on = 'permalink', how = 'left')
print(len(rounds_df), len(companies_df), len(master_frame))


# In[311]:


master_frame.head()


# # Checkpoint 2: Funding Type Analysis

# In[312]:


temp = pd.DataFrame(master_frame.groupby('funding_round_type').raised_amount_usd.mean()).reset_index()
temp.raised_amount_usd = temp.raised_amount_usd.apply(lambda x: '{:.2f}'.format(x))
temp.sort_values('raised_amount_usd', ascending = False)


# # Checkpoint 3: Country Analysis

# In[313]:


temp = master_frame[master_frame.funding_round_type == 'venture']
temp.head()


# In[314]:


temp.country_code.unique()


# In[315]:


top9 = temp.groupby('country_code').raised_amount_usd.sum().reset_index()
top9 = top9.sort_values('raised_amount_usd', ascending = False).reset_index(drop = True).iloc[:9,:]
top9.raised_amount_usd = top9.raised_amount_usd.apply(lambda x: '{:.2f}'.format(x))
top9


# # Checkpoint 4: Sector Analysis 1

# In[316]:


mapping_df = pd.read_csv('mapping.csv')
mapping_df['main_sector'] = mapping_df.iloc[:, 1:].idxmax(axis=1)
mapping_df.head()


# In[317]:


master_frame['primary_sector'] = master_frame.category_list.str.split('|').str[0]


# In[318]:


master_frame = pd.merge(master_frame, mapping_df[['category_list', 'main_sector']], left_on = 'primary_sector',right_on = 'category_list', how = 'left')
master_frame.head()


# In[319]:


d1 = master_frame[(master_frame.funding_round_type == 'venture') & (master_frame.country_code == 'USA')]
d2 = master_frame[(master_frame.funding_round_type == 'venture') & (master_frame.country_code == 'GBR')]
d3 = master_frame[(master_frame.funding_round_type == 'venture') & (master_frame.country_code == 'IND')]


# In[320]:


d1.head()


# In[321]:


def place_value(number): 
    return ("{:,}".format(number).split('.')[0])


# In[322]:


# Total Number of Investments Count
print('Total number of Investments (count) for D1 is : {0}'.format(place_value(d1.raised_amount_usd.dropna().count())))
print('Total number of Investments (count) for D2 is : {0}'.format(place_value(d2.raised_amount_usd.dropna().count())))
print('Total number of Investments (count) for D3 is : {0}'.format(place_value(d3.raised_amount_usd.dropna().count())))


# In[323]:


# Total amount of investment (USD) 
print('Total amount of investment (USD) for D1 is : {0}'.format(place_value(d1.raised_amount_usd.dropna().sum())))
print('Total amount of investment (USD) for D2 is : {0}'.format(place_value(d2.raised_amount_usd.dropna().sum())))
print('Total amount of investment (USD) for D3 is : {0}'.format(place_value(d3.raised_amount_usd.dropna().sum())))


# In[324]:


# Top Sector name (no. of investment-wise)
print('Top Sector name (no. of investment-wise) for D1 is : {0}'.format(d1['main_sector'].value_counts().reset_index().iloc[0,0]))
print('Top Sector name (no. of investment-wise) for D2 is : {0}'.format(d2['main_sector'].value_counts().reset_index().iloc[0,0]))
print('Top Sector name (no. of investment-wise) for D3 is : {0}'.format(d3['main_sector'].value_counts().reset_index().iloc[0,0]))


# In[325]:


# Second Sector name (no. of investment-wise)
print('Second Sector name (no. of investment-wise) for D1 is : {0}'.format(d1['main_sector'].value_counts().reset_index().iloc[1,0]))
print('Second Sector name (no. of investment-wise) for D2 is : {0}'.format(d2['main_sector'].value_counts().reset_index().iloc[1,0]))
print('Second Sector name (no. of investment-wise) for D3 is : {0}'.format(d3['main_sector'].value_counts().reset_index().iloc[1,0]))


# In[326]:


# Third Sector name (no. of investment-wise)
print('Third Sector name (no. of investment-wise) for D1 is : {0}'.format(d1['main_sector'].value_counts().reset_index().iloc[2,0]))
print('Third Sector name (no. of investment-wise) for D2 is : {0}'.format(d2['main_sector'].value_counts().reset_index().iloc[2,0]))
print('Third Sector name (no. of investment-wise) for D3 is : {0}'.format(d3['main_sector'].value_counts().reset_index().iloc[2,0]))


# In[327]:


# Number of investments in top sector (3)
print('Number of investments in top sector for D1 is : {0}'.format(d1[d1.main_sector == d1['main_sector'].value_counts().reset_index().iloc[0,0]].raised_amount_usd.dropna().count()))
print('Number of investments in top sector for D2 is : {0}'.format(d2[d2.main_sector == d2['main_sector'].value_counts().reset_index().iloc[0,0]].raised_amount_usd.dropna().count()))
print('Number of investments in top sector for D3 is : {0}'.format(d3[d3.main_sector == d3['main_sector'].value_counts().reset_index().iloc[0,0]].raised_amount_usd.dropna().count()))


# In[328]:


# Number of investments in second sector (4)
print('Number of investments in second sector (4) for D1 is : {0}'.format(d1[d1.main_sector == d1['main_sector'].value_counts().reset_index().iloc[1,0]].raised_amount_usd.dropna().count()))
print('Number of investments in second sector (4) for D2 is : {0}'.format(d2[d2.main_sector == d2['main_sector'].value_counts().reset_index().iloc[1,0]].raised_amount_usd.dropna().count()))
print('Number of investments in second sector (4) for D3 is : {0}'.format(d3[d3.main_sector == d3['main_sector'].value_counts().reset_index().iloc[1,0]].raised_amount_usd.dropna().count()))


# In[329]:


# Number of investments in third sector (5)
print('Number of investments in third sector (5) for D1 is : {0}'.format(d1[d1.main_sector == d1['main_sector'].value_counts().reset_index().iloc[2,0]].raised_amount_usd.dropna().count()))
print('Number of investments in third sector (5) for D2 is : {0}'.format(d2[d2.main_sector == d2['main_sector'].value_counts().reset_index().iloc[2,0]].raised_amount_usd.dropna().count()))
print('Number of investments in third sector (5) for D3 is : {0}'.format(d3[d3.main_sector == d3['main_sector'].value_counts().reset_index().iloc[2,0]].raised_amount_usd.dropna().count()))


# In[330]:


# For point 3 (top sector count-wise), which company received the highest investment?
print('For point 3 (top sector count-wise), which company received the highest investment? for D1 is : {0}'.format(d1[d1.main_sector == d1['main_sector'].value_counts().reset_index().iloc[0,0]].groupby('name').raised_amount_usd.sum().reset_index().sort_values('raised_amount_usd', ascending = False).iloc[0,0]))
print('For point 3 (top sector count-wise), which company received the highest investment? for D2 is : {0}'.format(d2[d2.main_sector == d2['main_sector'].value_counts().reset_index().iloc[0,0]].groupby('name').raised_amount_usd.sum().reset_index().sort_values('raised_amount_usd', ascending = False).iloc[0,0]))
print('For point 3 (top sector count-wise), which company received the highest investment? for D3 is : {0}'.format(d3[d3.main_sector == d3['main_sector'].value_counts().reset_index().iloc[0,0]].groupby('name').raised_amount_usd.sum().reset_index().sort_values('raised_amount_usd', ascending = False).iloc[0,0]))


# In[331]:


# For point 4 (second best sector count-wise), which company received the highest investment?
print('For point 3 (top sector count-wise), which company received the highest investment? for D1 is : {0}'.format(d1[d1.main_sector == d1['main_sector'].value_counts().reset_index().iloc[1,0]].groupby('name').raised_amount_usd.sum().reset_index().sort_values('raised_amount_usd', ascending = False).iloc[0,0]))
print('For point 3 (top sector count-wise), which company received the highest investment? for D2 is : {0}'.format(d2[d2.main_sector == d2['main_sector'].value_counts().reset_index().iloc[1,0]].groupby('name').raised_amount_usd.sum().reset_index().sort_values('raised_amount_usd', ascending = False).iloc[0,0]))
print('For point 3 (top sector count-wise), which company received the highest investment? for D3 is : {0}'.format(d3[d3.main_sector == d3['main_sector'].value_counts().reset_index().iloc[1,0]].groupby('name').raised_amount_usd.sum().reset_index().sort_values('raised_amount_usd', ascending = False).iloc[0,0]))


# # Checkpoint 6: Plots

# ## Plot 1

# In[332]:


temp = master_frame[(master_frame.funding_round_type.isin(['venture', 'seed', 'angel', 'private_equity']))]
temp = temp.groupby('funding_round_type').agg({'raised_amount_usd' : ['sum', 'mean']}).reset_index()
temp.columns = temp.columns.droplevel()
temp.columns = ['Funding_Type', 'Sum_of_Investments', 'Average_of_Investments']

temp


# In[333]:


# Thanks to the Source 
# Code Imported from Link : https://dfrieds.com/data-visualizations/how-format-large-tick-values

sns.set(font_scale=1.4)

def reformat_large_tick_values(tick_val, pos):
    """
    Turns large tick values (in the billions, millions and thousands) such as 4500 into 4.5K and also appropriately turns 4000 into 4K (no zero after the decimal).
    """
    if tick_val >= 1000000000:
        val = round(tick_val/1000000000, 1)
        new_tick_format = '{:}B'.format(val)
    elif tick_val >= 1000000:
        val = round(tick_val/1000000, 1)
        new_tick_format = '{:}M'.format(val)
    elif tick_val >= 1000:
        val = round(tick_val/1000, 1)
        new_tick_format = '{:}K'.format(val)
    elif tick_val < 1000:
        new_tick_format = round(tick_val, 1)
    else:
        new_tick_format = tick_val

    # make new_tick_format into a string value
    new_tick_format = str(new_tick_format)

    # code below will keep 4.5M as is but change values such as 4.0M to 4M since that zero after the decimal isn't needed
    index_of_decimal = new_tick_format.find(".")

    if index_of_decimal != -1:
        value_after_decimal = new_tick_format[index_of_decimal+1]
        if value_after_decimal == "0":
            # remove the 0 after the decimal point since it's not needed
            new_tick_format = new_tick_format[0:index_of_decimal] + new_tick_format[index_of_decimal+2:]

    return new_tick_format


# In[334]:


sns.catplot(x="Funding_Type", y="Sum_of_Investments", data=temp, height=6, kind="bar", palette="muted")
ax = plt.gca()
ax.yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))


# In[335]:


sns.catplot(x="Funding_Type", y="Average_of_Investments", data=temp, height=6, kind="bar", palette="muted")
ax = plt.gca()
ax.yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))


# ## Plot 2

# In[336]:


temp = master_frame[master_frame.funding_round_type == 'venture']
top9 = temp.groupby('country_code').raised_amount_usd.sum().reset_index()
top9 = top9.sort_values('raised_amount_usd', ascending = False).reset_index(drop = True).iloc[:9,:]
top9


# In[337]:


sns.catplot(x="country_code", y="raised_amount_usd", data=top9, height=6, kind="bar", palette="muted")
ax = plt.gca()
ax.yaxis.set_major_formatter(tick.FuncFormatter(reformat_large_tick_values))


# ## Plot 3

# In[338]:


temp = master_frame[(master_frame.funding_round_type == 'venture') & (master_frame.country_code.isin(['USA','GBR','IND'])) & (master_frame.main_sector.isin(['Others','Cleantech / Semiconductors','Social, Finance, Analytics, Advertising']))]
temp = temp[['country_code', 'main_sector', 'raised_amount_usd']].dropna()
temp = temp.groupby(['country_code', 'main_sector']).raised_amount_usd.count().reset_index()


# In[339]:


temp


# In[340]:


# Draw a nested barplot to show survival for class and sex
g = sns.catplot(x="main_sector", y="raised_amount_usd", hue="country_code", data=temp,
                height=6, kind="bar", palette="muted")
g.despine(left=True)
g.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
g.set_ylabels("Number of Investments")

