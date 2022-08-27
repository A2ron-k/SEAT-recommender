# Step 1. Create Virtual Environment => * python -m venv env
# Step 2. Activate Virtual Environment => * source env/bin/activate (For Mac) | * .\env\Scripts\activate (For Windows)
# Step 3. pip install -r requirements.txt
# Step 4. Tensorflow might not run on local
# 
# To push changes
# Step 1. pip freeze > requirements.txt (If added any dependancies)
# Step 2. Git add and commit to repo
# Step 3. Git heroku push main

from flask import Flask,jsonify,request
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/")
@cross_origin(origin='*')
def hello():
    return "The Recommender system is working!"

@app.route("/api/recommender",methods=["POST"])
@cross_origin(origin='*')
def api_recommend():
    import tensorflow as tf
    import numpy as np
    import json

    # Extract JSON Data from POST Request
    json_data = request.json

    input_userID = json_data['userid']
    input_indoorOutdoorScore = json_data['input_indoorOutdoorScore']
    input_leisureThrillScore = json_data['input_leisureThrillScore']
    input_cheapExpensiveScore = json_data['input_cheapExpensiveScore']

    INPUT = {
            "userid": np.array([input_userID]), 
            "indoorOutdoorScore": np.array([np.int32(input_indoorOutdoorScore)]),
            "leisureThrillScore": np.array([np.int32(input_leisureThrillScore)]),
            "cheapExpensiveScore": np.array([np.int32(input_cheapExpensiveScore)])
        }

    # Set Tensorflow Model Directory
    MODEL_PATH = "./model/"

    # Load & Compile Tensorflow Model
    loaded_model = tf.saved_model.load(MODEL_PATH)
    print("AARON -> Model Loaded - Success")

    # Parse userID value into TensorFlow BruteForce Layer to predict
    # Expected results into scores and titles (tf.tensor type)
    scores, attractionID = loaded_model(INPUT)
    print("AARON -> Model Predicted - Success")

    # Convert Tf.tensor to NdArray
    attractionID_tensor = attractionID[0][:5]
    attractionID_ndArr = attractionID_tensor.numpy()
    print("AARON -> Convert to nd_Array - Success")
    
    # Convert NdArray to list
    attractionID_list = attractionID_ndArr.tolist()
    print("AARON -> Convert to list - Success")

    # Decodes List to serialised list 
    # to be parse out to API Requester
    decoded_attractionID_list = []
    for value in attractionID_list:
        decoded_value = value.decode('utf-8')
        decoded_attractionID_list.append(decoded_value)

    # Processing of list to JSON format
    final_result = {
                    'attractions': decoded_attractionID_list
                    }
    print("AARON -> Data Preparation - Success")

    return jsonify(final_result)