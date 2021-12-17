##Import needed packages
import streamlit as st
import pandas as pd
import numpy as np
import time

##Streamlit section
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