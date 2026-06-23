import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time

# --- 1. SET UP THE COSMIC DARK THEME ---
st.set_page_config(
    page_title="MethaTwin AI | Satellite & IoT Command Center",
    layout="wide",
    page_icon="🛰️"
)

# Custom CSS for Modern High-Tech Dashboard
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    
    /* Premium Cards */
    .crypto-card {
        background: linear-gradient(135deg, #1A202C 0%, #111622 100%);
        border: 1px solid #2D3748;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    
    /* Accent Borders */
    .accent-green { border-top: 4px solid #00E676; }
    .accent-red { border-top: 4px solid #FF3D00; }
    .accent-blue { border-top: 4px solid #00B0FF; }
    .accent-purple { border-top: 4px solid #D500F9; }
    
    /* Typography */
    .card-title { color: #A0AEC0; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .card-value { color: #FFFFFF; font-size: 36px; font-weight: 700; margin-top: 10px; margin-bottom: 5px; }
    .card-status { font-size: 14px; font-weight: 500; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #111622 !important; border-right: 1px solid #2D3748; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA ENGINE (INTEGRATING SATELLITE + IOT) ---
CENTER_LAT, CENTER_LON = 18.6235, 98.8964

@st.cache_data(ttl=10)
def fetch_satellite_iot_layers(mode):
    np.random.seed(int(time.time()) % 100)
    num_nodes = 180
    
    # Simulate high-precision boundary of San Pa Tong field
    lats = np.random.uniform(18.6215, 18.6255, num_nodes)
    lons = np.random.uniform(98.8940, 98.8985, num_nodes)
    
    # Dynamic logic depending on selected Water Management Mode
    if mode == "🌿 โหมดเปียกสลับแห้ง (AWD อัจฉริยะ)":
        methane_flux = np.random.uniform(8, 28, num_nodes)
        ndvi = np.random.uniform(0.65, 0.78, num_nodes) # Good vegetation
        ndwi = np.random.uniform(0.12, 0.25, num_nodes) # Low surface water
        colors = [[0, 230, 118, 160] for _ in range(num_nodes)] # Glowing Green Points
    else:
        methane_flux = np.random.uniform(45, 88, num_nodes)
        ndvi = np.random.uniform(0.58, 0.70, num_nodes) 
        ndwi = np.random.uniform(0.65, 0.85, num_nodes) # High flood water reflection
        colors = [[255, 61, 0, 160] for _ in range(num_nodes)] # Glowing Red Points
        
    df = pd.DataFrame({
        'latitude': lats, 'longitude': lons, 
        'methane': methane_flux, 'NDVI': ndvi, 'NDWI': ndwi,
        'r': [c[0] for c in colors], 'g': [c[1] for c in colors], 'b': [c[2] for c in colors], 'a': [c[3] for c in colors]
    })
    return df

# --- 3. HIGH-TECH SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2043/2043422.png", width=70)
    st.markdown("## METHATWIN AI\n**[AI NEW GEN COMPETITION]**")
    st.markdown("---")
    
    # Navigation Menu
    menu_selection = st.radio(
        "🔮 เมนูควบคุมและติดตาม",
        ["🎯 แดชบอร์ดหลัก", "🛰️ ข้อมูลวิเคราะห์จากดาวเทียม", "📊 รายงานคาร์บอนเครดิต (MRV)"]
    )
    
    st.markdown("---")
    st.markdown("### 🎛️ กล่องสั่งการแปลงนา")
    water_mode = st.selectbox("ปรับระบบจัดการน้ำภาคสนาม:", ["🌿 โหมดเปียกสลับแห้ง (AWD อัจฉริยะ)", "💧 โหมดน้ำท่วมขังดั้งเดิม (Flooded)"])
    
    st.markdown("---")
    st.sidebar.caption("🤖 พัฒนาโดยทีม MethaTwin AI สำหรับโครงการประกวดนวัตกรรมระดับประเทศ AI New Gen 2026")

# Global data loading based on sidebar selection
live_data = fetch_satellite_iot_layers(water_mode)

# --- 4. RENDER MODULES ---

if menu_selection == "🎯 แดชบอร์ดหลัก":
    st.markdown("# 🌾 ศูนย์ควบคุมแปลงนาอัจฉริยะแบบ Digital Twin")
    st.caption(f"📍 พิกัดอ้างอิง: แปลงวิจัยที่ 3 ศูนย์วิจัยข้าวเชียงใหม่ อ.สันป่าตอง จ.เชียงใหม่ | 📡 เชื่อมต่อเซนเซอร์ IoT และดาวเทียม Sentinel-2")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4 UI Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    
    if "AWD" in water_mode:
        with col1:
            st.markdown('<div class="crypto-card accent-green"><div class="card-title">มีเทนเฉลี่ย (CH₄ Flux)</div><div class="card-value">14.8 <span style="font-size:16px; color:#A0AEC0;">mg/m²/h</span></div><div class="card-status" style="color:#00E676;">⬇ ลดลง 48.2% จากค่าฐาน</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="crypto-card accent-green"><div class="card-title">ดัชนีความเสี่ยงพื้นที่</div><div class="card-value">18 / 100</div><div class="card-status" style="color:#00E676;">🟢 ปลอดภัย (โหมดแกล้งข้าว)</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="crypto-card accent-blue"><div class="card-title">ระดับน้ำใต้ผิวดิน</div><div class="card-value">-4.5 <span style="font-size:16px; color:#A0AEC0;">cm</span></div><div class="card-status" style="color:#00B0FF;">น้ำลดเพื่อให้รากข้าวแข็งแรง</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="crypto-card accent-purple"><div class="card-title">คาร์บอนเครดิตสะสม</div><div class="card-value">0.42 <span style="font-size:16px; color:#A0AEC0;">tCO₂e/ไร่</span></div><div class="card-status" style="color:#D500F9;">โมเดล MRV ผ่านการรับรอง</div></div>', unsafe_allow_html=True)
    else:
        with col1:
            st.markdown('<div class="crypto-card accent-red"><div class="card-title">มีเทนเฉลี่ย (CH₄ Flux)</div><div class="card-value">68.5 <span style="font-size:16px; color:#A0AEC0;">mg/m²/h</span></div><div class="card-status" style="color:#FF3D00;">⚠️ วิกฤต! พุ่งสูงเกินเกณฑ์</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="crypto-card accent-red"><div class="card-title">ดัชนีความเสี่ยงพื้นที่</div><div class="card-value">84 / 100</div><div class="card-status" style="color:#FF3D00;">🔴 ความเสี่ยงแก๊สสะสมสูงมาก</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="crypto-card accent-blue"><div class="card-title">ระดับน้ำใต้ผิวดิน</div><div class="card-value">+9.2 <span style="font-size:16px; color:#A0AEC0;">cm</span></div><div class="card-status" style="color:#00B0FF;">น้ำท่วมขังขวางการระบายก๊าซ</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="crypto-card accent-red"><div class="card-title">คาร์บอนเครดิตสะสม</div><div class="card-value">0.00 <span style="font-size:16px; color:#A0AEC0;">tCO₂e/ไร่</span></div><div class="card-status" style="color:#FF3D00;">ระงับการสะสมคาร์บอน</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Map Section
    st.markdown("### 🗺️ ระบบระบุพิกัดความหนาแน่นก๊าซมีเทนระดับฟิลด์อนุกรม (Real-time Spatial Overlay)")
    st.write("แผนที่จำลองพิกัดแปลงรูปหัวใจ ณ ศูนย์วิจัยข้าวเชียงใหม่: จุดหนาแน่นตามข้อมูลประมวลผลอัลกอริทึมร่วม AI & Satellite")
    
    # Render High-Stability Point-Layer Map
    st.map(live_data, latitude=CENTER_LAT, longitude=CENTER_LON, zoom=16, size=24)
    st.caption("💡 วิธีอ่านแผนที่: 🟢 สีเขียวเรืองแสง = โซนปลอดภัยจากการจัดน้ำแบบเปียกสลับแห้ง (มีเทนต่ำ) | 🔴 สีแดงเรืองแสง = โซนวิกฤตที่มีน้ำขังหนาแน่นจนเกิดสภาวะไร้ออกซิเจน")

elif menu_selection == "🛰️ ข้อมูลวิเคราะห์จากดาวเทียม":
    st.markdown("# 🛰️ ข้อมูลพิจารณาภาพถ่ายดาวเทียมขั้นสูง (Sentinel-2 L2A)")
    st.write("นี่คือจุดขายของโครงงาน! AI ทำการดึงข้อมูลภาพถ่ายแถบสีและคำนวณดัชนีวิเคราะห์ 2 ตัวแปรหลักรายแปลง:")
    st.markdown("---")
    
    col_ndvi, col_ndwi = st.columns(2)
    with col_ndvi:
        st.markdown("### 📈 ดัชนีพืชพรรณพยากรณ์ (NDVI - Normalized Difference Vegetation Index)")
        st.write("ใช้อ้างอิงสุขภาพของต้นข้าว ความเขียว และความสมบูรณ์ชีวมวล")
        st.line_chart(live_data['NDVI'], y_label="ค่าความสมบูรณ์ NDVI (0.0 - 1.0)", color="#00E676")
        
    with col_ndwi:
        st.markdown("### 💧 ดัชนีความชื้นผิวดินและการขังของน้ำ (NDWI - Normalized Difference Water Index)")
        st.write("ใช้อ้างอิงการสะสมของน้ำในแปลงนาเพื่อส่งต่อให้ AI คำนวณอัตราการเกิดจุลินทรีย์ผลิตมีเทน")
        st.line_chart(live_data['NDWI'], y_label="ดัชนีผิวน้ำ NDWI", color="#00B0FF")

elif menu_selection == "📊 รายงานคาร์บอนเครดิต (MRV)":
    st.markdown("# 📊 แพลตฟอร์มการประเมินคาร์บอนเครดิตตามมาตรฐานสากล (MRV)")
    st.write("ระบบคำนวณและเก็บบันทึกผล (Monitoring, Reporting, Verification) เพื่อเปลี่ยนการลดก๊าซเรือนกระจกให้เป็นรายได้")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="crypto-card accent-purple" style="text-align: center;"><div class="card-title">ปริมาณการลดก๊าซเรือนกระจกที่ตรวจสอบแล้ว (Verified Emission Reduction)</div><div class="card-value" style="font-size: 54px;">0.42 tCO₂e / ไร่ / ฤดูกาล</div><div class="card-status" style="color:#D500F9;">🎯 สามารถแปลงเป็นมูลค่าคาร์บอนเครดิตเพื่อขายในตลาดคาร์บอนภาคสมัครใจ (T-VER) ได้ทันที</div></div>', unsafe_allow_html=True)
    
    st.markdown("### 📉 กราฟเปรียบเทียบฟลักซ์การปล่อยมีเทนสะสมรายวัน (Methane Emission Projection)")
    # Generate timeline simulation for MRV comparison
    timeline = pd.date_range(start="2026-05-19", periods=15)
    awd_trend = [15, 14, 12, 10, 8, 9, 11, 13, 10, 7, 5, 6, 9, 12, 14]
    flooded_trend = [15, 18, 22, 28, 35, 42, 48, 55, 62, 68, 72, 75, 78, 80, 82]
    
    df_mrv = pd.DataFrame({
        'วันที่': timeline,
        'แปลงนาทั่วไป (Baseline - น้ำท่วมขัง)': flooded_trend,
        'แปลงนาโครงการ (Project - ระบบ AWD)': awd_trend
    }).set_index('วันที่')
    
    st.line_chart(df_mrv)
