import streamlit as st
import yfinance as yf

# 設定網頁標題與外觀
st.set_page_config(page_title="我的專屬看盤室", page_icon="📈")
st.title("📈 每日股價追蹤儀表板")
st.markdown("歡迎來到您的個人股票網站！")

# 讓使用者輸入股票代碼
ticker = st.text_input("請輸入股票代碼 (台股請加 .TW，如 2330.TW；美股如 AAPL):", "2330.TW")

if ticker:
    with st.spinner('抓取最新資料中...'):
        try:
            # 抓取過去 3 個月的資料
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo")
            
            if not hist.empty:
                # 取得最新收盤價
                last_price = hist['Close'].iloc[-1]
                st.subheader(f"🏷️ {ticker} 最新收盤價: {last_price:.2f}")
                
                # 畫出走勢圖
                st.line_chart(hist['Close'])
            else:
                st.error("找不到該股票的資料，請確認代碼是否輸入正確 (台股記得加 .TW 喔！)")
        except Exception as e:
            st.error("系統發生一點小錯誤，請確認股票代碼或稍後再試。")
