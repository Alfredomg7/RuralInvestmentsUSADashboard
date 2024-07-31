import pandas as pd

df = pd.read_csv('data/rural-investments.csv')

# count unique values on each column and print the result
print(df.nunique())
