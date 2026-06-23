import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

# --- 1. PAGE SETUP & THEME ---
st.set_page_config(page_title="METHATWIN AI | San Pa Tong", layout="wide")

# --- 2. ADVANCED CSS (Deep Navy, Orange, White/Ice Blue) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&family=Michroma&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { font-family: 'Kanit', sans-serif; }
        
        /* พื้นหลังสีน้ำเงินเข้ม (Deep Navy) */
        .stApp { background-color: #0A192F; color: #E6F1FF; }
        
        /* โลโก้ METHATWIN */
        .brand-logo {
            font-family: 'Michroma', sans-serif;
            font-size: 42px;
            color: #F47B20;
            text-shadow: 0px 0px 15px rgba(244, 123, 32, 0.5);
            margin-bottom: 0px;
            letter-spacing: 2px;
        }
        .brand-sub { font-size: 13px; color: #8892B0; letter-spacing: 4px; margin-top: -5px; margin-bottom: 25px; text-transform: uppercase; }
        
        /* กรอบ Metric Cards (สีน้ำเงินกรมท่า ตัดขอบส้มและขาว) */
        .glass-panel {
            background-color: #112240;
            border: 1px solid #233554;
            border-left: 5px solid #F47B20;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            transition: 0.3s;
        }
        .glass-panel:hover { border-left: 5px solid #64FFDA; transform: translateY(-3px); }
        
        .panel-icon { color: #64FFDA; font-size: 18px; margin-right: 8px; }
        .panel-title { color: #8892B0; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500; }
        .panel-val { font-size: 34px; font-weight: 700; color: #FFFFFF; margin: 8px 0 0 0; line-height: 1.1; }
        .panel-sub { font-size: 13px; color: #CCD6F6; margin-top: 5px; }
        
        /* สีตัวอักษรเน้นย้ำ */
        .text-accent { color: #F47B20 !important; }
        .text-ice { color: #64FFDA !important; }
        .text-danger { color: #FF3D00 !important; }
        
        /* ซ่อนเมนู Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE: ข้อมูลแปลงนาจริง ศูนย์วิจัยข้าวสันป่าตอง ---
PLOT_DATA = {
    "PLOT_A": {
        "name": "แปลง A (แปลงทดลอง AWD)",
        "lat": 18.6185, "lon": 98.8920,
        "manager": "ศูนย์วิจัยข้าวเชียงใหม่ (แปลงนวัตกรรม)",
        "status": "AWD (กำลังระบายน้ำ)",
        "water_level": "-12 cm", "methane": 12.5, "ch4_status": "SAFE (ปลอดภัย)", "color": "#64FFDA",
        "ai_action": "รักษาระดับน้ำใต้ดินต่อไป"
    },
    "PLOT_B": {
        "name": "แปลง B (แปลงควบคุม น้ำท่วมขัง)",
        "lat": 18.6198, "lon": 98.8945,
        "manager": "แปลงเปรียบเทียบ (Baseline)",
        "status": "FLOODED (น้ำท่วมขังต่อเนื่อง 20 วัน)",
        "water_level": "+8 cm", "methane": 78.4, "ch4_status": "CRITICAL (วิกฤต)", "color": "#FF3D00",
        "ai_action": "สั่งการ IoT สูบน้ำออกด่วน!"
    },
    "PLOT_C": {
        "name": "แปลง C (เครือข่ายเกษตรกร)",
        "lat": 18.6165, "lon": 98.8890,
        "manager": "กลุ่มเกษตรกรแปลงใหญ่ ต.มะขามหลวง",
        "status": "TRANSITION (กำลังปรับตัว)",
        "water_level": "-2 cm", "methane": 45.2, "ch4_status": "WARNING (เฝ้าระวัง)", "color": "#F47B20",
        "ai_action": "แนะนำให้หยุดสูบน้ำเข้าแปลง"
    }
}

@st.cache_data(ttl=5)
def generate_radar_data(plot_key):
    np.random.seed(int(time.time()) % 100)
    num_points = 500
    
    # ดึงพิกัดศูนย์กลางจากแปลงที่เลือก
    center_lat = PLOT_DATA[plot_key]["lat"]
    center_lon = PLOT_DATA[plot_key]["lon"]
    
    lats = np.random.normal(center_lat, 0.0008, num_points)
    lons = np.random.normal(center_lon, 0.0008, num_points)
    
    if plot_key == "PLOT_B": # แดง/วิกฤต
        weights = np.random.normal(0.85, 0.15, num_points)
    elif plot_key == "PLOT_C": # ส้ม/เฝ้าระวัง
        weights = np.random.normal(0.60, 0.15, num_points)
    else: # เขียว/AWD
        weights = np.random.normal(0.20, 0.15, num_points)
        
    weights = np.clip(weights, 0, 1)
    data = [[lat, lon, weight] for lat, lon, weight in zip(lats, lons, weights)]
    data.extend([[0, 0, 1.0], [0, 0, 0.0]]) # Anchor สำหรับเรดาร์สี
    return data

# --- 4. SIDEBAR CONTROL ---
with st.sidebar:
    st.markdown('<h1 class="brand-logo">METHATWIN</h1><div class="brand-sub">IoT & Satellite Sync</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<div class="panel-title" style="margin-bottom:10px; color:#F47B20;"><i class="fa-solid fa-map-location-dot"></i> TARGET SELECTION</div>', unsafe_allow_html=True)
    selected_plot = st.radio(
        "เลือกแปลงนาเป้าหมาย:",
        ["PLOT_A", "PLOT_B", "PLOT_C"],
        format_func=lambda x: PLOT_DATA[x]["name"]
    )
    
    st.markdown("---")
    st.markdown('<div class="panel-title" style="margin-bottom:10px; color:#64FFDA;"><i class="fa-solid fa-microchip"></i> IoT SENSOR STATUS</div>', unsafe_allow_html=True)
    st.success("🟢 Node 01: Online\n🟢 Node 02: Online\n🟢 Sentinel-2 API: Synced")

heat_data = generate_radar_data(selected_plot)
current_data = PLOT_DATA[selected_plot]

# --- 5. MAIN DASHBOARD ---
st.markdown(f'<h2 style="color: #F47B20; font-weight: 700; margin-bottom: 0;">{current_data["name"]}</h2>', unsafe_allow_html=True)
st.markdown(f'<div style="color: #8892B0; font-size: 15px; margin-bottom: 20px;"><i class="fa-solid fa-user-tie"></i> ผู้รับผิดชอบ: {current_data["manager"]} | 📍 ต.มะขามหลวง อ.สันป่าตอง จ.เชียงใหม่</div>', unsafe_allow_html=True)

# Metrics Panel
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f'<div class="glass-panel" style="border-left-color: {current_data["color"]};"><div class="panel-title"><i class="fa-solid fa-cloud panel-icon" style="color:{current_data["color"]};"></i> Methane Flux</div><div class="panel-val" style="color:{current_data["color"]};">{current_data["methane"]}</div><div class="panel-sub">mg/m²/h ({current_data["ch4_status"]})</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-water panel-icon"></i> Water Level (IoT)</div><div class="panel-val text-ice">{current_data["water_level"]}</div><div class="panel-sub">{current_data["status"]}</div></div>', unsafe_allow_html=True)

# คำนวณคาร์บอนเครดิตจำลอง
cc_value = "0.45" if selected_plot == "PLOT_A" else ("0.12" if selected_plot == "PLOT_C" else "0.00")
c3.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-leaf panel-icon" style="color:#F47B20;"></i> Carbon Credit</div><div class="panel-val text-accent">{cc_value}</div><div class="panel-sub">tCO₂e / Rai (MRV EST.)</div></div>', unsafe_allow_html=True)

c4.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-robot panel-icon" style="color:#FFFFFF;"></i> AI Recommendation</div><div class="panel-val text-ice" style="font-size:20px; margin-top:14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{current_data["ai_action"]}</div><div class="panel-sub">Action Required</div></div>', unsafe_allow_html=True)

# --- MAP SECTION ---
st.markdown('<div style="margin-top:15px; margin-bottom:10px; color:#8892B0; font-size:14px; letter-spacing:1px; text-transform:uppercase;"><i class="fa-solid fa-satellite" style="color:#64FFDA; margin-right:8px;"></i> Hybrid Digital Twin Map (Satellite + Ground IoT)</div>', unsafe_allow_html=True)

m = folium.Map(
    location=[18.6180, 98.8920], # จุดกึ่งกลางภาพรวม
    zoom_start=16, 
    tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", 
    attr="Google Maps Satellite",
    control_scale=True
)

# วาดหมุด (Markers) สำหรับ แปลง A, B, C บนแผนที่
for key, plot in PLOT_DATA.items():
    icon_color = "green" if key == "PLOT_A" else ("red" if key == "PLOT_B" else "orange")
    folium.Marker(
        [plot["lat"], plot["lon"]],
        popup=folium.Popup(f"<b>{plot['name']}</b><br>ระดับน้ำ: {plot['water_level']}<br>มีเทน: {plot['methane']} mg/m²/h", max_width=250),
        tooltip=f"คลิกดูข้อมูล {plot['name']}",
        icon=folium.Icon(color=icon_color, icon="info-sign")
    ).add_to(m)

# เรดาร์ไล่สีสมจริง
color_gradient = { 0.2: '#64FFDA', 0.5: '#FFEA00', 0.7: '#F47B20', 1.0: '#FF3D00' }

HeatMap(
    heat_data, 
    radius=30,      
    blur=20,         
    gradient=color_gradient,
    max_zoom=18
).add_to(m)

st_folium(m, width=1200, height=500, returned_objects=[])

# --- DATA TABLE (ตัวแปรเชิงลึก) ---
st.markdown("### 📊 ข้อมูลพารามิเตอร์เชิงลึก (Deep Parameters Analysis)")
df_params = pd.DataFrame({
    "ตัวแปร": ["ดัชนีพืชพรรณ (NDVI)", "ดัชนีผิวน้ำ (NDWI)", "อุณหภูมิดิน (IoT)", "ความชื้นดิน (IoT)"],
    "PLOT A (AWD)": ["0.72 (สมบูรณ์)", "-0.15 (แห้ง)", "28.5 °C", "45% (เหมาะสม)"],
    "PLOT B (ท่วมขัง)": ["0.68 (ปกติ)", "0.45 (น้ำขังสูง)", "26.2 °C", "100% (อิ่มตัว)"],
    "แหล่งข้อมูล": ["ดาวเทียม Sentinel-2", "ดาวเทียม Sentinel-2", "เซนเซอร์ฝังดิน (Depth 10cm)", "เซนเซอร์ฝังดิน (Depth 10cm)"]
})
st.table(df_params)
