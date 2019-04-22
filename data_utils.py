import pandas as pd
import configparser


def prepare_data(data_file):
    """
        Prepare dataset in form of pandas dataframe and scale using the Standard Scaler
    """
    df = pd.read_csv(data_file)
    sample_features = ["Year", "Location", "State", "Dead", "Injured", "Total", "Race", "Gender", "Mental Health",
                       "Latitude", "Longitude"]

    return df[sample_features]


def get_year_bar_data(data):
    return data.Year.unique().tolist()


def get_incidents_per_year(data):
    return data['Year'].value_counts().to_dict()


# config = configparser.ConfigParser()
# config.read('config.ini')
# shooting_dataset = config['DATA']['INPUT_CSV_1']
# df = prepare_data(shooting_dataset)
# get_year_bar_data(df)
# year_dict = get_incidents_per_year(df)
