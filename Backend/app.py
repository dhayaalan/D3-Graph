from flask import Flask, request, jsonify
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

@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.json
    nodes_collection.insert_one(data)
    return jsonify({"message": "Node added successfully",'data': data})

@app.route('/add_link', methods=['POST'])
def add_link():
    data = request.json
    links_collection.insert_one(data)
    return jsonify({"message": "Link added successfully",'data':data})

if __name__ == '__main__':
    app.run(debug=True)
