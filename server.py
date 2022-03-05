import pandas as pd
import numpy as np
from flask import Flask, request, jsonify

server = Flask(__name__)

# app = Flask(__name__)
df = pd.read_csv("deliverytime.csv")

def predict_deltime(inp_ncases, inp_distance):
    
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    # from sklearn import metrics
    
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
        
        return jsonify(deltime_data), 201
    else:
        return jsonify({"error":"Request must be JSON"}), 415
   
# if __name__=='__main__':
#     app.run()
