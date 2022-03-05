import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import requests
import json
from flask import Flask, request, jsonify

from server import server
# app = dash.Dash()
app = dash.Dash(name='dash_app', server=server, url_base_pathname='/')

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

app.layout = html.Div([get_inputs, get_output, post_inputs, post_output])

# GET
@app.callback(
         Output('predict_output', 'children'),
         [Input('pred_button', 'n_clicks')],
         [State('get_ncases', 'value'),
         State('get_dist', 'value')])
def get_request(pred_button, get_ncases, get_dist):
    if pred_button > 0:
        # url = "http://127.0.0.1:5000/linearregression"
        url = request.host_url+"/linearregression"
        header = {'Content-type':'application/json', 'Accept':'text/plain', 'api-key':'mypassword', 'ncases':str(get_ncases), 'distance':str(get_dist)}
        res = requests.get(url, headers=header)
    
        if res.ok:
            return "Prediction: {}".format(res.json()['deltime'])
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
    if append_button > 0:
        # url = "http://127.0.0.1:5000/adddata"
        url = request.host_url+"/adddata"
        data = {"deltime":post_deltime, "distance":post_dist, "ncases":post_ncases}
        res = requests.post(url,json=data)
    
        if res.ok:
            res_dict = json.loads(res.content.decode('utf-8'))
            return "Added New Data: {}".format(res_dict)
        else:
            return res


# if __name__ == '__main__':
#     app.run_server()
