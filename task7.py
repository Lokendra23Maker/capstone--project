

import pandas as pd

df = pd.read_csv("task4_join_result.csv")
print(df.head())
print(df.info())
print(df.isnull().sum())

print((df.isnull().sum() / len(df)) * 100)

df = df.fillna("unknown")
print(df.isnull().sum())

print("Rows before:", len(df))
df = df.drop_duplicates()
print("Rows after:", len(df))

df.to_csv("task7_cleaned_data.csv", index=False)
print("task7 completed")


numeric_cols =df.select_dtypes(include="number").columns
print("Numeric columns:", 
list (numeric_cols))

