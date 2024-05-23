import streamlit as st
import FinanceDataReader as fdr
import plotly.express as px
import datetime

today = datetime.datetime.today().strftime('%Y-%m-%d')
st.subheader('지표 조회')
df_guri = fdr.DataReader('HG=F') # 구리 선물 (COMEX)
df_guri = df_guri.reset_index()
df_guri = df_guri[df_guri['Date'] > '2024-01-01']
today_value = df_guri['Close'].iloc[-1]
fig_guri = px.line(df_guri, x="Date", y="Close",title=f'【 구리 】 2024.01.01~ {today} / {today} = {today_value}')
fig_guri.update_xaxes(title=None)
fig_guri.update_yaxes(title=None)
st.plotly_chart(fig_guri, theme="streamlit")
st.divider()

df_gas = fdr.DataReader('NG=F') # 천연가스 선물 (NYMEX)
df_gas = df_gas.reset_index()
df_gas = df_gas[df_gas['Date'] > '2024-01-01']
today_value = df_gas['Close'].iloc[-1]
fig_gas = px.line(df_gas, x="Date", y="Close",title=f'【 천연가스 】 2024.01.01~ {today}  / {today} = {today_value}')
fig_gas.update_xaxes(title=None)
fig_gas.update_yaxes(title=None)
st.plotly_chart(fig_gas, theme="streamlit")
st.divider()


df_us10y = fdr.DataReader('US10YT') # 10년 만기 미국국채 수익률
df_us10y = df_us10y.reset_index()
df_us10y = df_us10y[df_us10y['Date'] > '2024-01-01']
today_value = df_us10y['Close'].iloc[-1]
fig_us10y = px.line(df_us10y, x="Date", y="Close",title=f'【 10년 채권금리 】 2024.01.01~ {today}  / {today} = {today_value}')
fig_us10y.update_xaxes(title=None)
fig_us10y.update_yaxes(title=None)
st.plotly_chart(fig_us10y, theme="streamlit")
st.divider()

df_wti = fdr.DataReader('CL=F') # WTI유 선물 Crude Oil (NYMEX)
df_wti = df_wti.reset_index()
df_wti = df_wti[df_wti['Date'] > '2024-01-01']
today_value = df_wti['Close'].iloc[-1]
fig_wti = px.line(df_wti, x="Date", y="Close",title=f'【 WTI 】 2024.01.01~ {today}  / {today} = {today_value}')
fig_wti.update_xaxes(title=None)
fig_wti.update_yaxes(title=None)
st.plotly_chart(fig_wti, theme="streamlit")
st.divider()

df_usdkrw = fdr.DataReader('USD/KRW') # 달러 원화
df_usdkrw = df_usdkrw.reset_index()
df_usdkrw = df_usdkrw[df_usdkrw['Date'] > '2024-01-01']
today_value = df_usdkrw['Close'].iloc[-1]
fig_usdkrw = px.line(df_usdkrw, x="Date", y="Close",title=f'【 USD/KRW 환율 】 2024.01.01~ {today}  / {today} = {today_value}')
fig_usdkrw.update_xaxes(title=None)
fig_usdkrw.update_yaxes(title=None)
st.plotly_chart(fig_usdkrw, theme="streamlit")
st.divider()

