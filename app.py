```python
import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. ตั้งค่าหน้าเว็บหน้าจอหลัก
st.set_page_config(page_title="MethaTwin Dashboard", layout="wide", page_icon="🍃")

# 2. ปรับแต่งสไตล์พื้นหลังเบื้องต้น
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: bold; color: #1E6F5C; }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🍃 MethaTwin: Digital Twin for Rice Field Methane Management</p>', unsafe_allow_html=True)
st.subheader("ระบบแบบจำลองเสมือนเพื่อประเมินแก๊สมีเทนและการจัดการน้ำแบบเปียกสลับแห้ง (AWD)")
st.caption(f"📍 พื้นที่ศึกษานำร่อง: ศูนย์วิจัยข้าวเชียงใหม่ อำเภอสันป่าตอง จังหวัดเชียงใหม่ | ข้อมูลจำลองสถานะ Real-time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("---")

# 3. ส่วนควบคุมจำลองสถานการณ์ (Scenario Simulation) ตามขอบเขตในข้อเสนอโครงงาน สสวท.pdf
st.sidebar.header("⚙️ การจำลองสถานการณ์แปลงนา")
selected_scenario = st.sidebar.selectbox(
    "เลือกรูปแบบการจัดการน้ำในแปลงนา:",
    ["การจัดการน้ำแบบเปียกสลับแห้ง (AWD)", "การทำนาแบบน้ำท่วมขังต่อเนื่อง (Flooded)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**📡 สถานะเซนเซอร์ IoT ภาคสนาม:**")
st.sidebar.success("🟢 Node 001 (สันป่าตอง): ออนไลน์ (100%)")

# 4. กำหนดค่าข้อมูลตามสถานการณ์ที่เลือก
if selected_scenario == "การจัดการน้ำแบบเปียกสลับแห้ง (AWD)":
    methane_flux = "12.4 mg/m²/h"
    methane_delta = "-45% (ลดลงจากการแกล้งข้าว)"
    water_level = "-7.5 cm"
    soil_moisture = "68%"
    risk_level = "🟢 ต่ำ (Low Methane Risk)"
    ai_recommendation = "💡 **คำแนะนำจาก AI:** ขณะนี้ระดับน้ำอยู่ที่ -7.5 cm ซึ่งอยู่ในช่วงแกล้งข้าว (AWD) ปล่อยให้ดินแห้งต่อไปอีก 3 วัน เพื่อตัดวงจรการปล่อยก๊าซมีเทน และกระตุ้นให้รากข้าวชอนไชหาอาหารได้ดีขึ้น"
    carbon_credit = "0.42 tCO2e"
    money_earned = "1,260 บาท"
    water_data_sim = [5.0, 3.5, 1.2, -1.0, -3.5, -5.0, -6.5, -7.5, -7.5, -7.5]
    methane_data_sim = [28.5, 26.2, 22.0, 18.1, 14.5, 12.8, 12.4, 12.4, 12.4, 12.4]
else:
    methane_flux = "37.6 mg/m²/h"
    methane_delta = "🔥 +18% (ก๊าซสะสมสูงกว่าปกติ)"
    water_level = "+8.0 cm"
    soil_moisture = "95%"
    risk_level = "🔴 สูงมาก (High Methane Risk)"
    ai_recommendation = "🚨 **คำแนะนำจาก AI:** ตรวจพบสภาพน้ำท่วมขังเป็นเวลานานเกิน 14 วัน ดินขาดออกซิเจนอย่างรุนแรงส่งผลให้จุลินทรีย์เมทาโนเจนผลิตมีเทนพุ่งสูง แนะนำให้ทำการระบายน้ำออกเพื่อแกล้งข้าวทันที"
    carbon_credit = "0.00 tCO2e"
    money_earned = "0 บาท"
    water_data_sim = [5.0, 6.0, 6.5, 7.0, 7.5, 8.0, 8.0, 8.0, 8.0, 8.0]
    methane_data_sim = [28.5, 30.1, 32.4, 34.0, 35.5, 36.8, 37.0, 37.5, 37.6, 37.6]

# 5. แสดงผลการ์ดข้อมูลสรุป (Metrics)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="ดัชนีความเสี่ยงมีเทน", value=risk_level)
with col2:
    st.metric(label="ค่าฟลักซ์ก๊าซมีเทนประมาณการ", value=methane_flux, delta=methane_delta, delta_color="inverse")
with col3:
    st.metric(label="ระดับน้ำในนา (Water Level)", value=water_level)
with col4:
    st.metric(label="คาร์บอนเครดิตสะสม (MRV Evaluation)", value=carbon_credit, delta=f"💵 มูลค่าประเมิน {money_earned}")

st.markdown("---")

# 6. แสดงแผนที่และกล่องแจ้งเตือน AI
col_map, col_alert = st.columns([3, 2])

with col_map:
    st.markdown("### 📍 พิกัดแปลงนาบนแผนที่ดิจิทัล (Digital Twin GIS)")
    # พิกัดศูนย์วิจัยข้าวสันป่าตอง
    sanpatong_coords = pd.DataFrame({'lat': [18.6235], 'lon': [98.8964]})
    st.map(sanpatong_coords, zoom=14)

with col_alert:
    st.markdown("### 🔔 ระบบสนับสนุนการตัดสินใจอัจฉริยะ")
    if "AWD" in selected_scenario:
        st.info(ai_recommendation)
    else:
        st.error(ai_recommendation)
        
    st.warning("🌤️ **พยากรณ์อากาศล่วงหน้า (อ.สันป่าตอง):** ตรวจพบกลุ่มฝนมีโอกาสตก 65% ในอีก 12 ชั่วโมงข้างหน้า แนะนำชะลอการสูบน้ำเข้าแปลงนาเพื่อประหยัดพลังงาน")

st.markdown("---")

# 7. แสดงกราฟแนวโน้ม (Time-Series)
st.markdown("### 📊 กราฟวิเคราะห์แนวโน้มข้อมูลย้อนหลัง 10 วัน")
dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(10)]
dates.reverse()

chart_data = pd.DataFrame({
    'วันที่': dates,
    'ระดับน้ำในนา (cm)': water_data_sim,
    'สถิติก๊าซมีเทน (mg/m²/h)': methane_data_sim
})
chart_data.set_index('วันที่', inplace=True)

st.line_chart(chart_data)
