# %%
import kagglehub as ka
import pandas as pd

data_link = "https://www.kaggle.com/datasets/blastchar/telco-customer-churn"
dataset = "blastchar/telco-customer-churn"
path = ka.dataset_download(dataset, output_dir="../data")

# %%
df = pd.read_csv("../data/Sample_Superstore.csv", encoding='cp1252')
print(df.head(2))
