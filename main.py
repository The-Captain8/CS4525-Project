import os.path
import random
import time

import pandas as pd
from BPlusTree import *
from datetime import datetime
import sqlite3


def build_datebase(index=False):
    db_file = './db.sqlite3'

    if os.path.exists(db_file):
        os.remove(db_file)

    con = sqlite3.connect(db_file)
    cur = con.cursor()

    cur.execute("create table if not exists data (timestamp int, value int)")

    if index:
        cur.execute("create index if not exists timestamp on data (timestamp)")

    cur.close()
    con.close()


# Create synthetic data for prior years
def repeat_dataframe(df, years):
    synthetic_dfs = []
    for year in range(1, years + 1):
        df_copy = df.copy()
        df_copy['Date'] = df_copy['Date'].apply(lambda x: (x - (31536000 * years) - random.randint(0, 10000)))
        dup = df_copy[df_copy.duplicated(['Date'], keep=False)]
        synthetic_dfs.append(df_copy)
    return pd.concat([] + synthetic_dfs).reset_index(drop=True)


def run_tests(data, index=False):
    time_data = []
    tree = BPlusTree(3)

    build_datebase(index)
    con = sqlite3.connect('./db.sqlite3')
    cur = con.cursor()

    # Insertion time
    results = ["Insertion"]

    start = time.perf_counter_ns()
    for row in data.iterrows():
        date = row[1]['Date']
        price = row[1]['Price']
        tree.insert(float(price), date)

    end = time.perf_counter_ns()
    results.append(end - start)

    start = time.perf_counter_ns()
    for row in data.iterrows():
        date = row[1]['Date']
        price = row[1]['Price']
        cur.execute("insert into data (timestamp, value) values(?, ?)", (date, price))

    end = time.perf_counter_ns()
    results.append(end - start)
    time_data.append(results)

    # Search time
    results = ["Search"]

    start = time.perf_counter_ns()
    for row in data.iterrows():
        price = row[1]['Price']
        tree.search(float(price))

    end = time.perf_counter_ns()
    results.append(end - start)

    start = time.perf_counter_ns()
    for row in data.iterrows():
        price = row[1]['Price']
        cur.execute(f"select value from data where value = {price}")

    end = time.perf_counter_ns()
    results.append(end - start)
    time_data.append(results)

    # Sum
    results = ["Sum"]

    start = time.perf_counter_ns()
    tree.sum()
    end = time.perf_counter_ns()
    results.append(end - start)

    start = time.perf_counter_ns()
    cur.execute("select sum(value) from data")
    end = time.perf_counter_ns()
    results.append(end - start)
    time_data.append(results)

    # Sum
    results = ["Average"]

    start = time.perf_counter_ns()
    tree.average()
    end = time.perf_counter_ns()
    results.append(end - start)

    start = time.perf_counter_ns()
    cur.execute("select avg(value) from data")
    end = time.perf_counter_ns()
    results.append(end - start)
    time_data.append(results)

    cur.close()
    con.close()
    os.remove('./db.sqlite3')

    return time_data


dataset = pd.read_csv('./CAD_USD Historical Data.csv')
dataset['Date'] = dataset["Date"].apply(lambda x: datetime.strptime(x, '%m/%d/%Y').timestamp())

results = run_tests(dataset)
indexed_results = run_tests(dataset, index=True)

print('SMALL DATASET')
print('--- UN-INDEXED ---')
for test, btree_time, sqlite_time in results:
    print(f'\n {test}:')
    print(f'             B+ Tree: {btree_time}')
    print(f'              SQLite: {sqlite_time}')
    print(f' B+ Tree Performance: {(btree_time / sqlite_time) * 100} % of SQLite')

print('--- INDEXED ---')
for test, btree_time, sqlite_time in indexed_results:
    print(f' {test}:')
    print(f'             B+ Tree: {btree_time}')
    print(f'              SQLite: {sqlite_time}')
    print(f' B+ Tree Performance: {(btree_time / sqlite_time) * 100} % of SQLite')

# Create a larger dataset and test again
print('MEDIUM DATASET')
dataset = repeat_dataframe(dataset.copy(), 20)
results = run_tests(dataset)
indexed_results = run_tests(dataset, index=True)

print('--- UN-INDEXED ---')
for test, btree_time, sqlite_time in results:
    print(f'\n {test}:')
    print(f'             B+ Tree: {btree_time}')
    print(f'              SQLite: {sqlite_time}')
    print(f' B+ Tree Performance: {(btree_time / sqlite_time) * 100} % of SQLite')

print('--- INDEXED ---')
for test, btree_time, sqlite_time in indexed_results:
    print(f' {test}:')
    print(f'             B+ Tree: {btree_time}')
    print(f'              SQLite: {sqlite_time}')
    print(f' B+ Tree Performance: {(btree_time / sqlite_time) * 100} % of SQLite')


# Create a large dataset and test again
# print('LARGE DATASET')
# dataset = repeat_dataframe(dataset.copy(), 2000)
# results = run_tests(dataset)
# indexed_results = run_tests(dataset, index=True)
#
# print('--- UN-INDEXED ---')
# for test, btree_time, sqlite_time in results:
#     print(f'\n {test}:')
#     print(f'             B+ Tree: {btree_time}')
#     print(f'              SQLite: {sqlite_time}')
#     print(f' B+ Tree Performance: {(btree_time / sqlite_time) * 100} % of SQLite')
#
# print('--- INDEXED ---')
# for test, btree_time, sqlite_time in indexed_results:
#     print(f' {test}:')
#     print(f'             B+ Tree: {btree_time}')
#     print(f'              SQLite: {sqlite_time}')
#     print(f' B+ Tree Performance: {(btree_time / sqlite_time) * 100} % of SQLite')