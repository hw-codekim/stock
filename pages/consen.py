import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime,timedelta
import streamlit as st

today = (datetime.today()-timedelta(days=1)).strftime('%Y/%m/%d')
st.set_page_config(layout="wide")
@st.cache_data
def consensus(code,name):
    url = f'https://comp.fnguide.com/SVO2/json/data/01_06/03_{code}.json'
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = 'utf-8-sig'
    data = response.json()
    df = pd.DataFrame(data['comp'])
    df.columns = ['no','증권사','일자','목표주가','직전목표주가','증감율','투자의견','직전투자의견','평균목표주가','평균직전목표주가','평균투자의견','평균직전투자의견']
    df.insert(0,'name',name)
    df.insert(0,'code',code)
    return df

# dd = consensus('A356860','티엘비')
# dd
@st.cache_data
def corp_sector(code):
    url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode={code}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    sector = soup.select_one('#compBody > div.section.ul_corpinfo > div.corp_group1 > p > span.stxt.stxt2').text
    price = soup.select_one('#svdMainChartTxt11').text
    sichong = soup.select_one('#svdMainGrid1 > table > tbody > tr:nth-child(4) > td:nth-child(2)').text
    return sector,price,sichong

@st.cache_data
def corp_code():
    ddf = pd.DataFrame()
    url = 'https://comp.fnguide.com/XML/Market/CompanyList.txt'
    response = requests.get(url)
    response.encoding = 'utf-8-sig'
    data = BeautifulSoup(response.text,'html.parser')
    data = response.json()
    dfs = pd.DataFrame(data['Co'])
    # dfs = dfs.head(30)
    for k,v in zip(dfs['cd'],dfs['nm']):
        try:
            daf = consensus(k,v)
            cs = corp_sector(k)
            daf.insert(2,'주가',cs[1])
            daf.insert(2,'시총',cs[2])
            daf.insert(2,'섹터',cs[0])
            ddf = pd.concat([ddf,daf])
         
        except:
            continue
    
    return ddf

result = corp_code()
st.write(f'출처 : fnguide/기업정보/컨센서스 ')
st.write(f'참고 : 하루늦게 올라옴 예)2024/06/12(오늘) 조회하면 0건, 어제껀 다 올라와 있음')
st.divider()

datein = st.sidebar.date_input('날짜를 입력하세요', pd.to_datetime(f'{today}').date())
datein = datein.strftime('%Y/%m/%d')
st.write(f'{datein} 발행한 컨센서스')



date_result = result [result['일자'] == datein]
st.write(f'총 {len(date_result)} 건')
# result = result.sort_values('일자',ascending=False)
st.write(date_result)
st.divider()


corp_input = st.sidebar.text_input('종목을 입력하세요')
st.write('좌측 종목 입력')
corp_result = result[result['name'] == corp_input]
st.write(corp_result)