import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")

search = st.sidebar.text_input('검색어 입력')
st.sidebar.button('clear')
def get_search_naver(input_text):
    data = []
    for i in range(3):
        response = requests.get(f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={input_text}&start={i}1")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.select(".list_news > li")
        for article in articles:
            title = article.select_one(".news_tit").text
            link = article.select_one(".news_tit").attrs['href']
            # date_tag = article.select_one(".info_group > .info")
            data.append([title, link])

    # 데이터 프레임 만들기
    df = pd.DataFrame(data, columns=['제목', '링크'])
    df = df.reset_index()
    return df

def get_search_google(input_text):
    dd = []
    url = f'https://news.google.com/rss/search?q={input_text}&hl=ko&gl=KR&ceid=KR%3Ako'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'lxml')
    items = soup.find_all('item')
    # st.write(items[0])
    # item 태그에서 제목, 날짜, 링크 추출
    for item in items:
        # st.write(item)
        title = item.find('title').get_text()
        pub_date = item.find('pubdate').get_text()
        pub_date = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
        link = item.find('description')
        description_soup = BeautifulSoup(link.get_text(), 'html.parser')
        a_tag = description_soup.find('a')
        link = a_tag['href']   
        dd.append([pub_date,title,link])
    ddf = pd.DataFrame(dd, columns=['날짜','제목','링크'])
    ddf = ddf.sort_values('날짜',ascending=False)

    return ddf

st.subheader(f'키워드 : {search}')
st.caption(f'검색창에 키워드 적고 조회 눌렀을때 결과와 동일')
if search:
    col1,col2 = st.columns(2)
    with col1:
        
        st.divider()
        st.write('네이버 뉴스')
        naver = get_search_naver(search)
        table = st.dataframe(naver,width=700,height=1000,
        column_config={
        '링크' : st.column_config.LinkColumn('링크',display_text='연결')},
        hide_index=True )

    with col2:
        
        st.divider()
        st.write('구글 뉴스')
        google = get_search_google(search)
        table = st.dataframe(google,width=600,height=1000,
        column_config={
        '링크' : st.column_config.LinkColumn('링크',display_text='연결')},
        hide_index=True )

