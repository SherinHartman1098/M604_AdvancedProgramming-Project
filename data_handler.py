import pandas as pd

class DataHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.filepath)
        #self._map_state_abbreviations()
        self._drop_unused_columns()
        self._drop_duplicates_and_na()
        return self.df

    def _map_state_abbreviations(self):
        if self.df is not None:
            states_abbreviation = {
                "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
                "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
                "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
                "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
                "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
                "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
                "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
                "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
                "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
                "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
                "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
                "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
                "Wisconsin": "WI", "Wyoming": "WY"
            }
            self.df['State Abbreviation'] = self.df['State/Area'].map(states_abbreviation)

    def _drop_unused_columns(self):
        if self.df is not None:
            self.df = self.df.drop(columns=['FIPS Code'])

    def _drop_duplicates_and_na(self):
        if self.df is not None:
            self.df.drop_duplicates(keep='last', inplace=True)
            self.df.dropna(inplace=True)

    def filter_data(self, start_date=None, end_date=None, states=None):
        if self.df is None:
            return None
        
        df_filtered = self.df.copy()

        if start_date and end_date:
            df_filtered['Date'] = pd.to_datetime(df_filtered[['Year', 'Month']].assign(DAY=1))
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            df_filtered = df_filtered[(df_filtered['Date'] >= start_date) & (df_filtered['Date'] <= end_date)]
        
        if states:
            df_filtered = df_filtered[df_filtered['State/Area'].isin(states)]
        
        return df_filtered