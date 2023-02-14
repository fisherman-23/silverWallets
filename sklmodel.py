#scikitlearn model
#!/usr/bin/env python
# coding: utf-8

# In[1]:

import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor as RFR
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# In[22]:


#Summing total expenditure for the day:
def predict_spending(totalArr):
    date_sum = []
    indiv_sum = 0
    for x in range(-2, len(totalArr)-1):
        if totalArr[x][0] == totalArr[x+1][0]:
            indiv_sum += float(totalArr[x][2])
        else:
            indiv_sum += float(totalArr[x][2])
            date_sum.append([totalArr[x][0],totalArr[x][1],indiv_sum])
            indiv_sum = 0 
    date_sum.append(date_sum[0])
    date_sum.pop(0)


    #Creation of DataFrame:
    df = pd.DataFrame(date_sum, columns = ['Date', 'Day', 'Amount'])



    #Data Augmentation:
    def add_noise(data, sigma= 20):
        noise = np.random.normal(0, sigma, data.shape)
        noisy_data = data + noise
        return noisy_data

    augment = pd.DataFrame(date_sum, columns = ['Date', 'Day', 'Amount'])
    augment['Amount'] = add_noise(df['Amount'])
    df = pd.concat([df, augment])
    df['Amount'].clip(lower=0, inplace=True)
    df['Amount'] = df['Amount'].clip(lower=0)


    #Declaring x and y variables:
    X = np.array([df['Day']]).reshape(-1, 1)
    y = df['Amount'].tolist()

    #Train Test Split:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    #Linear Regression
    linear_reg = LinearRegression()
    linear_reg.fit(X_train,y_train)
    predictions = linear_reg.predict(X_test)
    linear_reg_rmse = np.sqrt(metrics.mean_squared_error(y_test, predictions))

    #Support Vector Regression
    svr = SVR(kernel='rbf')
    svr.fit(X_train,y_train)
    predictions = svr.predict(X_test)
    svr_rmse = np.sqrt(metrics.mean_squared_error(y_test, predictions))

    #Random Forest Regression
    rfr = RFR(max_depth = 3)
    rfr.fit(X_train,y_train)
    predictions = rfr.predict(X_test)
    rfr_rmse = np.sqrt(metrics.mean_squared_error(y_test, predictions))


    # In[23]:

    #Rolling Date Feature:
    current_day = datetime.datetime.now().weekday()
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
    days_of_week = days_of_week[current_day:] + days_of_week[:current_day]
    days_dict = {'Mon' : 0, 'Tue' : 1, 'Wed' : 2, 'Thurs' : 3, 'Fri': 4, 'Sat' : 5, 'Sun' : 6}
    days_num = [[days_dict[days_of_week[0]]],[days_dict[days_of_week[1]]],[days_dict[days_of_week[2]]],[days_dict[days_of_week[3]]], [days_dict[days_of_week[4]]], [days_dict[days_of_week[5]]], [days_dict[days_of_week[6]]]]
    #Comparing the best RMSE:
    if rfr_rmse < linear_reg_rmse and rfr_rmse < svr_rmse:
        predictions = rfr.predict(days_num)
    elif svr_rmse < rfr_rmse and svr_rmse < linear_reg_rmse:
        predictions = svr.predict(days_num)
    elif linear_reg_rmse < rfr_rmse and linear_reg_rmse < svr_rmse:
        predictions = linear_reg.predict(days_num)
    else:
        predictions = rfr.predict(days_num)
    return(predictions,days_of_week)
    # In[ ]: