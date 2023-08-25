from flask import Flask, request, jsonify
# import json
import pymongo

app = Flask(__name__)

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
def add_node():
    data = request.json
    id = data['id']
    group = data['group']
    label = data['label']
    level = data['level']

    new_data = {
        'id': id,
        'group': group,
        'label': label,
        'level': level
    }

    nodes_collection.insert_one(new_data)

    new_data['_id'] = str(new_data['_id'])
    return jsonify({"message": "Node added successfully", "new_data": new_data}), 200


@app.route('/add_link', methods=['POST'])
def add_link():
    data = request.json
    target = data['target']
    source = data['source']
    strength = data['strength']

    new_data = {
        "target": target,
        "source": source,
        "strength": strength
    }

    new_data['_id'] = str(new_data['_id'])
    links_collection.insert_one(data)
    return jsonify({"message": "Link added successfully", 'new_data': new_data})


if __name__ == '__main__':
    app.run(debug=True)
