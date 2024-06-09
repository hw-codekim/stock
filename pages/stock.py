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
    col = ['날짜','제목','내용','링크']
    lst = []
    for i in range(1,2):
        url = f'https://m.stock.naver.com/api/news/stock/{corp_code}?pageSize=20&page={i}'
        res = requests.get(url)
        js = res.json()

        for idx,content in enumerate(js):
            datetime = content['items'][0]['datetime']
            # officeName = content['items'][0]['officeName']
            title = content['items'][0]['title']
            body = content['items'][0]['body']
            base_link = 'https://n.news.naver.com/article/'
            link = base_link + content['items'][0]['officeId'] +'/'+ content['items'][0]['id'][3:]
            # lst.append([datetime,officeName,title,body,link])
            lst.append([datetime,title,body,link])

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
    # corpInfo = {
    #     'code': [], 
    #     'name': [],
    #     'sector': [], 
    # }
    # # dfs = dfs.head(10)
    # for k,v in zip(dfs['cd'],dfs['nm']):
    #     k = k[1:]
    #     try:
    #         __sector = sector(k)
    #         corpInfo['code'].append(k)
    #         corpInfo['name'].append(v)
    #         corpInfo['sector'].append(__sector)
    #         # daf = naver_m_news_stock(k,v)
    #         # ddf = pd.concat([ddf,daf])
    #     except:
    #         continue
    # return corpInfo
    


def trading_price(code,name,sector):
    global today
    today = datetime.today().strftime('%Y%m%d')
    pykrx = stock.get_market_trading_value_by_date("20240101", today, code, etf=False, etn=False, elw=False, detail=True)    
    pykrx = pykrx.apply(lambda x: round(x/100000000,1))
    pykrx.insert(0,'name',name)
    pykrx.insert(0,'sector',sector)
    return pykrx
    
def sector(code):
    url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A{code}'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    sector_text = soup.select_one('#compBody > div.section.ul_corpinfo > div.corp_group1 > p > span.stxt.stxt2').text.replace('\xa0','').replace('FICS','').strip()
    return sector_text

@st.cache_data
def sector_merge():
    sec_df = pd.DataFrame()
    path = './corpInfo.csv'
    corp = pd.read_csv(path)
    df = pd.DataFrame(corp,columns=['code','name','sector','big','middle','small'])
    df['code'] = df['code'].apply(lambda x : str(x).zfill(6))
    df = df.head(3)
    for code,name,sector in zip(df['code'],df['name'],df['middle']):
        try:
            tp = trading_price(code,name,sector)
            sec_df = pd.concat([sec_df,tp])
            time.sleep(1)
        except:
            pass
    return sec_df

dd = sector_merge().reset_index()
st.write(dd)
fori = dd.groupby(['날짜','sector'])['금융투자','보험','투신','사모','연기금','개인','외국인'].sum().reset_index().sort_values('외국인',ascending=False)
fori = fori[fori['날짜'] == '2024-06-07']
st.write(fori)