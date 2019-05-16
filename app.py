import configparser
import json
from data_utils import prepare_data, get_incidents_per_year, render_state_csv_by_year, get_incidents_per_state, get_index_stats
from flask import Flask, render_template, request, redirect, Response, jsonify


app = Flask(__name__)


@app.route("/home", methods=['POST', 'GET'])
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


@app.route("/maps", methods=['POST', 'GET'])
def data_maps():
    """
        Regional Content / Maps page
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    shooting_dataset = config['DATA']['INPUT_CSV_1']
    df = prepare_data(shooting_dataset)
    data = get_incidents_per_state(df)
    data = {'init_data': data}
    return render_template('maps.html', data=data)


@app.route("/getStateDataByYear", methods=['POST', 'GET'])
def data_maps_by_year():
    """
        Regional Content / Maps page
    """

    if request.method == 'POST':
        data = request.get_json()
        start = int(data['s'])
        end = int(data['e'])
        config = configparser.ConfigParser()
        config.read('config.ini')
        shooting_dataset = config['DATA']['INPUT_CSV_1']
        df = prepare_data(shooting_dataset)
        result = render_state_csv_by_year(df, start, end)
        status_dict = {'status' : '1',
                       'data'   :  result}
        return json.dumps(status_dict)


@app.route("/rmix", methods=['POST', 'GET'])
def racial_mix():
    return render_template('racial_mix.html')


@app.route("/indexStat", methods=['POST', 'GET'])
def index_statistics():

    if request.method == 'POST':
        data = request.get_json()
        start = int(data['s'])
        end = int(data['e'])
        config = configparser.ConfigParser()
        config.read('config.ini')
        shooting_dataset = config['DATA']['INPUT_CSV_1']
        df = prepare_data(shooting_dataset)
        result = get_index_stats(df, start, end)
        return json.dumps(result)


if __name__ == "__main__":
    app.run(debug=True)
