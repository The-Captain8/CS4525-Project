import pandas
from BPlusTree import *

data = pandas.read_csv('./CAD_USD Historical Data.csv')
tree = BPlusTree(3)


for row in data.iterrows():
    date = row[1]['Date']
    price = row[1]['Price']
    tree.insert(str(price), str(date))

pass