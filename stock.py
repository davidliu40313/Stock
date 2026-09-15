import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(
    page_title="台股即時搜尋儀表板",
    page_icon="🔍",
    layout="wide"
)

# 2. 側邊欄搜尋介面
st.sidebar.title("🔍 搜尋台股")
st.sidebar.write("請輸入純數字代號即可，系統會自動判斷上市/上櫃。")

search_input = st.sidebar.text_input(
    "股票代號 (如: 0050, 2330)", 
    value="0050"
).strip().upper()

period = st.sidebar.selectbox("選擇走勢圖區間", ["1mo", "3mo", "6mo", "1y", "ytd"], index=0)

st.sidebar.markdown("---")
st.sidebar.write("💡 **快速測試代號參考**")
st.sidebar.caption(
    "大盤與ETF: 0050, 0052, 00631L, 00935\n\n"
    "AI與硬體供應鏈: 3515, 2382, 3231, 2317, 3037\n\n"
    "航運與其他: 2637, 6781"
)

# 3. 智慧抓取函數 (修正快取序列化問題)
@st.cache_data(ttl=300) 
def fetch_taiwan_stock(stock_code, period):
    if stock_code.endswith(".TW") or stock_code.endswith(".TWO"):
        tickers_to_try = [stock_code]
    else:
        tickers_to_try = [f"{stock_code}.TW", f"{stock_code}.TWO"]
        
    for ticker in tickers_to_try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        if not hist.empty:
            # 在這裡先把字串拿出來，不要回傳 Ticker 物件
            try:
                short_name = stock.info.get('shortName', ticker)
            except:
                short_name = ticker
            
            # 只回傳可序列化的資料：字串、字串、DataFrame
            return short_name, ticker, hist
            
    return "", None, pd.DataFrame()

# 4. 畫面渲染邏輯
if search_input:
    with st.spinner(f"正在搜尋 {search_input} 的最新報價..."):
        # 接收回傳的字串與 DataFrame
        short_name, actual_ticker, hist = fetch_taiwan_stock(search_input, period)

    if not hist.empty:
        # 計算今日與昨日數據
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        
        price_change = current_price - prev_price
        pct_change = (price_change / prev_price) * 100
        
        today_open = hist['Open'].iloc[-1]
        today_high = hist['High'].iloc[-1]
        today_low = hist['Low'].iloc[-1]
        volume = hist['Volume'].iloc[-1]

        # 主畫面頂部：顯示代號、名稱與主報價
        st.markdown(f"## {actual_ticker} {short_name}")
        st.metric(
            label="目前股價 (即時/收盤)", 
            value=f"{current_price:.2f}", 
            delta=f"{price_change:.2f} ({pct_change:.2f}%)"
        )
        
        st.divider()

        # 主畫面中段：四宮格數據
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

        # 主畫面下段：互動式 K 線圖
        st.subheader(f"走勢圖 (區間: {period})")
        
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name="K線",
            increasing_line_color='#ef5350', # 上漲紅色
            decreasing_line_color='#26a69a'  # 下跌綠色
        )])
        
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            margin=dict(l=0, r=0, t=20, b=0),
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"找不到代號為 '{search_input}' 的股票，請確認代號是否正確。")
