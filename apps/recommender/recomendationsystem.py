import matplotlib.pyplot as plt
import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import json
from sklearn.metrics.pairwise import linear_kernel

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
d= pd.read_csv('C:/Users/nassim/Desktop/pi/material-dashboard-django/apps/recommender/recommandation.csv' ,delimiter= ';')
data = d[['ProductId','Text','Product_Name','Product_Type']]
tfidf = TfidfVectorizer (stop_words='english')
data['Text'] = data['Text'].fillna("")
tfidf_matrix = tfidf.fit_transform(data['Text'])
import random

# Sample 10% of the data
# d_sample = d.iloc[:10000, :]
data_sample = d.drop_duplicates(subset='Product_Name', keep='first')

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data_sample['Text'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(data_sample.index, index=data_sample['Product_Name']).drop_duplicates()

def get_recommandation(title , cosine_sim = cosine_sim):
    idx = indices[title]
    sim_scores = enumerate(cosine_sim[idx].tolist()) # conversion en list
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores [1:11]
    
    sim_index = [i[0] for i in sim_scores]
    return (data_sample['Product_Name'].iloc[sim_index]).tolist()