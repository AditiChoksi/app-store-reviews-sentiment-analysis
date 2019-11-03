import nltk
import pandas as pd
#import sentiment_mod
import numpy as np
df = pd.read_csv('merged_file.csv')

df = df['Review'].replace('',np.nan,inplace=True)

df = df.dropna(subset=['Tenant'], inplace=True)

df.to_csv()
