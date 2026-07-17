# %%
import kagglehub as ka
import pandas as pd

data_link = "https://www.kaggle.com/datasets/blastchar/telco-customer-churn"
dataset = "blastchar/telco-customer-churn"
path = ka.dataset_download(dataset, output_dir="../data")

# %%
df = pd.read_csv("../data/Telco_Churn.csv", encoding='cp1252')
print(df.head(2))

# %%
# print(df.shape)
# print(df.columns)
# print(df.isnull().sum())
# print(df.dtypes)

# print(df['TotalCharges'].dtype)
# print(df['TotalCharges'].head())

# print(df.info)
# %%
