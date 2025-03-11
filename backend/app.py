import features_extraction
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import sys

# Import the feature extraction module
sys.path.append("F:\\Sanchalak")

app = Flask(__name__)
CORS(app)


def train_rf():
    df = pd.read_csv('train/data/uci-ml-phishing-dataset.csv')

    # Drop less useful columns
    df = df.drop(columns=['SSLfinal_State', 'port',
                 'popUpWidnow', 'Page_Rank', 'Links_pointing_to_page'])

    y = df['Result']
    X = df.drop('Result', axis=1)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=12)

    # Handle class imbalance using SMOTE
    smote = SMOTE(random_state=42)
    X_train, y_train = smote.fit_resample(X_train, y_train)

    # Train RandomForestClassifier
    clf = RandomForestClassifier(max_depth=20, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate model
    y_pred_rf = clf.predict(X_test)
    score = metrics.accuracy_score(y_test, y_pred_rf)
    print(f"Model trained. Accuracy: {score:.3f}")

    return clf


# Train model when server starts
clf = train_rf()


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        test_url = data.get("url")

        if not test_url:
            return jsonify({"error": "No URL provided"}), 400

        # Extract features for the given URL
        features_test = features_extraction.main(test_url)
        features_test = np.array(features_test).reshape((1, -1))

        # Predict using the pre-trained model
        pred = clf.predict(features_test)

        # Send response to extension
        result = "SAFE" if pred[0] == 1 else "PHISHING"
        return jsonify({"url": test_url, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
