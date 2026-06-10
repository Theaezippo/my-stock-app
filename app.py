import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="✨ RM New x Ae 💕 Phi Vic 🐱", layout="wide", page_icon="💜")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 4px solid #4e2a84; }
    h1, h2, h3 { color: #4e2a84; }
    .script-box { background-color: #f3eef9; padding: 25px; border-radius: 12px; border-left: 6px solid #4e2a84; margin-bottom: 20px; font-size: 16px; line-height: 1.8;}
    .fwd-box { background-color: #fff0e6; padding: 25px; border-radius: 12px; border-left: 6px solid #e87722; margin-bottom: 20px; font-size: 16px; line-height: 1.8;}
    </style>
    """, unsafe_allow_html=True)

# --- แถบเมนูด้านข้าง ---
st.sidebar.markdown("## 💜 SCB Wealth & FWD")
st.sidebar.title("🗂️ โหมดการทำงาน")
app_mode = st.sidebar.radio("เลือกโหมดสำหรับให้บริการลูกค้า:", 
                            ["📈 โหมดการลงทุน (Wealth Allocation)", "🛡️ โหมดประกันสุขภาพ/ชีวิต (FWD)"])

st.sidebar.divider()
st.sidebar.caption("👨‍💻 พัฒนาโดย: เอ้ & นิว (มีพี่วิคเหมียว 🐱 ให้กำลังใจอยู่ข้างๆ)")

# ==========================================
# โหมดที่ 1: การลงทุน (Wealth & Investment)
# ==========================================
if app_mode == "📈 โหมดการลงทุน (Wealth Allocation)":
    st.title("✨ RM New x Ae 💖: ระบบวางแผนพอร์ตการลงทุน 🚀")
    st.caption("อัปเดตข้อมูล Real-time | วิเคราะห์กราฟด้วยโครงสร้างราคา และตารางข่าวสารเศรษฐกิจโลก")

    # --- ระบบสแกนหุ้น (เอากลับมาให้ใช้ง่ายๆ บนมือถือ) ---
    with st.expander("🎯 กดตรงนี้เพื่อเปิดระบบสแกนหาสินทรัพย์น่าช้อนซื้อ (Quick Scan)"):
        st.write("ค้นหาสินทรัพย์ที่ราคาปรับฐานลงมาในโซนถูก (Oversold) เพื่อเป็นไอเดียให้ลูกค้า")
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
                            rsi = 100 - (100 / (1 + rs))
                            curr_rsi = rsi.iloc[-1]
                            if curr_rsi < 40: 
                                recommended.append({'สินทรัพย์': name, 'ราคาล่าสุด': hist['Close'].iloc[-1], 'RSI': curr_rsi})
                    except:
                        pass
                if recommended:
                    st.success("✅ เจอสินทรัพย์ที่น่าสนใจแล้ว!")
                    st.dataframe(pd.DataFrame(recommended).sort_values(by='RSI').style.format({'ราคาล่าสุด': '{:.2f}', 'RSI': '{:.2f}'}), hide_index=True)
                else:
                    st.info("ตลาดกำลังตึงตัว ยังไม่มีสินทรัพย์ไหนลงมาในโซนน่าช้อนครับ")

    st.divider()

    # --- เลือกสินทรัพย์ ---
    asset_class = st.radio("เลือกประเภทสินทรัพย์ที่ต้องการนำเสนอ:", 
                           ["🇹🇭 หุ้นไทย (Core/Satellite)", "🇺🇸 หุ้นระดับโลก & ETF", "🛢️ สินทรัพย์ทางเลือก (ทอง, น้ำมัน, จีน)", "🏦 กองทุนรวม SCB & หุ้นกู้"], horizontal=True)

    if asset_class in ["🇹🇭 หุ้นไทย (Core/Satellite)", "🇺🇸 หุ้นระดับโลก & ETF", "🛢️ สินทรัพย์ทางเลือก (ทอง, น้ำมัน, จีน)"]:
        col1, col2 = st.columns([1, 2])
        with col1:
            if asset_class == "🇹🇭 หุ้นไทย (Core/Satellite)":
                popular_stocks = ["PTT", "AOT", "KBANK", "CPALL", "ADVANC", "BBL", "SCB", "SCC", "BDMS", "GULF", "DELTA"]
                stock_input = st.selectbox("เลือกหุ้นพื้นฐานดี", popular_stocks)
                full_symbol = f"{stock_input}.BK"
                asset_name = stock_input
            elif asset_class == "🇺🇸 หุ้นระดับโลก & ETF":
                popular_us = ["SPY (S&P 500 ETF)", "QQQ (Nasdaq ETF)", "AAPL", "MSFT", "NVDA", "TSLA"]
                stock_input = st.selectbox("เลือกหุ้น/ETF ต่างประเทศ", popular_us).split(" ")[0]
                full_symbol = stock_input
                asset_name = stock_input
            else:
                alt_assets = {
                    "ทองคำ (Spot Gold - XAUUSD)": "XAUUSD=X",
                    "น้ำมันดิบ (WTI Crude Oil)": "CL=F",
                    "ETF หุ้นจีน (FXI)": "FXI"
                }
                selected_alt = st.selectbox("เลือกสินทรัพย์เพื่อกระจายความเสี่ยง:", list(alt_assets.keys()))
                full_symbol = alt_assets[selected_alt]
                asset_name = selected_alt

        with col2:
            period = st.select_slider("เลือกมุมมองระยะเวลาการลงทุน", options=["3mo", "6mo", "1y", "3y"], value="6mo")

        st.divider()

        if full_symbol:
            try:
                ticker = yf.Ticker(full_symbol)
                data = ticker.history(period=period)
                
                if data.empty:
                    st.error("ไม่พบข้อมูล กรุณาลองตรวจสอบตัวสะกดอีกครั้ง")
                else:
                    close_data = data['Close'].squeeze()
                    current_price = float(close_data.iloc[-1])
                    
                    recent_high = close_data.max()
                    recent_low = close_data.min()
                    drawdown = ((current_price - recent_high) / recent_high) * 100
                    
                    st.subheader(f"ภาพรวมพอร์ตสินทรัพย์: {asset_name}")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("ราคาปัจจุบัน", f"{current_price:,.2f}")
                    m2.metric("จุดสูงสุดในรอบที่เลือก (High)", f"{recent_high:,.2f}")
                    m3.metric("ส่วนลดจากจุดสูงสุด (Drawdown)", f"{drawdown:.2f}%", "น่าทยอยสะสม" if drawdown < -15 else "ราคาตึงตัว", delta_color="off")

                    # RM Wealth Talk
                    st.markdown("### 🎙️ บทสนทนาแนะนำลูกค้า (RM Wealth Talk)")
                    if asset_class == "🛢️ สินทรัพย์ทางเลือก (ทอง, น้ำมัน, จีน)":
                        if "ทองคำ" in asset_name:
                            script = f"คุณลูกค้าคะ นิวขออนุญาตอัปเดตภาพรวมพอร์ตนิดนึงนะคะ ช่วงนี้สภาวะโลกมีความไม่แน่นอนสูง ทั้งเรื่องนโยบายและการแถลงข่าวต่างๆ นิวเลยอยากแนะนำให้เรามี **ทองคำ** ติดพอร์ตไว้สัก 5-10% ค่ะ ไม่ได้กะเก็งกำไรระยะสั้นนะคะ แต่เอาไว้เป็น 'เบาะกันกระแทก' เผื่อมีเหตุการณ์ไม่คาดฝัน พอร์ตของคุณลูกค้าจะได้ยังมีสินทรัพย์ที่รักษาความมั่งคั่งได้ค่ะ"
                        elif "จีน" in asset_name:
                            script = f"สำหรับตลาดจีนตอนนี้ Valuation อยู่ในโซนที่ถูกมากค่ะคุณลูกค้า นิวแนะนำว่าถ้าเรามีเงินเย็น สามารถแบ่งมาทยอยสะสมเป็นไม้เล็กๆ (Satellite) ไว้รอลุ้นการกระตุ้นเศรษฐกิจรอบใหญ่จากรัฐบาลจีนได้ค่ะ"
                        else:
                            script = f"สำหรับตัว **{asset_name}** ตอนนิวมองว่าเหมาะสำหรับใช้กระจายความเสี่ยงในพอร์ตค่ะ เราอาจจะแบ่งเงินทุนส่วนน้อยมาวางไว้ตรงนี้ เพื่อรับโอกาสเติบโตตามวัฏจักรเศรษฐกิจโลกค่ะ"
                    else:
                        if drawdown < -15:
                            script = f"สวัสดีค่ะคุณลูกค้า นิวติดตาม **{asset_name}** ให้อยู่นะคะ ตอนนี้ราคาปรับฐานลงมาประมาณ {abs(drawdown):.1f}% จากจุดสูงสุด พื้นฐานบริษัท/กองทุนยังแข็งแกร่งเหมือนเดิมเลยค่ะ นิวและทีม Wealth มองว่าจังหวะที่ตลาดกำลังกลัวนี่แหละค่ะ เป็น **'โอกาสทองในการทยอยสะสม'** นิวแบ่งไม้เข้าให้ดีไหมคะ จะได้ต้นทุนเฉลี่ยสวยๆ ค่ะ"
                        elif drawdown > -5:
                            script = f"คุณลูกค้าคะ อัปเดตตัว **{asset_name}** นะคะ ตอนนี้ราคาวิ่งขึ้นมาใกล้จุดสูงสุดแล้วค่ะ พอร์ตเรามีกำไรตรงนี้พอสมควร เพื่อวินัยการลงทุนที่ดี นิวแนะนำให้เราทำ **Portfolio Rebalancing** ดีไหมคะ? ทยอยรินขายทำกำไรบางส่วน เอาเงินสดมาเก็บไว้รอจังหวะตลาดปรับฐาน หรือโยกไปสินทรัพย์อื่นเพื่อล็อคความเสี่ยงค่ะ"
                        else:
                            script = f"สำหรับตัว **{asset_name}** ภาพรวมยังเกาะเทรนด์การเติบโตได้ดีค่ะคุณลูกค้า นิวแนะนำให้เรา **'ถือลงทุนต่อเนื่อง (Let Profit Run)'** ได้สบายใจเลยค่ะ นิวจะคอยมอนิเตอร์ข่าวสำคัญให้ตลอด ถ้าระบบมีสัญญาณเตือนเมื่อไหร่ นิวจะรีบแจ้งทันทีเลยค่ะ"

                    st.markdown(f"<div class='script-box'>👩‍💼 <b>นิว:</b><br><br>\"{script}\"</div>", unsafe_allow_html=True)

                    # กราฟ (แก้ปัญหา Volume ทองคำ/Forex)
                    st.markdown("#### 📊 โครงสร้างราคาและแนวโน้ม (Macro View)")
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.7])
                    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'].squeeze(), high=data['High'].squeeze(), low=data['Low'].squeeze(), close=close_data, name="ราคา"), row=1, col=1)
                    data['EMA50'] = close_data.ewm(span=50, adjust=False).mean()
                    fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], line=dict(color='orange', width=1.5, dash='dot'), name="Trend (50 Days)"), row=1, col=1)
                    
                    # เช็กว่ามีข้อมูล Volume ไหม (ถ้าเป็นทอง XAUUSD มักจะไม่มี)
                    has_volume = 'Volume' in data.columns and not data['Volume'].isna().all() and data['Volume'].sum() > 0
                    if has_volume:
                        colors = ['red' if row['Open'] - row['Close'] >= 0 else 'green' for index, row in data.iterrows()]
                        fig.add_trace(go.Bar(x=data.index, y=data['Volume'], marker_color=colors, name='Volume'), row=2, col=1)
                    else:
                        # ถ้าไม่มี Volume ให้โชว์แค่ราคากราฟบน
                        fig.update_layout(yaxis2=dict(visible=False))

                    fig.update_layout(template="plotly_white", height=500 if has_volume else 400, margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
                    fig.update_xaxes(rangeslider_visible=False) 
                    st.plotly_chart(fig, use_container_width=True)

    # --- ส่วนของปฏิทินข่าวสารเศรษฐกิจ (สำคัญมากสำหรับทอง/น้ำมัน) ---
    st.divider()
    st.markdown("### 📅 ปฏิทินข่าวเศรษฐกิจ & การแถลงการณ์ (อัปเดต Real-time เวลาไทย)")
    st.caption("รวบรวมตารางการประกาศตัวเลขเศรษฐกิจ การแถลงของ Fed และเหตุการณ์สำคัญระดับโลก (สีแดง = ข่าวแรงกระทบกราฟรุนแรง)")
    
    # ฝัง Widget ของ TradingView แบบเรียลไทม์
    components.html(
        """
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
          {
          "colorTheme": "light",
          "isTransparent": false,
          "width": "100%",
          "height": "500",
          "locale": "th_TH",
          "importanceFilter": "-1,0,1",
          "currencyFilter": "USD,EUR,CNY,GBP,JPY,THB"
          }
          </script>
        </div>
        """,
        height=500,
        scrolling=True
    )

# ==========================================
# โหมดที่ 2: ประกันสุขภาพและชีวิต (FWD)
# ==========================================
elif app_mode == "🛡️ โหมดประกันสุขภาพ/ชีวิต (FWD)":
    st.title("🛡️ RM New x FWD 🧡: ออกแบบความอุ่นใจเฉพาะบุคคล")
    st.caption("เพราะประกันไม่ใช่แค่กระดาษ แต่คือความรับผิดชอบและความรักที่ส่งต่อได้")

    with st.container():
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("อายุลูกค้า (ปี)", min_value=1, max_value=80, value=35)
        gender = c2.selectbox("ความหลากหลาย", ["ชาย", "หญิง", "LGBTQ+"])
        kids = c3.radio("ครอบครัว", ["ไม่มีบุตร", "มีบุตร"])
        
        concern = st.selectbox("สิ่งที่ลูกค้ากังวลใจที่สุดในตอนนี้ (Pain Point)", 
                               ["กลัวป่วยหนักแล้วเป็นภาระคนอื่น / ค่ารักษาแพง", 
                                "จ่ายภาษีเยอะจนเสียดายเงิน", 
                                "กลัวแก่ไปไม่มีเงินใช้ / อยากเกษียณสบายๆ", 
                                "อยากเตรียมมรดกและทุนการศึกษาให้คนข้างหลัง"])

    st.divider()
    
    recommended_product = ""
    selling_point = ""
    script = ""
    benefit = ""

    if concern == "กลัวป่วยหนักแล้วเป็นภาระคนอื่น / ค่ารักษาแพง":
        recommended_product = "FWD Precious Care (เหมาจ่ายสุขภาพ)"
        if kids == "มีบุตร":
            benefit = "✔️ **ไม่เป็นภาระลูกหลาน:** เวลาเจ็บป่วย คุณพ่อคุณแม่ไม่ต้องเกรงใจลูกเรื่องค่ารักษาเลย\n✔️ **เข้าถึงหมอเก่งๆ:** เลือกโรงพยาบาลระดับท็อปได้ทันที เพื่อให้หายป่วยไวที่สุดและกลับมาอยู่กับลูก"
            script = f"พี่คะ... นิวเองก็มีครอบครัว (มีลูกรักเป็นน้องแมวพี่วิคด้วย 🐱) นิวเข้าใจเลยค่ะว่าคนเป็นพ่อเป็นแม่ เวลาเราป่วย สิ่งที่เรากลัวที่สุดไม่ใช่ความเจ็บปวดนะคะ แต่เรากลัวว่าเงินเก็บที่เตรียมไว้ให้ลูก จะต้องละลายหายไปกับค่าหมอ นิวอยากแนะนำ FWD Precious Care ตัวนี้ค่ะ พี่ไม่ต้องกังวลเรื่องค่ารักษาหลักล้านเลย ให้ FWD เป็นคนรับความเสี่ยงตรงนี้แทน พี่จะได้เอาเงินเก็บไปปูทางอนาคตให้น้องได้อย่างสบายใจนะคะ"
        else:
            benefit = "✔️ **เจ็บป่วย ไม่กระทบความมั่งคั่ง:** เงินเก็บจากการทำงานหนักยังอยู่ครบถ้วน\n✔️ **มีศักดิ์ศรี พึ่งพาตัวเองได้:** เลือกการรักษาที่ดีที่สุดให้ตัวเองได้ โดยไม่ต้องรบกวนเงินใคร"
            script = f"พี่คะ ด้วยความที่เราทำงานหนักมาตลอด ร่างกายเรานี่แหละค่ะคือ 'สินทรัพย์ที่แพงที่สุด' ถ้าวันนึงเครื่องจักรตัวนี้มันรวนขึ้นมา ค่าซ่อมเดี๋ยวนี้หลักแสนหลักล้านเลยนะคะ นิวอยากให้พี่มี FWD Precious Care ติดไว้ค่ะ เราหาเงินเก่งแล้ว เราต้องฉลาดปกป้องเงินเราด้วย ให้ประกันจ่ายค่าหมอแทนเรานะคะ พี่จะได้ใช้ชีวิตโสดๆ สวยๆ แบบไม่ต้องกังวลอะไรเลยค่ะ"

    elif concern == "จ่ายภาษีเยอะจนเสียดายเงิน":
        recommended_product = "FWD For Pension / ประกันสะสมทรัพย์ 10/5"
        benefit = "✔️ **เปลี่ยนบิลภาษี เป็นเงินออม:** ดึงเงินที่ต้องจ่ายทิ้งกลับมาเป็นเงินก้อนของตัวเอง\n✔️ **ความเสี่ยงต่ำที่สุด:** การันตีผลตอบแทนแน่นอน ชนะเงินฝากออมทรัพย์"
        script = f"พี่คะ ปีนี้โดนภาษีไปเยอะไหมคะ? นิวเห็นฐานภาษีคนเก่งๆ แบบพี่แล้วแอบเสียดายเงินแทนเลยค่ะ แทนที่เราจะจ่ายทิ้งไปเปล่าๆ นิวมีวิธีเปลี่ยนบิลภาษีตรงนั้น ให้กลายมาเป็น 'เงินเก็บส่วนตัว' ของพี่แบบชัวร์ๆ การันตีเงินต้นไม่หายด้วยตัวออมทรัพย์ของ FWD ค่ะ ได้ทั้งลดหย่อนภาษีปีนี้ และได้เงินก้อนคืนในอนาคตด้วย นิวทำให้ดูนะคะว่าเราจะดึงเงินภาษีคืนมาได้กี่หมื่น"

    elif gender == "LGBTQ+" and concern in ["อยากเตรียมมรดกและทุนการศึกษาให้คนข้างหลัง", "กลัวแก่ไปไม่มีเงินใช้ / อยากเกษียณสบายๆ"]:
        recommended_product = "FWD Unit Linked / FWD Life Protector"
        benefit = "✔️ **ความคุ้มครองที่เท่าเทียม:** ระบุชื่อคู่ชีวิตเป็นผู้รับประโยชน์ได้ 100% โดยไม่มีเงื่อนไขทางกฎหมายมาขวาง\n✔️ **ส่งมอบความมั่นคง:** สร้างกองทุนดูแลกันและกันในวันที่ใครคนใดคนหนึ่งไม่อยู่"
        script = f"พี่คะ นิวชื่นชมและสนับสนุนความรักของพี่มากๆ เลยนะคะ นิวเลยอยากเล่าให้ฟังว่า FWD เราเป็นบริษัทแรกๆ เลยนะคะที่เปิดกว้างเรื่องนี้ แผนความคุ้มครองตัวนี้ **พี่สามารถใส่ชื่อคนรักของพี่เป็นผู้รับเงินผลประโยชน์ได้เลยค่ะ โดยไม่ต้องรอใบทะเบียนสมรสเท่าเทียมเลย** นิวอยากช่วยเป็นส่วนหนึ่งในการวางแผน ให้ความรักของพี่มั่นคงและดูแลกันไปได้ตลอดชีวิตเลยนะคะ นิวออกแบบแผนให้ดูนะคะ"

    elif kids == "มีบุตร" and concern == "อยากเตรียมมรดกและทุนการศึกษาให้คนข้างหลัง":
        recommended_product = "FWD Unit Linked (ประกันชีวิตควบการลงทุน)"
        benefit = "✔️ **เสาหลักไม่สั่นคลอน:** สร้างเงินสดหลักล้านทันที เพื่อเป็นเบาะรองรับให้ครอบครัว\n✔️ **ทุนการศึกษาการันตี:** มั่นใจว่าลูกจะเรียนจบตามที่ฝันไว้แน่นอน"
        script = f"พี่คะ ในมุมของเสาหลักครอบครัว นิวรู้ว่าพี่วางแผนอนาคตให้น้องไว้หมดแล้ว ทั้งเรื่องเรียน เรื่องคุณภาพชีวิต แต่ถ้าวันนึงเกิดเหตุไม่คาดฝันขึ้นมา นิวไม่อยากให้อนาคตของน้องต้องสะดุดเลยค่ะ แผนนี้คือการใช้เงินก้อนเล็กหลักหมื่น สร้างหลักประกันเงินสดหลักล้านไว้ให้น้องทันทีค่ะ ให้มันเป็น 'จดหมายรักฉบับสุดท้าย' ที่การันตีว่าลูกจะมีทุนการศึกษาจนจบแน่นอนนะคะ"

    elif concern == "กลัวแก่ไปไม่มีเงินใช้ / อยากเกษียณสบายๆ":
        recommended_product = "FWD Annuity (ประกันบำนาญ)"
        benefit = "✔️ **การันตีมีเงินเดือนใช้:** รับเงินรายเดือนจาก FWD ไปจนถึงอายุ 85-90 ปี\n✔️ **ไม่ต้องพึ่งพาใคร:** เป็นผู้สูงอายุที่ดูแลตัวเองได้ มีอิสระทางการเงินอย่างแท้จริง"
        script = f"พี่คะ ยุคนี้คนเราอายุยืนขึ้นมาก การวางแผนเกษียณไม่ใช่เรื่องไกลตัวเลยนะคะ นิวอยากให้ภาพตอนอายุ 60 ของพี่ คือการได้ตื่นมาจิบกาแฟ ไปเที่ยว ไปทำสิ่งที่รัก โดยที่มี **'เงินเดือน'** โอนเข้าบัญชีพี่ทุกเดือนจาก FWD ค่ะ พี่จะได้เป็นคนโสดที่เกษียณแบบมีอิสระ พึ่งพาตัวเองได้ 100% นิวจัดพอร์ตบำนาญตัวนี้ให้นะคะ รับรองว่าเกษียณแบบสุขใจแน่นอนค่ะ"

    st.success(f"🏆 **ผลิตภัณฑ์ที่เหมาะกับลูกค้าที่สุด:** {recommended_product}")
    st.info(f"🌟 **ประโยชน์ที่แท้จริงที่ลูกค้าจะได้รับ:**\n{benefit}")

    st.markdown("### 💬 บทสนทนาเพื่อนำเสนอใจถึงใจ (Empathy Pitching)")
    st.markdown(f"<div class='fwd-box'>👩‍💼 <b>นิว:</b><br><br>\"{script}\"</div>", unsafe_allow_html=True)
