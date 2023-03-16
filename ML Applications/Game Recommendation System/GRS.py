#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import tensorflow as tf
import random
from collections import Counter
from sklearn.metrics import roc_curve, auc, average_precision_score
import seaborn as sns
import matplotlib. pyplot as plt


# In[2]:


#load the data set
path = 'steam-200k.csv'

#create dataFrame
df = pd.read_csv(path, header = None,
                 names = ['UserID', 'Game', 'Action', 'Hours', 'No used'])
df.head()


# In[3]:


df['Played Time'] = df['Hours'].astype('float32')

df.loc[(df['Action'] == 'purchase') & (df['Hours'] == 1.0), 'Played Time'] = 0

df.UserID = df.UserID.astype('int')
df = df.sort_values(['UserID', 'Game', 'Played Time'])

#drop the no used column
clean_df = df.drop_duplicates(['UserID', 'Game'], keep = 'last').drop(['Action', 'Hours', 'No used'], axis = 1)

clean_df.head()


# In[4]:


purchase_ratings = df[df.Action == "purchase"].groupby(["UserID","Game"])["Hours"].count()
purchase_ratings.describe()


# In[5]:


purchase_ratings[purchase_ratings > 1][:5] #user who bought the same game two times


# In[6]:


purchase_ratings[purchase_ratings > 1].shape


# In[7]:


#make the purchase of game as rating of 1
purchase_ratings[purchase_ratings > 1] = 1


# In[8]:


games_played = df[df.Action == "play"].groupby(["UserID","Game"])["Hours"].sum()
games_played_per_user = df[df.Action =="play"].groupby(["UserID"])["Game"].nunique()

average_games_played = games_played_per_user.mean()
weighted_games_played = games_played * (average_games_played / games_played_per_user)

print (games_played_per_user.describe())
print ()
print (games_played_per_user[games_played_per_user == 498][:])
print ()
print (games_played_per_user[games_played_per_user == 1][:5])
print ()
print (games_played_per_user[games_played_per_user > average_games_played][:1])


# In[9]:


#function to define the ratings
def to_explicit_ratings(series):
    games = series.index.levels[1].tolist()
    hours_ratings = series.copy()
    for game_played in games:
        sliced_data = hours_ratings.xs(game_played, level=1)
        descr = sliced_data.describe()
        a = sliced_data[sliced_data >= descr["75%"]].index.tolist()
        hours_ratings.loc[(a, game_played)] = 5
        b = sliced_data[(sliced_data >= descr["50%"]) & (sliced_data < descr["75%"])].index.tolist()
        hours_ratings.loc[(b, game_played)] = 4
        c = sliced_data[(sliced_data >= descr["25%"]) & (sliced_data < descr["50%"])].index.tolist()
        hours_ratings.loc[(c, game_played)] = 3
        d = sliced_data[sliced_data < descr["25%"]].index.tolist()
        hours_ratings.loc[(d, game_played)] = 2
    
    return hours_ratings


# In[10]:


hours_ratings = to_explicit_ratings(weighted_games_played)


# In[11]:


mean_weighted_ratings = purchase_ratings.combine(hours_ratings, max)
print (mean_weighted_ratings.shape)
print (mean_weighted_ratings.describe())

sns.displot(mean_weighted_ratings, kde=False)
plt.show()


# In[12]:


#display change before apply weight and after apply weight
def display_before_and_after(user_id, before, after):
    print ("====Before====")
    games_played = min(len(non_weighted_ratings.loc[user_id]), 10)
    idx = before.xs(user_id, level=0).sample(games_played).index.tolist()
    print (before.xs(user_id, level=0)[idx])
    print ("====After====")
    print (after.xs(user_id, level=0)[idx])


# In[13]:


non_weighted_ratings = to_explicit_ratings(games_played)
non_weighted_ratings = purchase_ratings.combine(non_weighted_ratings, max)
display_before_and_after(62990992, non_weighted_ratings, mean_weighted_ratings)


# In[14]:


display_before_and_after(309167186, non_weighted_ratings, mean_weighted_ratings)


# In[15]:


# cleanup
purchase_ratings = None
hours_ratings = None


# In[16]:


ratings = mean_weighted_ratings.reset_index()
ratings.rename(columns={0:"Rating"}, inplace=True)


# In[17]:


ratings[ratings.UserID == 309167186]


# In[18]:


df2 = ratings
df2.head()


# In[19]:


combine_game_rating = df2.dropna(axis = 0, subset = ['Game'])
game_ratingCount = (combine_game_rating.groupby(by = ['Game'])['Rating'].count().reset_index().rename(columns = 
                            {'Rating': 'totalRatingCount'})
                               [['Game','totalRatingCount']])
game_ratingCount.head(10)


# In[20]:


rating_with_totalRatingCount = combine_game_rating.merge(game_ratingCount, left_on = 'Game', right_on = 'Game', how = 'left')
rating_with_totalRatingCount.head()


# In[21]:


pd.set_option('display.float_format', lambda x: '%.3f' % x)
print(game_ratingCount['totalRatingCount'].describe())


# In[22]:


popularity_threshold = 50
rating_popular_game= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
rating_popular_game.head(10)


# In[23]:


rating_popular_game.shape


# In[24]:


## First lets create a Pivot matrix

game_features_df=rating_popular_game.pivot_table(index='Game',columns='UserID',values='Rating').fillna(0)
game_features_df.head()


# In[25]:


from scipy.sparse import csr_matrix

game_features_df_matrix = csr_matrix(game_features_df.values)

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(game_features_df_matrix)


# In[26]:


list(game_features_df.index)
#print(game_features_df[game_features_df.index == '7 Days to Die'])


# In[27]:


query_index = 0
find = "Star Wars - Battlefront II"
print(query_index)
#distances, indices = model_knn.kneighbors(game_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)
distances, indices = model_knn.kneighbors(game_features_df[game_features_df.index == find].values.reshape(1, -1), n_neighbors=6)


# In[28]:


game_features_df.head()


# In[29]:


for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recommendations for {0}:\n'.format(find))
    else:
        print('{0}: {1}, with distance of {2}:'.format(i, game_features_df.index[indices.flatten()[i]], distances.flatten()[i]))


# In[ ]:




