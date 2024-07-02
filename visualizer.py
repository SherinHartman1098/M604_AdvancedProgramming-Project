import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

class Visualizer:
    def __init__(self, df):
        self.df = df

    def plot_unemployment_rate_by_state(self):
        fig = px.bar(
            self.df,
            x='State/Area',
            y='Percent (%) of Labor Force Unemployed in State/Area',
            animation_frame='Year',
            title='Unemployment Rate by State Over Time',
            labels={'Percent (%) of Labor Force Unemployed in State/Area': 'Unemployment Rate (%)'},
            color='Percent (%) of Labor Force Unemployed in State/Area',
            color_continuous_scale='Rainbow',
            template='plotly_white'
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            xaxis_title="State/Area",
            yaxis_title="Unemployment Rate (%)",
            title_x=0.5
        )
        return fig

    def plot_unemployment_rate_trends(self):
        self.df['Date'] = pd.to_datetime(self.df[['Year', 'Month']].assign(DAY=1))
        fig = px.line(
            self.df,
            x='Date',
            y='Percent (%) of Labor Force Unemployed in State/Area',
            color='State/Area',
            title='Unemployment Rate Trends Over Time by State',
            labels={'Percent (%) of Labor Force Unemployed in State/Area': 'Unemployment Rate (%)'}
        )
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Unemployment Rate (%)",
            title_x=0.5,
            legend_title_text='State',
            hovermode="x unified"
        )
        return fig

    def plot_employment_vs_unemployment(self, sample_fraction=0.1):
        df_sampled = self.df.sample(frac=sample_fraction, random_state=42)
        fig = px.scatter(
            df_sampled,
            x='Total Employment in State/Area',
            y='Total Unemployment in State/Area',
            color='State/Area',
            title='Employment vs. Unemployment (Sampled Data)',
            labels={'Total Employment in State/Area': 'Total Employment', 'Total Unemployment in State/Area': 'Total Unemployment'},
            template='plotly_white'
        )
        fig.update_traces(marker=dict(size=10))
        fig.update_layout(
            xaxis_title="Total Employment",
            yaxis_title="Total Unemployment",
            title_x=0.5
        )
        return fig

    def plot_avg_unemployment_indicator(self):
        # Generate data
        years = list(range(1980, 2024))
        states = ['California', 'New York', 'Texas', 'Florida']
        data = {'Year': [], 'State': [], 'Total Unemployment': []}
        for year in years:
            for state in states:
                data['Year'].append(year)
                data['State'].append(state)
                data['Total Unemployment'].append(random.randint(50000, 1500000))

        df = pd.DataFrame(data)

        # Function to update the indicator
        def update_indicator(year):
            filtered_df = df[df['Year'] == year]
            avg_unemployment = filtered_df['Total Unemployment'].mean()
            return avg_unemployment

        # Create the indicator figure
        fig = go.Figure(go.Indicator(
            mode="number+gauge+delta",
            gauge={'shape': "bullet"},
            delta={'reference': df['Total Unemployment'].mean() }, # Reference for the delta mode
            value=update_indicator(years[0]), # Initial the value (first year)
            domain={'x': [0.3, 1], 'y': [0.2, 0.9]},
            title={'text': "Average Employment"}
        ))

        # Update layout for the dropdown
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(label=str(year),
                             method="update",
                             args=[{"value": update_indicator(year)}])  # Update value on dropdown changes
                        for year in years
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,  # Adjust dropdown position as per requirements
                    y=1.1
                ),
            ]
        )
        fig.update_layout(title="Year to Year Unemployment Difference in USA")

        return fig

    def plot_total_unemployment_over_time(self):
        # Generate data
        years = list(range(1980, 2024))
        states = ['California', 'New York', 'Texas', 'Florida']
        data = {'Year': [], 'State': [], 'Total Unemployment': []}
        for year in years:
            for state in states:
                data['Year'].append(year)
                data['State'].append(state)
                data['Total Unemployment'].append(random.randint(50000, 1500000))

        df = pd.DataFrame(data)

        fig = go.Figure()

        for state in states:
            df_state = df[df['State'] == state]
            fig.add_trace(go.Scatter(x=df_state['Year'], y=df_state['Total Unemployment'],
                                     mode='lines+markers', name=state))

        fig.update_layout(title="Total Unemployment in Major States Over Time",
                          xaxis_title="Year",
                          yaxis_title="Total Unemployment")

        return fig