import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd



def naver_m_news_stock(corp_code,corp_name):
    col = ['날짜','발행사','제목','내용','링크']
    lst = []
    for i in range(1,2):
        url = f'https://m.stock.naver.com/api/news/stock/{corp_code}?pageSize=20&page={i}'
        res = requests.get(url)
        js = res.json()

        for idx,content in enumerate(js):
            datetime = content['items'][0]['datetime']
            officeName = content['items'][0]['officeName']
            title = content['items'][0]['title']
            body = content['items'][0]['body']
            base_link = 'https://n.news.naver.com/article/'
            link = base_link + content['items'][0]['officeId'] +'/'+ content['items'][0]['id'][3:]
            lst.append([datetime,officeName,title,body,link])

    df = pd.DataFrame(lst,columns=[col]) 
    df.insert(0,'종목',corp_name)
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

    # dfs = dfs.head(5)
    # for k,v in zip(dfs['cd'],dfs['nm']):
    #     k = k[1:]
    #     try:
    #         daf = naver_m_news_stock(k,v)
    #         ddf = pd.concat([ddf,daf])
    #     except:
    #         continue
    # return ddf
    
input = st.text_input('입력')
code = corp_code(input)
news = naver_m_news_stock(code,input)

print(news)


