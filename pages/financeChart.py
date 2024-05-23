import streamlit as st
import pandas as pd
import numpy as np
from datalink.data_loader import dbData
from datetime import datetime,timedelta
import datetime
import random
import FinanceDataReader as fdr
import plotly.graph_objects as go
from pykrx import stock

st.set_page_config(layout="wide")

col1,col2 = st.columns(2)
# from streamlit_option_menu import option_menu
db = dbData
finance = db.get_finance()

corp_name = finance['회사명'].unique()
selected = st.text_input('회사명',value='',placeholder='선택')
selected_corp = finance[finance['회사명'] == selected]
with col1:
    if selected:
        if '연결' in selected_corp['분류'].values:
            st.write('연결')
            finance1 = selected_corp[selected_corp['분류'] == '연결']
        else:
            st.text('별도')
            finance1 = selected_corp[selected_corp['분류'] == '별도']
        df_long = finance1.melt(id_vars=['회사명', '분류', '항목코드'], var_name='Quarter', value_name='Value')

        # Filter for '매출액' and '영업이익'
        sales_df = df_long[df_long['항목코드'] == '매출액']
        operating_income_df = df_long[df_long['항목코드'] == '영업이익']

        # Merge the sales and operating income dataframes
        merged_df = sales_df.merge(operating_income_df, on=['회사명', '분류', 'Quarter'], suffixes=('_sales', '_op_income'))

        # Calculate OPM
        merged_df['OPM'] = (merged_df['Value_op_income'] / merged_df['Value_sales']) * 100
        text_colors = merged_df['OPM'].apply(lambda x: 'red' if x > 0 else 'blue')
        # Create a combined figure with bar and line charts
        fig = go.Figure()

        # Add bar chart for 매출액 with light blue colors and gray border
        fig.add_trace(go.Bar(
            x=merged_df['Quarter'],
            y=merged_df['Value_sales'],
            name='매출액',
            marker_color='rgba(173, 216, 230, 0.9)',  # Light blue
            marker_line_color='gray',  # Gray border
            marker_line_width=1,       # Width of the border
            yaxis='y'
        ))
        text_colors = merged_df['OPM'].apply(lambda x: 'red' if x > 0 else 'blue')
        # Add line chart for OPM with dark pink line color and marker color, and larger marker size
        fig.add_trace(go.Scatter(
            x=merged_df['Quarter'],
            y=merged_df['OPM'],
            name='OPM',
            mode='lines+markers+text',
            line=dict(color='rgb(219, 112, 147)'),  # Dark pink for the line
            marker=dict(color='rgb(219, 112, 147)', size=8),  # Dark pink for the markers and larger size
            text=merged_df['OPM'].round(1),
            textposition='top center',
            textfont=dict(color=text_colors),
            yaxis='y2'  # Specify secondary y-axis
        ))

        # Update layout for dual y-axes and pastel theme
        fig.update_layout(
            title='매출액 및 OPM',
            xaxis_title='Quarter',
            yaxis=dict(
                title='매출액',
                titlefont=dict(color='rgba(135, 206, 235, 0.1)'),
                tickfont=dict(color='rgba(135, 206, 235, 0.1)')
            ),
            yaxis2=dict(
                title='OPM (%)',
                titlefont=dict(color='rgb(219, 112, 147)'),  # Matching the text color to the line color
                tickfont=dict(color='rgb(219, 112, 147)'),  # Matching the text color to the line color
                overlaying='y',  # Overlay on primary y-axis
                side='right'     # Place on right side
            ),
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            xaxis_tickangle=90  # Rotate x-axis tick labels by 90 degrees
        )
        
        # Show the plot in Streamlit
        st.plotly_chart(fig)

    # 종목명으로부터 종목 코드 가져오기
    def get_stock_code(company_name):
        df = fdr.StockListing('krx')
        df = df[df['Name'] == company_name]
        df = df.iloc[0][0]
        return df
    today = datetime.datetime.today().strftime('%Y%m%d')
    # 종목 코드로부터 주가 정보 가져오기
    def get_stock_price(code):
        df = stock.get_market_ohlcv_by_date("20230101", today, code)
        weekly_df = df.resample('W').agg({'시가': 'first', '고가': 'max', '저가': 'min', '종가': 'last'})
        return weekly_df

    with col2:
    # 스트림릿 애플리케이션

        if selected:
    # 사용자로부터 회사명 입력받기
    # selected = st.text_input("회사명을 입력하세요")
            code = get_stock_code(selected)
        # 종목 코드 가져오기
            
        
            if code:
                st.write(f"회사명: {selected}, 종목코드: {code}")

                # 주가 정보 가져오기
                price_info = get_stock_price(code)

                if not price_info.empty:
                    # 최근 주가 정보 가져오기
                    recent_price = price_info.iloc[-1]
                    max_price = price_info['고가'].max()

                    # 최근 종가와 시작가 차이 계산
                    price_diff = recent_price['종가'] - recent_price['시가']
                    price_diff_percent = price_diff / recent_price['시가'] * 100

                    # Plotly를 사용하여 캔들 차트 그리기
                    fig = go.Figure()

                    fig.add_trace(go.Candlestick(
                        x=price_info.index,
                        open=price_info['시가'],
                        high=price_info['고가'],
                        low=price_info['저가'],
                        close=price_info['종가'],
                        increasing_fillcolor='red',  # 상승할 때 캔들의 본체 색상
                        decreasing_fillcolor='blue',  # 하락할 때 캔들의 본체 색상
                        increasing_line_color='red',  # 상승할 때 캔들의 선 색상
                        decreasing_line_color='blue',  # 하락할 때 캔들의 선 색상
                        line_width=1,  # 캔들의 선 두께
                        name='캔들 차트'
                    ))

                    # 등락률 설명을 추가한 caption
                    st.caption(f" 이번주 등락률 : ({price_diff_percent:.2f}%) ,종가 : {recent_price['종가']}원 입니다.")

                    fig.update_layout(
                        # title=f"최근 종가와 시작가의 등락률: {price_diff:.2f} ({price_diff_percent:.2f}%)",
                        xaxis_title=None,  # x축 라벨 제거
                        yaxis_title=None,  # y축 라벨 제거
                        xaxis_rangeslider_visible=True,
                        plot_bgcolor='white',  # 배경색상을 흰색으로 변경
                        paper_bgcolor='white',  # 차트 바깥 영역 배경색상을 흰색으로 변경                        
                    )

                    st.plotly_chart(fig)
                else:
                    st.write("주가 정보를 가져올 수 없습니다.")
            else:
                st.write("종목 코드를 찾을 수 없습니다. 회사명을 확인하세요.")