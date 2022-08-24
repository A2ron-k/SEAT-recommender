# Step 1. Create Virtual Environment => * python -m venv env
# Step 2. Activate Virtual Environment => * source env/bin/activate (For Mac) | * .\env\Scripts\activate (For Windows)
# Step 3. pip install -r requirements.txt
# Step 4. Tensorflow might not run on local
# 
# To push changes
# Step 1. pip freeze > requirements.txt (If added any dependancies)
# Step 2. Git add and commit to repo
# Step 3. Git heroku push main

from flask import Flask,jsonify


app = Flask(__name__)

@app.route("/")
def hello():
    return "The Recommender system is working!"

@app.route("/api/parseinfo",methods=["GET"])
def api_parse():

    test_dict = [
        {
            "color": "red",
            "value": "#f00"
        },
        {
            "color": "green",
            "value": "#0f0"
        },
        {
            "color": "blue",
            "value": "#00f"
        },
        {
            "color": "cyan",
            "value": "#0ff"
        }
    ]
    return jsonify(test_dict)

@app.route("/api/parseinfotest",methods=["GET"])
def api_parse_test():
    import tensorflow as tf
    import numpy as np
    import json

    # Encoder Class
    # Helps with np.ndarray/bytes to dict/list
    # The `default` method is called with the object that is to be serialized. 
    # The `default` method returns a serializable object.
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, bytes):
                return str(obj, encoding='utf-8');
            return json.JSONEncoder.default(self, obj)

    # Set Tensorflow Model Directory
    MODEL_PATH = "./tfmodel/"

    # Load & Compile Tensorflow Model
    loaded_model = tf.saved_model.load(MODEL_PATH)
    print("AARON -> Model Loaded - Success")

    # Parse userID value into TensorFlow BruteForce Layer to predict
    # Expected results into scores and titles (tf.tensor type)
    scores, titles = loaded_model(['42'])
    print("AARON -> Model Predicted - Success")
    print(titles[0][:3])

    # Convert Tf.tensor to NdArray
    titles_ndArr = titles.numpy()
    print(titles_ndArr)
    print("AARON -> Convert to nd_Array - Success")
    
    # Convert NdArray to byte/ list
    titles_bytesList = titles_ndArr.tolist()
    print("AARON -> Convert to bytesList - Success")

    # Encodes bytesList to serialised object to be parse out to API Requester
    encoded = json.dumps(titles_bytesList,cls=MyEncoder,indent=4)
    print("AARON -> Encoding - Success")

    return jsonify(encoded)