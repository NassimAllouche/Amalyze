import pandas as pd
import os
from transformers import pipeline
import torch
reviews =  pd.read_excel('C:/Users/nassim/Desktop/pi/material-dashboard-django/apps/sentimentanalysis/C.xlsx' )
pipe = pipeline('sentiment-analysis', model='arpanghoshal/EkmanClassifier') 
def ekman_classifier(text):
    emotion = pipe(text)[0]['label']
    return(emotion)
