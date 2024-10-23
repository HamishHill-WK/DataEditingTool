from dash import Dash, html, dcc, callback, Output, Input 
import plotly.express as px
import random
import pandas as pd
#I used ChatGPT gpt4o model to assist with some of the syntax for this library 
#I used the 'minimal application' from the getting started guide as the starting point for this code https://dash.plotly.com/minimal-app

#this function creates a dash app layout for comparing
def compare_axes(data : pd.DataFrame, app : Dash): #enforce type of arguments to avoid ambiguity
    numerical_columns = data.select_dtypes(include=['number']).columns #this variable is to ensure only numerical columns can be selected for the graph axes
    categorical_columns = data.select_dtypes(include=['object', 'category', 'string']).columns
    using_index = False
    
    if len(categorical_columns) == 0:
        using_index = True
        categorical_columns = data['index'] = data.index  # Create a new column with the DataFrame index
    
    # Ensure the dataset passed in contains at least one categorical and two numerical columns
    if len(categorical_columns) < 1 or len(numerical_columns) < 2:
        raise ValueError("Data must contain at least one categorical (object) column and two numerical columns.")
    
    if not using_index:
        initial_category = random.choice(categorical_columns) if len(categorical_columns) > 0 else None #randomise the category column
 
    app.layout = html.Div([
        html.Div([
            html.Label("Select Category:"),
            dcc.Dropdown(categorical_columns, initial_category, id='dropdown-category-selection')
        ], style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'marginRight': '20px', 'background-color': 'coral'}),
        html.Div([
            html.Label("Select Values Within Category Column:"),
            dcc.Dropdown(id='dropdown-value-selection', multi=True, value=[])
        ], style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'marginRight': '20px', 'background-color': 'coral'}),
         html.Div([
            html.Label("X-Axis"),
            dcc.Dropdown(numerical_columns, numerical_columns[0], id='dropdown-x-selection')
        ], style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'marginRight': '20px', 'background-color': 'coral'}),  
        html.Div([
            html.Label("Y-Axis:"),
            dcc.Dropdown(numerical_columns, numerical_columns[1], id='dropdown-y-selection')
        ], style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'marginRight': '20px', 'background-color': 'coral'}),
        html.Div([
            dcc.Checklist(options=[{'label': 'Include Regression Line', 'value': 'show'}], id='regression-toggle',value=[])  # Empty list means it's unchecked by default
        ], style={'marginTop': '20px', 'background-color': 'coral'}),
        dcc.Graph(id='graph-content')
    ])
    # Update the values dropdown based on the selected categorical column
    @callback(
        Output('dropdown-value-selection', 'options'),
        Output('dropdown-value-selection', 'value'),  # Output the random value
        Input('dropdown-category-selection', 'value')
    )
    def update_value_options(selected_category):
        if(using_index):
            return 0
        else:
            # previous_category = selected_category
            unique_values = data[selected_category].unique()
            formatted_values = [{'label': str(i), 'value': str(i)} for i in unique_values]
            options = random.sample([i['value'] for i in formatted_values], 3)
            return formatted_values, options
    
    #update graph values
    @callback(
        Output('graph-content', 'figure'),
        Input('dropdown-category-selection', 'value'),
        Input('dropdown-value-selection', 'value'),
        Input('dropdown-x-selection', 'value'),
        Input('dropdown-y-selection', 'value'),
        Input('regression-toggle', 'value')
    )
    def update_graph(category_column, selected_values, valuex, valuey, regression_toggle):
        if selected_values:
            dff = data[data[category_column].isin(selected_values)]
            
        trendline = "ols" if "show" in regression_toggle else None  #sometimes it takes a little time for the regression line to appear on first loading up the notebook
        return px.scatter(dff, valuex, valuey, color=category_column, trendline=trendline, trendline_color_override='red')
    return app.layout