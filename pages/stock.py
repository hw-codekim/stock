import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO

# 한국 주식 종목 코드 가져 오는 함수

def get_stock_info(maket_type=None):
    base_url = "http://kind.krx.co.kr/corpgeneral/corpList.do"
    method = 'download'
    if maket_type == 'kospi':
        marketType = 'stockMkt'
    elif maket_type == 'kosdaq':
        marketType = 'kosdaqMkt'
    elif maket_type == None:
        marketType = ''
    url = '{0}?method={1}&marketType={2}'.format(base_url,method,marketType)
    df = pd.read_html(url,head=0)[0]

    #종목 코드 열을 6자리 숫자로 표시된 문자열로 변환
    df['종목코드'] = df['종목코드'].apply(lambda x : f'{x:06d}')

    #회사명과 종목코드 열 데이터만 남김
    df = df[['회사명','종목코드']]

    return df

# yfinance 에 이용할 ticker  심볼을 반환하는 함수

def get_ticker_symbol(company_name,maket_type):
    # df = get_stock_info(maket_type)
    # code = df[df['회사명'] == company_name]['종목코드'].values
    # code = code[0]
    code = '005930'

    if maket_type == 'kospi':
        ticker_symbol = code +'.KS'
    elif maket_type == 'kosdaq':
        ticker_symbol = code +'.KQ'
    
    return ticker_symbol

st.title('주식 정보를 가져오는 웹 앱')

#사이드바의 폭을 조절. 폭을 250픽셀로 지정

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded='true]> div:first-child{width:250px;}
    </style>    
    """,unsafe_allow_html=True
)

st.sidebar.header('회사 이름과 기간 입력')

# 주식 종목 이름을 입력 받아서 지정
stock_name = st.sidebar.text_input('회사이름',value='삼성전자')
#기간을 입력 받아서 지정
date_range = st.sidebar.date_input('시작일과 종료일',
                                   [datetime.date(2019,1,1),datetime.date(2021,12,31)])
clicked=st.sidebar.button('주가 데이터 가져오기')

if (clicked == True):
    #주식 종목과 종류 지정해 ticker 심볼 획득
    ticker_symbol = get_ticker_symbol(stock_name,'kospi')
    ticker_data = yf.Ticker(ticker_symbol)

    start_p = date_range[0] # 시작일
    end_p = date_range[1]+datetime.timedelta(days=1) # 종료일(지정된 날짜에 하루를 더함)

    #시작일과 종료일 지정해 주가 데이터 가져오기
    df = ticker_data.history(start=start_p, end = end_p)
    
    #주식 데이터 표시
    st.subheader(f'[{stock_name}] 주가 데이터')
    st.dataframe(df.head())

    #차트 그리기
    #matplotlib을 이용한 그래프에 한들을 표시하기 위한 설정

    matplotlib.rcParams['font.family'] = 'Malgun Gothic'
    matplotlib.rcParams['axes.unicode_minus'] = False

    #선 그래프 그리기
    ax = df['Close'].plot(grid = True, figsize = (15,5))
    ax.set_title('주가(종가) 그래프', fontsize = 30)
    ax.set_xlabel('기간',fontsize = 20)
    ax.set_ylabel('주가(원)',fontsize = 20)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    fig = ax.get_figure()
    st.pyplot(fig)
