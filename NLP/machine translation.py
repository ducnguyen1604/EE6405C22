import pandas as pd
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect
import os
print(os.listdir(rREMOVED_SECRETC:\Users\65988\Desktop\EE6405C22\notebook\datasetREMOVED_SECRET))
amazon_df = pd.read_csv(rREMOVED_SECRETC:/Users/65988/Desktop/EE6405C22/notebook/dataset/Amazon_en_to_es.csvREMOVED_SECRET)
shopee_df = pd.read_csv(rREMOVED_SECRETC:/Users/65988/Desktop/EE6405C22/notebook/dataset/Shopee_CN_to_EN.csvREMOVED_SECRET)
italian_df = pd.read_csv(rREMOVED_SECRETC:/Users/65988/Desktop/EE6405C22/notebook/dataset/target_en_to_it.csvREMOVED_SECRET)
print(shopee_df.columns)
print(amazon_df.columns)
print(italian_df.columns)