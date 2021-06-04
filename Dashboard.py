import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json

df = pd.read_csv('sensor_data.csv')

df['id'] = df['time']
df.set_index('id', inplace=True, drop=False)

app = dash.Dash(__name__)

app.layout = html.Div([
html.Div([
    html.H3('Dashboard')
]),

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

    dcc.Input(id='filter-query-input', placeholder='Enter filter query'),

    html.Div(id='filter-query-output'),

    html.Hr(),

    dash_table.DataTable(
        id='datatable-advanced-filtering',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in df.columns
            # omit the id column
            if i != 'id'
        ],
        data=df.to_dict('records'),
        editable=True,
        page_action='native',
        page_size=10,
        filter_action="native",
        style_cell={
            'textAlign':'left',
            'minWidth': 210,'maxWidth': 210,'Width': 210,
            'backgroundColor':'white'
        },
        style_cell_conditional=[{'textAlign':'left'}]
    ),
    html.Hr(),
    html.Div(id='datatable-query-structure', style={'whitespace': 'pre'})
])
])

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

# @app.callback(
#     Output(component_id='datatable-query-structure', component_property='children'),
#     [Input(component_id='datatable', component_property="derived_virtual_data"),
#      Input(component_id='datatable', component_property='derived_virtual_selected_rows'),
#      Input(component_id='datatable', component_property='derived_virtual_selected_row_ids'),
#      Input(component_id='datatable', component_property='selected_rows'),
#      Input(component_id='datatable', component_property='derived_virtual_indices'),
#      Input(component_id='datatable', component_property='derived_virtual_row_ids'),
#      Input(component_id='datatable', component_property='active_cell'),
#      Input(component_id='datatable', component_property='selected_cells')]
# )
# def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows,
#                order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
#     print('***************************************************************************')
#     print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
#     print('---------------------------------------------')
#     print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
#     print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
#     print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
#     print('---------------------------------------------')
#     print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
#     print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
#     print("---------------------------------------------")
#     print("Complete data of active cell: {}".format(actv_cell))
#     print("Complete data of all selected cells: {}".format(slctd_cell))


if __name__ == '__main__':
    app.run_server(debug=True)
