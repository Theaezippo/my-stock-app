import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="SCB RM Stock Assistant", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #4e2a84; }
    </style>
    """, unsafe_allow_index=True)

st.title("💜 ระบบช่วยวิเคราะห์หุ้นไทย (RM Edition)")
st.caption("ข้อมูลจาก Yahoo Finance (ดีเลย์ 15 นาที) | สำหรับช่วยสกรีนหุ้นเบื้องต้น")

col1, col2 = st.columns([1, 3])
with col1:
    stock_symbol = st.text_input("พิมพ์ชื่อหุ้นไทย (เช่น PTT, CPALL)", value="PTT").upper()
    period = st.select_slider("เลือกช่วงเวลาย้อนหลัง", options=["3mo", "6mo", "1y", "2y"], value="6mo")

if stock_symbol:
    full_symbol = f"{stock_symbol}.BK"
    
    try:
        data = yf.download(full_symbol, period=period, interval="1d")
        
        if data.empty:
            st.error("ไม่พบข้อมูลหุ้นตัวนี้ กรุณาลองตรวจสอบตัวสะกดอีกครั้ง")
        else:
            # คำนวณ RSI แบบเขียนสูตรเอง (ไม่ใช้ pandas-ta แล้ว จะได้ไม่เออเร่อ)
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            current_price = data['Close'].iloc[-1].item()
            prev_price = data['Close'].iloc[-2].item()
            price_diff = current_price - prev_price
            current_rsi = data['RSI'].iloc[-1].item()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("ราคาปัจจุบัน", f"{current_price:,.2f} THB", f"{price_diff:,.2f}")
            
            with m2:
                if current_rsi < 30:
                    st.success("✅ สัญญาณ: น่าช้อนซื้อ (Oversold)")
                elif current_rsi > 70:
                    st.warning("⚠️ สัญญาณ: ระวัง (Overbought)")
                else:
                    st.info("📊 สัญญาณ: ปกติ (Neutral)")
            
            m3.metric("RSI (14)", f"{current_rsi:.2f}")

            fig = go.Figure(data=[go.Candlestick(x=data.index,
                            open=data['Open'], high=data['High'],
                            low=data['Low'], close=data['Close'], name="ราคา")])
            
            # คำนวณ EMA20 แบบสูตรดั้งเดิม
            data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], line=dict(color='orange', width=1), name="EMA 20"))

            fig.update_layout(title=f"กราฟหุ้น {stock_symbol}", yaxis_title="ราคา (บาท)", template="plotly_white", height=500)
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("💡 มุมมองสำหรับ RM")
            c1, c2 = st.columns(2)
            with c1:
                st.write("**กลยุทธ์แนะนำสำหรับลูกค้า:**")
                if current_rsi < 35:
                    st.write("- หุ้นอยู่ในโซนราคาถูก มีโอกาสเด้งกลับสูง เหมาะกับการแนะนำลูกค้าทยอยสะสม")
                elif current_rsi > 65:
                    st.write("- หุ้นขึ้นมาเยอะเกินไปแล้ว ไม่แนะนำให้ไล่ราคา เสี่ยงติดดอย ควรรอจังหวะย่อตัว")
                else:
                    st.write("- ราคาพักตัวในกรอบปกติ สามารถถือหรือรอเลือกข้างเทรนด์")
            with c2:
                st.write("**ข้อควรระวัง:**")
                st.write("- โปรดตรวจสอบข่าวสารหรือประกาศงบการเงินประกอบ")
                st.write("- ข้อมูลดีเลย์ 15 นาที ไม่เหมาะกับการเทรดไวแบบ Day Trade")

    except Exception as e:
        st.error(f"ระบบกำลังดึงข้อมูล กรุณารอสักครู่... ({e})")
