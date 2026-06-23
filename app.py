import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

# --- 1. PAGE SETUP & THEME ---
st.set_page_config(page_title="METHATWIN AI", layout="wide")

# --- 2. ADVANCED CSS INJECTION (Fonts, Icons, Modern UI) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&family=Michroma&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { font-family: 'Kanit', sans-serif; }
        .stApp { background-color: #0a0a0a; color: #e0e0e0; }
        
        /* โลโก้ METHATWIN เรืองแสง */
        .brand-logo {
            font-family: 'Michroma', sans-serif;
            font-size: 48px;
            background: linear-gradient(90deg, #F47B20, #FFB74D, #FF5722);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0px 0px 20px rgba(244, 123, 32, 0.4);
            margin-bottom: 0px;
            letter-spacing: 3px;
            line-height: 1.2;
        }
        .brand-sub { font-size: 14px; color: #888; letter-spacing: 5px; margin-top: -5px; margin-bottom: 30px; text-transform: uppercase; }
        
        /* กรอบ Metric Cards สไตล์หน้าปัดยาน/แผงควบคุม */
        .glass-panel {
            background: rgba(25, 25, 25, 0.8);
            border: 1px solid #333;
            border-left: 4px solid #F47B20;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
            transition: 0.3s;
        }
        .glass-panel:hover { border-left: 4px solid #FFB74D; background: rgba(35, 35, 35, 0.9); }
        
        .panel-icon { color: #F47B20; font-size: 18px; margin-right: 8px; }
        .panel-title { color: #8a8a8a; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500; }
        .panel-val { font-size: 34px; font-weight: 700; color: #fff; margin: 8px 0 0 0; line-height: 1.1; }
        
        .text-green { color: #00E676 !important; }
        .text-red { color: #FF3D00 !important; }
        .text-orange { color: #F47B20 !important; }
        .text-blue { color: #00B0FF !important; }
        
        .panel-sub { font-size: 13px; color: #666; margin-top: 5px; }
        
        /* ซ่อน UI ของ Streamlit ที่ไม่จำเป็น */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA ENGINE (ย้ายพิกัดลงทุ่งนา & สร้างควันแบบไล่สี) ---
# พิกัดใหม่: ลึกเข้าไปในแปลงนาทดลอง หลบหมู่บ้าน
FIELD_LAT, FIELD_LON = 18.6185, 98.8920

@st.cache_data(ttl=5)
def generate_radar_data(mode):
    np.random.seed(int(time.time()) % 100)
    num_points = 800
    
    # สร้างจุดฟุ้งกระจายในพื้นที่แปลงนา (รัศมีประมาณ 200-300 เมตร)
    lats = np.random.normal(FIELD_LAT, 0.0012, num_points)
    lons = np.random.normal(FIELD_LON, 0.0012, num_points)
    
    if mode == "FLOODED":
        # น้ำท่วมขัง: สร้างค่าความเข้มข้นสูง (ดันไปทางส้ม-แดง)
        weights = np.random.normal(0.85, 0.15, num_points)
    else:
        # AWD: สร้างค่าความเข้มข้นต่ำ (อยู่โซนเขียว-เหลือง)
        weights = np.random.normal(0.3, 0.15, num_points)
        
    # ตัดขอบเขตค่าให้อยู่ระหว่าง 0 ถึง 1
    weights = np.clip(weights, 0, 1)
    
    data = [[lat, lon, weight] for lat, lon, weight in zip(lats, lons, weights)]
    
    # ใส่จุด Anchor บังคับสีให้ Folium แสดงสเกลครบ (เขียวไปแดง) เสมอ (ซ่อนไว้ไกลๆ)
    data.append([0, 0, 1.0]) # บังคับให้มีค่า Max (สีแดง)
    data.append([0, 0, 0.0]) # บังคับให้มีค่า Min (สีเขียว)
    
    return data

# --- 4. SIDEBAR (CONTROL MODULE) ---
with st.sidebar:
    st.markdown('<h1 class="brand-logo" style="font-size:28px;">METHATWIN</h1><div class="brand-sub">Command Center</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<div class="panel-title" style="margin-bottom:10px;"><i class="fa-solid fa-layer-group panel-icon"></i> NAVIGATION</div>', unsafe_allow_html=True)
    menu = st.radio("", ["LIVE RADAR", "FARMING PROTOCOL"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown('<div class="panel-title" style="margin-bottom:10px;"><i class="fa-solid fa-sliders panel-icon"></i> WATER MANAGEMENT</div>', unsafe_allow_html=True)
    water_mode_raw = st.selectbox("", ["AWD (แกล้งข้าว / ระบายน้ำ)", "FLOODED (น้ำท่วมขังขีดสุด)"], label_visibility="collapsed")
    water_mode = "FLOODED" if "FLOODED" in water_mode_raw else "AWD"

heat_data = generate_radar_data(water_mode)

# --- 5. DASHBOARD INTERFACE ---

if menu == "LIVE RADAR":
    # Header โลโก้
    st.markdown('<h1 class="brand-logo">METHATWIN</h1>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">ARTIFICIAL INTELLIGENCE FOR SUSTAINABLE AGRICULTURE</div>', unsafe_allow_html=True)
    
    # Metrics Panel
    c1, c2, c3, c4 = st.columns(4)
    if water_mode == "AWD":
        c1.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-cloud panel-icon"></i> Methane Flux</div><div class="panel-val text-green">14.2</div><div class="panel-sub">mg/m²/h (SAFE ZONE)</div></div>', unsafe_allow_html=True)
        c2.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-water panel-icon"></i> Water Level</div><div class="panel-val text-blue">-12 cm</div><div class="panel-sub">DRAINING IN PROGRESS</div></div>', unsafe_allow_html=True)
        c3.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-leaf panel-icon"></i> Carbon Credit</div><div class="panel-val">0.42</div><div class="panel-sub">tCO₂e / Rai</div></div>', unsafe_allow_html=True)
        c4.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-robot panel-icon"></i> AI Action</div><div class="panel-val text-green" style="font-size:24px; margin-top:14px;">MAINTAIN</div><div class="panel-sub">คงสภาพดินแห้งต่อ 3 วัน</div></div>', unsafe_allow_html=True)
    else:
        c1.markdown('<div class="glass-panel" style="border-color: #FF3D00;"><div class="panel-title"><i class="fa-solid fa-cloud panel-icon" style="color:#FF3D00;"></i> Methane Flux</div><div class="panel-val text-red">82.5</div><div class="panel-sub">mg/m²/h (CRITICAL)</div></div>', unsafe_allow_html=True)
        c2.markdown('<div class="glass-panel" style="border-color: #FF3D00;"><div class="panel-title"><i class="fa-solid fa-water panel-icon" style="color:#FF3D00;"></i> Water Level</div><div class="panel-val text-blue">+8 cm</div><div class="panel-sub">OVERFLOW DETECTED</div></div>', unsafe_allow_html=True)
        c3.markdown('<div class="glass-panel" style="border-color: #FF3D00;"><div class="panel-title"><i class="fa-solid fa-leaf panel-icon" style="color:#FF3D00;"></i> Carbon Credit</div><div class="panel-val text-red">0.00</div><div class="panel-sub">MRV FAILED</div></div>', unsafe_allow_html=True)
        c4.markdown('<div class="glass-panel" style="border-color: #FF3D00;"><div class="panel-title"><i class="fa-solid fa-robot panel-icon" style="color:#FF3D00;"></i> AI Action</div><div class="panel-val text-red" style="font-size:24px; margin-top:14px;">DRAIN NOW</div><div class="panel-sub">ระบายน้ำออกฉุกเฉิน!</div></div>', unsafe_allow_html=True)

    # Map Section
    st.markdown('<div style="margin-top:20px; margin-bottom:10px; color:#A0AEC0; font-size:14px; letter-spacing:1px; text-transform:uppercase;"><i class="fa-solid fa-satellite" style="color:#F47B20; margin-right:8px;"></i> Satellite Radar Overlay (Google Maps)</div>', unsafe_allow_html=True)
    
    # กำหนดแผนที่ Google Maps แบบเห็นแปลงนาชัดๆ
    m = folium.Map(
        location=[FIELD_LAT, FIELD_LON], 
        zoom_start=17, 
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", 
        attr="Google Maps Satellite",
        control_scale=True
    )
    
    # 🎨 เรดาร์ไล่สีสมจริง (เขียว -> เหลือง -> ส้ม -> แดง)
    color_gradient = {
        0.2: '#00E676', # สีเขียว (ปลอดภัย)
        0.5: '#FFEA00', # สีเหลือง (เฝ้าระวัง)
        0.7: '#FF9100', # สีส้ม (เริ่มอันตราย)
        1.0: '#FF3D00'  # สีแดง (วิกฤตมีเทน)
    }

    HeatMap(
        heat_data, 
        radius=28,      
        blur=22,         
        gradient=color_gradient,
        max_zoom=18
    ).add_to(m)
    
    st_folium(m, width=1200, height=520, returned_objects=[])

elif menu == "FARMING PROTOCOL":
    st.markdown('<h1 class="brand-logo" style="font-size:36px;">FARMING PROTOCOL</h1>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">ACTIONABLE INSIGHTS FOR FARMERS</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel"><div class="panel-title text-blue"><i class="fa-solid fa-droplet panel-icon text-blue"></i> PHASE 1: VEGETATIVE STAGE (0-20 DAYS)</div><p style="margin-top:10px;">รักษาระดับน้ำให้ท่วมผิวดิน 2-5 ซม. เพื่อควบคุมวัชพืชหลังปักดำ</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel" style="border-left: 4px solid #F47B20; background: rgba(40,20,10,0.8);"><div class="panel-title text-orange"><i class="fa-solid fa-sun panel-icon text-orange"></i> PHASE 2: ACTIVE TILLERING / AWD (20-45 DAYS) - CURRENT STAGE</div><p style="margin-top:10px;"><b>ระบบปฏิบัติการ:</b> หยุดเติมนํ้า ปล่อยให้นํ้าแห้งจนระดับนํ้าใต้ดินลดลงไปถึง -15 ซม. ท่อ PVC ดินจะเริ่มแตกแตง ออกซิเจนแทรกซึมลงสู่ราก จุลินทรีย์สร้างมีเทนตายลง ตัดวงจรแก๊สเรือนกระจก</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel"><div class="panel-title text-green"><i class="fa-solid fa-wheat-awn panel-icon text-green"></i> PHASE 3: REPRODUCTIVE STAGE (45-80 DAYS)</div><p style="margin-top:10px;">เติมน้ำกลับเข้าแปลงให้สูง 5 ซม. ตลอดช่วงนี้ เพื่อให้ข้าวผสมเกสรและสร้างเมล็ดอย่างสมบูรณ์ ป้องกันผลผลิตร่วงหล่น</p></div>', unsafe_allow_html=True)
