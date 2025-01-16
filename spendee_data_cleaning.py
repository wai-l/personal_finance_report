import pandas as pd
from os import listdir
from os.path import isfile, join

# put the path of all files into a list
path = 'data/spendee/'
files = [f for f in listdir(path) if isfile(join(path, f))]

# create an empty data frame
df = pd.DataFrame(
    {'Date': [], 
     'Wallet': [], 
     'Type': [], 
     'Category name': [], 
     'Amount': [], 
     'Currency': [], 
     'Note': [], 
     'Labels': [], 
     'Author': []
})

# concat all data into the empty dataframe
for file in files: 
    file_path = f'{path}{file}'
    file_data = pd.read_csv(file_path)
    df = pd.concat([df, file_data], ignore_index=True)

# change some amended category
df['Category name'] = df['Category name'].replace(
    {'Alcohol and cigarettes': 'Tobaco', 
     'Food & Drink': 'Groceries'}
)

df = df.drop_duplicates()

df['Date'] = pd.to_datetime(df['Date'])

df = df.rename(columns={'Category name': 'Category'})

df=df[['Date', 'Type', 'Category', 'Amount', 'Note', 'Labels']]

df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['YearMonth'] = df['Date'].dt.strftime('%Y-%m')

# data cleaning
## replace \n
df['Note'] = df['Note'].replace(
    {'Giffgaff\n': 'Giffgaff'}
)

## every Giffgaff should be monthly transactions
df.loc[df['Note']=='Giffgaff', 'Labels'] = 'monthly'

## rebate should be time to time
df.loc[df['Note'].str.contains('rebate', na=False), 'Labels'] = 'time to time'

## if category is eating out, label = monthly
df.loc[(df['Category']=='Eating out/take away') & (df['Labels'].isnull()), 'Labels'] = 'monthly'

df.to_csv('data/cleaned/spendee.csv', index=False)
