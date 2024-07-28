import os
import pandas as pd
import matplotlib as plt
from path_info import DATA_DIR



df = pd.read_csv(os.path.join(DATA_DIR, 'prefecture_data_with_pairs_info.csv'))

df['male_ratio'] = df['Male_Subs'] / df['Male_Population']
df['femal_ratio'] = df['Female_subs'] / df['Female_Population']
df['total_ratio'] = df['Total_subs'] / df['Total_Population']

#print(df)

df.to_csv(os.path.join(DATA_DIR, 'prefecture_data_with_pairs_info_v2.csv'))

