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

st.set_page_config(layout="wide")
today = datetime.today().strftime('%Y-%m-%d')

st.divider()
sol1,sol2,sol3 = st.columns(3)
# krx = fdr.StockListing('KRX')
with sol1:
    st.write(f'{today} 등락률 상위 10위')
    krx = fdr.StockListing('KRX')
    krx_ratio = krx[krx['Market'] !='KONEX']
    krx_ratio = krx_ratio[['Name', 'Close','ChagesRatio', 'Amount','Marcap']]
    krx_ratio['Amount'] = (krx_ratio['Amount']/100000000).astype(int)
    krx_ratio['Marcap'] = (krx_ratio['Marcap']/100000000).astype(int)
    krx_ratio = krx_ratio.sort_values('ChagesRatio',ascending=False).reset_index().drop(columns='index')
    krx_ratio.columns = ['종목', '종가','등락률', '거래금액','시총']
    krx_ratio = krx_ratio.iloc[0:10]
    krx_ratio = krx_ratio.set_index('종목')
    st.dataframe(krx_ratio)
with sol2:
    st.write(f'{today} 코스피 상위 10위')
    krx_kospi = krx[krx['Market'] =='KOSPI']
    krx_kospi = krx_kospi[['Name', 'Close','ChagesRatio', 'Amount','Marcap']]
    krx_kospi['Amount'] = (krx_kospi['Amount']/100000000).astype(int)
    krx_kospi['Marcap'] = (krx_kospi['Marcap']/100000000).astype(int)
    # krx_kospi = krx_ratio.sort_values('Marcap',ascending=False).reset_index().drop(columns='index')
    krx_kospi.columns = ['종목', '종가','등락률', '거래금액','시총']
    krx_kospi = krx_kospi.iloc[0:10]
    krx_kospi = krx_kospi.set_index('종목')
    st.dataframe(krx_kospi)
with sol3:
    st.write(f'{today} 코스닥 상위 10위')
    krx_kosdaq = krx[krx['Market'].str.contains('KOSDAQ')]
    krx_kosdaq = krx_kosdaq[['Name', 'Close','ChagesRatio', 'Amount','Marcap']]
    krx_kosdaq['Amount'] = (krx_kosdaq['Amount']/100000000).astype(int)
    krx_kosdaq['Marcap'] = (krx_kosdaq['Marcap']/100000000).astype(int)
    krx_kosdaq = krx_kosdaq.sort_values('Marcap',ascending=False).reset_index().drop(columns='index')
    krx_kosdaq.columns = ['종목', '종가','등락률', '거래금액','시총']
    krx_kosdaq = krx_kosdaq.iloc[0:10]
    krx_kosdaq = krx_kosdaq.set_index('종목')
    st.dataframe(krx_kosdaq)
    

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
        df_stock = df_stock.reset_index()
        df_stock['Date'] = df_stock['Date'].apply(lambda x : datetime.strftime(x, '%Y-%m-%d')) # Datetime to str

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
        x=df_stock['Date'],
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

        fig.add_trace(go.Scatter(x=df_stock['Date'], y=df_stock['MA5'], mode='lines', name='MA5', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df_stock['Date'], y=df_stock['MA20'], mode='lines', name='MA20', line=dict(color='purple')))
        # fig.add_trace(go.Scatter(x=df_stock['Date'], y=df_stock['MA60'], mode='lines', name='MA60', line=dict(color='red')))

        
        fig.update_layout(
        title='Stock Price Candlestick Chart 2024.01.01~',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            tickmode='linear',
            dtick='30',
            # tickformat='%Y-%m-%d',
            tickangle=0,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray',
            type='category',
            categoryorder='category ascending'
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
        


# sol1,sol2 = st.columns(2)
# with sol1:
#     st.subheader(f'{today} 등락률 평균 15')
#     krx = fdr.StockListing('KRX')
#     krx = krx[['Code', 'Name', 'Market', 'Close','ChagesRatio', 'Open', 'High', 'Low', 'Volume', 'Amount','Marcap']]
#     krx['Amount'] = (krx['Amount']/100000000).round(2)
#     krx['Marcap'] = (krx['Marcap']/100000000).astype(int)
#     krx = krx.sort_values('ChagesRatio',ascending=False)
#     path = './corpInfo.csv'
#     corp = pd.read_csv(path)
#     df = pd.DataFrame(corp,columns=['code','name','sector','big','middle','small'])
#     df = df[['code','name','middle']]

#     dd = pd.merge(krx,df,how='left',left_on='Name',right_on='name')
#     dd = dd[dd['Market'] !='KONEX']
#     dd = dd[~dd['Name'].str.endswith('우')]
#     ddf = dd.groupby('middle').agg({'ChagesRatio':['mean','max'],'Amount':'sum'}).reset_index()
#     ddf.columns = pd.MultiIndex.from_tuples(ddf.columns)
#     ddf[('ChagesRatio', 'mean')] = ddf[('ChagesRatio', 'mean')].round(2)
#     ddf = ddf.sort_values(('ChagesRatio','mean'),ascending=False)
#     ddf.columns = ['섹터', '등락률_mean', '등락률_max', '거래대금_sum']
#     ddf['거래대금_sum'] = ddf['거래대금_sum'].round(0)
#     ddf = ddf.head(15).reset_index().drop(columns='index')
    
#     # Figure 생성
#     fig = go.Figure()

#     #테이블 생성
#     fig.add_trace(go.Table(columnwidth = [300,200],
#         header=dict(values=list(ddf.columns),
#                     fill_color='lightskyblue',
#                     align='center',
#                     font=dict(color='black', size=13),
#                     height=30),
#         cells=dict(values=[ddf.섹터, ddf.등락률_mean, ddf.등락률_max, ddf.거래대금_sum],
#                 fill_color='lightcyan',
#                 align='center',
#                 font=dict(color='black', size=13),
#                 height=30)))
#           # 빈 공백을 흰색으로 채움
#     fig.update_layout(width=600)
#     fig.update_layout(height=1500)
    
#     st.plotly_chart(fig,config={'displayModeBar': False})
# with sol2:
#     st.subheader(f'{today} 반도체 종목')
#     dd = dd.fillna('기타')
#     se = dd[dd['middle'].str.contains('반도체')]
#     se = se[['middle','Name','ChagesRatio','Close','Amount','Marcap']]
#     se.columns = ['섹터','종목','등락률','종가','거래대금','시총']
    
#     se = se.sort_values(['섹터','등락률'],ascending=False)
    
#     # 함수를 이용해 값에 따라 색상을 반환하는 함수 정의
#     def get_font_color(value):
#         if value > 0:
#             return 'red'
#         elif value < 0:
#             return 'blue'
#         else:
#             return 'black'
#     # Figure 생성
#     fig = go.Figure()
#     a = [get_font_color(i) for i in se['등락률']] # 수정필요. 안 맞음. 
    
#     #테이블 생성
#     fig.add_trace(go.Table(columnwidth = [350,250],
#         header=dict(values=list(se.columns),
#                     fill_color='lightskyblue',
#                     align='center',
#                     font=dict(color='black', size=13),
#                     height=30),
#         cells=dict(values=[se.섹터, se.종목, se.등락률, se.종가, se.거래대금, se.시총],
#                 fill_color='lightcyan',
#                 align='center',
#                 font=dict(color=['black','black',a,'black','black','black'], size=13),
#                 height=30)))
#           # 빈 공백을 흰색으로 채움
#     fig.update_layout(width=650)
#     fig.update_layout(height=1500)
    
#     st.plotly_chart(fig,config={'displayModeBar': False})
        
        
        