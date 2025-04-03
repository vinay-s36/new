from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import os
from src.pipeline.predict_pipeline import PredictPipeline
import re

app = Flask(__name__)

# get the path to the models folder
model_path = "./models"

# load the model
with open(os.path.join(model_path, 'dt1.pkl'), 'rb') as f:
    model = pickle.load(f)

# print(model)
pred = PredictPipeline()

# Enable CORS with all origins
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def clean_url(url):
    return re.sub(r'^https?:\/\/|\/$', '', url)


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():

    url = request.json['url']
    cleaned_url = clean_url(url)

    transform_url = pred.transformURL(cleaned_url)

    transform_url = transform_url.reshape(1, -1)

    print("transform_url", transform_url)

    prediction = model.predict(transform_url)

    if (prediction == 0):
        res = 'benign'
    elif (prediction == 1):
        res = 'defacement'
    elif (prediction == 2):
        res = 'phishing'
    else:
        res = 'malware'
    print(res)
    response = jsonify({'prediction': res})

    return response


if __name__ == '__main__':
    app.run(port=8000)
