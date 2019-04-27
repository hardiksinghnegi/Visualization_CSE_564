import configparser
import json
from data_utils import prepare_data, get_incidents_per_year
from flask import Flask, render_template, request, redirect, Response, jsonify


app = Flask(__name__)


@app.route("/home", methods = ['POST', 'GET'])
def index():
    """
        Main Index page
    """

    config = configparser.ConfigParser()
    config.read('config.ini')
    shooting_dataset = config['DATA']['INPUT_CSV_1']
    df = prepare_data(shooting_dataset)
    year_dict = get_incidents_per_year(df)
    year_json = json.dumps(year_dict)
    data = {'incident_data': year_json}
    return render_template('index.html', data=data)


@app.route("/maps", methods = ['POST', 'GET'])
def data_maps():
    """
        Regional Content / Maps page
    """
    return render_template('maps.html')


if __name__ == "__main__":
    app.run(debug=True)
