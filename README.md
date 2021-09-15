[CURRENTLY WIP]

San Francisco Police Open Data Project
==============================

A project examining the incident report database from the DataSF data portal site. The data used for the project can be accessed here (https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783). More detailed information regarding the variables and structure of the dataset can be accessed here: https://support.datasf.org/help/police-department-incident-reports-2018-to-present-overview. 

Aims of Project
-------------------------------
In 2018, the San Francisco Police Department was sued by the Northern California ACLU regarding racial bias in policing by officers from 2013-2016. In the suit, the ACLU stated there was evidence of clear racial targeting of black and hispanic indivduals by officers.  
Following the suit and reaching a settlement with the ACLU, the department promised to address and prevent further racial disparities in policing by their officers. The aim of this project was to assess whether recent data regading police incident reports reflect the San Francisco Police Department's pledge towards more equitable policing. 
The project used the category/type of incident (violent vs non-violent crime) as the outcome of interest, using other characteristics listed in the data for each incident as predictors. In addition, lacking the personal characteristics of individuals involved in an incident, characteristics of the Supervisor District in which an incident occured are used as additional predictors.

Data Processing 
==============================

Police Incidents
--------------------------
Police Incident information was retrieved from the DataSF website. Data columns for each incident that were in non-numeric form (such as "analysis neighborhood" or "incident category") were re-encoded as being numeric values for usability purposes for the algorithm.
 
Supervisor District
---------------------

The data regarding socio-economic characteristics of each supervisor district can be found here: https://default.sfplanning.org/publications_reports/SF_NGBD_SocioEconomic_Profiles/2010-2014_ACS_Profile_SupeDistricts_v3AH.pdf

The different characteristics for each supervisor districts were normalized using Min-Max normalization to result in each only having values that ranged from 0-1 for uniformity.

For more information on the process, see the 3.0 & 4.0 notebooks.

The Model
==============================

Test Results
-------------------------------
After training, the model produced a 26.1% accuracy on the test data.