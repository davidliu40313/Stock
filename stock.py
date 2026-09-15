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


# 2. 初始化 Session State
if "watchlist" not in st.session_state:
    st.session_state.watchlist = [
        "0050",
        "006208",
        "00935",
        "3231",
        "VOO"
    ]

if "current_search" not in st.session_state:
    st.session_state.current_search = "0050"


# 3. 側邊欄：搜尋表單
st.sidebar.title("🔍 搜尋標的")
st.sidebar.write("輸入台股代號或美股代號，例如：0050、006208、2330、VOO、AAPL")


with st.sidebar.form(key="search_form"):
    search_input = st.text_input(
        "股票代號",
        value=st.session_state.current_search
    ).strip().upper()

    period = st.selectbox(
        "選擇走勢圖區間",
        ["1mo", "3mo", "6mo", "1y", "ytd"],
        index=0
    )

    submit_button = st.form_submit_button(
        label="開始搜尋 🚀"
    )


# 按下搜尋按鈕
if submit_button and search_input:
    st.session_state.current_search = search_input


# 4. 側邊欄：觀察清單
st.sidebar.markdown("---")
st.sidebar.subheader("⭐ 我的觀察清單")


if not st.session_state.watchlist:
    st.sidebar.info("目前清單為空，搜尋股票後可以加入。")

else:
    for item in st.session_state.watchlist.copy():

        cols = st.sidebar.columns([4, 1])

        with cols[0]:
            if st.button(
                f"📊 {item}",
                key=f"view_{item}",
                use_container_width=True
            ):
                st.session_state.current_search = item
                st.rerun()

        with cols[1]:
            if st.button(
                "❌",
                key=f"del_{item}"
            ):
                st.session_state.watchlist.remove(item)
                st.rerun()


# 5. 股票資料抓取函數
@st.cache_data(ttl=300)
def fetch_stock(stock_code, period):

    stock_code = stock_code.strip().upper()

    # -----------------------------
    # 台股
    # -----------------------------
    # 只要是純數字，就視為台股
    #
    # 例如：
    # 2330   -> 2330.TW
    # 0050   -> 0050.TW
    # 006208 -> 006208.TW
    # 00919  -> 00919.TW
    #
    if stock_code.isdigit():

        tickers_to_try = [
            f"{stock_code}.TW",   # 上市
            f"{stock_code}.TWO"   # 上櫃
        ]

    # -----------------------------
    # 已經輸入 .TW / .TWO
    # -----------------------------
    elif stock_code.endswith(".TW") or stock_code.endswith(".TWO"):

        tickers_to_try = [stock_code]

    # -----------------------------
    # 美股
    # -----------------------------
    else:

        tickers_to_try = [stock_code]


    # 依序嘗試
    for ticker in tickers_to_try:

        try:

            stock = yf.Ticker(ticker)

            hist = stock.history(
                period=period,
                auto_adjust=False
            )

            if hist is None or hist.empty:
                continue


            # 股票名稱
            short_name = ticker

            try:
                info = stock.info

                short_name = info.get(
                    "shortName",
                    ticker
                )

            except Exception:
                pass


            return (
                short_name,
                ticker,
                hist
            )


        except Exception as e:

            print(
                f"{ticker} 抓取失敗：{e}"
            )

            continue


    return (
        "",
        None,
        pd.DataFrame()
    )


# 6. 主畫面
current_target = st.session_state.current_search


if current_target:

    with st.spinner(
        f"正在抓取 {current_target} 的最新報價..."
    ):

        short_name, actual_ticker, hist = fetch_stock(
            current_target,
            period
        )


    # -----------------------------
    # 有成功抓到股票
    # -----------------------------
    if not hist.empty:

        current_price = hist["Close"].iloc[-1]


        # 昨日收盤
        if len(hist) > 1:

            prev_price = hist["Close"].iloc[-2]

        else:

            prev_price = current_price


        price_change = (
            current_price
            - prev_price
        )


        if prev_price != 0:

            pct_change = (
                price_change
                / prev_price
            ) * 100

        else:

            pct_change = 0


        today_open = hist["Open"].iloc[-1]

        today_high = hist["High"].iloc[-1]

        today_low = hist["Low"].iloc[-1]

        volume = hist["Volume"].iloc[-1]


        # 7. 股票名稱 + 加入觀察清單
        col_title, col_btn = st.columns(
            [4, 1]
        )


        with col_title:

            st.markdown(
                f"## {actual_ticker}　{short_name}"
            )


        with col_btn:

            # 使用使用者實際輸入的代號存 watchlist
            watchlist_code = current_target.upper()


            if watchlist_code in st.session_state.watchlist:

                if st.button(
                    "🌟 移出清單",
                    use_container_width=True
                ):

                    st.session_state.watchlist.remove(
                        watchlist_code
                    )

                    st.rerun()


            else:

                if st.button(
                    "⭐ 加入清單",
                    use_container_width=True
                ):

                    st.session_state.watchlist.append(
                        watchlist_code
                    )

                    st.rerun()


        # 8. 目前股價
        st.metric(
            label="目前股價（即時 / 收盤）",
            value=f"{current_price:.2f}",
            delta=f"{price_change:.2f} ({pct_change:.2f}%)"
        )


        st.divider()


        # 9. 四宮格數據
        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                label="開盤價",
                value=f"{today_open:.2f}"
            )


        with col2:

            st.metric(
                label="昨收價",
                value=f"{prev_price:.2f}"
            )


        with col3:

            st.metric(
                label="最高價",
                value=f"{today_high:.2f}"
            )


        with col4:

            st.metric(
                label="最低價",
                value=f"{today_low:.2f}"
            )


        st.metric(
            label="總成交量",
            value=f"{volume:,.0f}"
        )


        st.divider()


        # 10. K 線圖
        st.subheader(
            f"📊 走勢圖（區間：{period}）"
        )


        fig = go.Figure()


        fig.add_trace(

            go.Candlestick(

                x=hist.index,

                open=hist["Open"],

                high=hist["High"],

                low=hist["Low"],

                close=hist["Close"],

                name="K線",

                # 台股習慣
                increasing_line_color="#ef5350",

                decreasing_line_color="#26a69a"
            )
        )


        fig.update_layout(

            xaxis_rangeslider_visible=False,

            template="plotly_dark",

            margin=dict(
                l=0,
                r=0,
                t=20,
                b=0
            ),

            height=450
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # -----------------------------
    # 找不到股票
    # -----------------------------
    else:

        st.error(
            f"找不到代號為「{current_target}」的股票，請確認代號是否正確。"
        )
