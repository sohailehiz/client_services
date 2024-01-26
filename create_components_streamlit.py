import streamlit as st
from datetime import datetime
import access_mongodb as amdb
import pandas as pd
import calendar
import time

mydate = datetime.now()
current_date = mydate.date()
current_month = datetime.now().month
current_month_name = mydate.strftime("%B")
current_year = datetime.now().year
st.set_page_config(page_title="Service History")

def normalize_json(param_json_data):
    df = pd.json_normalize(param_json_data)
    return df

def sum_group_by_dataframe(param_df,param_groupby,param_sum):
    '''
    param_df: dataframe
    param_sum: List
    param_groupby: List
    '''
    if len(param_groupby) > 0 and len(param_sum) > 0:
        sum_dict = {}
        for col in param_sum:
            sum_dict[col] = 'sum'
        df = param_df.groupby(param_groupby).agg(sum_dict).reset_index()
        return df
    else:
        return None

st.header(str(current_year),divider="green")
st.subheader(current_month_name,divider="grey")
data = {}

with st.expander("Client Service Inputs"):
    with st.form("Input Service Data",clear_on_submit=True, border=True):
        client_name = st.text_input("Enter Client Name")
        plot_calendar = st.date_input("Select Date of Event", datetime.now())
        event_date = plot_calendar
        amount_collected = st.number_input('Total Amount Received',value=0, placeholder="Enter Amount...")
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        
        
        if submitted:
            data['client_name'] = client_name
            data['event_date'] = event_date.strftime('%Y-%m-%d')
            data['year'] = event_date.year
            data['month'] = event_date.strftime("%B")
            data['amount'] = amount_collected
            if data['client_name'] != "" and data['amount'] > 0 and event_date <= current_date:
                msg = st.json(data)
                amdb.create_collection_if_not_exists(amdb.set_client,"client_services","year_"+str(current_year))
                amdb.insert_data_into_collection(amdb.set_client,"client_services","year_"+str(current_year),data)
                time.sleep(5)
                msg.empty()
            else:
                st.warning("*Client Name can't be empty")
                st.warning("*Amount can't be Zero (0)")
                st.warning("*No future Dates")
col1, col2 = st.columns(2)
with col1:
    with st.expander("Monthly Report"):
        # Get list of month names
        months = [calendar.month_name[i] for i in range(1, 13)]
        # Create a selectbox to select the month
        selected_month = st.selectbox("Select a month:", months)
        get_data = normalize_json(amdb.get_data_from_collection(amdb.set_client,"client_services","year_"+str(current_year),{'month':selected_month}))
        selected_month_columns = ["event_date","client_name", "amount"]
        selected_month_df = get_data[selected_month_columns]
        st.dataframe(selected_month_df)
with col2:
    with st.expander("YTD Report"):
        selected_year = st.selectbox("Current:", [current_year])   
        get_data = normalize_json(amdb.get_data_from_collection(amdb.set_client,"client_services","year_"+str(current_year)))
        sum_ytd = sum_group_by_dataframe(get_data,['client_name','month'],['amount'])
        st.table(sum_ytd)

