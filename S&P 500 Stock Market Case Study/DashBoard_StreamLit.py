# To run the Local host use streamlit run project_name.py
import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


company_list = [  
 r'C:\\Users\\Neeraj\\Desktop\\Project\\S&P 500 Stock Market Case Study\\DataSet\\individual_stocks_5yr\\AAPL_data.csv',
 r'C:\\Users\\Neeraj\\Desktop\\Project\\S&P 500 Stock Market Case Study\\DataSet\\individual_stocks_5yr\\AMZN_data.csv',
 r'C:\\Users\\Neeraj\\Desktop\\Project\\S&P 500 Stock Market Case Study\\DataSet\\individual_stocks_5yr\\GOOG_data.csv',
 r'C:\\Users\\Neeraj\\Desktop\\Project\\S&P 500 Stock Market Case Study\\DataSet\\individual_stocks_5yr\\MSFT_data.csv',
]

all_data = pd.DataFrame()

for file in company_list:
    current_df = pd.read_csv(file)
    all_data = pd.concat([current_df, all_data], ignore_index=True)

all_data['date'] = pd.to_datetime(all_data['date'])

st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
st.title("Tech Stock Analysis Dashboard")

tech_list = all_data['Name'].unique()
st.sidebar.title("Coose a Company")

selected_company = st.sidebar.selectbox("Select a Stock", tech_list)

company_df = all_data[all_data['Name'] == selected_company]
company_df.sort_values('date', inplace=True)

# 1st Plot:
st.subheader(f"1. Closing Price of {selected_company} Over Time")
fig1 = px.line(company_df, x="date", y="close", title = selected_company + 'closing price over time')
st.plotly_chart(fig1, use_container_width=True)


# 2nd Plot
st.subheader("2. Moving Average (10, 20, 50 days)")

ma_day = [10,20,50]

for ma in ma_day:
    company_df['close_'+str(ma)] = company_df['close'].rolling(ma).mean()

fig2 = px.line(company_df, x="date", y=["close", "close_10", "close_20", "close_50"], title = selected_company + 'closing price with moving average')
st.plotly_chart(fig2, use_container_width=True)


# 3rd Plot
st.subheader("3. Daily Returns for " + selected_company)
company_df['Daily return(in %)'] = company_df['close'].pct_change()*100

fig3 = px.line(company_df, x="date", y="Daily return(in %)", title = 'Daily Return(%)')
st.plotly_chart(fig3, use_container_width=True)


# 4th Plot
st.subheader("4. Resampled CLosing Price (Monthly / Quarterly / Yearly)")
company_df.set_index('date', inplace=True)
Resample_option = st.radio("Select Resample Frequency", ['Monthly', 'Quarterly', 'Yearly'])

if(Resample_option == 'Monthly'):
    resampled = company_df['close'].resample('ME').mean()
elif(Resample_option == 'Quarterly'):
    resampled = company_df['close'].resample('QE').mean()
else:
    resampled = company_df['close'].resample('YE').mean()

fig4 = px.line(resampled, title = selected_company + " " + Resample_option + "Average Closing Price")
st.plotly_chart(fig4, use_container_width=True)


# 5th Plot
closing_price = pd.DataFrame()

closing_price['apple_close'] = pd.read_csv(company_list[0])['close']
closing_price['amzn_close'] = pd.read_csv(company_list[1])['close']
closing_price['goog_close'] = pd.read_csv(company_list[2])['close']
closing_price['msft_close'] = pd.read_csv(company_list[3])['close']

fig5, ax = plt.subplot()
sns.headmap(closing_price.corr(), annot = True, cmap = "coolwarm", ax=ax)
st.pyplot(fig5)

st.markdown("---")
st.markdown("**Note:** This dashboard provide basic technical analysis of major tech stocks using Python")