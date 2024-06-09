import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import FinanceDataReader as fdr
import plotly.graph_objects as go
from pykrx import stock
import time
from datetime import datetime

# 코드와 네임을 넣으면 naver 종목 기사의 2페이지를 가져와서 보여줌
def naver_m_news_stock(corp_code,corp_name):
    # col = ['날짜','발행사','제목','내용','링크']
    col = ['날짜','제목','링크']
    lst = []
    for i in range(1,2):
        url = f'https://m.stock.naver.com/api/news/stock/{corp_code}?pageSize=20&page={i}'
        res = requests.get(url)
        js = res.json()

        for idx,content in enumerate(js):
            datetime = content['items'][0]['datetime']
            # officeName = content['items'][0]['officeName']
            title = content['items'][0]['title']
            # body = content['items'][0]['body']
            base_link = 'https://n.news.naver.com/article/'
            link = base_link + content['items'][0]['officeId'] +'/'+ content['items'][0]['id'][3:]
            # lst.append([datetime,officeName,title,body,link])
            lst.append([datetime,title,link])

    df = pd.DataFrame(lst,columns=col) 
    df.insert(0,'종목',corp_name)
    df['날짜'] = df['날짜'].apply(lambda x: f"{x[:4]}-{x[4:6]}-{x[6:8]}")
    df['제목'] = df['제목'].str.replace('&quot;','')
    return df 


#기업 이름을 넣으면 코드를 알려줌.
def corp_code(name):
    ddf = pd.DataFrame()
    url = 'https://comp.fnguide.com/XML/Market/CompanyList.txt'
    response = requests.get(url)
    response.encoding = 'utf-8-sig'
    data = BeautifulSoup(response.text,'html.parser')
    data = response.json()
    dfs = pd.DataFrame(data['Co'])
    dfs = dfs[dfs['nm'] == name]
    dfs['cd'] = dfs['cd'].iloc[0][1:]
    return dfs['cd'].iloc[0]

input = st.text_input('종목명 입력')


if input:
    code = corp_code(input)
    news = naver_m_news_stock(code,input)
    col1,col2 = st.columns(2)
    with col1:    
        st.dataframe(news,
        column_config={
        '링크' : st.column_config.LinkColumn('링크',display_text='연결')},
        hide_index=True
        )
    with col2:
        df_stock = fdr.DataReader(code,'2024-01-01')
        df_stock['MA5'] = df_stock['Close'].rolling(window=5).mean()
        df_stock['MA10'] = df_stock['Close'].rolling(window=10).mean()
        df_stock['MA20'] = df_stock['Close'].rolling(window=20).mean()
        df_stock['MA60'] = df_stock['Close'].rolling(window=60).mean()
        
        # df_stock = df_stock.reset_index()
        # st.write(df_stock)
        # df_stock = df_stock[df_stock.index.weekday < 5]
        
        # df_stock['Date'] = df_stock['Date'].strftime('%Y-%m-%d')

        # Define holidays (example)
        # holidays = ['2024-02-09', '2024-02-12', '2024-03-01', '2024-05-06', '2024-05-15', '2024-06-06']  # Add your actual holiday dates
        # holidays = pd.to_datetime(holidays)
        # df_stock = df_stock[~df_stock.index.isin(holidays)]
        
        
        
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
        x=df_stock.index,
        open=df_stock['Open'],
        high=df_stock['High'],
        low=df_stock['Low'],
        close=df_stock['Close'],
        increasing_line_color='green', 
        decreasing_line_color='red',
        increasing_line_width=0.5,  # Set the line width for increasing candles
        decreasing_line_width=0.5,  # Set the line width for decreasing candles
        name='Candlestick'
         ))

        
        
        fig.update_layout(
        title='Stock Price Candlestick Chart 2024.01.01~',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            tickmode='linear',
            dtick='M1',
            tickformat='%Y-%m-%d',
            tickangle=0,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            tickformat=',.0f'  # Remove the 'k' format and show full numbers
        ),
        template='plotly_white',
        margin=dict(l=10, r=10, t=30, b=20)
        )
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)
    

        
        st.plotly_chart(fig)
        
        
        