from flask import Flask, request, jsonify
from flask_cors import CORS
import flask_cors
# import json
import pymongo


app = Flask(__name__)
CORS(app)

cors_ip = '*'


# MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"
database_name = "graph_data"
collection_name_nodes = "nodes"
collection_name_links = "links"

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
nodes_collection = db[collection_name_nodes]
links_collection = db[collection_name_links]


# class CustomJSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return super().default(o)


# app.json_encoder = CustomJSONEncoder


# @app.route('/add_node', methods=['POST'])
# def add_node():
#     data = request.json
#     id = data['id']
#     group = data['group']
#     label = data['label']
#     level = data['level']
#     # print(node, 'result')

#     new_data = {
#         'id': id,
#         'group': group,
#         'label': label,
#         'level': level
#     }
#     print(new_data)

#     nodes_collection.insert_one(new_data)
#     return jsonify({"message": "Node added successfully", "new_data": new_data}), 200


@app.route('/add_node', methods=['POST'])
@flask_cors.cross_origin(origin=cors_ip, support_credentials=True)
def add_node():
    data = request.json
    print(data, "data")
    id = data['id']
    group = data['group']
    label = data['label']
    level = data['level']

    new_node = {
        'id': id,
        'group': group,
        'label': label,
        'level': level
    }
    # print(new_node)
    nodes_collection.insert_one(new_node)

    new_node['_id'] = str(new_node['_id'])
    node = [new_node]
    print(node, 'new node')
    return jsonify({"message": "Node added successfully", "new_data": node}), 200


@app.route('/add_link', methods=['POST'])
@flask_cors.cross_origin(origin=cors_ip, support_credentials=True)
def add_link():
    data = request.json
    target = data['target']
    source = data['source']
    strength = data['strength']

    new_link = {
        "target": target,
        "source": source,
        "strength": strength
    }

    links_collection.insert_one(new_link)

    new_link['_id'] = str(new_link['_id'])
    link = [new_link]
    return jsonify({"message": "Link added successfully", 'new_data': link}), 200


@app.route('/get_nodes', methods=['GET'])
@flask_cors.cross_origin(origin=cors_ip, support_credentials=True)
def get_nodes():
    nodes = list(nodes_collection.find([], {'_id': 0}))
    return jsonify({"nodes": nodes}), 200


@app.route('/get_links', methods=['GET'])
@flask_cors.cross_origin(origin=cors_ip, support_credentials=True)
def get_links():
    links = list(links_collection.find({}, {'_id': 0}))
    return jsonify({"links": links}), 200


if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')
