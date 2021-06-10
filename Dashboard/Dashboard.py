import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import csv

df = pd.read_csv('sensor_data.csv') # open the csv file to get data
sensorID = df['sensorID']
sensorIDlist = sensorID.values.tolist()
li=[]
for i in sensorIDlist:
    if i in li:
        continue
    else:
        li.append(i)
x = li[len(li)-1]
x= int(x)

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
            # add temp
            csv_dictionary[str(row[0])][1].append(temp)
            # add vib
            csv_dictionary[str(row[0])][2].append(vib)
        else:
            csv_dictionary[str(row[0])] = [[time],[temp],[vib]]

app = dash.Dash(__name__)

data=[]

for i in range(0, x+1):
    name = 'sensor_'+str(i+1)+'_temp'
    name2 = 'sensor_'+str(i+1)+'_vib'
    data.append({'x': csv_dictionary[str(i)][0], 'y': csv_dictionary[str(i)][1], 'type': 'line', 'name': name})
    data.append({'x': csv_dictionary[str(i)][0], 'y': csv_dictionary[str(i)][2], 'type': 'line', 'name': name2})
figure={'data':data,
                    'layout':{
                        'title': 'Line Graph', #the title of the bar chart
                             },
                      }

data2=[]
for i in range(0, x+1):
    name = 'sensor_'+str(i+1)+'_temp'
    name2 = 'sensor_'+str(i+1)+'_vib'
    data2.append({'x': csv_dictionary[str(i)][0], 'y': csv_dictionary[str(i)][1], 'type': 'bar', 'name': name})
    data2.append({'x': csv_dictionary[str(i)][0], 'y': csv_dictionary[str(i)][2], 'type': 'bar', 'name': name2})
figure2={'data':data2,
                    'layout':{
                        'title': 'Bar Chart', #the title of the bar chart
                             },
                      }

app.layout = html.Div([
html.Div([
    html.H3('Dashboard')
]),
# make a title for dashboard


html.Div([
    html.Br(),
    #define some id, these will be used later

    dcc.Graph(id='line garph',
              figure=figure
              ),

    dcc.Graph(id='bar chart',
              figure=figure2,
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
        editable=True, #editing the cells
        page_action='native', # all data is passed to the table up-front or not ('none')
        page_size=10,   # number of rows visible per page
        filter_action="native",# filtering by column
        style_cell={
            'textAlign':'left', # align text columns to left. By default they are aligned to right
            'minWidth': 210,'maxWidth': 210,'Width': 210,
            # couse some of the texts are too long so I make the width big
            'backgroundColor':'white'
        },
    ),
    html.Hr()
])
])

if __name__ == '__main__':
    app.run_server(debug=True)
