import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

import plotly.express as px
import dash_table as dt
import plotly.offline as pyo

import requests
import json
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

styleHead = {
            'textAlign': 'left',
            'color': '#007bff',
            'fontSize':20, 
            'font-family':'calibri'
            }
styleButton = {
            'background-color': '#007bff',
            'color': 'white',
            'height': '40px',
            'width': '120px',
            # 'margin-top': '50px',
            'margin-left': '100px',
            'borderRadius':5,
            # 'border': '2px #007bff solid',
            'font-family':'calibri',
            'font-weight': 'bold',
            'fontSize':16, 
            }

get_inputs = html.Div([
            html.H1(
                    children='Delivery Time Linear Regression Model',
                    style = styleHead
                    ),
            html.Table([
                    html.Tr([
                            html.Td("Number of Cases: "),
                            html.Td(dcc.Input(
                                            id="get_ncases",
                                            type="number",
                                            value = 10))
                            ]),
                    html.Tr([
                            html.Td("Distance: "),
                            html.Td(dcc.Input(
                                            id="get_dist",
                                            type="number",
                                            value = 300))
                            ]),
                    ]),
            html.Div([
                    html.Button("Predict", 
                                id="pred_button", 
                                n_clicks=0,
                                style = styleButton
                                )
                    ],
                )
            ] 
        )

get_output = html.Div([
    html.Div("Prediction: ", id='predict_output')
    ])

post_inputs = html.Div([
            html.Hr(),
            html.H1(
                    children='Append New Data in Dataset',
                    style = styleHead
                    ),
            html.Table([
                    html.Tr([
                            html.Td("Delivery Time: "),
                            html.Td(dcc.Input(
                                            id="post_deltime",
                                            type="number",
                                            value = 22.5))
                            ]),
                    html.Tr([
                            html.Td("Number of Cases: "),
                            html.Td(dcc.Input(
                                            id="post_ncases",
                                            type="number",
                                            value = 10))
                            ]),
                    html.Tr([
                            html.Td("Distance: "),
                            html.Td(dcc.Input(
                                            id="post_dist",
                                            type="number",
                                            value = 300))
                            ])
                    ]),
            html.Div([
                    html.Button("Append", 
                                id="append_button", 
                                n_clicks=0,
                                style = styleButton
                                )
                    ],
                )
            ] 
        )
post_output = html.Div([
    html.Div(id='append_output')
    ])

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/'
)
app.layout = html.Div([get_inputs, get_output, post_inputs, post_output])
app.title = 'Linear Regression Model'

# GET
@app.callback(
         Output('predict_output', 'children'),
         [Input('pred_button', 'n_clicks')],
         [State('get_ncases', 'value'),
         State('get_dist', 'value')])
def get_request(pred_button, get_ncases, get_dist):
    if pred_button!=0:
        url = request.host_url+"/linearregression"
        header = {'Content-type':'application/json', 'Accept':'text/plain', 'api-key':'mypassword', 'ncases':str(get_ncases), 'distance':str(get_dist)}
        res = requests.get(url, headers=header)
    
        if res.ok:
            return "Prediction: {}".format(res.json())
        else:
            return res

# POST
@app.callback(
         Output('append_output', 'children'),
         [Input('append_button', 'n_clicks')],
         [State('post_deltime', 'value'),
         State('post_ncases', 'value'),
         State('post_dist', 'value')])
def post_request(append_button, post_deltime, post_ncases, post_dist):
    if append_button!=0:
        url = request.host_url+"/adddata"
        data = {"deltime":post_deltime, "ncases":post_ncases, "distance":post_dist}
        res = requests.post(url,json=data)
    
        if res.ok:
            return "Prediction: {}".format(res.content)
        else:
            return res

df = pd.read_csv("deliverytime.csv")

def predict_deltime(inp_ncases, inp_distance):
    
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn import metrics
    
    #Specify Training and Test Data and Response and Predictors
    X = df.drop(['deltime'], axis=1)
    y = df['deltime']
    X_train, X_test , y_train , y_test = train_test_split (X, y, test_size = 0.2)

    #Learn the Coefficients
    regressor = LinearRegression()
    regressor.fit(X_train , y_train)
    
    return regressor.predict(np.array([[inp_ncases,inp_distance]]))


@server.get("/linearregression")
def get_model():
    headers = request.headers
    auth = headers.get("api-key")
    input_ncases = headers.get("ncases")
    input_distance = headers.get("distance")
    
    print(df)
    
    try:
        f_ncases = float(input_ncases)
        f_distance = float(input_distance)
    except:
        return jsonify({"message":"ERROR: Wrong Input Type"}), 404
    if auth == 'mypassword':
        pred = predict_deltime(f_ncases, f_distance)
        return jsonify(deltime=pred[0]), 200
    else:
        return jsonify({"message":"ERROR: Unauthorized"}), 401
    
@server.post("/adddata")
def add_data():
    if request.is_json:
        deltime_data = request.get_json()
        
        global df, post_flag
        
        df_dict = df.to_dict('records')
        
        df_dict.append(deltime_data)
        print(df_dict)
        
        df = pd.DataFrame.from_dict(df_dict, orient='columns')
        
        return deltime_data, 201
    return {"error":"Request must be JSON"}, 415


if __name__ == '__main__':
    app.run_server()


