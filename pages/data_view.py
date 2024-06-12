import streamlit as st
import FinanceDataReader as fdr
import plotly.express as px
from datetime import datetime
import pandas as pd

today = datetime.today().strftime('%Y-%m-%d')
st.subheader('지표 조회')
df_guri = fdr.DataReader('HG=F') # 구리 선물 (COMEX)
df_guri = df_guri.reset_index()
df_guri['Date'] = pd.to_datetime(df_guri['Date']).dt.date
comparison_date = pd.to_datetime('2024-01-02').date()
df_guri = df_guri[df_guri['Date'] >= comparison_date]
today_value = df_guri['Close'].iloc[-1]
df_guri['Date'] = df_guri['Date'].apply(lambda x : datetime.strftime(x, '%Y-%m-%d')) # Datetime to str
df_guri = df_guri.dropna()
fig_guri = px.line(df_guri, x="Date", y="Close",title=f'【 구리 】 2024.01.01~ {today} / {today} = {today_value}')
fig_guri.update_layout(
    xaxis=dict(
            tickmode='linear',
            dtick='30',
            tickangle=0,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            type='category',
            categoryorder='category ascending'))

fig_guri.update_xaxes(title=None)
fig_guri.update_yaxes(title=None)
st.plotly_chart(fig_guri, theme="streamlit")
st.divider()



df_gas = fdr.DataReader('NG=F') # 천연가스 선물 (NYMEX)
df_gas = df_gas.reset_index()

df_gas['Date'] = pd.to_datetime(df_gas['Date']).dt.date
comparison_date = pd.to_datetime('2024-01-02').date()
df_gas = df_gas[df_gas['Date'] >= comparison_date]

today_value = df_gas['Close'].iloc[-1]
df_gas['Date'] = df_gas['Date'].apply(lambda x : datetime.strftime(x, '%Y-%m-%d')) # Datetime to str
df_gas = df_gas.dropna()
fig_gas = px.line(df_gas, x="Date", y="Close",title=f'【 천연가스 】 2024.01.01~ {today}  / {today} = {today_value}')

fig_gas.update_layout(
    xaxis=dict(
            tickmode='linear',
            dtick='30',
            tickangle=0,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            type='category',
            categoryorder='category ascending'))


fig_gas.update_xaxes(title=None)
fig_gas.update_yaxes(title=None)
st.plotly_chart(fig_gas, theme="streamlit")
st.divider()



df_us10y = fdr.DataReader('US10YT') # 10년 만기 미국국채 수익률
df_us10y = df_us10y.reset_index()

df_us10y['Date'] = pd.to_datetime(df_us10y['Date']).dt.date
comparison_date = pd.to_datetime('2024-01-02').date()
df_us10y = df_us10y[df_us10y['Date'] >= comparison_date]

today_value = df_us10y['Close'].iloc[-1]
df_us10y['Date'] = df_us10y['Date'].apply(lambda x : datetime.strftime(x, '%Y-%m-%d')) # Datetime to str
df_us10y = df_us10y.dropna()
fig_us10y = px.line(df_us10y, x="Date", y="Close",title=f'【 10년 채권금리 】 2024.01.01~ {today}  / {today} = {today_value}')

fig_us10y.update_layout(
    xaxis=dict(
            tickmode='linear',
            dtick='30',
            tickangle=0,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            type='category',
            categoryorder='category ascending'))


fig_us10y.update_xaxes(title=None)
fig_us10y.update_yaxes(title=None)
st.plotly_chart(fig_us10y, theme="streamlit")
st.divider()

df_wti = fdr.DataReader('CL=F') # WTI유 선물 Crude Oil (NYMEX)
df_wti = df_wti.reset_index()

df_wti['Date'] = pd.to_datetime(df_wti['Date']).dt.date
comparison_date = pd.to_datetime('2024-01-02').date()
df_wti = df_wti[df_wti['Date'] >= comparison_date]

today_value = df_wti['Close'].iloc[-1]
df_wti['Date'] = df_wti['Date'].apply(lambda x : datetime.strftime(x, '%Y-%m-%d')) # Datetime to str
df_wti = df_wti.dropna()
fig_wti = px.line(df_wti, x="Date", y="Close",title=f'【 WTI 】 2024.01.01~ {today}  / {today} = {today_value}')

fig_wti.update_layout(
    xaxis=dict(
            tickmode='linear',
            dtick='30',
            tickangle=0,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            type='category',
            categoryorder='category ascending'))


fig_wti.update_xaxes(title=None)
fig_wti.update_yaxes(title=None)
st.plotly_chart(fig_wti, theme="streamlit")
st.divider()

df_usdkrw = fdr.DataReader('USD/KRW') # 달러 원화
df_usdkrw = df_usdkrw.reset_index()

df_usdkrw['Date'] = pd.to_datetime(df_usdkrw['Date']).dt.date
comparison_date = pd.to_datetime('2024-01-02').date()
df_usdkrw = df_usdkrw[df_usdkrw['Date'] >= comparison_date]


today_value = (df_usdkrw['Close'].iloc[-1]).round(2)
fig_usdkrw = px.line(df_usdkrw, x="Date", y="Close",title=f'【 USD/KRW 환율 】 2024.01.01~ {today}  / {today} = {today_value}')
fig_usdkrw.update_xaxes(title=None)
fig_usdkrw.update_yaxes(title=None)
st.plotly_chart(fig_usdkrw, theme="streamlit")
st.divider()
st.divider()
