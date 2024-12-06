import json

import BPlusTree
from flask import Flask, request, jsonify

app = Flask(__name__)
trees: list[BPlusTree] = []


@app.route('/init', methods=['POST'])
def init():
    trees.append(BPlusTree.BPlusTree(3))
    return jsonify({'id': f'{len(trees) - 1}'})


@app.route('/search_range', methods=['GET'])
def search_range():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'no id'})

    key = request.args.get('key')
    if not key:
        return jsonify({'error': 'no key'})

    key_range = request.args.get('range')

    try:
        tree = trees[int(id)]
    except IndexError:
        return jsonify({'error': 'invalid id'})

    if key_range:
        result = tree.get_key_range(key, key_range)
    else:
        result = tree.search(key)

    return jsonify({'result': result})


@app.route('/search', methods=['GET'])
def search():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'no id'})

    key = request.args.get('key')
    if not key:
        return jsonify({'error': 'no key'})

    try:
        tree = trees[int(id)]

        result = tree.search(key)
        if result:
            return jsonify({'result': [result.keys, result.values]})

        return jsonify({'error': 'invalid key'})
    except IndexError:
        return jsonify({'error': 'invalid id'})


@app.route('/insert', methods=['POST'])
def insert():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'no id'})

    key = request.args.get('key')
    if not key:
        return jsonify({'error': 'no key'})

    value = request.args.get('value')
    if not value:
        return jsonify({'error': 'no value'})

    try:
        tree = trees[int(id)]

        tree.insert(value, int(key))
        return jsonify({'result': True})
    except IndexError:
        return jsonify({'error': 'invalid id'})

@app.route('/sum', methods=['GET'])
def find_sum():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'no id'})

    key = request.args.get('key')

    key_range = request.args.get('range')

    try:
        tree = trees[int(id)]
    except IndexError:
        return jsonify({'error': 'invalid id'})

    if key_range and key:
        result = tree.sum(key, key_range)
    elif key:
        result = tree.sum(key)
    else:
        result = tree.sum()

    return jsonify({'result': result})

@app.route('/average', methods=['GET'])
def find_average():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'no id'})

    key = request.args.get('key')

    key_range = request.args.get('range')

    try:
        tree = trees[int(id)]
    except IndexError:
        return jsonify({'error': 'invalid id'})

    if key_range and key:
        result = tree.average(key, key_range)
    elif key:
        result = tree.average(key)
    else:
        result = tree.average()

    return jsonify({'result': result})

@app.route('/max', methods=['GET'])
def find_max():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'no id'})

    key = request.args.get('key')

    key_range = request.args.get('range')

    try:
        tree = trees[int(id)]
    except IndexError:
        return jsonify({'error': 'invalid id'})

    if key_range and key:
        result = tree.max(key, key_range)
    elif key:
        result = tree.max(key)
    else:
        result = tree.max()

    return jsonify({'result': result})

@app.route('/min', methods=['GET'])
def find_min():
    id = request.args.get('id')
    if not id:
        return jsonify({'error': 'no id'})

    key = request.args.get('key')

    key_range = request.args.get('range')

    try:
        tree = trees[int(id)]
    except IndexError:
        return jsonify({'error': 'invalid id'})

    if key_range and key:
        result = tree.max(key, key_range)
    elif key:
        result = tree.max(key)
    else:
        result = tree.max()

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run()
