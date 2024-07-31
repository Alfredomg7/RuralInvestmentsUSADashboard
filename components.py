from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px

def create_card(title, value_id):
    """
    Create a card using Dash Bootstrap Components.
    
    Parameters
    ----------
    title : str
        The title of the card.
    value_id : str
        The ID of the value to be displayed

    Returns
    -------
    dbc.Col
        The card component.
    """
    card = dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4(title, className='card-title', style={'font-size': '1.25rem'}),
                            html.H2(id=value_id, className='card-text', style={'font-size': '2rem'}),
                        ],
                        style={'text-align': 'center', 'padding': '1rem'}
                    )
                ],
                className='w-100 bg-success text-white',
                style={
                    'border-radius': '0.5rem',
                    'border': 'none',
                    'box-shadow': '0 0 1rem 0 rgba(0, 0, 0, 0.1)',
                    'margin': 'auto',
                }
            )
    return card

def create_tabs(options, id='tabs'):
    """
    Create tabs using Dash Bootstrap Components.
    
    Parameters
    ----------
    options : list
        A list of options to be used as the tabs.
    id : str
        The ID of the tabs.

    Returns
    -------
    dbc.Col
        The tabs component. 
    """
    tabs = dbc.Col(dbc.Tabs(
                            id=id,
                            active_tab=options[0],
                            class_name='nav nav-pills nav-fill my-2 d-flex justify-content-center w-100',
                            style= {'background-color': '#f5f6f7'},
                            children=[
                                dbc.Tab(label=option, tab_id=option, class_name='nav-item fw-bold') for option in options
                                    ]
                            ), width=12)
    return tabs

def create_radio_items(options, id='radio-items'):
    """
    Create radio items using Dash Bootstrap Components.
    
    Parameters
    ----------
    options : list
        A list of options to be used as the radio items.
    id : str
        The ID of the radio items.

    Returns
    -------
    dbc.Col
        The radio items component.
    """ 
    radio_items = dbc.RadioItems(
                                id=id,
                                options=[{'label': option, 'value': option} for option in options],
                                value=options[0],
                                inline=True,
                                class_name='mb-3'
                                )
    return radio_items

def create_treemap(df, dimensions, values, title):
    """
    Create a treemap plot using Plotly Express.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to be visualized.
    dimensions : list
        A list of columns to be used as the hierarchical structure of the treemap.
    values : str
        The column to be used as the values of the treemap.
    title : str 
        The title of the treemap plot

    Returns
    -------
    plotly.graph_objects.Figure
        The treemap plot.
    """
    value_by_dimensions = df.groupby(dimensions).agg({values: 'sum'}).reset_index()

    fig = px.treemap(
        value_by_dimensions,
        path=dimensions,
        values=values,
        title=title,
    )
    
    fig.update_layout(
        title_font_size=28,
        title_font_family='sans-serif',
        title_x=0.5,
        plot_bgcolor='#f5f6f7',
        paper_bgcolor='#f5f6f7'
    )
    
    return fig

def create_bar_chart(df, dimension, values, title):
    """
    Create a bar chart using Plotly Express.

    Parameters

    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to be visualized.
    dimension : str
        The column to be used as the x-axis of the bar chart.
    values : str    
        The column to be used as the y-axis of the bar chart.
    title : str 
        The title of the treemap plot
    
    Returns
    -------
    fig: plotly.graph_objects.Figure
        The bar chart.
    """
    value_by_dimension = df.groupby([dimension]).agg({values: 'sum'}).reset_index()
    value_by_dimension = value_by_dimension.sort_values(by=values, ascending=False)
    
    fig = px.bar(
        value_by_dimension,
        x=dimension,
        y=values,
        title=title,
    )
    
    fig.update_xaxes(title_text='', tickfont_size=18)
    fig.update_yaxes(title_text='Investment USD ($)', tickfont_size=18, title_font_size=20)

    fig.update_layout(
        title_font_size=28,
        title_font_family='sans-serif',
        title_x=0.5,
        plot_bgcolor='#f5f6f7',
        paper_bgcolor='#f5f6f7'
    )
    
    return fig
