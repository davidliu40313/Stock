import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd


# ============================================================
# 1. 網頁基本設定
# ============================================================

st.set_page_config(
    page_title="台美股即時儀表板",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# 2. Session State
# ============================================================

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


# ============================================================
# 3. 側邊欄搜尋
# ============================================================

st.sidebar.title("🔍 搜尋標的")

st.sidebar.write(
    "台股直接輸入數字，美股輸入英文代號。"
)

st.sidebar.caption(
    "例如：0050、006208、2330、3231、VOO、AAPL"
)


with st.sidebar.form(key="search_form"):

    search_input = st.text_input(
        "股票代號",
        value=st.session_state.current_search
    ).strip().upper()

    period = st.selectbox(
        "歷史 K 線區間",
        [
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "ytd"
        ],
        index=0
    )

    submit_button = st.form_submit_button(
        "開始搜尋 🚀",
        use_container_width=True
    )


if submit_button and search_input:

    st.session_state.current_search = search_input


# ============================================================
# 4. 觀察清單
# ============================================================

st.sidebar.markdown("---")

st.sidebar.subheader("⭐ 我的觀察清單")


if not st.session_state.watchlist:

    st.sidebar.info(
        "目前清單為空。"
    )

else:

    for item in st.session_state.watchlist.copy():

        cols = st.sidebar.columns(
            [4, 1]
        )

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
                key=f"delete_{item}"
            ):

                st.session_state.watchlist.remove(
                    item
                )

                st.rerun()


# ============================================================
# 5. 股票代號轉換
# ============================================================

def get_tickers_to_try(stock_code):

    stock_code = (
        stock_code
        .strip()
        .upper()
    )

    # 台股純數字
    #
    # 2330
    # 0050
    # 006208
    # 00919
    #
    if stock_code.isdigit():

        return [
            f"{stock_code}.TW",
            f"{stock_code}.TWO"
        ]

    # 使用者自己輸入 .TW / .TWO
    if (
        stock_code.endswith(".TW")
        or
        stock_code.endswith(".TWO")
    ):

        return [
            stock_code
        ]

    # 其他視為美股
    return [
        stock_code
    ]


# ============================================================
# 6. 歷史資料
# ============================================================

@st.cache_data(ttl=300)
def fetch_stock(stock_code, period):

    tickers_to_try = get_tickers_to_try(
        stock_code
    )

    for ticker in tickers_to_try:

        try:

            stock = yf.Ticker(
                ticker
            )

            hist = stock.history(
                period=period,
                auto_adjust=False
            )

            if (
                hist is None
                or
                hist.empty
            ):

                continue


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
                f"{ticker} 歷史資料抓取失敗：{e}"
            )


    return (
        "",
        None,
        pd.DataFrame()
    )


# ============================================================
# 7. 今日分時資料
# ============================================================

# 注意：
# 這個函數不要使用 300 秒 cache
# 因為我們要讓它持續更新

def fetch_intraday(ticker):

    try:

        stock = yf.Ticker(
            ticker
        )

        intraday = stock.history(
            period="1d",
            interval="1m",
            auto_adjust=False,
            prepost=False
        )

        if (
            intraday is None
            or
            intraday.empty
        ):

            return pd.DataFrame()


        return intraday


    except Exception as e:

        print(
            f"{ticker} 即時資料抓取失敗：{e}"
        )

        return pd.DataFrame()


# ============================================================
# 8. 主畫面
# ============================================================

current_target = (
    st.session_state
    .current_search
    .strip()
    .upper()
)


if current_target:

    with st.spinner(
        f"正在取得 {current_target} 資料..."
    ):

        short_name, actual_ticker, hist = fetch_stock(
            current_target,
            period
        )


    # ========================================================
    # 有找到股票
    # ========================================================

    if not hist.empty:

        # ----------------------------------------------------
        # 基本價格
        # ----------------------------------------------------

        current_price = float(
            hist["Close"].iloc[-1]
        )


        if len(hist) > 1:

            prev_price = float(
                hist["Close"].iloc[-2]
            )

        else:

            prev_price = current_price


        price_change = (
            current_price
            -
            prev_price
        )


        if prev_price != 0:

            pct_change = (
                price_change
                /
                prev_price
                *
                100
            )

        else:

            pct_change = 0


        today_open = float(
            hist["Open"].iloc[-1]
        )

        today_high = float(
            hist["High"].iloc[-1]
        )

        today_low = float(
            hist["Low"].iloc[-1]
        )

        volume = float(
            hist["Volume"].iloc[-1]
        )


        # ====================================================
        # 9. 標題 + 加入觀察清單
        # ====================================================

        col_title, col_button = st.columns(
            [4, 1]
        )


        with col_title:

            st.markdown(
                f"## 📈 {actual_ticker}　{short_name}"
            )


        with col_button:

            watchlist_code = (
                current_target
                .replace(".TW", "")
                .replace(".TWO", "")
            )


            if (
                watchlist_code
                in
                st.session_state.watchlist
            ):

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


        # ====================================================
        # 10. 股價資訊
        # ====================================================

        if price_change > 0:

            delta_text = (
                f"+{price_change:.2f} "
                f"(+{pct_change:.2f}%)"
            )

        else:

            delta_text = (
                f"{price_change:.2f} "
                f"({pct_change:.2f}%)"
            )


        st.metric(
            label="目前股價 / 最新收盤",
            value=f"{current_price:.2f}",
            delta=delta_text
        )


        st.divider()


        # ====================================================
        # 11. 四宮格
        # ====================================================

        col1, col2, col3, col4 = st.columns(
            4
        )


        with col1:

            st.metric(
                "開盤價",
                f"{today_open:.2f}"
            )


        with col2:

            st.metric(
                "昨收價",
                f"{prev_price:.2f}"
            )


        with col3:

            st.metric(
                "最高價",
                f"{today_high:.2f}"
            )


        with col4:

            st.metric(
                "最低價",
                f"{today_low:.2f}"
            )


        st.metric(
            "成交量",
            f"{volume:,.0f}"
        )


        st.divider()


        # ====================================================
        # 12. Tab
        # ====================================================

        tab1, tab2 = st.tabs(
            [
                "⚡ 今日分時走勢",
                "📊 歷史 K 線"
            ]
        )


        # ====================================================
        # 13. 今日分時
        # ====================================================

        with tab1:

            st.caption(
                "畫面每 10 秒自動更新；"
                "Yahoo / yfinance 分時資料最細約為 1 分鐘。"
            )


            # ------------------------------------------------
            # Streamlit Fragment
            # ------------------------------------------------

            @st.fragment(
                run_every="10s"
            )
            def live_stock_chart():

                intraday = fetch_intraday(
                    actual_ticker
                )


                if intraday.empty:

                    st.warning(
                        "目前沒有取得今日分時資料。"
                    )

                    return


                # ============================================
                # 最新股價
                # ============================================

                latest_price = float(
                    intraday["Close"].iloc[-1]
                )


                day_open = float(
                    intraday["Open"].iloc[0]
                )


                day_high = float(
                    intraday["High"].max()
                )


                day_low = float(
                    intraday["Low"].min()
                )


                day_volume = float(
                    intraday["Volume"].sum()
                )


                change = (
                    latest_price
                    -
                    prev_price
                )


                if prev_price != 0:

                    change_pct = (
                        change
                        /
                        prev_price
                        *
                        100
                    )

                else:

                    change_pct = 0


                # ============================================
                # 最新資料時間
                # ============================================

                latest_time = (
                    intraday
                    .index[-1]
                )


                try:

                    time_text = (
                        latest_time
                        .strftime(
                            "%Y/%m/%d %H:%M"
                        )
                    )

                except Exception:

                    time_text = str(
                        latest_time
                    )


                # ============================================
                # 即時資訊
                # ============================================

                live_col1, live_col2, live_col3 = st.columns(
                    3
                )


                if change > 0:

                    live_delta = (
                        f"+{change:.2f} "
                        f"(+{change_pct:.2f}%)"
                    )

                else:

                    live_delta = (
                        f"{change:.2f} "
                        f"({change_pct:.2f}%)"
                    )


                with live_col1:

                    st.metric(
                        "最新價格",
                        f"{latest_price:.2f}",
                        live_delta
                    )


                with live_col2:

                    st.metric(
                        "今日開盤",
                        f"{day_open:.2f}"
                    )


                with live_col3:

                    st.metric(
                        "資料時間",
                        time_text
                    )


                live_col4, live_col5, live_col6 = st.columns(
                    3
                )


                with live_col4:

                    st.metric(
                        "今日最高",
                        f"{day_high:.2f}"
                    )


                with live_col5:

                    st.metric(
                        "今日最低",
                        f"{day_low:.2f}"
                    )


                with live_col6:

                    st.metric(
                        "累計成交量",
                        f"{day_volume:,.0f}"
                    )


                # ============================================
                # 決定上漲 / 下跌顏色
                # ============================================

                if latest_price >= prev_price:

                    line_color = "#ef5350"

                else:

                    line_color = "#26a69a"


                # ============================================
                # 分時價格圖
                # ============================================

                live_fig = go.Figure()


                live_fig.add_trace(

                    go.Scatter(

                        x=intraday.index,

                        y=intraday["Close"],

                        mode="lines",

                        name="成交價",

                        line=dict(
                            width=2,
                            color=line_color
                        )
                    )
                )


                # ============================================
                # 昨收線
                # ============================================

                live_fig.add_hline(

                    y=prev_price,

                    line_dash="dash",

                    line_color="#aaaaaa",

                    annotation_text=(
                        f"昨收 {prev_price:.2f}"
                    ),

                    annotation_position=(
                        "top left"
                    )
                )


                # ============================================
                # 分時圖 Layout
                # ============================================

                live_fig.update_layout(

                    template="plotly_dark",

                    height=480,

                    margin=dict(
                        l=10,
                        r=10,
                        t=30,
                        b=10
                    ),

                    hovermode="x unified",

                    xaxis_title="時間",

                    yaxis_title="股價",

                    showlegend=True
                )


                live_fig.update_xaxes(

                    rangeslider_visible=False,

                    showgrid=True
                )


                live_fig.update_yaxes(

                    showgrid=True
                )


                st.plotly_chart(

                    live_fig,

                    use_container_width=True,

                    key=(
                        f"live_price_"
                        f"{actual_ticker}"
                    )
                )


                # ============================================
                # 成交量
                # ============================================

                volume_fig = go.Figure()


                volume_fig.add_trace(

                    go.Bar(

                        x=intraday.index,

                        y=intraday["Volume"],

                        name="成交量"
                    )
                )


                volume_fig.update_layout(

                    template="plotly_dark",

                    height=220,

                    margin=dict(
                        l=10,
                        r=10,
                        t=20,
                        b=10
                    ),

                    xaxis_title="",

                    yaxis_title="成交量",

                    showlegend=False
                )


                st.plotly_chart(

                    volume_fig,

                    use_container_width=True,

                    key=(
                        f"live_volume_"
                        f"{actual_ticker}"
                    )
                )


                st.caption(
                    "🔄 此區塊每 10 秒自動重新抓取資料"
                )


            live_stock_chart()


        # ====================================================
        # 14. 歷史 K 線
        # ====================================================

        with tab2:

            st.subheader(
                f"📊 K 線圖（{period}）"
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

                    # 台灣股市
                    # 上漲紅色
                    increasing_line_color="#ef5350",

                    # 下跌綠色
                    decreasing_line_color="#26a69a",

                    increasing_fillcolor="#ef5350",

                    decreasing_fillcolor="#26a69a"
                )
            )


            fig.update_layout(

                template="plotly_dark",

                xaxis_rangeslider_visible=False,

                height=500,

                margin=dict(
                    l=10,
                    r=10,
                    t=30,
                    b=10
                ),

                hovermode="x unified",

                xaxis_title="日期",

                yaxis_title="股價"
            )


            st.plotly_chart(

                fig,

                use_container_width=True,

                key=(
                    f"historical_"
                    f"{actual_ticker}_"
                    f"{period}"
                )
            )


    # ========================================================
    # 股票不存在
    # ========================================================

    else:

        st.error(
            f"找不到代號「{current_target}」的股票。"
        )

        st.info(
            "台股可直接輸入 2330、0050、006208；"
            "美股可輸入 AAPL、VOO、NVDA。"
        )
