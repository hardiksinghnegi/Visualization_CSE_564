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
    csv_df = data[['Year']]
    csv_df['Year'] = pd.to_datetime(csv_df['Year'], format="%Y")
    tmp = csv_df.groupby('Year').size()
    df = tmp.to_frame()
    df = tmp.reset_index(name = 'count')
    df['Year'] = pd.to_datetime(df["Year"]).dt.strftime('%-d-%b-%Y')
    df.rename(columns={'Year': 'date'}, inplace=True)
    df.to_csv('static/data_files/csv/scree_index.csv', index=False)
    return data['Year'].value_counts().to_dict()


def get_incidents_per_state(data):
    csv_df = data[['State']]
    tmp = csv_df.groupby('State').size()
    df = tmp.to_frame()
    df = tmp.reset_index(name = 'cases')
    df.rename(columns={'State':'state'}, inplace=True)

    result_list = []

    for index, row in df.iterrows():
        state_obj = {
                        'state' : row['state'],
                        'cases'  : str(row['cases'])
                    }

        result_list.append(state_obj)

    return result_list


def get_incident_race_distribution(data):
    distribution = data[["Race"]]
    tmp = distribution.groupby('Race').size()
    df = tmp.to_frame()
    df = tmp.reset_index(name='Incidents')
    df['Distribution'] = (df['Incidents'] / df['Incidents'].sum())
    df.to_csv('static/data_files/csv/shooting_racial_distribution.csv', index=False)
    print(df)


def render_state_csv_by_year(data, start, end):
    csv_df = data.loc[(data['Year'] >= start) & (data['Year'] <= end)]
    return get_incidents_per_state(csv_df)


config = configparser.ConfigParser()
config.read('config.ini')
shooting_dataset = config['DATA']['INPUT_CSV_1']
df = prepare_data(shooting_dataset)
# # get_year_bar_data(df)
get_incidents_per_state(df)
# get_incident_race_distribution(df)
# render_state_csv_by_year(df, 1966, 2019)