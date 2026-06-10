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
st.set_page_config(page_title="✨ RM New x Ae 💕 Phi Vic 🐱", layout="wide", page_icon="💜")

# CSS ตกแต่ง
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .fund-card { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #4e2a84; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;}
    .script-box { background-color: #f3eef9; padding: 25px; border-radius: 12px; border-left: 6px solid #4e2a84; margin-bottom: 20px; font-size: 16px; line-height: 1.8;}
    </style>
    """, unsafe_allow_html=True)

# แถบเมนูด้านข้าง
st.sidebar.markdown("## 💜 SCB FIRST & FWD")
app_mode = st.sidebar.radio("เลือกโหมด:", ["📈 โหมดการลงทุน (SCB FIRST)", "🛡️ โหมดประกัน FWD"])

if app_mode == "📈 โหมดการลงทุน (SCB FIRST)":
    st.title("✨ ระบบบริหารพอร์ต SCB FIRST")
    
    # -----------------------------------------------------
    # ปรับปรุง: คลังข้อมูลกองทุน SCB แบบเต็มสูบ
    # -----------------------------------------------------
    st.subheader("🏦 คลังข้อมูลกองทุนรวม SCBAM (Pitching Guide)")
    
    fund_options = {
        "SCBS&P500": {"นโยบาย": "เน้นลงทุนในดัชนี S&P 500 สหรัฐฯ (500 บริษัทที่ใหญ่ที่สุด)", "ความเสี่ยง": "ระดับ 6 (สูง)", "จุดเด่น": "เป็น Core Portfolio ที่สร้างการเติบโตระยะยาว"},
        "SCBNDQ (Nasdaq 100)": {"นโยบาย": "เน้นหุ้นเทคโนโลยีชั้นนำ 100 ตัวในสหรัฐฯ", "ความเสี่ยง": "ระดับ 6 (สูง)", "จุดเด่น": "โอกาสเติบโตสูงจาก AI และนวัตกรรมโลก"},
        "SCBSEMI": {"นโยบาย": "ลงทุนในกลุ่มเซมิคอนดักเตอร์และ AI", "ความเสี่ยง": "ระดับ 7 (สูงมาก)", "จุดเด่น": "กระดูกสันหลังของ AI ยุคใหม่"},
        "SCBCE (หุ้นจีน)": {"นโยบาย": "ลงทุนในหุ้นจีนขนาดใหญ่ที่จดทะเบียนในตลาดต่างประเทศ", "ความเสี่ยง": "ระดับ 6 (สูง)", "จุดเด่น": "Valuation จีนตอนนี้ถูกมาก น่าสะสม"},
        "SCBDV (หุ้นไทยปันผล)": {"นโยบาย": "เน้นหุ้นไทยพื้นฐานดีที่จ่ายปันผลสม่ำเสมอ", "ความเสี่ยง": "ระดับ 6 (สูง)", "จุดเด่น": "เน้นสร้าง Cash Flow กระแสเงินสด"}
    }

    selected_fund = st.selectbox("เลือกกองทุนเพื่อดูรายละเอียด:", list(fund_options.keys()))
    
    # แสดงข้อมูลกองทุนแบบสวยๆ
    fund = fund_options[selected_fund]
    st.markdown(f"""
        <div class="fund-card">
            <h3>{selected_fund}</h3>
            <p><b>นโยบาย:</b> {fund['นโยบาย']}</p>
            <p><b>ระดับความเสี่ยง:</b> {fund['ความเสี่ยง']}</p>
            <p><b>จุดเด่นสำหรับ FIRST:</b> {fund['จุดเด่น']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎙️ สคริปต์เสนอขายสำหรับลูกค้า SCB FIRST")
    script = f"พี่คะ สำหรับกองทุน <b>{selected_fund}</b> ตัวนี้นะคะ นิวประเมินแล้วว่าเหมาะกับพอร์ตของพี่มากค่ะ เพราะ {fund['จุดเด่น']} ถ้าพี่อยากปรับสัดส่วนการลงทุนเพื่อรับโอกาสในตลาดนี้ นิวแนะนำให้เราลองแบ่งเงินเข้ามาเพิ่มสัดส่วนตัวนี้ดูนะคะ นิวช่วยทำจองผ่านแอป SCB EASY ให้พี่เดี๋ยวนี้เลยค่ะ"
    st.markdown(f"<div class='script-box'>{script}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.info("💡 หมายเหตุ: ข้อมูลกองทุนเป็นข้อมูลสรุปเบื้องต้น พี่เอ้สามารถอัปเดตสัดส่วนลงทุน (Asset Allocation) ตามความเหมาะสมของลูกค้าแต่ละท่านได้เลยค่ะ")

elif app_mode == "🛡️ โหมดประกันสุขภาพ/ชีวิต (FWD)":
    st.title("🛡️ RM New x FWD 🧡")
    st.write("โหมดประกันพร้อมใช้งาน (เหมือนเดิมครับพี่เอ้)")
