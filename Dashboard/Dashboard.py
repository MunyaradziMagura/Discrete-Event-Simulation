import json
import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('sensor_data.csv')
# open the csv file to get data
df.drop(['sensor_one_warning','sensor_one_alarm','sensor_one_emergency','sensor_one_warning_vib',
         'sensor_one_alarm_vib','sensor_one_emergency_vib','sensor_two_warning','sensor_two_alarm',
         'sensor_two_emergency','sensor_two_warning_vib','sensor_two_alarm_vib','sensor_two_emergency_vib',
         'sensor_three_warning', 'sensor_three_alarm', 'sensor_three_emergency', 'sensor_three_warning_vib',
         'sensor_three_alarm_vib', 'sensor_three_emergency_vib'],axis=1,inplace=True)
#delete the unuseful columns


app = dash.Dash(__name__)

app.layout = html.Div([
html.Div([
    html.H3('Dashboard')
]),
# make a title for dashboard

html.Div([

    html.Br(),
    #define some id, these will be used later

    html.Div(id='bar-chart'),
    html.Div(id='line-graph'),

# define the detail of datatable
    dash_table.DataTable(
        id='datatable-advanced-filtering',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
            # omit the id column
            if i != 'id'
        ],
        data=df.to_dict('records'),
        editable=True, #editing the cells
        page_action='native', # all data is passed to the table up-front or not ('none')
        page_size=10,   # number of rows visible per page
        filter_action="native", #filtering by column
        style_cell={
            'textAlign':'left', # align text columns to left. By default they are aligned to right
            'minWidth': 210,'maxWidth': 210,'Width': 210,
            # couse some of the texts are too long so I make the width big
            'backgroundColor':'white'
        },
    ),
    html.Hr(),
    html.Div(id='datatable-query-structure', style={'whitespace': 'pre'})

])
])


@app.callback(
    Output('datatable-query-structure', 'children'),
    Input('datatable-advanced-filtering', 'derived_filter_query_structure')
)
def display_query(query):
    if query is None:
        return ''
    return html.Details([
        html.Summary('Derived filter query structure'),
        html.Div(dcc.Markdown('''```json
{}
```'''.format(json.dumps(query, indent=4))))
    ])


#bar chart
@app.callback(
    Output('bar-chart', 'children'),
    Input('datatable-advanced-filtering', "derived_virtual_data"),
)
def update_bar(all_rows_data):
    dff = pd.DataFrame(all_rows_data)
    if "time" in dff and "sensor_one_temp" in dff:
        return [
            dcc.Graph(
                id='bar-chart',
                figure={
                    'data':[
                        # six bars for six different data
                        {'x': df['time'], 'y': df['sensor_one_temp'], 'type':'bar', 'name':'sensor_one_temp'},
                        {'x': df['time'], 'y': df['sensor_one_vib'], 'type':'bar', 'name':'sensor_one_vib'},
                        {'x': df['time'], 'y': df['sensor_two_temp'], 'type':'bar', 'name': 'sensor_two_temp'},
                        {'x': df['time'], 'y': df['sensor_two_temp_vib'], 'type':'bar', 'name': 'sensor_two_temp_vib'},
                        {'x': df['time'], 'y': df['sensor_three_temp'], 'type':'bar', 'name': 'sensor_three_temp'},
                        {'x': df['time'], 'y': df['sensor_three_temp_vib'], 'type':'bar', 'name': 'sensor_three_temp_vib'}
                    ],
                    'layout':{
                        'title': 'Bar Chart' #the title of the bar chart
                    }
                }
            )
        ]

# line graph
@app.callback(
    Output('line-graph', 'children'),
    Input('datatable-advanced-filtering', "derived_virtual_data"),
)
def update_line(all_rows_data):
    dff = pd.DataFrame(all_rows_data)
    if "time" in dff and "sensor_one_temp" in dff:
        return [
            dcc.Graph(
                id='line-graph',
                figure={
                    'data':[
                        # six lines for six different data
                        {'x': df['time'], 'y': df['sensor_one_temp'], 'type':'line', 'name':'sensor_one_temp'},
                        {'x': df['time'], 'y': df['sensor_one_vib'], 'type':'line', 'name':'sensor_one_vib'},
                        {'x': df['time'], 'y': df['sensor_two_temp'], 'type':'line', 'name': 'sensor_two_temp'},
                        {'x': df['time'], 'y': df['sensor_two_temp_vib'], 'type':'line', 'name': 'sensor_two_temp_vib'},
                        {'x': df['time'], 'y': df['sensor_three_temp'], 'type':'line', 'name': 'sensor_three_temp'},
                        {'x': df['time'], 'y': df['sensor_three_temp_vib'], 'type':'line', 'name': 'sensor_three_temp_vib'}
                    ],
                    'layout':{
                        'title': 'Line Graph' #the title of the line Graph
                    }
                }
            )
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
