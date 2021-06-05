import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import plotly.express as px

df = pd.read_csv('sensor_data.csv') # open the csv file to get data

df['id'] = df['time']
df.set_index('id', inplace=True, drop=False)

app = dash.Dash(__name__)

app.layout = html.Div([
html.Div([
    html.H3('Dashboard')
]),
# make a title for dashboard
    
html.Div([
    dcc.RadioItems(
        id='datatable',
        options=[
            {'label': 'Read filter_query', 'value': 'read'},
            {'label': 'Write to filter_query', 'value': 'write'}
        ],
        value='read'
    ),

    html.Br(),
    #define some id, these will be used later
    dcc.Input(id='filter-query-input', placeholder='Enter filter query'),

    html.Div(id='filter-query-output'),

    html.Hr(),
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
        editable=True,  #editing the cells
        page_action='native',   # all data is passed to the table up-front or not ('none')
        page_size=10,   # number of rows visible per page
        filter_action="native", #filtering by column
        style_cell={
            'textAlign':'left', # align text columns to left. By default they are aligned to right
            'minWidth': 210,'maxWidth': 210,'Width': 210,   # couse some of the texts are too long so I make the width big
            'backgroundColor':'white'
        },
        style_cell_conditional=[{'textAlign':'left'}]
    ),
    html.Hr(),
    html.Div(id='datatable-query-structure', style={'whitespace': 'pre'})
])
])

# use callback to pass the value returned by def below to id 'filter-query-input'
@app.callback(
    Output('filter-query-input', 'style'),
    Output('filter-query-output', 'style'),
    Input('datatable', 'value')
)
def query_input_output(val):
    input_style = {'width': '200%'}
    output_style = {}
    if val == 'read':
        input_style.update(display='none')
        output_style.update(display='inline-block')
    else:
        input_style.update(display='inline-block')
        output_style.update(display='none')
    return input_style, output_style


@app.callback(
    Output('datatable-advanced-filtering', 'filter_query'),
    Input('filter-query-input', 'value')
)
def write_query(query):
    if query is None:
        return ''
    return query


@app.callback(
    Output('filter-query-output', 'children'),
    Input('datatable-advanced-filtering', 'filter_query')
)
def read_query(query):
    if query is None:
        return "No filter query"
    return dcc.Markdown('`filter_query = "{}"`'.format(query))


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
    Output('bar-chart','children'),
    Input('datatable-advanced-filtering', "derived_virtual_data"),
    Input('datatable-advanced-filtering', "derived_virtual_selected_rows")
)
def update_bar(all_rows_data, slctd_row_indices):
    print('***************************************************************************')
    print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    print('---------------------------------------------')
    print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    dff = pd.DataFrame(all_rows_data)
    colors = ['#7FDBFF' if i in slctd_row_indices else '#0074D9'
              for i in range(len(dff))]
    if "time" in dff and "sensor_one_temp" in dff:
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x="time",
                          y='sensor_one_temp',
                          labels={"sensor_one_temp": "The data of sensors"},
                      ).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
                      .update_traces(marker_color=colors, hovertemplate="<b>%{y}%</b><extra></extra>")
                      ),
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
                        {'x': df['time'], 'y': df['sensor_one_temp'], 'name':'sensor_one_temp'},
                        {'x': df['time'], 'y': df['sensor_one_vib'], 'name':'sensor_one_vib'},
                        {'x': df['time'], 'y': df['sensor_two_temp'], 'name': 'sensor_two_temp'},
                        {'x': df['time'], 'y': df['sensor_two_temp_vib'], 'name': 'sensor_two_temp_vib'},
                        {'x': df['time'], 'y': df['sensor_three_temp'], 'name': 'sensor_three_temp'},
                        {'x': df['time'], 'y': df['sensor_three_temp_vib'], 'name': 'sensor_three_temp_vib'}
                    ],
                    'layout':{
                        'title': 'Line Graph' #the title of the line Graph
                    }
                }
            )
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
