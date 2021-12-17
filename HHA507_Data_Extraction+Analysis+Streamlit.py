##Import needed packages

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time
import sweetviz
import pandas_profiling 
from pandas_profiling import ProfileReport


##Load the CSV files for analysis

df_hospital = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
df_inpatient = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
df_outpatient = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')

##Length for the 3 dataframes

print ('Hospital_Info:',len(df_hospital) )
##Hospital_Info: 5314 
print ('Inpatient_Info:',len(df_inpatient) )
##Inpatient_Info: 201876
print ('Outpatient_Info:',len(df_outpatient) )
##Outpatient_Info: 32532

##To generate a profile report of each dataframe
hospital_profile = ProfileReport(df_hospital, title = 'Pandas Profiling Report - Hospital Info')
hospital_profile

inpatient_profile = ProfileReport(df_inpatient, title = 'Pandas Profiling Report - Inpatient Info')
inpatient_profile

outpatient_profile = ProfileReport(df_outpatient, title = 'Pandas Profiling Report - Outpatient Info')
outpatient_profile

##Displaying each dataframes
list(df_hospital)
"""Each row represents a hospital with specific information relevant to the hospital"""
list(df_inpatient)
"""Each row represents specific drug code for different inpatient locations, 
including information such as averages for covered charges, total payments, and medicare payments"""
list(df_outpatient)
"""Each row represents a unique ambulatory payment classifications code (APC) for each hospital,
including information such as estimated charges and total payments."""

##Data cleaning of each dataframes
import janitor
from janitor import clean_names, remove_empty
##These clean the column names and removes any dupilicated rows.

##Cleaning of df_hospital
df_hospital_2 = pd.DataFrame.from_dict(df_hospital)
df_hospital_2 = clean_names(df_hospital)
df_hospital_2 = remove_empty(df_hospital)
##Check and confirm for null values
df_hospital_2.isnull().sum()
##Required columns don't have null values, doesn't require further cleaning
display(df_hospital_2)

##Cleaning of df_inpatient
df_inpatient_2 = pd.DataFrame.from_dict(df_inpatient)
df_inpatient_2 = clean_names(df_inpatient)
df_inpatient_2 = remove_empty(df_inpatient)
##Check and confirm for null values
df_inpatient_2.isnull().sum()

display(df_inpatient_2)

##Cleaning of df_outpatient
df_outpatient_2 = pd.DataFrame.from_dict(df_outpatient)
df_outpatient_2 = clean_names(df_outpatient)
df_outpatient_2 = remove_empty(df_outpatient)
##Check and confirm for null values
df_outpatient_2.isnull().sum()

display(df_outpatient_2)


##Merge datasets using provider_id
##Change provider_id to a string for easy merging
df_hospital_2['provider_id'] = df_hospital_2['provider_id'].astype(str)
df_inpatient_2['provider_id'] = df_inpatient_2['provider_id'].astype(str)
df_outpatient_2['provider_id'] = df_outpatient_2['provider_id'].astype(str)

##Merge the cleaned inpatient dataframe with cleaned hospital dtaframe
inpatient_hospital = df_inpatient_2.merge(df_hospital_2, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
inpatient_hospital.head()

##Merge the cleaned outpatient dataframe with cleaned hospital dtaframe
outpatient_hospital = df_outpatient_2.merge(df_hospital_2, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
outpatient_hospital.head()
outpatient_hospital.head()

##Generate a summary for Stony Brook Hospital
SBU_hospital = df_hospital_2[df_hospital_2['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
SBU_hospital
"""rovider_id = 330393
Hospital type = Acute Care Hospitals
hospital_ownership = Government - State
hospital_overall_rating = 4
mortality_national_comparison = Above national average
safety_of_care_national_comparison = Above national average
readmission_national_comparison = Below national average
patient_experience_national_comparison = Below national average
effectiveness_of_care_national_comparison = Same as national average
timeliness_of_care_national_comparison = Below national average
efficient_use_of_medical_imaging_national_comparison = Same as national average"""

SBU_inpatient_info = df_inpatient_2[df_inpatient_2['provider_id'] == '330393']
SBU_inpatient_info

SBU_outpatient_info = df_outpatient_2[df_outpatient_2['provider_id'] == '330393']
SBU_outpatient_info

##Save the cleaned dataframes for visualizations

##Create a dataframe unique for New York hospitals
NY_hospitals = df_hospital_2[df_hospital_2['state'] == 'NY']
##Set the index of the dtaframe to hospital name
NY_hospitals_2 = NY_hospitals.set_index('hospital_name')
##Check to confirm the change is completed
NY_hospitals_2.head()
##Exclude Stony Brook University Hospital for comparison by name
NY_hospitals_2 = NY_hospitals_2.drop('SUNY/STONY BROOK UNIVERSITY HOSPITAL')

"""Questions to answer:
1. How does Stony Brook Univeristy Hospital compare to the rest of New York in overall rating?
2. What is the most expensive inpatient DRGs code for Stony Brook University Hospital?
3. What is the most expensive outpatient APCs code for Stony Brook University Hospital?
4. Where are hospitals in New York located?
5. What is the frequency for hospital type across the nation?
6. Which state has the most hospitals?"""

##Streamlit section
##Import needed packages
import streamlit as st
import pandas as pd
import numpy as np
import time

##Load in the 3 primary csv files for display  
@st.cache
def load_hospitals():
   hospital_df = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/hospital_info.csv')
   return hospital_df
@st.cache
def load_inpatient():
    inpatient_df = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/inpatient_2015.csv')
    return inpatient_df
@st.cache
def load_outpatient():
    outpatient_df = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/outpatient_2015.csv')
    return outpatient_df

# FAKE LOADER BAR TO STIMULATE LOADING    
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)

st.title('HHA 507 - Final Assignment')
st.write('Shuwen Tan :sunglasses:') 
st.write('This app answers the following questions:')
st.write('1. How does Stony Brook Univeristy Hospital compare to the rest of New York in overall rating?')
st.write('2. What is the most expensive inpatient DRGs code for Stony Brook University Hospital?')
st.write('3. What is the most expensive outpatient APCs code for Stony Brook University Hospital?')
st.write('4. Where are hospitals in New York located?')
st.write('5. What is the frequency for hospital type across the nation?')
st.write('6. Which state has the most hospitals?')

##Load the datasets:     
hospital_df = load_hospitals()
inpatient_df = load_inpatient()
outpatient_df = load_outpatient()

##Preview the datasets
st.header('Hospital Data Preview')
st.dataframe(hospital_df)

st.header('Outpatient Data Preview')
st.dataframe(inpatient_df)

st.header('Inpatient Data Preview')
st.dataframe(outpatient_df)

##Create dataframe unique for Stony Brook University Hospital
SBU = hospital_df[hospital_df['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
st.header('Info for Stony Brook University Hospital')
st.markdown('This dataset shows information for Stony Brook University Hospital')
st.dataframe(SBU)

##Create dataframe unique for New York hospitals not including Stony Brook University Hospital
NY = hospital_df[hospital_df['state'] == 'NY']
st.header('Summary Info for Hospitals in New York')
st.markdown('This dataset shows hospitals located in New York, filtered out from the main hospital dataframe, excluding SBU hospital')
st.dataframe(NY)

##Answering question 1.
table1 = NY['hospital_overall_rating'].value_counts().reset_index()
st.header('Q1. How does Stony Brook Univeristy Hospital compare to the rest of New York in overall rating?')
st.subheader('Hospital rating for New York')
st.markdown('From this table, we can determine that most hospitals in New York has an overall rating of 1, with 5 representing the highest rating.')
st.markdown('To answer question 1, we know from the previous table that Stony Brook University Hospital has an overall rating of 4, thus Stony Brook University has a higher overall rating than most hospitals within New York. ')
st.dataframe(table1)

##Create dataframe unique for Stony Brook University Hospital Inpatient info for question 2
SBU_inpatient = inpatient_df[inpatient_df['provider_id']==330393]
st.header('Inpatient Data for Stony Brook')
st.markdown('This shows inpatient data for Stony Brook University Hospital, which is filtered from the main inpatient dataset')
st.dataframe(SBU_inpatient)

##Question 2. Most expensive inpatient DRGs for SBU
st.header('Q2. What is the most expensive inpatient DRGs code for Stony Brook University Hospital?')
st.subheader('Stony Brook Inpatient DRGs Pivot Table')
SBU_inpatient_DRGs_pivot = SBU_inpatient.pivot_table(index=['provider_id','provider_name','drg_definition'],values=['average_total_payments'])
SBU_inpatient_DRGs_desc = SBU_inpatient_DRGs_pivot.sort_values(['average_total_payments'], ascending=False)
st.markdown('DRGs is diagnostic related group, which is a classification system that stanrdardizes prospective payment to hospitals')
st.markdown('With information listed on this table, we can determine that the most expensive inpatient DRGs code for Stony Brook Univeristy Hospital is 003, with an average total payments of $21,667.00')
st.markdown('003 - ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R.')
st.dataframe(SBU_inpatient_DRGs_desc)

##Create dataframe unique for Stony Brook University Hospital Outpatient info for question 3
SBU_outpatient = outpatient_df[outpatient_df['provider_id']==330393]
st.header('Outpatient Data for Stony Brook')
st.markdown('This shows outpatient data for Stony Brook University Hospital, which is filtered from the main inpatient dataset')
st.dataframe(SBU_outpatient)

##Question 3. Most expensive inpatient APCs for SBU
st.header('Q3. What is the most expensive inpatient APCs code for Stony Brook University Hospital?')
st.subheader('Stony Brook Inpatient APCs Pivot Table')
SBU_outpatient_DRGs_pivot = SBU_outpatient.pivot_table(index=['provider_id','provider_name','apc'],values=['average_total_payments'])
SBU_outpatient_DRGs_desc = SBU_outpatient_DRGs_pivot.sort_values(['average_total_payments'], ascending=False)
st.markdown('APCs is ambulatory payment classsifications, a classification system for outpatient services')
st.markdown('With information listed on this table, we can determine that the most expensive outpatient APCs code for Stony Brook Univeristy Hospital is 0074, with an average total payments of $2,307.21')
st.markdown('0074 - Level IV Endoscopy Upper Airway')
st.dataframe(SBU_outpatient_DRGs_desc)

##Question 4. Map for NY hospitals
st.header('Q4. Where are hospitals in New York located?')
st.subheader('Map of New York Hospitals')
ny_locations = NY['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
ny_locations['lon'] = ny_locations['lon'].str.strip('(')
ny_locations = ny_locations.dropna()
ny_locations['lon'] = pd.to_numeric(ny_locations['lon'])
ny_locations['lat'] = pd.to_numeric(ny_locations['lat'])

st.map(ny_locations)

##Question 5. Bar chart for hospital type in the U.S
st.header('Q5. What is the frequency for hospital types across the nation?')
st.subheader('Hospital Types - United States')
bar1 = hospital_df['hospital_type'].value_counts().reset_index()
st.bar_chart(data=bar1, width=0, height=0, use_container_width=True)
st.markdown('The majority of hospitals in the United States are acute care, followed by critical access')

##Question 6. Bar chart for number of hospitals by state
st.header('6. Which state has the most hospitals?')
st.subheader('Number of Hospitals for each State')
bar2 = hospital_df['state'].value_counts().reset_index()
st.bar_chart(data=bar2, width=0, height=0, use_container_width=True)
st.markdown('Texas has 449 hospitals, which makes it the state with the most hospitals, followed by California')

st.title('Thank you for stopping by!')

##Link for streamlit:
##https://share.streamlit.io/shuwentan321/hha507_streamlit/main/HHA507_Streamlit.py