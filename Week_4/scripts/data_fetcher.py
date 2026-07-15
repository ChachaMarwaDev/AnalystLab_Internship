# %%
import kagglehub as ka
import pandas as pd
import numpy as np

link = "https://www.kaggle.com/datasets/vivek468/superstore-dataset-final"
path = ka.dataset_download("vivek468/superstore-dataset-final", output_dir="../data")

# %%
df = pd.read_csv()