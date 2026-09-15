import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 1. 網頁基本設定 (預設為寬版，套用深色主題感)
st.set_page_config(
    page_title="即時股票儀表板",
    page_icon="📈",
    layout="wide"
)

# 2. 預設觀察清單 (您可以隨時增刪)
TICKERS = {
    "0050.TW": "元大台灣50",
    "0052.TW": "富邦科技",
    "00631L.TW": "元大台灣50正2",
    "00935.TW": "野村臺灣新科技50",
    "VOO": "Vanguard 標普500 ETF",
    "2317.TW": "鴻海",
    "2382.TW": "廣達",
    "3231.TW": "緯創",
    "2637.TW": "慧洋-KY"
}

# 3. 側邊欄設計 (選單)
st.sidebar.title("📊 儀表板設定")
selected_symbol = st.sidebar.selectbox(
    "請選擇標的", 
    options=list(TICKERS.keys()), 
    format_func=lambda x: f"{x} ({TICKERS[x]})"
)
period = st.sidebar.selectbox("選擇走勢圖區間", ["1mo", "3mo", "6mo", "1y", "ytd"], index=0)

# 4. 抓取真實數據函數 (使用快取避免重複讀取)
@st.cache_data(ttl=300) # 快取 5 分鐘
def load_data(symbol, period):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    return stock.info, hist

# 讀取資料
with st.spinner("抓取最新報價中..."):
    info, hist = load_data(selected_symbol, period)

if not hist.empty:
    # 5. 計算今日與昨日數據
    current_price = hist['Close'].iloc[-1]
    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
    
    price_change = current_price - prev_price
    pct_change = (price_change / prev_price) * 100
    
    today_open = hist['Open'].iloc[-1]
    today_high = hist['High'].iloc[-1]
    today_low = hist['Low'].iloc[-1]
    volume = hist['Volume'].iloc[-1]

    # 6. 主畫面頂部：大標題與主報價
    st.markdown(f"## {selected_symbol} {TICKERS[selected_symbol]}")
    st.metric(
        label="目前股價 (即時/收盤)", 
        value=f"{current_price:.2f}", 
        delta=f"{price_change:.2f} ({pct_change:.2f}%)"
    )
    
    st.divider()

    # 7. 主畫面中段：四宮格數據 (還原您設計圖的版型)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="開盤價", value=f"{today_open:.2f}")
    with col2:
        st.metric(label="昨收價", value=f"{prev_price:.2f}")
    with col3:
        st.metric(label="最高價", value=f"{today_high:.2f}")
    with col4:
        st.metric(label="最低價", value=f"{today_low:.2f}")
    
    st.metric(label="總成交量", value=f"{volume:,.0f}")
    st.divider()

    # 8. 主畫面下段：互動式 K 線圖
    st.subheader(f"走勢圖 (區間: {period})")
    
    fig = go.Figure(data=[go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
        name="K線",
        increasing_line_color='#26a69a', # 上漲綠色 (可依喜好調整，美股預設綠漲紅跌)
        decreasing_line_color='#ef5350'  # 下跌紅色
    )])
    
    # 調整圖表外觀為深色模式
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        margin=dict(l=0, r=0, t=20, b=0),
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("無法取得該檔股票的資料，請檢查代碼或稍後再試。")
