import pandas as pd
import configparser
from sklearn.preprocessing import MinMaxScaler, StandardScaler

def prepare_data(data_file):
    """
        Prepare dataset in form of pandas dataframe and scale using the Standard Scaler
    """
    df = pd.read_csv(data_file)
    sample_features = ["Year", "Location", "State", "Dead", "Injured", "Total", "Race", "Gender", "Mental Health",
                       "Latitude", "Longitude", "Party"]

    return df[sample_features]


def get_year_bar_data(data):
    return data.Year.unique().tolist()


def get_incidents_per_year(data, state="All"):
    if state != "All":
        data = data.loc[data['State'] == state]
    csv_df = data[['Year']]
    csv_df['Year'] = pd.to_datetime(csv_df['Year'], format="%Y")
    tmp = csv_df.groupby('Year').size()
    df = tmp.to_frame()
    df = tmp.reset_index(name = 'count')
    df['Year'] = pd.to_datetime(df["Year"]).dt.strftime('%-d-%b-%Y')
    df.rename(columns={'Year': 'date'}, inplace=True)
    #df.to_csv('static/data_files/csv/scree_index.csv', index=False)
    #data['Year'] = data['Year'].astype(str)
    return data['Year'].value_counts().to_dict()


def get_scree_incidents(data, state="All"):
    if state != "All":
        data = data.loc[data['State'] == state]
    csv_df = data[['Year']]
    csv_df['Year'] = pd.to_datetime(csv_df['Year'], format="%Y")
    tmp = csv_df.groupby('Year').size()
    df = tmp.to_frame()
    df = tmp.reset_index(name = 'count')
    df['Year'] = pd.to_datetime(df["Year"]).dt.strftime('%-d-%b-%Y')
    df.rename(columns={'Year': 'date'}, inplace=True)

    result = []
    for index, row in df.iterrows():
        year_obj = {
            'date': row['date'],
            'count': int(row['count'])
        }
        result.append(year_obj)

    return result


def get_incidents_per_state(data):
    state_list = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","D.C.","Delaware",
                  "Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
                  "Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
                  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina",
                  "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","South Carolina","South Dakota","Tennessee",
                  "Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

    state_df = pd.DataFrame(state_list, columns=['state'])
    csv_df = data[['State']]
    tmp = csv_df.groupby('State').size()

    df = tmp.to_frame()
    df = tmp.reset_index(name = 'cases')
    df.rename(columns={'State':'state'}, inplace=True)

    res_df = pd.merge(state_df, df, how='left', on=['state'])

    result_list = []

    for index, row in res_df.iterrows():
        state_obj = {
                        'state' : row['state'],
                        'cases'  : str(row['cases'])[:-2]
                    }
        if state_obj['cases'] == 'n':
            state_obj['cases'] = '0'
        result_list.append(state_obj)
    return result_list


def get_incident_race_distribution(data):
    distribution = data[["Race"]]
    tmp = distribution.groupby('Race').size()
    df = tmp.to_frame()
    df = tmp.reset_index(name='Incidents')
    df['Distribution'] = (df['Incidents'] / df['Incidents'].sum())
    result = []
    for index, row in df.iterrows():
        race_obj = {
                        'Race' : row['Race'],
                        'Incidents'  : row['Incidents'],
                        'Distribution' : row['Distribution']
                    }

        result.append(race_obj)

    return result;


def render_state_csv_by_year(data, start, end):
    csv_df = data.loc[(data['Year'] >= start) & (data['Year'] <= end)]
    return get_incidents_per_state(csv_df)


def render_race_csv_by_year_govt(data, start, end, govt):
    csv_df = data.loc[(data['Year'] >= start) & (data['Year'] <= end)]
    if govt != 'Both':
        csv_df = csv_df.loc[data['Party'] == govt]
    data = get_incident_race_distribution(csv_df)
    data = {'distribution_data': data}
    return data


def get_index_stats(data, start, end, state):
    csv_df = data.loc[(data['Year'] >= start) & (data['Year'] <= end)]
    if state != "All":
        csv_df = csv_df.loc[csv_df['State'] == state]
    csv_df = csv_df[['Dead','Injured']]
    incidents = csv_df.shape[0]
    dead =  csv_df['Dead'].sum()
    injured = csv_df['Injured'].sum()
    stat_dict = {
                    'fatalities' : str(dead),
                    'injuries'   : str(injured),
                    'incidents'  : str(incidents)
                }
    return stat_dict


def get_year_stack(data):
    csv_df = data[['Year', 'Dead', 'Injured']]
    csv_df=csv_df.groupby('Year')['Dead', 'Injured'].sum()
    csv_df.to_csv('static/data_files/csv/data.csv')


def process_unemployment_rate(data):
    scaler = StandardScaler()
    data[['Rate', 'Incidents']] = scaler.fit_transform(data[['Rate','Incidents']])
    print(data[['Rate', 'Incidents']].corr())
    # data.to_csv('static/data_files/csv/unemp.csv', index=False)


def process_national_unemployment_data(data):
    df = data.interpolate(method ='linear', limit_direction ='backward')
    df.to_csv('static/data_files/csv/national_unemp.csv')


def process_google_index(data):
    data = data.groupby('Year')['Depression', 'Mental Health'].mean()
    data.to_csv('static/data_files/csv/google_index.csv')


def get_mental_distribution(data,start,end):
    data = data[['Mental Health']]
    data = data.groupby('Mental Health').size().reset_index(name='counts')
    res_list = data['counts'].tolist()
    print(data)
    return res_list

config = configparser.ConfigParser()
config.read('config.ini')
shooting_dataset = config['DATA']['INPUT_CSV_1']
unemployment_dataset = config['DATA']['INPUT_CSV_2']
n_unemployment_dataset = config['DATA']['INPUT_CSV_3']
g_index_dataset = config['DATA']['INPUT_CSV_4']

x = config['DATA']['INPUT_CSV_5']

df = prepare_data(shooting_dataset)

s_df = pd.read_csv(unemployment_dataset)
g_df = pd.read_csv(g_index_dataset)

h_df = pd.read_csv(x)

get_mental_distribution(df,1960,2019)
# process_unemployment_rate(h_df)
#
# # n_df = pd.read_csv(n_unemployment_dataset)
# #
# # process_national_unemployment_data(n_df)
#
# process_google_index(g_df)

# process_unemployment_rate(s_df)
# render_race_csv_by_year_govt(df, 2000, 2020, "Republican")
# # get_scree_incidents(df)
# # # # get_year_bar_data(df)
# # get_index_stats(df, 1966, 2018, "Alaska")
# # get_incident_race_distribution(df)
# # render_state_csv_by_year(df, 1966, 2019)
# get_year_stack(df)

