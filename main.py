import os.path
import time

import pandas
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

def run_tests(index=False):
    time_data = []
    data = pandas.read_csv('./CAD_USD Historical Data.csv')
    tree = BPlusTree(3)

    build_datebase(index)
    con = sqlite3.connect('./db.sqlite3')
    cur = con.cursor()

    data = pandas.read_csv('./CAD_USD Historical Data.csv')

    # Insertion time
    results = ["Insertion"]

    start = time.perf_counter_ns()
    for row in data.iterrows():
        date = row[1]['Date']
        date =  datetime.strptime(date, '%m/%d/%Y').timestamp()
        price = row[1]['Price']
        tree.insert(price, date)

    end = time.perf_counter_ns()
    results.append(end - start)

    start = time.perf_counter_ns()
    for row in data.iterrows():
        date = row[1]['Date']
        date =  datetime.strptime(date, '%m/%d/%Y').timestamp()
        price = row[1]['Price']
        cur.execute("insert into data (timestamp, value) values(?, ?)", (date, price))

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

    return time_data

results = run_tests()
indexed_results = run_tests(index=True)

print('--- UN-INDEXED ---')
for test, btree_time, sqlite_time in results:
    print(f'\n {test}:')
    print(f'             B+ Tree: {btree_time}')
    print(f'              SQLite: {sqlite_time}')
    print(f' B+ Tree Performance: {(btree_time/sqlite_time) * 100 } % of SQLite')

print('--- INDEXED ---')
for test, btree_time, sqlite_time in indexed_results:
    print(f' {test}:')
    print(f'             B+ Tree: {btree_time}')
    print(f'              SQLite: {sqlite_time}')
    print(f' B+ Tree Performance: {(btree_time/sqlite_time) * 100 } % of SQLite')