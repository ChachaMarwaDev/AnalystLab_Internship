# %%
import kagglehub as ka
import pandas as pd
import numpy as np

link = "https://www.kaggle.com/datasets/vivek468/superstore-dataset-final"
path = ka.dataset_download("vivek468/superstore-dataset-final", output_dir="../data")

# %%
df = pd.read_csv("../data/Sample_Superstore.csv", encoding='cp1252')
print(df.head(2))

# %%
"""
EXPLORATORY DATA ANALYSIS
Shape is (9994, 21)
Zero nulls in the table
"""
# print(df.shape)
# print(df.columns)
# print(df.isnull().sum())
# print(df.dtypes)

# print(df['Order Date'].dtype)
# print(df['Order Date'].head())

# print(df.info)

