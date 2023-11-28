import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

st.set_page_config(layout="wide")
st.title("📈 주식 대시보드")
company = ["삼성전자", "LG에너지솔루션", "SK하이닉스"]
company_code = ["005930.KS", "373220.KS", "000660.KS"]
selected = st.sidebar.selectbox("Select a stock symbol:", company)

# 선택한 기업의 종목 코드로 ticker 생성
ticker = yf.Ticker(company_code[company.index(selected)])

# 상단에 노출할 정보 데이터
stock_data = ticker.history(
              interval='1d',
              period = '1y',
              actions=True,
              auto_adjust=True)

# 전날 종가
latest_close_price = stock_data.iloc[-2]["Close"]
# 52주 고저
max_52_week_high = stock_data["High"].tail(252).max()
min_52_week_low = stock_data["Low"].tail(252).min()
# 1년 가격 변화
price_dif = stock_data.iloc[-1]["Close"] - stock_data.iloc[0]["Close"]
percentage_difference = price_dif / stock_data.iloc[-1]["Close"] * 100

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("종가", f"{latest_close_price:,.0f} ₩")
with col2:
    st.metric("가격 변화 (YoY)", f"{price_dif:,.0f} ₩", f"{percentage_difference:+,.0f}%")
with col3:
    st.metric("52-주 최고", f"{max_52_week_high:,.0f} ₩")
with col4:
    st.metric("52-주 최저", f"{min_52_week_low:,.0f} ₩")

# 1일, 최대 버튼 생성
col1,col2, col3 =  st.columns([1,1,6])

with col1:
  day1 = st.button("1일")
with col2:
  year1 = st.button('1년')

# 주가 호출 기간 및 간격 설정
# 디폴트
period='1d'
interval='5m'
text = '오늘'
if day1:
  period='1d'
  interval='5m'
  text = '오늘'
elif year1:
  period='1y'
  interval='1d'
  text = '1년'

# 주가 호출
df = ticker.history(
              interval=interval,
              period = period,
              actions=True,
              auto_adjust=True)

# 캔들스틱 차트 생성
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'])
                     ])

fig.update_layout(xaxis_rangeslider_visible=False, title = f"{selected} ({text})")
fig.update_layout(hovermode="x unified")

# 차트 표시
st.plotly_chart(fig)

# 재무 정보
st.write("손익계산서")
statement = ticker.financials
st.write(statement)