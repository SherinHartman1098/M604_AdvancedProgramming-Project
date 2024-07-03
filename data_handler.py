import pandas as pd

class DataHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.state_data = None

    def load_data(self):
        self.state_data = pd.read_csv(self.filepath)
        #self._map_state_abbreviations()
        self._drop_unused_columns()
        self._drop_duplicates_and_na()
        return self.state_data

    # def _map_state_abbreviations(self):
    #     if self.state_data is not None:
    #         states_abbreviation = {
    #             "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    #             "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    #             "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    #             "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    #             "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    #             "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    #             "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    #             "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    #             "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    #             "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    #             "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    #             "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    #             "Wisconsin": "WI", "Wyoming": "WY"
    #         }
    #         self.state_data['State Abbreviation'] = self.state_data['State/Area'].map(states_abbreviation)

    def _drop_unused_columns(self):
        if self.state_data is not None:
            self.state_data = self.state_data.drop(columns=['FIPS Code'])

    def _drop_duplicates_and_na(self):
        if self.state_data is not None:
            self.state_data.drop_duplicates(keep='last', inplace=True)
            self.state_data.dropna(inplace=True)

    def filter_data(self, start_date=None, end_date=None, states=None):
        if self.state_data is None:
            return None
        
        state_data_filtered = self.state_data.copy()

        if start_date and end_date:
            state_data_filtered['Date'] = pd.to_datetime(state_data_filtered[['Year', 'Month']].assign(DAY=1))
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            state_data_filtered = state_data_filtered[(state_data_filtered['Date'] >= start_date) & (state_data_filtered['Date'] <= end_date)]
        
        if states:
            state_data_filtered = state_data_filtered[state_data_filtered['State/Area'].isin(states)]
        
        return state_data_filtered