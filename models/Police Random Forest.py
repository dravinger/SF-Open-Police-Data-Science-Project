# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 13:32:50 2021

@author: DeAndre
"""

import pandas as pd
from sodapy import Socrata
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
client = Socrata("data.sfgov.org", "6MxY0IBE0i8PhcQtqMYKjKm7g")
results = client.get("wg3w-h783", limit=500000)
results_df = pd.DataFrame.from_records(results)
Supervisor_Districts_info_df = pd.read_excel('C:/Users/DeAndre/Documents/GitHub/SFPD-Police-Data-Project/data/interim/Supervisor Districts Dataframe for processing.xlsx')
scaler = MinMaxScaler()
scaled = scaler.fit_transform(Supervisor_Districts_info_df)
scaled_df = pd.DataFrame(scaled, columns = ['supervisor_district', 'Total Population', 'Group Quarter Population', 'Male Population','Female Population',
 'Households', 'Family Households', 'Non-Family Households',' Single Person Households', 'Households with Children',
 'Households with 60 years and older', 'Average Household Size', 'Average Family Houeshold Size',
 'Asian', 'Black/African American', 'White', 'Native American Indian', 'Native Hawaiian/Pacific Islander', 'Other/Two or More Races', '% Latino (of Any Race)',
 'Age: 0-4 years', 'Age: 5-17 years', 'Age: 18-34 years', 'Age: 35-59 years', 'Age: 60 and older', 'Median Age', 'Foreign Born',
 'Educational Attainment: High School or less', 'Educational Attainment: Some College/Associate Degree', 'Educational Attainment: College Degree', 'Educational Attainment: Graduate/Professional Degree',
' Language Spoken at Home: English Only',' Language Spoken at Home: Spanish Only', 'Language Spoken at Home: Asian/Pacific Islander Only',
 'Language Spoken at Home: Other European Language', 'Language Spoken at Home: Other Languages', 'Lingusitic Isolation: % of All Houesholds', 'Lingusitic Isolation: % of Spanish Speaking Houesholds',
 'Lingusitic Isolation: % of Asian Language Speaking Houesholds','Lingusitic Isolation: % of Other European Speaking Houesholds', 'Lingusitic Isolation: % of Houesholds Speaking Other Languages',
 'Total Number of Units', 'Median Year Structure Built', 'Occupied Units: Owner occupied',' Occupied Units: Renter Occupied', 'Vacant Units',
 'For Rent', 'For sale only', 'Rented or sold', 'not occupied',' For seasonal, recreaction, or occasional use', 'Other Vacant',
 'Median Year Moved in to Unit (Own)', 'Median Year Moved in to Unit (Rent)', 'Percent in Same House Last Year', 'Percent Abroad Last Year',
 'Single Family Housing'',2-4 Units',' 5-9 Units',' 10-19 Units',' 20 Units or more', 'Other',' No Bedrooms', '1 Bedroom', '2 Bedrooms',' 3-4 Bedrooms',' 5+ Bedrooms',
' Median Rent',' Median Contract Rent','Median Rent as % of Household Income', 'Median Home Value', 'Vehicles Available',' Homeowners', 'Renters',' Vehicles per Capita', 'Households with no vehicle',
 'Households with no vehicle: Percent of Homeowning households', 'Households with no vehicle: Percent of Renting Households', 'Median Household Income', 'Median Family Income',
 'Per Capita Income', 'Percent in Poverty', 'Unemployment Rate', 'Unemployment Rate: Percent Female', 'Unemployment Rate: Percent Male', 'Employed Residents',
 'Employed Residents: Managerial Professional', 'Employed Residents: Services', 'Employed Residents: Sales and Office', 'Employed Residents: Natural Resources',
 'Employed Residents: Production Transport Materials',' Workers 16 Years and Older', 'Journey to Work: Car', 'Journey to Work: Car - Drove Alone', 'Journey to Work: Car - Carpooled',
 'Journey to Work: Transit','Journey to Work: Bike','Journey to Work: Walk', 'Journey to Work: Other','Journey to Work: Worked at Home', 'Population Density per Acre' ])
scaled_df.supervisor_district = ('1','2','3','4','5','6','7','8','9','10','11')
Joined_Dataframe_df = results_df.set_index('supervisor_district').join(scaled_df.set_index('supervisor_district'))
X = Joined_Dataframe_df.drop(Joined_Dataframe_df.columns[[0, 1, 5, 6, 7, 8, 10, 11, 12, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]], axis=1)
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
X_category = [
    'incident_time',
    'incident_year',
    'incident_day_of_week',
    'incident_category',
    'report_type_code',
    'police_district',
    'analysis_neighborhood',
]

for col in X_category:
    X[col] = le.fit_transform(X[col].astype("str"))
    
X_new = X.dropna(axis = 0, how = 'any')
Y= X_new['incident_category']
X_rnd = X_new.drop('incident_category', axis = 1)
from sklearn.ensemble import RandomForestClassifier
rnd_clf = RandomForestClassifier(n_estimators = 100, verbose = 1)
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
x_train, x_test, y_train, y_test = train_test_split(X_rnd, Y, test_size = 300000, random_state = 3)
model = rnd_clf.fit(x_train, y_train)
yhat = rnd_clf.predict(x_test)
acc = accuracy_score(y_test, yhat)
print('Accuracy: %.3f' % acc)


model.feature_importances_
important_features = np.sort(model.feature_importances_)[:15]
sorted_idx = important_features.argsort()
plt.barh(X_rnd.columns.values[sorted_idx], important_features[sorted_idx])
plt.xlabel("Random Forest Feature Importance")


import time
from sklearn.inspection import permutation_importance
start_time = time.time()
result = permutation_importance(
    model, x_test, y_test, n_repeats=10, random_state=42, n_jobs=1)
elapsed_time = time.time() - start_time
print(f"Elapsed time to compute the importances: "
      f"{elapsed_time:.3f} seconds")


important_permeutation_features_mean = np.sort(result['importances_mean'])[:20]
important_permeutation_features_std = np.sort(result['importances_mean'])[:20]
important_permeutation_features_importances = np.sort(result['importances'])[:20]
sorted_idx = important_permeutation_features_mean.argsort()
plt.barh(X_rnd.columns.values[sorted_idx], important_permeutation_features_mean[sorted_idx])
plt.xlabel("Random Forest Permutation Feature Importance")
plt.ylabel("Random Forest Features")
plt.show()
plt.savefig('Permutation Feature Importance')