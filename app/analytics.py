
import numpy as np
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import time
import datetime
import logging
import sys
from flask import Flask
logging.basicConfig(stream= sys.stdout, level=logging.INFO)



# while(True):
    
try:

    logging.info("Doing Analytics")

    data = pd.read_csv('app/events.txt', delimiter = '\n', header = None)

    data.rename(columns = {0:'Y'}, inplace = True) 
    X_train = np.arange(1,len(data)+1).reshape(-1, 1)
    Y_train = data['Y'].values.reshape(-1, 1)

    regressor = LinearRegression() 
    #training the algorithm
    regressor.fit(X_train, Y_train) 

    X_test = [[len(data)+1]]
    y_pred = regressor.predict(X_test)
    ts = datetime.datetime.now().timestamp()
    os.chdir("../app")
    f = open("results.txt","a+")
    f.write(str(ts))
    f.write(" ")
    f.write(str(y_pred))
    f.write("\n")
    f.close() 

    logging.info(y_pred)

except: 
    
    logging.info("No data recieved yet")

