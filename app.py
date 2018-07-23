import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import cleaningData as data

app = dash.Dash()
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

#Loading Poverty Data
povertyData = pd.read_csv('Datasets/1_povertyData.csv', low_memory=False)
nvm_p = ['race_eth_code', 'county_fips','geotype', 'geotypevalue', 'geoname','region_name','region_code','TotalPop','NumPov','LL_95CI_percent', 'UL_95CI_percent', 'percent_SE', 'percent_RSE',
       'place_decile', 'CA_RR','ConcentratedCT']

df_p = data.p_extractUsefulInfo("Poverty ", povertyData, nvm_p)
county_options = df_p['county_name'].unique()


#Loading Unemployment Data
unemploymentData = pd.read_csv('Datasets/4_unemploymentData.csv', low_memory=False)
ump_nvm = ['ind_id', 'ind_definition', 'race_eth_code','geotype', 'geotypevalue', 'geoname','county_fips', 'region_code', 'region_name', 'll_95ci',
       'ul_95ci', 'se', 'rse', 'ca_decile', 'ca_rr', 'version']

df_u = data.u_extractUsefulInfo("Unemployment ", unemploymentData, ump_nvm)


### Visual Layout
tab1_layout = html.Div([
    html.H4(children='Poverty Trends'),
    html.Div(
        html.Div(id = "poverty-graph"),
        style={'width': '80%', 'float': 'right'}
        )                      
    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': '2%',
        'margin-right': '2%',
    })
tab2_layout = html.Div([
    html.H4(children='Unemployment Trends'),
    html.Div(
        html.Div(id = "unemployment-graph"),
        style={'width': '80%', 'float': 'right'}
        )                      
    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': '2%',
        'margin-right': '2%',
    })


app.layout = html.Div([
    html.H1(children='SDOH - CA Health Impact Assessment'),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='county-value',
                options=[{'label': i, 'value': i} for i in county_options],
                value='Los Angeles'
            )
        ],
        style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),
    html.Div(
        dcc.Tabs(
            tabs=[
            {'label': 'Poverty > 40%', 'value': 1},
            {'label': 'Unemployment', 'value': 2},
            #{'label': 'Food Affordability', 'value': 3},
            #{'label': 'Education', 'value': 4},
            ],
            value=1,
            id='tabs',
            vertical=True,
            style={
                'height': '100vh',
                'borderRight': 'thin lightgrey solid',
                'textAlign': 'left'
            }
        ),
        style={'width': '20%', 'float': 'left'}
    ),
    html.Div(
        html.Div(id='tab-layout'),
        style={'width': '80%', 'float': 'right'}
    )
], style={
    'fontFamily': 'Sans-Serif',
    'margin-left': '2%',
    'margin-right': '2%',
})



#switching between tabs
@app.callback(Output('tab-layout', 'children'),[Input('tabs', 'value')])
def call_tab_layout(tab_value):
    if tab_value == 1:
        return tab1_layout
    elif tab_value == 2:
        return tab2_layout
    else:
        html.Div()



## Poverty
@app.callback(Output('poverty-graph', 'children'), [Input('county-value', 'value')])
def display_tab1Content(countyVal):
    year = ['2000', '2006-2010', '2005-2007', '2008-2010']

    df_all = df_p[(df_p['percent'] > 40)]
    s = df_all.groupby(['reportyear','county_name']).size()

    total_xId = []
    total_xLabel = list(df_all['reportyear'].unique())
    for i in total_xLabel:
        total_xId.append(year.index(i))
    total_yVals = [0,0,0,0]
    small_xId = []
    small_xLabel = []
    small_yVals = []
    for i, v in s.items():
        if i[1] == countyVal:
            small_xId.append(year.index(i[0]))
            small_xLabel.append(i[0])
            small_yVals.append(v)
        for j in year:
            if i [0] == j:
                idd = year.index(j)
                total_yVals[idd] = total_yVals[idd] + v

    print("For {} county = {} & {}".format(countyVal, total_xLabel, small_xLabel))

    data = [
        {
            'x': total_xId,
            'y': total_yVals,
            'name': 'Rest of world',
            'marker': {
                'color': 'rgb(55, 83, 109)'
            },
            'type': 'bar'
        },
        {
            'x': small_xId,
            'y': small_yVals,
            'name': countyVal,
            'marker': {
                'color': 'rgb(26, 118, 255)'
            },
            'type': 'bar'
        }
    ]

    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                    'margin': {
                        'l': 30,
                        'r': 0,
                        'b': 30,
                        't': 0
                    },
                    'legend': {'x': 0, 'y': 1},
                    'xaxis': dict(tickvals = total_xId, ticktext = total_xLabel, title='Year',showticklabels = True,)
                }
            }
        ),
        html.Div(' ')
    ],style={'width': '90%', 'margin-left': '2%'})

## Unemployment
@app.callback(Output('unemployment-graph', 'children'), [Input('county-value', 'value')])
def display_tab1Content(countyVal):
    year = ['Total', 'American Indian or Alaska Native', 'Black or African American', 'Asian', 'Hispanic or Latino', 'Multiple',
            'Native Hawaiian or Other Pacific Islander', 'Other', 'White']

    df_all = df_u[(df_u['Unemployment_rate'] > 20)]
    s = df_all.groupby(['race_eth_name','county_name']).size()

    total_xId = []
    total_xLabel = list(df_all['race_eth_name'].unique())
    for i in total_xLabel:
        total_xId.append(year.index(i))
    total_yVals = [0,0,0,0,0,0,0,0,0]
    small_xId = []
    small_xLabel = []
    small_yVals = []
    for i, v in s.items():
        if i[1] == countyVal:
            small_xId.append(year.index(i[0]))
            small_xLabel.append(i[0])
            small_yVals.append(v)
        for j in year:
            if i [0] == j:
                idd = year.index(j)
                total_yVals[idd] = total_yVals[idd] + v

    print("For {} county = {} & {}".format(countyVal, total_xLabel, small_xLabel))

    data = [
        {
            'x': total_xId,
            'y': total_yVals,
            'name': 'Rest of world',
            'marker': {
                'color': 'rgb(55, 83, 109)'
            },
            'type': 'bar'
        },
        {
            'x': small_xId,
            'y': small_yVals,
            'name': countyVal,
            'marker': {
                'color': 'rgb(26, 118, 255)'
            },
            'type': 'scatter'
        }
    ]

    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,
                'layout': {
                    'margin': {
                        'l': 30,
                        'r': 0,
                        'b': 30,
                        't': 0
                    },
                    'legend': {'x': 0, 'y': 1},
                    'xaxis': dict(tickvals = total_xId, ticktext = total_xLabel, title='Ethnicity',showticklabels = True,)
                }
            }
        ),
        html.Div(' ')
    ],style={'width': '90%', 'margin-left': '2%'})


if __name__ == '__main__':
    app.run_server(debug=True)
