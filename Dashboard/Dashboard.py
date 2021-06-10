import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import csv

df = pd.read_csv('sensor_data.csv')  # open the csv file to get data
# this is used to get the final number of sensorID, in this way can get the whole number of sensors that used
sensorID = df['sensorID']
sensorID_list = sensorID.values.tolist()  # change the value of sensorID to list to operate on it
list_num = []
for i in sensorID_list:  # use for loop to get all different value in sensorID
    if i in list_num:
        continue
    else:
        list_num.append(i)  # put the value into list
sensorID_num = list_num[len(list_num) - 1]  # get the last number of list_num
sensorID_num = int(sensorID_num)  # change it to int format

# use dictionary to storage data in this way can use it during making line graph and bar chart
csv_dictionary = {}
with open('sensor_data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        # print(row[1])
        time = row[1]
        temp = row[2]
        vib = row[3]
        if str(row[0]) in csv_dictionary:
            # add time
            csv_dictionary[str(row[0])][0].append(time)
            # add temperature
            csv_dictionary[str(row[0])][1].append(temp)
            # add vibration
            csv_dictionary[str(row[0])][2].append(vib)
        else:
            csv_dictionary[str(row[0])] = [[time], [temp], [vib]]

app = dash.Dash(__name__)

# write the figure outside, so just need to calling this function in dcc.graph
# figure for line graph
data_line = []
for i in range(0, sensorID_num + 1):
    name_temp = 'sensor_' + str(i + 1) + '_temp'  # because i is 0 at begin, so use i+1. Set the name for each temp line
    name_vib = 'sensor_' + str(i + 1) + '_vib'  # set the name for each temp line
    # set x,y value and name for each line we will get
    data_line.append({'x': csv_dictionary[str(i)][0], 'y': csv_dictionary[str(i)][1], 
                      'type': 'line', 'name': name_temp})
    data_line.append({'x': csv_dictionary[str(i)][0], 'y': csv_dictionary[str(i)][2], 
                      'type': 'line', 'name': name_vib})
figure_line_graph = {'data': data_line,
                     'layout': {
                         'title': 'Line Graph',  # the title of the line graph
                     },
                     }

# figure for line graph
data_bar = []
for i in range(0, sensorID_num + 1):
    name_temp = 'sensor_' + str(i + 1) + '_temp'  # set the name for each temp bar
    name_vib = 'sensor_' + str(i + 1) + '_vib'  # set the name for each vib bar
    # set x,y value and name for each bar we will get
    data_bar.append({'x': csv_dictionary[str(i)][0], 'y': csv_dictionary[str(i)][1], 
                     'type': 'bar', 'name': name_temp})
    data_bar.append({'x': csv_dictionary[str(i)][0], 'y': csv_dictionary[str(i)][2], 
                     'type': 'bar', 'name': name_vib})
figure_barchart = {'data': data_bar,
                   'layout': {
                       'title': 'Bar Chart',  # the title of the bar chart
                   },
                   }

app.layout = html.Div([
    html.Div([
        html.H3('Dashboard')
    ]),
    # make a title for dashboard

    html.Div([
        html.Br(),

        dcc.Graph(id='line garph',
                  figure=figure_line_graph  # calling figure_line_graph
                  ),

        dcc.Graph(id='bar chart',
                  figure=figure_barchart,  # calling figure_barchart
                  ),

        # define the detail of datatable
        dash_table.DataTable(
            id='datatable-advanced-filtering',
            columns=[
                {'name': i, 'id': i, 'deletable': True} for i in df.columns
                # omit the id column
                if i != 'id'
            ],
            data=df.to_dict('records'),
            editable=True,  # editing the cells
            page_action='native',  # all data is passed to the table up-front or not ('none')
            page_size=10,  # number of rows visible per page
            filter_action="native",  # filtering by column
            style_cell={
                'textAlign': 'left',  # align text columns to left. By default they are aligned to right
                'minWidth': 210, 'maxWidth': 210, 'Width': 210,
                # cause some of the texts are too long so I make the width big
                'backgroundColor': 'white'
            },
        ),
        html.Hr()
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
