from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from sklearn import svm
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
def predict_fulfilled_by(categ, courierstatus, amount, qty):
    encoder = OrdinalEncoder()

    # Load the dataset
    d = pd.read_csv('C:/Users/nassim/Desktop/pi/material-dashboard-django/apps/shippingmethod/Amazon Sale Report 3 (1).csv', delimiter=';')

    # Encode categorical variables
    fulfil = encoder.fit_transform(d[['Fulfilment']])
    shipservicelevel = encoder.fit_transform(d[['ship-service-level']])
    categ_enc = encoder.fit_transform(d[['Category']])
    courierstatus_enc = encoder.fit_transform(d[['Courier Status']])
    fulfilledby_enc = encoder.fit_transform(d[['fulfilled-by']])

    # Prepare the feature matrix
    a = d.drop(['Fulfilment', 'Courier Status', 'fulfilled-by', 'ship-service-level'], axis=1)
    a['categ'] = categ_enc
    a['fulfil'] = fulfil
    a['courierstatus'] = courierstatus_enc
    shipservicelevel = encoder.fit_transform(d[['ship-service-level']])
    b = a.iloc[:, 2:7]
    c = b.iloc[0:12000, :]
    features_df = c[['categ', 'Qty', 'Amount', 'courierstatus']]
    A = np.asarray(features_df)

    # Prepare the target variable
    B = np.asarray(c['fulfil'])

    # Split the data into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(A, B, test_size=0.3)

    # Perform undersampling on the training set
    rus = RandomUnderSampler(random_state=42)
    X_train_resampled, Y_train_resampled = rus.fit_resample(X_train, Y_train)

    # Train the SVM classifier
    classifier = svm.SVC(kernel='rbf', C=1, gamma=0.1, random_state=0)
    classifier.fit(X_train_resampled, Y_train_resampled)

    # Prepare the input data for prediction
    input_data = np.array([[categ, qty, amount, courierstatus]])

    # Make the prediction
    prediction = classifier.predict(input_data)

    return prediction.tolist()

