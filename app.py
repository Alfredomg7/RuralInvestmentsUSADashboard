import components as cmp
from clean import clean_data
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd

# Create a Dash app with custom theme
load_figure_template('litera')
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

# Load data
file_path = 'data/rural-investments.csv'
df = pd.read_csv(file_path)

# Clean data
df = clean_data(df)

# Create components
title = html.H1('Rural Investments 2024', className='display-3 text-center')
subtitle = html.H3('Visualize investment in rural areas across USA', className='lead text-center')
linebreaker = html.Hr(className='my-2')
total_investment_card = cmp.create_card('Total Investment', 'total-investment')
program_areas = ['All'] + list(df['Program Area'].unique())
tabs = cmp.create_tabs(program_areas, id='program-area-tabs')
dimension_options = ['Program Area', 'Investment Type']
radio_items = cmp.create_radio_items(dimension_options, id='dimension-radio-items')
investment_by_state_fig_style = {'height': '80vh', 'width': '100%', 'margin': '0 auto', 'margin-bottom': '20px'}
investment_by_program_fig_style = {'height': '60vh', 'width': '100%', 'margin': '0 auto', 'margin-bottom': '20px'}
investment_by_state_fig = dcc.Graph(id='investment-by-state-fig', style=investment_by_state_fig_style)
investment_by_program_fig = dcc.Graph(id='investment-by-program-fig',style=investment_by_program_fig_style)
footer = html.Footer(
    [
        html.Div(
            [
                html.A('Author: Alfredo M.', href='https://github.com/Alfredomg7', target='_blank', className='footer-link'),
                html.Span(' | '),
                html.A('Dataset Source', href='https://github.com/plotly/Figure-Friday/blob/main/2024/week-30/rural-investments.csv', target='_blank', className='footer-link')
            ],
            className='text-center py-4 fs-5',
            style={
                'background-color': '#f5f6f7',
                'border-top': '1px solid #d1d1d1',
                'width': '100%',
                'box-shadow': '0 -1px 5px rgba(0,0,0,0.1)'
            }
        )
    ]
)

# Define the layout of the app
app.layout = html.Div(
    [   
        # Header section
        dbc.Row(
            [
                dbc.Col(
                    [
                        title,
                        subtitle,
                    ],
                    width=8,
                    className='p-3 mb-0'
                ),
                dbc.Col(
                    [
                        total_investment_card
                    ],
                    xl=2,
                    lg=3,
                    md=4,
                    className='p-3 mb-0'
                ),
            ],
            align='center',
            style={'background-color': '#eeeff0'}
        ),
        linebreaker,
        # Main section
        dbc.Row(
            [
                dbc.Col(
                    [
                        tabs,
                        investment_by_state_fig
                    ], 
                    width=12,
                )
            ],
            className='px-xs-1 px-sm-2 px-md-3 px-lg-4 px-xl-5',
            style={'background-color': '#f5f6f7'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [   radio_items,
                        investment_by_program_fig
                    ], 
                    width=12
                )
            ],
            className='px-xs-1 px-sm-2 px-md-3 px-lg-4 px-xl-5',
            style={'background-color': '#f5f6f7'}
        ),
        # Footer section
        footer
    ], style={'background-color': '#f5f6f7'})

# Callback to update the total investment value
@app.callback(
    Output('total-investment', 'children'),
    Input('program-area-tabs', 'active_tab')
)
def update_total_investment(active_tab):
    if active_tab == 'All':
        total_investment = df['Investment'].sum()
    else:
        total_investment = df[df['Program Area'] == active_tab]['Investment'].sum()
    return f'${total_investment/1e6:.2f}M'

# Callback to update the treemap plot based on the selected program area
@app.callback(
    Output('investment-by-state-fig', 'figure'),
    Input('program-area-tabs', 'active_tab')
)
def update_treemap(active_tab):
    if active_tab == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Program Area'] == active_tab]
    fig = cmp.create_treemap(filtered_df, dimensions=['State', 'City'], values='Investment', title='Investment by State and City')
    return fig

# Callback to update the bar chart based on the selected program area and dimension
@app.callback(
    Output('investment-by-program-fig', 'figure'),
    Input('program-area-tabs', 'active_tab'),
    Input('dimension-radio-items', 'value')
)
def update_bar_chart(active_tab, dimension):
    if active_tab == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Program Area'] == active_tab]
    fig = cmp.create_bar_chart(filtered_df, dimension=dimension, values='Investment', title='Investment by {}'.format(dimension))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
