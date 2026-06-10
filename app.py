import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="✨ RM New x Ae 💕 Phi Vic 🐱", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 4px solid #4e2a84; }
    h1, h2, h3 { color: #4e2a84; }
    .script-box { background-color: #e2d9f3; padding: 20px; border-radius: 10px; border-left: 5px solid #4e2a84; margin-bottom: 20px; font-size: 16px; line-height: 1.6;}
    .scan-box { background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 1px solid #4caf50; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ RM New x Ae 💖 (มีพี่วิคเหมียวร่วมคุมพอร์ต 🐱🐾): ระบบสแกนหุ้นทำเงิน 🚀📊")
st.caption("อัปเดตข้อมูล Real-time | วิเคราะห์ด้วย Demand/Supply Zone, SMC Logic และปัจจัยพื้นฐาน")

# ลิสต์หุ้นแนะนำเบื้องต้น
popular_stocks = ["PTT", "AOT", "KBANK", "CPALL", "ADVANC", "BBL", "SCB", "SCC", "BDMS", "GULF", "DELTA", "CPN", "MINT", "KTB", "OR", "TISCO", "WHA", "TRUE"]

# --- แถบเครื่องมือด้านข้าง (Sidebar) สำหรับสแกนหุ้น ---
with st.sidebar:
    st.header("🎯 ระบบสแกนหาหุ้นน่าช้อนซื้อ")
    st.write("กดปุ่มด้านล่างเพื่อสแกนหาหุ้นที่ราคาลงมาในโซนถูก (Oversold) จากลิสต์หุ้นยอดฮิต")
    if st.button("🔍 เริ่มสแกนหุ้นเดี๋ยวนี้", use_container_width=True):
        with st.spinner('พี่วิคกำลังดมกลิ่นหาหุ้นทำเงิน...'):
            recommended = []
            # สแกนแบบเร็วๆ ย้อนหลัง 1 เดือน
            for sym in popular_stocks:
                try:
                    tk = yf.Ticker(f"{sym}.BK")
                    hist = tk.history(period="1mo")
                    if not hist.empty:
                        # คำนวณ RSI แบบง่าย
                        delta = hist['Close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                        rs = gain / loss
                        rsi = 100 - (100 / (1 + rs))
                        curr_rsi = rsi.iloc[-1]
                        
                        if curr_rsi < 40: # หาตัวที่เริ่มถูกหรือถูกมาก
                            recommended.append({'หุ้น': sym, 'ราคา': hist['Close'].iloc[-1], 'RSI': curr_rsi})
                except:
                    pass
            
            if recommended:
                st.success("✅ เจอหุ้นเข้าเกณฑ์แล้ว!")
                df_rec = pd.DataFrame(recommended).sort_values(by='RSI')
                st.dataframe(df_rec.style.format({'ราคา': '{:.2f}', 'RSI': '{:.2f}'}), hide_index=True)
                st.write("*💡 สามารถนำชื่อหุ้นเหล่านี้ไปพิมพ์ค้นหาในระบบหลักเพื่อดูแผนเทรดแบบละเอียดได้เลยครับ*")
            else:
                st.info("ยังไม่มีหุ้นตัวไหนลงมาในโซนถูกจัดๆ ในช่วงนี้ครับ (ตลาดอาจจะตึง)")

# --- ส่วนรับอินพุตหลัก ---
col1, col2 = st.columns([1, 2])
with col1:
    search_mode = st.radio("วิธีค้นหาหุ้น:", ["📋 เลือกจากรายชื่อยอดฮิต", "✍️ พิมพ์ชื่อหุ้นเอง"])
    if search_mode == "📋 เลือกจากรายชื่อยอดฮิต":
        stock_symbol = st.selectbox("เลือกหุ้นที่ต้องการวิเคราะห์", popular_stocks)
    else:
        stock_symbol = st.text_input("พิมพ์ชื่อหุ้นไทย (ไม่ต้องใส่ .BK)", value="PTT").upper()

with col2:
    period = st.select_slider("เลือกช่วงเวลาย้อนหลังเพื่อดูกราฟ", options=["3mo", "6mo", "1y", "2y"], value="6mo")

st.divider()

if stock_symbol:
    full_symbol = f"{stock_symbol}.BK"
    
    try:
        ticker = yf.Ticker(full_symbol)
        data = ticker.history(period=period)
        
        if data.empty:
            st.error("ไม่พบข้อมูลหุ้นตัวนี้ กรุณาลองตรวจสอบตัวสะกดอีกครั้ง")
        else:
            close_data = data['Close'].squeeze()
            
            # --- ดึงข้อมูลพื้นฐาน (Fundamental) ---
            info = ticker.info
            pe_ratio = info.get('trailingPE', 'N/A')
            div_yield = info.get('dividendYield', 'N/A')
            if div_yield != 'N/A' and div_yield is not None:
                div_yield = f"{(div_yield * 100):.2f}%"
            else:
                div_yield = "ไม่มีข้อมูล"
                
            if type(pe_ratio) == float:
                pe_ratio = f"{pe_ratio:.2f} เท่า"

            # --- คำนวณ Technical & SMC Zones ---
            delta = close_data.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            recent_20d = data.tail(20)
            supply_zone = recent_20d['High'].max() 
            demand_zone = recent_20d['Low'].min()  
            pivot_point = (supply_zone + demand_zone + close_data.iloc[-1]) / 3
            
            current_price = float(close_data.iloc[-1])
            prev_price = float(close_data.iloc[-2])
            price_diff = current_price - prev_price
            current_rsi = float(data['RSI'].iloc[-1])
            
            # --- สร้าง Dashboard สรุปตัวเลข ---
            st.subheader(f"สรุปข้อมูลหุ้น {stock_symbol}")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("ราคาปัจจุบัน", f"{current_price:,.2f} ฿", f"{price_diff:,.2f}")
            m2.metric("RSI (ความร้อนแรง)", f"{current_rsi:.2f}", "Oversold" if current_rsi < 30 else "Overbought" if current_rsi > 70 else "Neutral", delta_color="off")
            m3.metric("Demand (แนวรับ)", f"{demand_zone:,.2f} ฿")
            m4.metric("Supply (แนวต้าน)", f"{supply_zone:,.2f} ฿")
            m5.metric("ปันผล / P/E", f"{div_yield}", f"P/E: {pe_ratio}", delta_color="off")

            # --- ตรรกะการวิเคราะห์สไตล์คุณพอล (Market Psychology) ---
            if current_rsi < 30:
                mood = "ตลาดกำลังอยู่ในสภาวะ 'ตื่นตระหนก' (Panic) ขาดสภาพคล่องทางฝั่งซื้อ ทำให้ราคาไหลลงมาทดสอบ Demand Zone"
                action_plan = "ทยอยสะสม (Accumulate)"
                script = f"คุณลูกค้าครับ วันนี้ผมกับทีมงาน (รวมถึงพี่วิค 🐱) สแกนเจอว่า {stock_symbol} ปรับตัวลงมาอยู่ในโซนที่น่าสนใจมากครับ แถวๆ **{demand_zone:.2f} บาท** สภาวะตอนนี้รายย่อยกำลังตกใจเทขาย แต่ในมุมมองของการลงทุน นี่คือโอกาสในการเก็บของดีราคาถูกครับ แถมหุ้นตัวนี้มีปันผลระดับ **{div_yield}** ไว้เป็นเบาะรองรับด้วย\n\n**แผนของเราคือ:** ทยอยเข้าซื้อไม้แรกแถวนี้เลยครับ และตั้งจุด Cut Loss เผื่อผิดทางไว้ที่ **{(demand_zone * 0.98):.2f} บาท** ส่วนเป้าหมายทำกำไรระยะสั้น เรามองไปที่การปิดแกปด้านบนแถว **{pivot_point:.2f} บาท** ครับ"
            
            elif current_rsi > 70:
                mood = "ตลาดกำลังอยู่ในสภาวะ 'โลภ' (Greed) มีแรงไล่ซื้อจนราคาแพงเกินไป (Overbought) เสี่ยงโดน Smart Money เทขายใส่"
                action_plan = "ถือรันเทรนด์ / ทยอยทำกำไร (Take Profit)"
                script = f"คุณลูกค้าครับ ตอนนี้ผมอยากให้เราระมัดระวังกับ {stock_symbol} นิดนึงครับ ราคามันวิ่งขึ้นมาทดสอบ Supply Zone ที่ **{supply_zone:.2f} บาท** แล้ว อินดิเคเตอร์ฟ้องว่าตลาดไล่ราคาจนตึงมากไปแล้ว\n\n**แผนของเราคือ:** ถ้าคุณลูกค้ายังไม่มีของ **'ห้ามไล่ราคาเด็ดขาด'** ครับ รอให้ตลาดย่อตัวสร้างฐานใหม่ก่อน แต่ถ้าเรามีของอยู่ในมือมาตั้งแต่ต้นทาง จุดนี้คือจุดที่ผมแนะนำให้ **'แบ่งขายล็อกกำไรเข้ากระเป๋าซัก 30-50%'** ครับ แล้วส่วนที่เหลือปล่อยให้มันรันเทรนด์ทำเงินต่อไปครับ"
            
            else:
                if current_price > data['Close'].ewm(span=20, adjust=False).mean().iloc[-1]:
                    mood = "ราคายกตัวขึ้นอย่างมีโครงสร้าง (Bullish Structure) ตลาดกำลังซึมซับแรงซื้ออย่างค่อยเป็นค่อยไป"
                    action_plan = "ถือต่อไป (Let Profit Run)"
                    script = f"สภาวะของ {stock_symbol} ตอนนี้ดูดีเลยครับคุณลูกค้า ราคาสามารถยืนเหนือเส้นค่าเฉลี่ยและรักษาโครงสร้างขาขึ้นได้มั่นคง ตลาดกำลังค่อยๆ เลือกทางไปต่อ\n\n**แผนของเราคือ:** แนะนำให้ **'ถือต่อไป (Hold)'** ครับ แนวโน้มยังมีโอกาสไปทดสอบแนวต้านด้านบนที่ **{supply_zone:.2f} บาท** ตราบใดที่ราคายังไม่หลุดแนวรับที่ **{demand_zone:.2f} บาท** เราสามารถปล่อยให้กำไรมันทำงานได้อย่างสบายใจครับ"
                else:
                    mood = "ราคายังอยู่ในช่วงพักตัว สะสมพลัง (Consolidation) ยังไม่มีการเบรกโครงสร้างราคาที่ชัดเจน"
                    action_plan = "รอดูความชัดเจน (Wait & See)"
                    script = f"สำหรับ {stock_symbol} ตอนนี้ กราฟกำลังอยู่ในช่วงพักตัวเพื่อสะสมพลังครับ รายใหญ่กำลังฟอร์มตัวเก็บของ ราคายังแกว่งอยู่ในกรอบแคบๆ\n\n**แผนของเราคือ:** ผมแนะนำให้ **'Wait & See'** รอดูความชัดเจนไปก่อนครับ เรายังไม่ต้องรีบเอาเงินไปจมรอ ถ้าอยากจะเข้าจริงๆ ผมอยากให้รอราคาลงมาใกล้ๆ โซน Liquidity ด้านล่างที่ **{demand_zone:.2f} บาท** จะเป็นจุดที่เราได้เปรียบเรื่องต้นทุนที่สุดครับ"

            # --- แสดงผล Script คุยกับลูกค้า ---
            st.markdown("### 🎙️ สคริปต์พูดคุยกับลูกค้า (พร้อมเสิร์ฟ)")
            st.markdown(f"<div class='script-box'>{script}</div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            c1.write(f"**🧠 สภาวะตลาด (Market Mood):** {mood}")
            c2.write(f"**🎯 สรุป Action Plan:** :blue[{action_plan}]")

            # --- สร้างกราฟเทคนิคอล (แท่งเทียน + Volume) ---
            st.markdown(f"#### 📊 กราฟวิเคราะห์โครงสร้างราคา & ปริมาณการซื้อขาย ({stock_symbol})")
            
            # ใช้ make_subplots เพื่อแยกส่วนราคาและ Volume
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                vertical_spacing=0.03, subplot_titles=('Price & Zones', 'Volume'), 
                                row_width=[0.2, 0.7])

            # กราฟราคา
            fig.add_trace(go.Candlestick(x=data.index,
                            open=data['Open'].squeeze(), high=data['High'].squeeze(),
                            low=data['Low'].squeeze(), close=close_data, name="ราคา"), row=1, col=1)
            
            data['EMA20'] = close_data.ewm(span=20, adjust=False).mean()
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], line=dict(color='orange', width=1), name="Trend (EMA 20)"), row=1, col=1)
            
            # เส้น Zone
            fig.add_hline(y=supply_zone, line_dash="dot", line_color="red", annotation_text="Supply Zone", row=1, col=1)
            fig.add_hline(y=demand_zone, line_dash="dot", line_color="green", annotation_text="Demand Zone", row=1, col=1)

            # กราฟ Volume
            colors = ['red' if row['Open'] - row['Close'] >= 0 else 'green' for index, row in data.iterrows()]
            fig.add_trace(go.Bar(x=data.index, y=data['Volume'], marker_color=colors, name='Volume'), row=2, col=1)

            fig.update_layout(template="plotly_white", height=650, margin=dict(l=0, r=0, t=30, b=0), showlegend=False)
            fig.update_xaxes(rangeslider_visible=False) # ปิด slider ด้านล่างกราฟราคาเพื่อความสะอาดตา
            st.plotly_chart(fig, use_container_width=True)

            # --- ระบบดึงข่าวสารอัตโนมัติ ---
            st.divider()
            st.markdown("### 📰 ข่าวสารและปัจจัยพื้นฐานล่าสุด")
            st.caption("ดึงข้อมูลอัตโนมัติจากฐานข้อมูลสากล (Yahoo Finance)")
            
            news_items = ticker.news
            if news_items:
                for n in news_items[:5]:
                    title = n.get('title', 'ไม่มีหัวข้อข่าว')
                    link = n.get('link', '#')
                    publisher = n.get('publisher', 'Unknown Publisher')
                    import datetime
                    pub_time = n.get('providerPublishTime')
                    if pub_time:
                        date_str = datetime.datetime.fromtimestamp(pub_time).strftime('%Y-%m-%d %H:%M')
                    else:
                        date_str = "Recent"
                        
                    st.write(f"▪️ [{title}]({link}) - *{publisher} ({date_str})*")
            else:
                st.info("ขณะนี้ไม่มีข่าวอัปเดตล่าสุดบนระบบสำหรับหุ้นตัวนี้ครับ")

    except Exception as e:
        st.error(f"ระบบกำลังวิเคราะห์ข้อมูล หรือกรอกชื่อหุ้นไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง... ({e})")
