import numpy as np
import pandas as pd
from os import path
from textblob import TextBlob
def opinionanalysis(pragraph):
    text = str(pragraph)
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        sentiment_label = "positive"
    elif sentiment_score < 0:
        sentiment_label = "negative"
    else:
        sentiment_label = "neutral"
    return(sentiment_label)