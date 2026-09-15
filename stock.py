import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 1. 網頁基本設定
st.set_page_config(
    page_title="台美股即時儀表板",
    page_icon="📈",
    layout="wide"
)

# 2. 初始化 Session State (記憶觀察清單與目前搜尋)
if 'watchlist' not in st.session_state:
    # 預設觀察清單，測試完可自行在畫面上刪除
    st.session_state.watchlist = ["0050", "00935", "3231", "VOO"]

if 'current_search' not in st.session_state:
    st.session_state.current_search = "0050"

# 3. 側邊欄：搜尋表單
st.sidebar.title("🔍 搜尋標的")
st.sidebar.write("輸入數字(台股)或英文(美股)。")

with st.sidebar.form(key='search_form'):
    search_input = st.text_input(
        "股票代號 (如: 0050, 2330, VOO)", 
        value=st.session_state.current_search
    ).strip().upper()
    
    period = st.selectbox("選擇走勢圖區間", ["1mo", "3mo", "6mo", "1y", "ytd"], index=0)
    
    submit_button = st.form_submit_button(label='開始搜尋 🚀')

# 若按下搜尋按鈕，更新目前的搜尋目標
if submit_button and search_input:
    st.session_state.current_search = search_input

# 4. 側邊欄：我的觀察清單
st.sidebar.markdown("---")
st.sidebar.subheader("⭐ 我的觀察清單")

if not st.session_state.watchlist:
    st.sidebar.info("目前清單為空，請從右側搜尋後加入。")
else:
    for item in st.session_state.watchlist:
        # 使用欄位排版，左邊放切換按鈕，右邊放刪除按鈕
        cols = st.sidebar.columns([4, 1])
        with cols[0]:
            if st.button(f"📊 {item}", key=f"view_{item}", use_container_width=True):
                st.session_state.current_search = item
                st.rerun() # 重新整理頁面以顯示該檔股票
        with cols[1]:
            if st.button("❌", key=f"del_{item}"):
                st.session_state.watchlist.remove(item)
                st.rerun()

# 5. 智慧抓取函數：支援台股自動補後綴，且支援美股
@st.cache_data(ttl=300) 
def fetch_stock(stock_code, period):
    # 判斷是否為純英文 (美股)，或已經帶有台股後綴
    if stock_code.isalpha() or stock_code.endswith(".TW") or stock_code.endswith(".TWO"):
        tickers_to_try = [stock_code]
    else:
        # 數字代號預設先猜上市，再猜上櫃，最後直接當原始代號查
        tickers_to_try = [f"{stock_code}.TW", f"{stock_code}.TWO", stock_code]
        
    for ticker in tickers_to_try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if not hist.empty:
            short_name = ticker 
            try:
                info = stock.info
                if 'shortName' in info:
                    short_name = info['shortName']
            except Exception:
                pass
            
            return short_name, ticker, hist
            
    return "", None, pd.DataFrame()

# 6. 畫面渲染邏輯
current_target = st.session_state.current_search

if current_target:
    with st.spinner(f"正在抓取 {current_target} 的最新報價..."):
        short_name, actual_ticker, hist = fetch_stock(current_target, period)

    if not hist.empty:
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        price_change = current_price - prev_price
        pct_change = (price_change / prev_price) * 100
        
        today_open = hist['Open'].iloc[-1]
        today_high = hist['High'].iloc[-1]
        today_low = hist['Low'].iloc[-1]
        volume = hist['Volume'].iloc[-1]

        # 主畫面頂部：標題與「加入/移除清單」按鈕
        col_title, col_btn = st.columns([4, 1])
        with col_title:
            st.markdown(f"## {actual_ticker} {short_name}")
        with col_btn:
            # 判斷目前標的是否已在觀察清單中
            if current_target in st.session_state.watchlist:
                if st.button("🌟 移出清單", use_container_width=True):
                    st.session_state.watchlist.remove(current_target)
                    st.rerun()
            else:
                if st.button("⭐ 加入清單", use_container_width=True):
                    st.session_state.watchlist.append(current_target)
                    st.rerun()
                    
        st.metric(
            label="目前股價 (即時/收盤)", 
            value=f"{current_price:.2f}", 
            delta=f"{price_change:.2f} ({pct_change:.2f}%)"
        )
        
        st.divider()

        # 四宮格數據
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

        # 互動式 K 線圖
        st.subheader(f"走勢圖 (區間: {period})")
        
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name="K線",
            increasing_line_color='#ef5350', # 上漲紅色 (台股習慣)
            decreasing_line_color='#26a69a'  # 下跌綠色 (台股習慣)
        )])
        
        fig.update_layout(
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            margin=dict(l=0, r=0, t=20, b=0),
            height=450
        )
        
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"找不到代號為 '{current_target}' 的股票，請確認代號是否正確。")
