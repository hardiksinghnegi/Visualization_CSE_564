import json

from flask import Flask, render_template, request, redirect, Response, jsonify
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd


app = Flask(__name__)

def prepare_data(file):
    '''
        Prepare dataset in form of pandas dataframe and scale using the Standard Scaler
    '''
    df = pd.read_csv(file)
    sample_features = ["Overall", "Finishing", "Crossing", "Vision", "Composure", "ShortPassing", "LongPassing", 
                     "Aggression", "Interceptions", "Penalties"]
    scaler = StandardScaler()
    df[sample_features] = scaler.fit_transform(df[sample_features])
    return df[sample_features]


@app.route("/", methods = ['POST', 'GET'])
def index():
    '''
        Main Index page
    '''
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
