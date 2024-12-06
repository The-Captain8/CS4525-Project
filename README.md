# CS4525-Project: B+ Tree Implementation

**Author: Nathan McGugan**

A Python implementation of a B+ Tree data structure with a Flask API interface and SQLite comparison benchmarks.

## Features

- B+ Tree implementation with the following operations:
  - Insert
  - Search
  - Range Search
  - Aggregation Functions (Sum, Average, Min, Max)
- API for B+ Tree operations
- Performance comparison with SQLite

## Dependencies
```bash
pip install flask pandas sqlite3
```

## Usage
The data structure can either be imported or created and accessed via an API server.
The tree assumes that timestamps will be sent as the key, so make sure to convert dates into timestamps.
### Running the API Server

1. Start the Flask server:
```bash
python api.py
```

This will start the server on `http://localhost:5000`

### API Endpoints

- **POST /init**
  - Initializes a new B+ Tree
  - Returns: `{"id": "<tree_id>"}`

- **POST /insert**
  - Parameters:
    - `id`: Tree ID
    - `key`: Key to insert
    - `value`: Value to insert
  - Returns: `{"result": true}` on success

- **GET /search**
  - Parameters:
    - `id`: Tree ID
    - `key`: Key to search
  - Returns: `{"result": [keys, values]}` or error message

- **GET /search_range**
  - Parameters:
    - `id`: Tree ID
    - `key`: Starting key
    - `range`: End of range (optional)
  - Returns: `{"result": [[key, value], ...]}` 

#### Aggregate Queries

These queries all take the same parameters and return the result. If no range is specified, the entire tree is included.

  - Parameters:
    - `id`: Tree ID
    - `key`: Starting key (optional)
    - `range`: End of range (optional)
  - Returns: `{"result": aggregate_result}`


  - End Points:
    - **GET /sum**
    - **GET /average**
    - **GET /max**
    - **GET /min**

### Performance Evaluations

To run a series of evaluations which test the speed of my B+ Tree and a SQLite database, run:

```bash
python main.py
```

This will output performance difference for indexed and unindexed SQLite database and my B+ Tree.

Note: Testing for large datasets has been commented out as it takes a couple of minutes.