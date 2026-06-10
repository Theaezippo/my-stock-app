import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="✨ RM New x Ae 💕 Phi Vic 🐱", layout="wide", page_icon="💜")

# CSS ตกแต่ง
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 4px solid #4e2a84; }
    h1, h2, h3 { color: #4e2a84; }
    .script-box { background-color: #f3eef9; padding: 20px; border-radius: 10px; border-left: 5px solid #4e2a84; margin-bottom: 20px; font-size: 16px; line-height: 1.6;}
    .fwd-box { background-color: #fff0e6; padding: 20px; border-radius: 10px; border-left: 5px solid #e87722; margin-bottom: 20px; font-size: 16px; line-height: 1.6;}
    .benefit-box { background-color: #e6f9ec; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# --- แถบเมนูด้านข้าง ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/4/47/Siam_Commercial_Bank_logo.svg/1200px-Siam_Commercial_Bank_logo.svg.png", width=150)
st.sidebar.title("🗂️ โหมดการทำงาน")
app_mode = st.sidebar.radio("เลือกโหมดสำหรับให้บริการลูกค้า:", 
                            ["📈 โหมดการลงทุน (Wealth)", "🛡️ โหมดประกันสุขภาพ/ชีวิต (FWD)"])

st.sidebar.divider()
st.sidebar.caption("👨‍💻 พัฒนาโดย: เอ้ & นิว (มีพี่วิคเหมียว 🐱 คุมระบบ)")

# ==========================================
# โหมดที่ 1: การลงทุน (Wealth & Investment)
# ==========================================
if app_mode == "📈 โหมดการลงทุน (Wealth)":
    st.title("✨ RM New x Ae 💖: ระบบวางแผนการลงทุน 🚀📊")
    st.caption("ข้อมูลหุ้นไทย/ต่างประเทศ, กองทุนรวม SCBAM และหุ้นกู้")

    asset_class = st.radio("เลือกประเภทสินทรัพย์ที่ต้องการนำเสนอ:", 
                           ["🇹🇭 หุ้นไทย (InnovestX)", "🇺🇸 หุ้นต่างประเทศ / ETF (Easy Invest)", "🏦 กองทุนรวม SCB & หุ้นกู้"], horizontal=True)

    if asset_class in ["🇹🇭 หุ้นไทย (InnovestX)", "🇺🇸 หุ้นต่างประเทศ / ETF (Easy Invest)"]:
        col1, col2 = st.columns([1, 2])
        with col1:
            if asset_class == "🇹🇭 หุ้นไทย (InnovestX)":
                popular_stocks = ["PTT", "AOT", "KBANK", "CPALL", "ADVANC", "BBL", "SCB", "SCC", "BDMS", "GULF", "DELTA"]
                search_mode = st.radio("วิธีค้นหาหุ้น:", ["📋 เลือกจากรายชื่อยอดฮิต", "✍️ พิมพ์ชื่อหุ้นเอง"])
                if search_mode == "📋 เลือกจากรายชื่อยอดฮิต":
                    stock_input = st.selectbox("เลือกหุ้น", popular_stocks)
                else:
                    stock_input = st.text_input("พิมพ์ชื่อหุ้นไทย (ไม่ต้องใส่ .BK)", value="PTT").upper()
                full_symbol = f"{stock_input}.BK"
            else:
                popular_us = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "TSLA", "GOOGL", "META", "AMZN"]
                search_mode = st.radio("วิธีค้นหาหุ้น:", ["📋 เลือกจากรายชื่อยอดฮิต (S&P500/Tech)", "✍️ พิมพ์ Ticker เอง"])
                if search_mode == "📋 เลือกจากรายชื่อยอดฮิต (S&P500/Tech)":
                    stock_input = st.selectbox("เลือกหุ้น/ETF ต่างประเทศ", popular_us)
                else:
                    stock_input = st.text_input("พิมพ์ Ticker (เช่น AAPL)", value="SPY").upper()
                full_symbol = stock_input

        with col2:
            period = st.select_slider("เลือกช่วงเวลาย้อนหลังเพื่อดูกราฟ", options=["3mo", "6mo", "1y", "2y"], value="6mo")

        st.divider()

        if stock_input:
            try:
                ticker = yf.Ticker(full_symbol)
                data = ticker.history(period=period)
                
                if data.empty:
                    st.error("ไม่พบข้อมูล กรุณาลองตรวจสอบตัวสะกดอีกครั้ง")
                else:
                    close_data = data['Close'].squeeze()
                    
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
                    
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("ราคาปัจจุบัน", f"{current_price:,.2f}", f"{price_diff:,.2f}")
                    m2.metric("RSI (ความร้อนแรง)", f"{current_rsi:.2f}", "Oversold" if current_rsi < 30 else "Overbought" if current_rsi > 70 else "Neutral", delta_color="off")
                    m3.metric("Demand (แนวรับ)", f"{demand_zone:,.2f}")
                    m4.metric("Supply (แนวต้าน)", f"{supply_zone:,.2f}")

                    st.markdown("### 🎙️ สคริปต์แนะนำการลงทุน (สำหรับ RM นิว)")
                    if current_rsi < 35:
                        script = f"สวัสดีค่ะคุณลูกค้า นิวขออนุญาตอัปเดตตัว {stock_input} นะคะ ตอนนี้ราคาย่อลงมาในโซนแนวรับที่น่าสนใจมากแถวๆ **{demand_zone:.2f}** อินดิเคเตอร์ฟ้องว่าตลาดเริ่มเทขายจนต่ำกว่ามูลค่า (Oversold) นิวและทีมงานมองว่าตรงนี้เป็นโอกาสดีที่เราจะ **'ทยอยสะสมไม้แรก'** ค่ะ เผื่อรับจังหวะเด้งกลับไปที่เป้าหมายระยะสั้นแถว **{pivot_point:.2f}** ค่ะ"
                    elif current_rsi > 65:
                        script = f"คุณลูกค้าคะ นิวคอยมอนิเตอร์ตัว {stock_input} ให้ ตอนนี้ราคาวิ่งขึ้นมาทดสอบแนวต้านสำคัญที่ **{supply_zone:.2f}** แล้วค่ะ กราฟเริ่มมีความตึงตัว (Overbought) ถ้ารับความเสี่ยงได้น้อย นิวแนะนำให้เรา **'แบ่งขายทำกำไรล็อคเป้าหมายไว้ก่อนบางส่วน'** ดีไหมคะ? แล้วส่วนที่เหลือค่อยปล่อยรันเทรนด์ไปค่ะ"
                    else:
                        script = f"อัปเดตสภาวะตลาดของ {stock_input} นะคะคุณลูกค้า ตอนนี้ราคากำลังฟอร์มตัวสะสมพลังอยู่ในกรอบค่ะ แนวโน้มหลักยังทรงตัว ถือว่าสามารถ **'ถือต่อไป (Hold)'** ได้อย่างสบายใจค่ะ นิวจะคอยเฝ้าจุดแนวรับที่ **{demand_zone:.2f}** ให้อย่างใกล้ชิดเลยค่ะ"

                    st.markdown(f"<div class='script-box'>👩‍💼 <b>นิว:</b> {script}</div>", unsafe_allow_html=True)

                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.7])
                    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'].squeeze(), high=data['High'].squeeze(), low=data['Low'].squeeze(), close=close_data, name="ราคา"), row=1, col=1)
                    data['EMA20'] = close_data.ewm(span=20, adjust=False).mean()
                    fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], line=dict(color='orange', width=1), name="Trend (EMA 20)"), row=1, col=1)
                    fig.add_hline(y=supply_zone, line_dash="dot", line_color="red", row=1, col=1)
                    fig.add_hline(y=demand_zone, line_dash="dot", line_color="green", row=1, col=1)
                    colors = ['red' if row['Open'] - row['Close'] >= 0 else 'green' for index, row in data.iterrows()]
                    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], marker_color=colors, name='Volume'), row=2, col=1)
                    fig.update_layout(template="plotly_white", height=500, margin=dict(l=0, r=0, t=10, b=0), showlegend=False)
                    fig.update_xaxes(rangeslider_visible=False) 
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error("ระบบกำลังโหลดข้อมูล กรุณารอสักครู่...")

    elif asset_class == "🏦 กองทุนรวม SCB & หุ้นกู้":
        st.subheader("📚 คลังข้อมูลกองทุนเด่น & หุ้นกู้ (Pitching Guide)")
        fund_type = st.selectbox("เลือกประเภทผลิตภัณฑ์:", ["กองทุนหุ้นสหรัฐฯ / S&P500 (SCBS&P500)", "กองทุนเทคโนโลยี / AI (SCBNDQ / SCBSEMI)", "กองทุนปันผลหุ้นไทย (SCBDV)", "หุ้นกู้ออกใหม่ (Debentures)"])
        
        st.markdown("### 🎙️ สคริปต์สำหรับ RM นิว")
        if fund_type == "กองทุนหุ้นสหรัฐฯ / S&P500 (SCBS&P500)":
            st.markdown("""<div class='script-box'>👩‍💼 <b>นิว:</b> "คุณลูกค้าคะ ถ้าอยากกระจายความเสี่ยงไปเติบโตพร้อมกับเศรษฐกิจโลก นิวแนะนำกองทุน <b>SCBS&P500</b> ค่ะ กองนี้จะลงทุนใน 500 บริษัทที่ใหญ่ที่สุดในอเมริกา ซื้อกองเดียวเหมือนได้เป็นเจ้าของทั้ง Apple, Microsoft, Amazon ระยะยาวเติบโตมั่นคงมากๆ ค่ะ"</div>""", unsafe_allow_html=True)
        elif fund_type == "กองทุนเทคโนโลยี / AI (SCBNDQ / SCBSEMI)":
             st.markdown("""<div class='script-box'>👩‍💼 <b>นิว:</b> "ช่วงนี้เทรนด์ AI มาแรงมากๆ ค่ะ ถ้ารับความเสี่ยงได้สูงขึ้นนิดนึง นิวอยากให้แบ่งเงินมาลงใน <b>SCBNDQ</b> หรือ <b>SCBSEMI</b> ค่ะ เป็นสินทรัพย์แห่งอนาคตที่ผลตอบแทนคาดหวังสูงมากๆ ค่ะ"</div>""", unsafe_allow_html=True)
        elif fund_type == "หุ้นกู้ออกใหม่ (Debentures)":
             st.markdown("""<div class='script-box'>👩‍💼 <b>นิว:</b> "คุณลูกค้ามีเงินเย็นที่ยังหาที่พักไม่ได้ไหมคะ? นิวมี <b>หุ้นกู้บริษัทชั้นนำระดับ Investment Grade</b> มาเสนอค่ะ จ่ายดอกเบี้ยประจำทุกๆ 3-6 เดือน ผลตอบแทนชนะเงินฝากแน่นอน นิวช่วยทำจองผ่านแอป SCB Easy ให้ได้เลยนะคะ"</div>""", unsafe_allow_html=True)


# ==========================================
# โหมดที่ 2: ประกันสุขภาพและชีวิต (FWD)
# ==========================================
elif app_mode == "🛡️ โหมดประกันสุขภาพ/ชีวิต (FWD)":
    st.title("🛡️ RM New x FWD 🧡: ระบบจัดพอร์ตความคุ้มครอง")
    st.caption("ระบบ AI ช่วยวิเคราะห์และหา 'จุดที่ลูกค้าได้ประโยชน์สูงสุด' ตาม Lifestyle เฉพาะบุคคล")

    st.markdown("### 📋 1. กรอกโปรไฟล์ลูกค้า")
    with st.container():
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("อายุลูกค้า (ปี)", min_value=1, max_value=80, value=30)
        gender = c2.selectbox("เพศ / ตัวตน", ["ชาย", "หญิง", "LGBTQ+"])
        status = c3.selectbox("สถานภาพ", ["โสด", "สมรส", "หย่าร้าง"])
        
        c4, c5 = st.columns(2)
        kids = c4.radio("บุตร", ["ไม่มีบุตร", "มีบุตร"])
        concern = c5.selectbox("ความต้องการหลักของลูกค้า (Pain Point)", 
                               ["ต้องการความคุ้มครองสุขภาพ/โรคร้าย", 
                                "ต้องการลดหย่อนภาษี", 
                                "วางแผนเกษียณ/ออมเงิน", 
                                "วางแผนมรดกให้คนข้างหลัง/คนรัก"])

    st.divider()
    st.markdown("### 🎯 2. ผลการวิเคราะห์และแผนที่แนะนำ")
    
    recommended_product = ""
    selling_point = ""
    script = ""
    benefit = ""

    # Rule 1: สุขภาพ
    if concern == "ต้องการความคุ้มครองสุขภาพ/โรคร้าย":
        recommended_product = "FWD Precious Care (เหมาจ่ายสุขภาพ) + CI 50 (คุ้มครองโรคร้าย)"
        selling_point = "ค่ารักษาเหมาจ่ายตามจริง ไม่จุกจิกวงเงินย่อย ครอบคลุม Targeted Therapy"
        benefit = "✔️ **ปกป้องเงินเก็บก้อนใหญ่:** ป่วยหนักแค่ไหนก็ไม่ต้องทุบกระปุกเงินเก็บตัวเองมาจ่ายค่าหมอ\n✔️ **เข้าถึงการรักษาที่ดีที่สุด:** เลือกโรงพยาบาลเอกชนชั้นนำได้ทันที ไม่ต้องรอคิว\n✔️ **หมดห่วงเรื่องโรคร้าย:** หากตรวจเจอโรคร้ายแรง มีเงินก้อนให้ไปใช้ดูแลตัวเองหรือครอบครัวทันที"
        script = f"คุณลูกค้าคะ ด้วยวัย {age} ปี เป็นช่วงที่นิวอยากให้ความสำคัญกับสุขภาพมากที่สุดค่ะ นิวขอแนะนำ **FWD Precious Care** ตัวนี้จะช่วยปิดความเสี่ยงเรื่องค่ารักษาพยาบาลที่แพงขึ้นทุกปี คุณลูกค้าจะได้ไม่ต้องเอาเงินเก็บจากการทำงานหนักมารับความเสี่ยงตรงนี้นะคะ ปล่อยให้ FWD จ่ายแทนค่ะ"

    # Rule 2: ลดหย่อนภาษี
    elif concern == "ต้องการลดหย่อนภาษี":
        recommended_product = "FWD For Pension (ประกันบำนาญ) หรือ 10/5 สะสมทรัพย์"
        selling_point = "ลดหย่อนภาษีได้สูงสุด (ตามสิทธิ) พร้อมผลตอบแทนแน่นอนและไม่ผันผวน"
        benefit = "✔️ **ได้เงินสดคืนจากภาษีทันที:** เปลี่ยนภาษีที่ต้องจ่ายทิ้ง เป็นเงินเก็บของตัวเอง\n✔️ **ความเสี่ยงเป็นศูนย์:** การันตีเงินต้นและผลตอบแทนตามสัญญา ไม่สวิงขึ้นลงตามตลาดหุ้น\n✔️ **สร้างวินัยทางการเงินแบบอัตโนมัติ:** บังคับเก็บเงินเพื่ออนาคตของตัวเอง"
        script = f"สำหรับคนเก่งแบบคุณลูกค้า ฐานภาษีต้องเริ่มสูงแล้วแน่ๆ นิวแนะนำตัว **ประกันออมทรัพย์ลดหย่อนภาษี** ค่ะ เราจะได้ประโยชน์ถึง 2 ต่อเลย ต่อแรกคือได้ดึงเงินภาษีกลับมาเข้ากระเป๋าทันทีในปีนี้ และต่อที่สองคือได้เงินเก็บก้อนใหญ่แบบชัวร์ๆ ตามสัญญาเลยค่ะ นิวคำนวณเบี้ยที่คุ้มที่สุดให้เลยดีไหมคะ?"

    # Rule 3: LGBTQ+ & มรดก/เกษียณ
    elif gender == "LGBTQ+" and concern in ["วางแผนมรดกให้คนข้างหลัง/คนรัก", "วางแผนเกษียณ/ออมเงิน"]:
        recommended_product = "FWD Unit Linked / FWD Life Protector"
        selling_point = "FWD เปิดกว้างและรองรับความหลากหลาย ระบุคู่ชีวิตเพศเดียวกันเป็นผู้รับประโยชน์ได้"
        benefit = "✔️ **ความเท่าเทียมที่จับต้องได้:** ทะลายข้อจำกัดทางกฎหมาย สามารถส่งมอบความมั่งคั่งให้ 'คนที่เรารัก' ได้ 100%\n✔️ **การันตีสิทธิไม่ตกหล่น:** มั่นใจได้ว่าเงินก้อนนี้จะไปถึงมือคู่ชีวิตโดยไม่ต้องผ่านกระบวนการศาลยุ่งยาก\n✔️ **วางแผนเกษียณคู่:** สร้างกองทุนไว้ดูแลกันและกันในยามเกษียณ"
        script = f"คุณลูกค้าคะ นิวขออนุญาตแนะนำความพิเศษของ FWD นะคะ FWD เป็นบริษัทที่เข้าใจและสนับสนุนความหลากหลายมากๆ ค่ะ แผนนี้ **สามารถระบุชื่อคู่ชีวิตของคุณลูกค้าเป็นผู้รับประโยชน์ได้เลยโดยไม่ต้องมีทะเบียนสมรส** ค่ะ นิวอยากช่วยส่งมอบความมั่นคงนี้ให้ทั้งคุณลูกค้าและคนที่คุณลูกค้ารักได้อุ่นใจไปตลอดชีวิตเลยนะคะ"

    # Rule 4: คนมีครอบครัว / มีลูก
    elif kids == "มีบุตร" and concern == "วางแผนมรดกให้คนข้างหลัง/คนรัก":
        recommended_product = "FWD Unit Linked (ควบการลงทุน) หรือ ประกันชีวิตคุ้มครองตลอดชีพ"
        selling_point = "สร้างทุนมรดกหลักล้านด้วยเงินก้อนเล็ก เพื่อเป็นทุนการศึกษาให้ลูก"
        benefit = "✔️ **การันตีอนาคตลูก:** มั่นใจได้ว่าอนาคตการศึกษาและคุณภาพชีวิตของลูกจะไม่สะดุด ไม่ว่าจะเกิดอะไรขึ้น\n✔️ **ใช้เงินก้อนเล็ก สร้างเงินก้อนใหญ่:** จ่ายหลักหมื่น แต่สร้างความคุ้มครองหลักล้านได้ตั้งแต่วันแรก\n✔️ **ส่งต่อความมั่งคั่งแบบปลอดภาษี:** มรดกจากประกันชีวิตจะถูกส่งต่อให้ลูกโดยไม่โดนหักภาษีมรดก"
        script = f"ในฐานะคนเป็นพ่อแม่ นิวเข้าใจเลยค่ะว่าน้องคือหัวใจสำคัญ นิวขอเสนอแผน **กองทุนมรดกและทุนการศึกษา** ค่ะ จ่ายเบี้ยเบาๆ แต่สร้างเบาะรองรับก้อนใหญ่ได้ทันที เพื่อเป็นหลักประกันว่า ไม่ว่าอนาคตจะเป็นยังไง คุณภาพชีวิตและการศึกษาของน้องจะถูกจัดเตรียมไว้อย่างสมบูรณ์แบบค่ะ"
    
    # Rule 5: โสด + ออมเงิน
    elif status == "โสด" and concern == "วางแผนเกษียณ/ออมเงิน":
        recommended_product = "FWD Annuity (บำนาญ) หรือ Unit Linked"
        selling_point = "สร้าง Active Income ให้ตัวเองในยามเกษียณ ดูแลตัวเองได้แบบไม่ต้องพึ่งใคร"
        benefit = "✔️ **มี 'เงินเดือน' ใช้ตลอดชีพ:** FWD จะโอนเงินให้คุณลูกค้าใช้ทุกเดือนหรือทุกปีหลังเกษียณ\n✔️ **โอนความเสี่ยงเรื่องอายุยืน (Longevity Risk):** ไม่ต้องกลัวว่า 'เงินจะหมดก่อนตาย' เพราะประกันบำนาญจ่ายให้จนถึงอายุ 85-90 ปี\n✔️ **เกษียณแบบมีเกียรติ:** ดูแลตัวเองได้สบายๆ จ่ายค่าพยาบาล หรือไปเที่ยวได้โดยไม่ต้องพึ่งพาคนอื่น"
        script = f"คนยุคใหม่โสดอย่างมีคุณภาพค่ะคุณลูกค้า! แผนนี้นิวจัดมาเพื่อการ **'เกษียณสุข'** โดยเฉพาะ เป็นการทยอยเก็บเงินตั้งแต่วัย {age} ปี พอถึงวัยเกษียณ ปล่อยให้ FWD ทำหน้าที่จ่ายเงินเดือนให้คุณลูกค้าใช้ชิลๆ ทุกเดือนเลยค่ะ ดูแลตัวเองได้แบบสวยๆ/หล่อๆ นิวทำตัวเลขคร่าวๆ ให้ดูนะคะ"

    # Fallback
    else:
        recommended_product = "FWD Life Protector (ประกันชีวิตพื้นฐาน)"
        selling_point = "สร้างรากฐานความมั่นคงพื้นฐาน ทุนประกันสูง เบี้ยต่ำ"
        benefit = "✔️ **คุ้มครองรายได้ (Income Protection):** หากเกิดเหตุไม่คาดฝัน ครอบครัวยังมีเงินก้อนตั้งตัว\n✔️ **สภาพคล่องฉุกเฉิน:** มูลค่ากรมธรรม์สามารถนำมาใช้เป็นเงินหมุนเวียนยามจำเป็นได้"
        script = f"เพื่อเป็นรากฐานทางการเงินที่แข็งแกร่ง นิวขอแนะนำความคุ้มครองพื้นฐานตัวนี้ค่ะ เป็นการป้องกันความเสี่ยงให้เงินเก็บก้อนใหญ่ของคุณลูกค้าปลอดภัย และสร้างความอุ่นใจให้คนในครอบครัวค่ะ"

    st.success(f"🏆 **ผลิตภัณฑ์ที่ระบบแนะนำ:** {recommended_product}")
    st.info(f"🌟 **ประโยชน์สูงสุดที่ลูกค้าจะได้รับ (Key Benefits):**\n{benefit}")

    st.markdown("### 💬 สคริปต์เสนอขาย (สำหรับ RM นิว)")
    st.markdown(f"<div class='fwd-box'>👩‍💼 <b>นิว:</b> \"{script}\"</div>", unsafe_allow_html=True)
