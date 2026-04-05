import pandas as pd
import os
from decimal import Decimal
from datetime import datetime




folder = "data"

all_data= []

for file in os.listdir(folder):
    if file.endswith(".csv"):
        path = os.path.join(folder, file)
        df = pd.read_csv(path)
        
        df["source_file"] = file

        all_data.append(df)

df = pd.concat(all_data, ignore_index=True)

#Normalize
df.columns = df.columns.str.lower()
df['date'] = pd.to_datetime(df['date'], errors = 'coerce')

#load  rules
rules = pd.read_csv('rules.csv')

def categorize(desc):
    desc = str(desc).upper()
    for _, row in rules.iterrows():
        if row['keyword'] in desc:
            return row['category']
    return 'OTHER'

df['category'] = df['description'].apply(categorize)

#Summary
summary = df.groupby('category')['amount'].sum().reset_index()

#output
os.makedirs('output', exist_ok = True)

df.to_excel('output/transactions.xlsx', index = False)
summary.to_excel('output/summary.xlsx', index = False)

print('Pipeline completed successfully')


