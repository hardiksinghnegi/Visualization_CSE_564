import configparser
import json
from data_utils import *
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
    #for key, value in year_dict.items():
    #    year_dict[key] = value.item()
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


@app.route("/getRaceDataByYear", methods=['POST', 'GET'])
def data_race_by_year():
    """
        Race Content / Racial Mix page
    """

    if request.method == 'POST':
        data = request.get_json()
        start = int(data['s'])
        end = int(data['e'])
        govt = data['govt']

        config = configparser.ConfigParser()
        config.read('config.ini')
        shooting_dataset = config['DATA']['INPUT_CSV_1']
        df = prepare_data(shooting_dataset)
        result = render_race_csv_by_year_govt(df, start, end, govt)

        status_dict = {'status' : '1',
                       'data'   :  result}
        return json.dumps(status_dict)


@app.route("/rmix", methods=['POST', 'GET'])
def racial_mix():
    config = configparser.ConfigParser()
    config.read('config.ini')
    shooting_dataset = config['DATA']['INPUT_CSV_1']
    df = prepare_data(shooting_dataset)
    data = get_incident_race_distribution(df)
    state_data = get_incidents_per_state(df)
    data_dict = {
                    'distribution' : data,
                    'state_data'   : state_data
                }
    data = {'distribution_data': data_dict}
    return render_template('racial_mix.html', data=data)


@app.route("/indexStat", methods=['POST', 'GET'])
def index_statistics():

    if request.method == 'POST':
        data = request.get_json()
        start = int(data['s'])
        end = int(data['e'])
        state = str(data['state'])
        config = configparser.ConfigParser()
        config.read('config.ini')
        shooting_dataset = config['DATA']['INPUT_CSV_1']
        df = prepare_data(shooting_dataset)
        result = get_index_stats(df, start, end, state)
        return json.dumps(result)


@app.route("/yearData", methods=['POST', 'GET'])
def index_year_data():

    if request.method == 'POST':
        data = request.get_json()
        state = str(data['state'])
        config = configparser.ConfigParser()
        config.read('config.ini')
        shooting_dataset = config['DATA']['INPUT_CSV_1']
        df = prepare_data(shooting_dataset)
        result_bar = get_incidents_per_year(df, state)
        #for key, value in result_bar.items():
        #    result_bar[key] = value.item()
        result_scree = get_scree_incidents(df, state)
        result_dict = {
                            'scree' : result_scree,
                            'bar'   : result_bar
                      }

        return json.dumps(result_dict)


@app.route("/features", methods=['POST', 'GET'])
def data_features():
    return render_template('features.html')


if __name__ == "__main__":
    app.run(debug=True)