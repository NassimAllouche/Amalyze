import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def predict_qty(Fulfilment, fulfilled_by, ship_service_level, Courier_Status, Category):
    # Load the data from the CSV file
    dataamazon = pd.read_csv("C:/Users/nassim/Desktop/pi/material-dashboard-django/apps/quantityprediction/Amazon Sale Report.csv", delimiter=";")
    
    # Encode the categorical variables
    le = LabelEncoder()
    dataamazon['Fulfilment'] = le.fit_transform(dataamazon['Fulfilment'])
    dataamazon['fulfilled-by'] = le.fit_transform(dataamazon['fulfilled-by'])
    dataamazon['ship-service-level'] = le.fit_transform(dataamazon['ship-service-level'])
    dataamazon['Courier Status'] = le.fit_transform(dataamazon['Courier Status'])
    dataamazon['Category'] = le.fit_transform(dataamazon['Category'])
    
    # Split the data into features (X) and target variable (y)
    X = dataamazon[['Fulfilment', 'ship-service-level', 'Category', 'Qty', 'Amount', 'fulfilled-by']]
    y = dataamazon["Qty"].values
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Create and fit the Random Forest Classifier model
    rf = RandomForestClassifier(n_estimators=100, random_state=0)
    rf.fit(X_train, y_train)
    
    # Create a new data point using the provided parameters
    new_data = pd.DataFrame([[Fulfilment, ship_service_level, Category, 0, 0, fulfilled_by]],
                            columns=['Fulfilment', 'ship-service-level', 'Category', 'Qty', 'Amount', 'fulfilled-by'])
    
    # Predict the Qty for the new data point
    qty_pred = rf.predict(new_data)
    
    return qty_pred.tolist()