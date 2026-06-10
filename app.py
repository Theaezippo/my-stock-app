import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="✨ RM New x Ae 💕 P' Vic 🐱", layout="wide", page_icon="💜")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 4px solid #4e2a84; }
    h1, h2, h3 { color: #4e2a84; }
    .script-box { background-color: #f3eef9; padding: 25px; border-radius: 12px; border-left: 6px solid #4e2a84; margin-bottom: 20px; font-size: 16px; line-height: 1.8;}
    .fwd-box { background-color: #fff0e6; padding: 25px; border-radius: 12px; border-left: 6px solid #e87722; margin-bottom: 20px; font-size: 16px; line-height: 1.8;}
    .news-box { background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 4px solid #d9534f; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    </style>
    """, unsafe_allow_html=True)

# --- แถบเมนูด้านข้าง ---
st.sidebar.markdown("## 💜 SCB Wealth & FWD")
st.sidebar.title("🗂️ โหมดการทำงาน")
app_mode = st.sidebar.radio("เลือกโหมดสำหรับให้บริการลูกค้า:", 
                            ["📈 โหมดการลงทุน (Wealth Allocation)", "🛡️ โหมดประกันสุขภาพ/ชีวิต (FWD)"])

st.sidebar.divider()
st.sidebar.caption("👨‍💻 พัฒนาโดย: เอ้ & นิว (มีพี่วิคลูกชาย 🐱 คอยให้กำลังใจ)")

# ==========================================
# โหมดที่ 1: การลงทุน (Wealth & Investment)
# ==========================================
if app_mode == "📈 โหมดการลงทุน (Wealth Allocation)":
    
    # 1. ริบบิ้นราคาหุ้นวิ่งๆ (Ticker Tape)
    components.html(
        """
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
          {
          "symbols": [
            {"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"},
            {"proName": "FOREXCOM:NSXUSD", "title": "Nasdaq 100"},
            {"proName": "FX_IDC:THBUSD", "title": "USD/THB (บาท)"},
            {"proName": "OANDA:XAUUSD", "title": "Gold (ทองคำ)"},
            {"description": "WTI Crude", "proName": "OANDA:WTICOUSD"}
          ],
          "showSymbolLogo": true, "colorTheme": "light", "isTransparent": true, "displayMode": "adaptive", "locale": "th_TH"
          }
          </script>
        </div>
        """, height=75
    )

    st.title("✨ RM New x Ae 💖: ระบบวางแผนพอร์ตการลงทุน")
    
    # แบ่งหน้าจอเป็น 3 แท็บ
    tab1, tab2, tab3 = st.tabs(["🎯 จัดพอร์ตรายตัว", "📰 ข่าวสารภาษาไทย & เรดาร์ตลาด", "💱 ค่าเงินบาท & ปฏิทิน"])

    # ------------------------------------
    # แท็บที่ 1: วิเคราะห์รายตัว 
    # ------------------------------------
    with tab1:
        with st.expander("🎯 กดตรงนี้เพื่อเปิดระบบสแกนหาสินทรัพย์น่าช้อนซื้อ (Quick Scan)"):
            if st.button("🔍 เริ่มสแกนเดี๋ยวนี้", use_container_width=True):
                with st.spinner('พี่วิคกำลังดมกลิ่นหาจังหวะเข้า...'):
                    scan_list = {"PTT":"PTT.BK", "AOT":"AOT.BK", "CPALL":"CPALL.BK", "SPY":"SPY", "QQQ":"QQQ", "GOLD":"XAUUSD=X"}
                    recommended = []
                    for name, sym in scan_list.items():
                        try:
                            tk = yf.Ticker(sym)
                            hist = tk.history(period="1mo")
                            if not hist.empty:
                                delta = hist['Close'].diff()
                                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                                rs = gain / loss
                                curr_rsi = (100 - (100 / (1 + rs))).iloc[-1]
                                if curr_rsi < 40: 
                                    recommended.append({'สินทรัพย์': name, 'ราคาล่าสุด': hist['Close'].iloc[-1], 'RSI': curr_rsi})
                        except:
                            pass
                    if recommended:
                        st.success("✅ เจอสินทรัพย์ที่น่าสนใจแล้ว!")
                        st.dataframe(pd.DataFrame(recommended).sort_values(by='RSI').style.format({'ราคาล่าสุด': '{:.2f}', 'RSI': '{:.2f}'}), hide_index=True)
                    else:
                        st.info("ตลาดกำลังตึงตัว ยังไม่มีสินทรัพย์ไหนลงมาในโซนน่าช้อนครับ")

        asset_class = st.radio("เลือกประเภทสินทรัพย์ที่ต้องการนำเสนอ:", 
                               ["🇹🇭 หุ้นไทย", "🇺🇸 หุ้นระดับโลก & ETF", "🛢️ สินทรัพย์ทางเลือก (ทอง, น้ำมัน, จีน)", "🏦 กองทุน SCB & หุ้นกู้"], horizontal=True)

        if asset_class in ["🇹🇭 หุ้นไทย", "🇺🇸 หุ้นระดับโลก & ETF", "🛢️ สินทรัพย์ทางเลือก (ทอง, น้ำมัน, จีน)"]:
            c1, c2 = st.columns([1, 2])
            with c1:
                if asset_class == "🇹🇭 หุ้นไทย":
                    stock_input = st.selectbox("เลือกหุ้น", ["PTT", "AOT", "KBANK", "CPALL", "ADVANC", "BBL", "SCB", "SCC", "BDMS", "GULF", "DELTA"])
                    full_symbol = f"{stock_input}.BK"
                    asset_name = stock_input
                elif asset_class == "🇺🇸 หุ้นระดับโลก & ETF":
                    stock_input = st.selectbox("เลือกหุ้น/ETF", ["SPY (S&P 500 ETF)", "QQQ (Nasdaq ETF)", "AAPL", "MSFT", "NVDA", "TSLA"]).split(" ")[0]
                    full_symbol = stock_input
                    asset_name = stock_input
                else:
                    alt_assets = {"ทองคำ (XAUUSD)": "XAUUSD=X", "น้ำมันดิบ (WTI)": "CL=F", "ETF หุ้นจีน (FXI)": "FXI"}
                    selected_alt = st.selectbox("เลือกสินทรัพย์:", list(alt_assets.keys()))
                    full_symbol = alt_assets[selected_alt]
                    asset_name = selected_alt

            with c2:
                period = st.select_slider("เลือกมุมมองระยะเวลา", options=["3mo", "6mo", "1y", "3y"], value="6mo")

            if full_symbol:
                try:
                    data = yf.Ticker(full_symbol).history(period=period)
                    if not data.empty:
                        close_data = data['Close'].squeeze()
                        current_price = float(close_data.iloc[-1])
                        recent_high, recent_low = close_data.max(), close_data.min()
                        drawdown = ((current_price - recent_high) / recent_high) * 100
                        
                        m1, m2, m3 = st.columns(3)
                        m1.metric("ราคาปัจจุบัน", f"{current_price:,.2f}")
                        m2.metric("จุดสูงสุดรอบที่เลือก (High)", f"{recent_high:,.2f}")
                        m3.metric("ส่วนลดจากจุดสูงสุด (Drawdown)", f"{drawdown:.2f}%", "น่าทยอยสะสม" if drawdown < -15 else "ราคาตึงตัว", delta_color="off")

                        st.markdown("### 🎙️ บทสนทนาแนะนำลูกค้า (RM Wealth Talk)")
                        if asset_class == "🛢️ สินทรัพย์ทางเลือก (ทอง, น้ำมัน, จีน)":
                            script = f"พี่คะ นิวขออนุญาตอัปเดตภาพรวมนะคะ สภาวะโลกมีความไม่แน่นอนสูง นิวแนะนำให้มี **{asset_name}** ติดพอร์ตไว้เพื่อเป็น 'เบาะกันกระแทก' และกระจายความเสี่ยงค่ะ เผื่อเกิดเหตุการณ์ไม่คาดฝัน พอร์ตจะได้ยังปลอดภัยค่ะ"
                        elif drawdown < -15:
                            script = f"สวัสดีค่ะพี่ นิวติดตาม **{asset_name}** ให้นะคะ ราคาปรับฐานลงมา {abs(drawdown):.1f}% นิวและทีมมองว่าเป็น **'โอกาสทองในการทยอยสะสม'** นิวแบ่งไม้เข้าให้ดีไหมคะ จะได้ต้นทุนเฉลี่ยสวยๆ ค่ะ"
                        elif drawdown > -5:
                            script = f"พี่คะ ตอนนี้ราคาวิ่งขึ้นมาใกล้จุดสูงสุดแล้ว เพื่อวินัยที่ดี นิวแนะนำให้ทำ **Portfolio Rebalancing** ดีไหมคะ? ทยอยรินขายทำกำไรบางส่วน เอาเงินสดมารอจังหวะตลาดปรับฐานค่ะ"
                        else:
                            script = f"ภาพรวม **{asset_name}** ยังเกาะเทรนด์ได้ดีค่ะ นิวแนะนำให้ **'ถือลงทุนต่อเนื่อง (Hold)'** ได้สบายใจเลยค่ะ นิวจะคอยมอนิเตอร์ข่าวสำคัญให้ตลอด ถ้าระบบมีสัญญาณเตือนเมื่อไหร่ นิวรีบแจ้งทันทีเลยค่ะ"

                        st.markdown(f"<div class='script-box'>👩‍💼 <b>นิว:</b><br><br>\"{script}\"</div>", unsafe_allow_html=True)

                        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.7])
                        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'].squeeze(), high=data['High'].squeeze(), low=data['Low'].squeeze(), close=close_data), row=1, col=1)
                        data['EMA50'] = close_data.ewm(span=50, adjust=False).mean()
                        fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], line=dict(color='orange', dash='dot')), row=1, col=1)
                        
                        if 'Volume' in data.columns and data['Volume'].sum() > 0:
                            colors = ['red' if r['Open'] - r['Close'] >= 0 else 'green' for i, r in data.iterrows()]
                            fig.add_trace(go.Bar(x=data.index, y=data['Volume'], marker_color=colors), row=2, col=1)
                        else:
                            fig.update_layout(yaxis2=dict(visible=False))

                        fig.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
                        fig.update_xaxes(rangeslider_visible=False) 
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error("ระบบกำลังโหลดข้อมูล กรุณารอสักครู่...")

        # -----------------------------------------------------
        # แก้ไข: ดึงระบบกองทุน SCB แบบเต็มสูบกลับมาแล้วครับ!
        # -----------------------------------------------------
        elif asset_class == "🏦 กองทุน SCB & หุ้นกู้":
            st.subheader("📚 คลังข้อมูลกองทุนเด่น & หุ้นกู้ (Pitching Guide)")
            fund_type = st.selectbox("เลือกประเภทผลิตภัณฑ์ที่ต้องการนำเสนอ:", 
                                     ["กองทุนหุ้นสหรัฐฯ / S&P500 (SCBS&P500)", 
                                      "กองทุนเทคโนโลยี / AI (SCBNDQ / SCBSEMI)", 
                                      "กองทุนหุ้นจีน (SCBCE / SCBCHA)", 
                                      "กองทุนปันผลหุ้นไทย (SCBDV)", 
                                      "หุ้นกู้ออกใหม่ (Debentures)"])
            
            st.markdown("### 🎙️ สคริปต์เสนอขาย (สำหรับ RM นิว)")
            if fund_type == "กองทุนหุ้นสหรัฐฯ / S&P500 (SCBS&P500)":
                script = "พี่คะ ถ้าอยากกระจายความเสี่ยงไปเติบโตพร้อมกับเศรษฐกิจโลก นิวแนะนำกองทุน <b>SCBS&P500</b> ค่ะ กองนี้จะลงทุนใน 500 บริษัทที่ใหญ่ที่สุดในอเมริกา ซื้อกองเดียวเหมือนได้เป็นเจ้าของทั้ง Apple, Microsoft, Amazon ระยะยาวเติบโตมั่นคงมากๆ เหมาะเป็น Core Portfolio เลยค่ะ"
            elif fund_type == "กองทุนเทคโนโลยี / AI (SCBNDQ / SCBSEMI)":
                script = "ช่วงนี้เทรนด์ AI มาแรงมากๆ ค่ะ ถ้ารับความเสี่ยงได้สูงขึ้นนิดนึง นิวอยากให้พี่แบ่งเงินมาลงใน <b>SCBNDQ</b> หรือ <b>SCBSEMI</b> ค่ะ เป็นสินทรัพย์แห่งอนาคตที่ผลตอบแทนคาดหวังสูงมากๆ นิวทยอยเก็บไม้แรกให้เลยดีไหมคะ?"
            elif fund_type == "กองทุนหุ้นจีน (SCBCE / SCBCHA)":
                script = "พี่คะ ตอนนี้ตลาดหุ้นจีนปรับฐานลงมาอยู่ในโซน Valuation ที่ถูกมากๆ ถือเป็นโอกาสดีสำหรับเงินเย็นระยะยาวเลยค่ะ นิวแนะนำกองทุน <b>SCBCE (เน้นหุ้นจีน Offshore)</b> หรือ <b>SCBCHA (เน้นหุ้น A-Shares)</b> ค่อยๆ ทยอยสะสมไม้แรกไว้รอรับการฟื้นตัวได้เลยค่ะ"
            elif fund_type == "กองทุนปันผลหุ้นไทย (SCBDV)":
                script = "สำหรับตลาดหุ้นไทยช่วงนี้ นิวแนะนำให้เน้นตั้งรับด้วยกองทุน <b>SCBDV</b> ค่ะ กองนี้จะเน้นเลือกหุ้นบริษัทใหญ่ที่จ่ายปันผลสม่ำเสมอ เอาไว้รับกระแสเงินสดเข้าพอร์ตเรื่อยๆ ลดความผันผวนของตลาดได้ดีเลยค่ะ"
            elif fund_type == "หุ้นกู้ออกใหม่ (Debentures)":
                script = "พี่คะ มีเงินเย็นที่ยังหาที่พักไม่ได้ไหมคะ? นิวมี <b>หุ้นกู้บริษัทชั้นนำระดับ Investment Grade</b> มาเสนอค่ะ จ่ายดอกเบี้ยประจำทุกๆ 3-6 เดือน ผลตอบแทนชนะเงินฝากแน่นอน และล็อคความเสี่ยงได้ดีกว่าหุ้น นิวช่วยทำจองสิทธิ์ผ่านแอปให้ได้เลยนะคะ"

            st.markdown(f"<div class='script-box'>👩‍💼 <b>นิว:</b><br><br>\"{script}\"</div>", unsafe_allow_html=True)


    # ------------------------------------
    # แท็บที่ 2: ข่าวภาษาไทย & เรดาร์ตลาด
    # ------------------------------------
    with tab2:
        colA, colB = st.columns([1.2, 1])
        with colA:
            st.markdown("### 🇹🇭 ข่าวสดเศรษฐกิจ & การเมืองโลก (ภาษาไทย)")
            st.caption("🔥 ดักจับคีย์เวิร์ด: ทรัมป์, น้ำมัน, สงคราม, เศรษฐกิจโลก (ดึงข้อมูลตรงจาก Google News TH)")
            
            try:
                query = urllib.parse.quote("เศรษฐกิจโลก OR ทรัมป์ OR น้ำมัน OR สงคราม")
                url = f"https://news.google.com/rss/search?q={query}&hl=th&gl=TH&ceid=TH:th"
                
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
                response = urllib.request.urlopen(req)
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                count = 0
                for item in root.findall('./channel/item'):
                    if count >= 10: 
                        break
                    title = item.find('title').text
                    link = item.find('link').text
                    pubDate = item.find('pubDate').text
                    
                    st.markdown(f"<div class='news-box'><b><a href='{link}' target='_blank' style='color:#4e2a84; text-decoration:none;'>🚨 {title}</a></b><br><small style='color:gray;'>🕒 ประกาศเมื่อ: {pubDate}</small></div>", unsafe_allow_html=True)
                    count += 1
            except Exception as e:
                st.error(f"ไม่สามารถโหลดข่าวภาษาไทยได้ในขณะนี้ กรุณาลองใหม่ภายหลัง ({e})")

        with colB:
            st.markdown("### 🗺️ แผนที่ความร้อนตลาด (S&P500)")
            st.caption("เช็กว่าวันนี้ตลาดโลกฝั่งไหนเขียว ฝั่งไหนแดง")
            components.html(
                """
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
                  {
                  "exchanges": [], "dataSource": "SPX500", "grouping": "sector", "blockSize": "market_cap_basic",
                  "blockColor": "change", "locale": "th_TH", "colorTheme": "light", "hasTopBar": true, "width": "100%", "height": "650"
                  }
                  </script>
                </div>
                """, height=650
            )

    # ------------------------------------
    # แท็บที่ 3: ค่าเงินบาท, หน้าปัดวิเคราะห์ทอง, ปฏิทิน
    # ------------------------------------
    with tab3:
        colX, colY = st.columns(2)
        with colX:
            st.markdown("### 💱 ค่าเงินบาท (USD/THB)")
            st.caption("สำคัญมากเวลากระทบยอดกำไรขาดทุนของกองทุนต่างประเทศและทองคำ")
            components.html(
                """
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
                  {
                  "symbol": "FX_IDC:THBUSD", "width": "100%", "height": "300", "locale": "th_TH",
                  "dateRange": "1M", "colorTheme": "light", "isTransparent": false, "autosize": false, "largeChartUrl": ""
                  }
                  </script>
                </div>
                """, height=300
            )
        with colY:
            st.markdown("### 🧭 หน้าปัดวิเคราะห์ทองคำ (Technical Gauge)")
            st.caption("เข็มไมล์ AI สรุปสัญญาณ ซื้อ/ขาย ทองคำโลก จากอินดิเคเตอร์ 20 ชนิด")
            components.html(
                """
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                  {
                  "interval": "1D", "width": "100%", "isTransparent": false, "height": "300",
                  "symbol": "OANDA:XAUUSD", "showIntervalTabs": true, "locale": "th_TH", "colorTheme": "light"
                  }
                  </script>
                </div>
                """, height=300
            )
            
        st.divider()
        st.markdown("### 📅 ปฏิทินข่าวเศรษฐกิจ & การแถลงการณ์ (เวลาไทย 🇹🇭)")
        st.caption("เช็กตารางล่วงหน้าว่า 'ลุงทรัมป์' หรือ 'ประธานเฟด' จะขึ้นโพเดียมแถลงข่าวกี่โมง (สังเกตแถบสีแดง = ข่าวแรง กราฟกระชาก)")
        components.html(
            """
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
              {
              "colorTheme": "light", "isTransparent": false, "width": "100%", "height": "500", "locale": "th_TH",
              "importanceFilter": "-1,0,1", "currencyFilter": "USD,EUR,CNY,GBP,JPY,THB"
              }
              </script>
            </div>
            """, height=500, scrolling=True
        )

# ==========================================
# โหมดที่ 2: ประกันสุขภาพและชีวิต (FWD) 
# ==========================================
elif app_mode == "🛡️ โหมดประกันสุขภาพ/ชีวิต (FWD)":
    st.title("🛡️ RM New x FWD 🧡: ออกแบบความอุ่นใจเฉพาะบุคคล")

    with st.container():
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("อายุลูกค้า (ปี)", min_value=1, max_value=80, value=35)
        gender = c2.selectbox("ความหลากหลาย", ["ชาย", "หญิง", "LGBTQ+"])
        kids = c3.radio("ครอบครัว", ["ไม่มีบุตร", "มีบุตร"])
        concern = st.selectbox("สิ่งที่ลูกค้ากังวลใจที่สุดในตอนนี้", 
                               ["กลัวป่วยหนักแล้วเป็นภาระคนอื่น / ค่ารักษาแพง", "จ่ายภาษีเยอะจนเสียดายเงิน", 
                                "กลัวแก่ไปไม่มีเงินใช้ / อยากเกษียณสบายๆ", "อยากเตรียมมรดกและทุนการศึกษาให้คนข้างหลัง"])

    st.divider()
    
    if concern == "กลัวป่วยหนักแล้วเป็นภาระคนอื่น / ค่ารักษาแพง":
        product = "FWD Precious Care (เหมาจ่ายสุขภาพ)"
        if kids == "มีบุตร":
            benefit = "✔️ **ไม่เป็นภาระลูกหลาน**\n✔️ **เข้าถึงหมอเก่งๆ ทันที**"
            script = f"พี่คะ... นิวเข้าใจเลยค่ะว่าคนเป็นแม่ เวลาป่วย สิ่งที่กลัวไม่ใช่ความเจ็บ แต่กลัวเงินเก็บของลูกจะหายไป นิวแนะนำ FWD Precious Care ค่ะ ให้ FWD รับความเสี่ยงตรงนี้แทนนะคะ"
        else:
            benefit = "✔️ **เจ็บป่วย ไม่กระทบความมั่งคั่ง**\n✔️ **พึ่งพาตัวเองได้ 100%**"
            script = f"พี่คะ ร่างกายเราคือ 'สินทรัพย์ที่แพงที่สุด' นิวอยากให้พี่มี FWD Precious Care ติดไว้ค่ะ ให้ประกันจ่ายค่าหมอแทนเรา พี่จะได้ใช้ชีวิตโสดๆ สวยๆ แบบไม่ต้องกังวลค่ะ"

    elif concern == "จ่ายภาษีเยอะจนเสียดายเงิน":
        product = "FWD For Pension / ประกันสะสมทรัพย์ 10/5"
        benefit = "✔️ **เปลี่ยนบิลภาษี เป็นเงินออม**\n✔️ **ความเสี่ยงต่ำที่สุด**"
        script = f"พี่คะ โดนภาษีไปเยอะไหมคะ? นิวเสียดายเงินแทนเลยค่ะ นิวมีวิธีเปลี่ยนบิลภาษีให้กลายมาเป็น 'เงินเก็บส่วนตัว' ด้วยออมทรัพย์ของ FWD ค่ะ นิวทำให้ดูนะคะว่าเราจะดึงเงินภาษีคืนมาได้กี่หมื่น"

    elif gender == "LGBTQ+" and concern in ["อยากเตรียมมรดกและทุนการศึกษาให้คนข้างหลัง", "กลัวแก่ไปไม่มีเงินใช้ / อยากเกษียณสบายๆ"]:
        product = "FWD Unit Linked / FWD Life Protector"
        benefit = "✔️ **ระบุคู่ชีวิตเป็นผู้รับประโยชน์ได้ 100%**\n✔️ **ส่งมอบความมั่นคงไร้รอยต่อ**"
        script = f"พี่คะ นิวชื่นชมความรักของพี่นะคะ FWD เปิดกว้างเรื่องนี้มาก แผนนี้ **ใส่ชื่อคนรักเป็นผู้รับผลประโยชน์ได้เลย ไม่ต้องรอจดทะเบียนสมรส** นิวช่วยวางแผนให้นะคะ"

    elif kids == "มีบุตร" and concern == "อยากเตรียมมรดกและทุนการศึกษาให้คนข้างหลัง":
        product = "FWD Unit Linked (ประกันควบการลงทุน)"
        benefit = "✔️ **สร้างเงินสดหลักล้านทันที**\n✔️ **ทุนการศึกษาการันตี**"
        script = f"พี่คะ นิวรู้ว่าพี่วางแผนอนาคตให้น้องไว้หมดแล้ว แผนนี้คือการใช้เงินหลักหมื่น สร้างหลักประกันหลักล้านให้น้องทันที เพื่อการันตีว่าลูกจะมีทุนการศึกษาจนจบแน่นอนค่ะ"

    else:
        product = "FWD Annuity (ประกันบำนาญ)"
        benefit = "✔️ **การันตีมีเงินเดือนใช้**\n✔️ **ไม่ต้องพึ่งพาใคร**"
        script = f"พี่คะ นิวอยากให้ภาพตอนอายุ 60 ของพี่ คือการได้ตื่นมาจิบกาแฟ ไปเที่ยว โดยที่มี **'เงินเดือน'** โอนเข้าบัญชีทุกเดือนจาก FWD ค่ะ เกษียณแบบสุขใจแน่นอนค่ะ"

    st.success(f"🏆 **ผลิตภัณฑ์แนะนำ:** {product}")
    st.info(f"🌟 **ประโยชน์สูงสุด:**\n{benefit}")
    st.markdown(f"<div class='fwd-box'>👩‍💼 <b>นิว:</b><br><br>\"{script}\"</div>", unsafe_allow_html=True)
