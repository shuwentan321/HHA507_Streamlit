# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 19:04:15 2021

@author: ikima
"""

##Streamlit section
## Load in the 3 primary csv files for display  
@st.cache
def load_hospitals():
   hospital_df = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/hospital_info.csv')
   return hospital_df
@st.cache
def load_inatpatient():
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
st.write('This answers the following questions:')
st.write('1. How does Stony Brook Univeristy Hospital compare to the rest of New York in overall rating?')
st.write('2. What is the most expensive inpatient DRGs code for Stony Brook University Hospital?')
st.write('3. What is the most expensive outpatient APCs code for Stony Brook University Hospital?')
st.write('4. ')
st.write('5. ')
st.write('6. ')

##Load the datasets:     
hospital_df = load_hospitals()
inpatient_df = load_inatpatient()
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
st.header('This dataset shows information for Stony Brook University Hospital')
##Merge datasets 
hospital_df['provider_id'] = hospital_df['provider_id'].astype(str)
inpatient_df['provider_id'] = inpatient_df['provider_id'].astype(str)
outpatient_df['provider_id'] = outpatient_df['provider_id'].astype(str)