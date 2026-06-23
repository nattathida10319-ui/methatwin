import streamlit as st
import pandas as pd
import numpy as np
import datetime

# --- 1. ตั้งค่าคอนฟิกหลักของเว็บ ---
st.set_page_config(page_title="MethaTwin Dashboard", layout="wide", page_icon="🍃")

# --- 2. ฟังก์ชันจำลองดาต้าเซต (Dataset Simulation) ตามขอบเขตโครงงาน สสวท. ---
# ดึงข้อมูลตัวแปรตามข้อเสนอ: ระดับน้ำ, ความชื้นดิน, อุณหภูมิ, ความชื้นสัมพัทธ์, NDVI, NDWI
@st.cache_data
def load_simulated_dataset():
    dates = [datetime.date(2026, 5, 19) + datetime.timedelta(days=i) for i in range(10)]
    
    # ดาต้าเซตแปลงที่ 1: ทำนาแบบน้ำท่วมขังต่อเนื่อง (Flooded / Control)
    df_flooded = pd.DataFrame({
        'วันที่': dates,
        'ระดับน้ำในนา (cm)': [5.0, 5.5, 6.0, 6.8, 7.2, 7.8, 8.0, 8.0, 7.8, 7.8],
        'ความชื้นดิน (%)': [90, 92, 95, 95, 95, 95, 96, 95, 95, 95],
        'อุณหภูมิอากาศ (°C)': [30.1, 30.5, 29.8, 30.2, 31.0, 30.2, 30.5, 29.9, 30.1, 30.2],
        'ความชื้นสัมพัทธ์ (%)': [75, 74, 78, 72, 70, 72, 73, 76, 75, 72],
        'ดัชนีพืชพรรณ (NDVI)': [0.45, 0.48, 0.50, 0.53, 0.55, 0.58, 0.60, 0.62, 0.63, 0.65],
        'ดัชนีความชื้นพื้นที่ (NDWI)': [0.60, 0.62, 0.65, 0.66, 0.68, 0.70, 0.72, 0.71, 0.70, 0.71],
        'ฟลักซ์ก๊าซมีเทน (mg/m²/h)': [15.2, 18.5, 22.1, 25.4, 28.0, 31.2, 34.5, 36.8, 37.5, 37.6],
        ' Methane Risk Index': [45, 52, 60, 68, 75, 82, 88, 92, 95, 98]
    })
    
    # ดาต้าเซตแปลงที่ 2: จัดการน้ำแบบเปียกสลับแห้ง (AWD / Treatment)
    df_awd = pd.DataFrame({
        'วันที่': dates,
        'ระดับน้ำในนา (cm)': [5.0, 3.5, 1.2, -1.5, -4.0, -7.5, -7.5, -3.0, 2.0, 5.0],
        'ความชื้นดิน (%)': [90, 85, 80, 72, 65, 68, 68, 78, 88, 92],
        'อุณหภูมิอากาศ (°C)': [30.1, 30.4, 29.9, 30.1, 30.8, 30.2, 30.4, 30.0, 30.2, 30.3],
        'ความชื้นสัมพัทธ์ (%)': [75, 73, 76, 71, 68, 72, 72, 75, 74, 73],
        'ดัชนีพืชพรรณ (NDVI)': [0.45, 0.47, 0.49, 0.52, 0.54, 0.57, 0.59, 0.61, 0.63, 0.64],
        'ดัชนีความชื้นพื้นที่ (NDWI)': [0.60, 0.55, 0.45, 0.32, 0.20, 0.22, 0.25, 0.40, 0.58, 0.61],
        'ฟลักซ์ก๊าซมีเทน (mg/m²/h)': [15.2, 16.0, 14.1, 11.5, 9.2, 8.0, 8.5, 10.2, 14.5, 22.4],
        ' Methane Risk Index': [45, 48, 40, 32, 24, 20, 22, 28, 42, 58]
    })
    return df_flooded, df_awd

df_flooded, df_awd = load_simulated_dataset()

# --- 3. การสร้างหน้าย่อยต่าง ๆ (Multi-Page Functions) ---

def page_dashboard():
    st.markdown('<h1 style="color:#1E6F5C;">🍃 MethaTwin: หน้าหลักแดชบอร์ด</h1>', unsafe_allow_html=True)
    st.caption("ระบบจำลองสถานะ Real-time แปลงนาข้าวศูนย์วิจัยข้าวเชียงใหม่ อ.สันป่าตอง")
    
    # แถบเลือกสถานการณ์ในหน้าหลัก
    scenario = st.radio("สลับมุมมองการจำลองสถานการณ์แปลงนา:", ["การจัดการน้ำแบบเปียกสลับแห้ง (AWD)", "การทำนาแบบน้ำท่วมขังต่อเนื่อง (Flooded)"], horizontal=True)
    df_current = df_awd if scenario == "การจัดการน้ำแบบเปียกสลับแห้ง (AWD)" else df_flooded
    latest = df_current.iloc[-1]
    
    # แสดงตัวเลขสรุป (Metrics) ให้เหมือนภาพตัวอย่าง
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        risk = "🔴 สูงมาก" if latest[' Methane Risk Index'] > 60 else "🟢 ต่ำ"
        st.metric("ดัชนีความเสี่ยงมีเทน", f"{latest[' Methane Risk Index']}/100", f"สถานะ: {risk}")
    with col2:
        st.metric("ค่าฟลักซ์มีเทนคาดการณ์", f"{latest['ฟลักซ์ก๊าซมีเทน (mg/m²/h)']} mg/m²/h")
    with col3:
        st.metric("ระดับน้ำในนาปัจจุบัน", f"{latest['ระดับน้ำในนา (cm)']} cm")
    with col4:
        st.metric("ความชื้นในดิน", f"{latest['ความชื้นดิน (%)']}%")

    st.markdown("---")
    col_map, col_ai = st.columns([2, 1])
    with col_map:
        st.subheader("📍 แผนที่ความเสี่ยงการปล่อยมีเทน (Digital Twin GIS)")
        # พิกัดศูนย์วิจัยข้าวสันป่าตอง
        coords = pd.DataFrame({'lat': [18.6235], 'lon': [98.8964]})
        st.map(coords, zoom=14)
    with col_ai:
        st.subheader("🤖 คำแนะนำจาก AI")
        if "AWD" in scenario:
            st.success("💡 **AI แนะนำ:** ระดับน้ำลดลงอยู่ในเกณฑ์แกล้งข้าว ปล่อยให้ดินแห้งต่อไปอีก 3 วัน เพื่อตัดวงจรจุลินทรีย์เมทาโนเจนและลดก๊าซมีเทนได้ถึง 31%!")
        else:
            st.error("🚨 **AI แจ้งเตือน:** ตรวจพบน้ำท่วมขังสะสมนานเกินไป ดินขาดออกซิเจน จุลินทรีย์กำลังผลิตมีเทนพุ่งสูง แนะนำให้ระบายน้ำออกทันที")

def page_satellite():
    st.markdown('<h1 style="color:#1E6F5C;">🛰️ ข้อมูลวิเคราะห์จากดาวเทียม (Sentinel-2)</h1>', unsafe_allow_html=True)
    st.write("ดึงข้อมูลค่าดัชนีทางพืชพรรณและดัชนีน้ำ เช็กความอุดมสมบูรณ์และน้ำท่วมขังราย 10 วัน")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 แนวโน้มดัชนีพืชพรรณ (NDVI)")
        chart_data = pd.DataFrame({'วันที่': df_awd['วันที่'], 'AWD (Treatment)': df_awd['ดัชนีพืชพรรณ (NDVI)'], 'Flooded (Control)': df_flooded['ดัชนีพืชพรรณ (NDVI)']}).set_index('วันที่')
        st.line_chart(chart_data)
    with col2:
        st.subheader("💧 แนวโน้มดัชนีความชื้นพื้นที่ (NDWI)")
        chart_data2 = pd.DataFrame({'วันที่': df_awd['วันที่'], 'AWD (Treatment)': df_awd['ดัชนีความชื้นพื้นที่ (NDWI)'], 'Flooded (Control)': df_flooded['ดัชนีความชื้นพื้นที่ (NDWI)']}).set_index('วันที่')
        st.line_chart(chart_data2)

def page_mrv():
    st.markdown('<h1 style="color:#1E6F5C;">📊 ส่วนเสริมการประเมินคาร์บอนเครดิต (MRV)</h1>', unsafe_allow_html=True)
    st.write("รายงานสรุปสถิติตามแนวคิด Monitoring, Reporting and Verification (MRV) เพื่อสนับสนุนนโยบายคาร์บอนต่ำ")
    
    st.info("💡 **เปรียบเทียบผลลัพธ์:** การจัดการน้ำแบบ AWD สามารถลดการปล่อยก๊าซมีเทนสะสมลงได้ คิดเป็นคาร์บอนเครดิตประเมินเบื้องต้น **0.42 tCO2e** (มูลค่าประมาณ 1,260 บาทต่อไร่)")
    
    st.subheader("📉 กราฟเปรียบเทียบฟลักซ์ก๊าซมีเทน (Methane Flux Trend)")
    chart_methane = pd.DataFrame({
        'วันที่': df_awd['วันที่'],
        'การทำนาแบบน้ำท่วมขัง (Flooded)': df_flooded['ฟลักซ์ก๊าซมีเทน (mg/m²/h)'],
        'การจัดการน้ำแบบเปียกสลับแห้ง (AWD)': df_awd['ฟลักซ์ก๊าซมีเทน (mg/m²/h)']
    }).set_index('วันที่')
    st.line_chart(chart_methane)

def page_dataset():
    st.markdown('<h1 style="color:#1E6F5C;">📁 คลังข้อมูลดิบ (IoT & Satellite Dataset)</h1>', unsafe_allow_html=True)
    st.write("ตารางแสดงข้อมูลดิบทั้งหมดที่ระบบนำเข้า (Input) มาใช้ประมวลผลในโมเดล Machine Learning")
    
    st.subheader("📂 ข้อมูลแปลงนาแบบเปียกสลับแห้ง (AWD Dataset)")
    st.dataframe(df_awd, use_container_width=True)
    
    st.subheader("📂 ข้อมูลแปลงนาแบบน้ำท่วมขัง (Flooded Dataset)")
    st.dataframe(df_flooded, use_container_width=True)

# --- 4. ระบบเปิดเมนูหลายหน้า (Navigation) ---
pg = st.navigation([
    st.Page(page_dashboard, title="หน้าหลักแดชบอร์ด", icon="🎯"),
    st.Page(page_satellite, title="ข้อมูลดาวเทียม Sentinel-2", icon="🛰️"),
    st.Page(page_mrv, title="รายงานคาร์บอนเครดิต (MRV)", icon="📊"),
    st.Page(page_dataset, title="คลังข้อมูลดิบแปลงนา", icon="📁")
])
pg.run()
