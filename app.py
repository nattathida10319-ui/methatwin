import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

# --- 1. PAGE INITIALIZATION ---
st.set_page_config(page_title="METHATWIN AI | PRECISION COMMAND", layout="wide")

# --- 2. THE ULTIMATE DEEP NAVY CSS (สีกรมท่า-ส้มสุดเท่ + Hover สีเขียว) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&family=Michroma&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { font-family: 'Kanit', sans-serif; }
        
        /* พื้นหลังโทนสเปซ/แล็บล้ำยุค */
        .stApp { background-color: #0A192F; color: #E6F1FF; }
        
        .brand-logo {
            font-family: 'Michroma', sans-serif;
            font-size: 46px;
            color: #F47B20;
            text-shadow: 0px 0px 15px rgba(244, 123, 32, 0.6);
            margin-bottom: 0px;
        }
        .brand-sub { font-size: 13px; color: #8892B0; letter-spacing: 4px; margin-top: -5px; margin-bottom: 25px; text-transform: uppercase; }
        
        /* กรอบ Metric Cards (สีกรมท่าเข้ม ตัดขอบส้ม) */
        .glass-panel {
            background-color: #112240;
            border: 1px solid #233554;
            border-left: 5px solid #F47B20; /* ขอบซ้ายเริ่มต้นสีส้ม */
            border-radius: 8px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            transition: all 0.3s ease;
        }
        
        /* HOVER EFFECT: ชี้แล้วขยับ + ขอบเปลี่ยนเป็นสีเขียว + ไอคอนเด้งและเป็นสีเขียว */
        .glass-panel:hover { 
            border-left: 5px solid #00E676; 
            transform: translateY(-4px); 
            box-shadow: 0 8px 25px rgba(0, 230, 118, 0.2);
            background-color: #1A2D4F;
        }
        .glass-panel:hover .panel-icon {
            color: #00E676 !important; 
            transform: scale(1.2) rotate(-5deg); 
        }
        
        /* ไอคอนตั้งต้นสีส้ม */
        .panel-icon { 
            color: #F47B20; 
            font-size: 20px; 
            margin-right: 10px; 
            display: inline-block;
            transition: all 0.3s ease; 
        }
        
        .panel-title { color: #8892B0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500; }
        .panel-val { font-size: 36px; font-weight: 700; color: #FFFFFF; margin: 10px 0 5px 0; line-height: 1.1; }
        .panel-sub { font-size: 13px; color: #CCD6F6; margin-top: 5px; }
        
        /* Text Colors */
        .text-ice { color: #64FFDA !important; }
        .text-danger { color: #FF3D00 !important; }
        .text-warning { color: #FFEA00 !important; }
        
        .stTabs [data-baseweb="tab"] { color: #8892B0 !important; }
        .stTabs [aria-selected="true"] { color: #F47B20 !important; border-bottom-color: #F47B20 !important; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE: พิกัดแปลงวิจัยแบบเป๊ะๆ (แบ่งล็อกสี่เหลี่ยมผืนผ้าติดกัน) ---
PLOT_DATABASE = {
    "PLOT_A": {
        "name": "แปลงทดลอง A (AWD Zone)",
        # บล็อกซ้ายบน
        "polygon": [[18.61800, 98.89100], [18.61800, 98.89150], [18.61700, 98.89150], [18.61700, 98.89100]],
        "center": [18.61750, 98.89125],
        "status": "SAFE (ดินแห้ง)", "flux": 12.4, "color": "#64FFDA"
    },
    "PLOT_B": {
        "name": "แปลงควบคุม B (Flooded Zone)",
        # บล็อกขวาบน (ติดกับแปลง A)
        "polygon": [[18.61800, 98.89155], [18.61800, 98.89205], [18.61700, 98.89205], [18.61700, 98.89155]],
        "center": [18.61750, 98.89180],
        "status": "CRITICAL (ท่วมขัง)", "flux": 85.2, "color": "#FF3D00"
    },
    "PLOT_C": {
        "name": "แปลงสาธิต C (Transition Zone)",
        # บล็อกล่าง (ยาวครอบ A และ B)
        "polygon": [[18.61695, 98.89100], [18.61695, 98.89205], [18.61645, 98.89205], [18.61645, 98.89100]],
        "center": [18.61670, 98.89152],
        "status": "WARNING (เฝ้าระวัง)", "flux": 41.8, "color": "#F47B20"
    }
}

@st.cache_data(ttl=5)
def generate_bounded_heatmap(selected_plot):
    np.random.seed(int(time.time()) % 100)
    # ทำให้ควันอยู่ *แค่ในกรอบแปลงที่เลือกเท่านั้น* ไม่ล้นออกไป
    poly = PLOT_DATABASE[selected_plot]["polygon"]
    lat_min, lat_max = min(p[0] for p in poly), max(p[0] for p in poly)
    lon_min, lon_max = min(p[1] for p in poly), max(p[1] for p in poly)
    
    # สร้างจุดควัน 500 จุด กระจายแบบ Uniform ให้อยู่เต็มพื้นที่สี่เหลี่ยมพอดี
    lats = np.random.uniform(lat_min, lat_max, 500)
    lons = np.random.uniform(lon_min, lon_max, 500)
    
    if selected_plot == "PLOT_B":
        weights = np.random.uniform(0.75, 1.0, 500)
    elif selected_plot == "PLOT_C":
        weights = np.random.uniform(0.40, 0.70, 500)
    else:
        weights = np.random.uniform(0.10, 0.35, 500)
        
    points = [[lat, lon, w] for lat, lon, w in zip(lats, lons, weights)]
    points.extend([[0, 0, 1.0], [0, 0, 0.0]]) # Anchor สี
    return points

# --- 4. SIDEBAR & SETTINGS ---
with st.sidebar:
    st.markdown('<h1 class="brand-logo" style="font-size:28px;">METHATWIN</h1><div class="brand-sub">Chiang Mai Rice Center</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<div class="panel-title" style="color:#F47B20; margin-bottom:10px;"><i class="fa-solid fa-map-location-dot"></i> FIELD SELECTION</div>', unsafe_allow_html=True)
    plot_key = st.radio(
        "", 
        ["PLOT_A", "PLOT_B", "PLOT_C"], 
        format_func=lambda x: PLOT_DATABASE[x]["name"], 
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    with st.expander("⚙️ SYSTEM CONFIGURATION", expanded=True):
        st.write("การทำงานของแผนที่")
        st.checkbox("ล็อกพิกัดศูนย์กลางอัตโนมัติ", value=True)
        st.checkbox("เปิดโหมด 3D Terrain", value=False)
        st.divider()
        st.write("ระบบแจ้งเตือน")
        st.toggle("เปิดเสียงเตือน Methane", value=True)
        if st.button("ปรับเทียบดาวเทียม (Sync)"):
            st.success("ซิงค์ข้อมูลสำเร็จ!")

active_plot = PLOT_DATABASE[plot_key]
heat_points = generate_bounded_heatmap(plot_key)

# --- 5. MAIN DASHBOARD ---
st.markdown('<h1 class="brand-logo">METHATWIN AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">HIGH-RESOLUTION DIGITAL TWIN & GHG MONITORING</div>', unsafe_allow_html=True)

# Metrics (ลองเอาเมาส์ไปชี้ดูครับ ไอคอนและขอบจะเปลี่ยนเป็นสีเขียว!)
c1, c2, c3 = st.columns(3)

with c1:
    flux_color = "text-ice" if active_plot["status"].startswith("SAFE") else ("text-danger" if "CRITICAL" in active_plot["status"] else "text-warning")
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-cloud-bolt panel-icon"></i> Methane Flux Emission</div><div class="panel-val {flux_color}">{active_plot["flux"]} <span style="font-size:16px; color:#8892B0;">mg/m²/h</span></div><div class="panel-sub">สถานะ: {active_plot["status"]}</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-satellite panel-icon"></i> Satellite Telemetry</div><div class="panel-val text-ice" style="font-size:32px; margin-top:14px;">SENTINEL-2 (Active)</div><div class="panel-sub">ความละเอียดภาพ: 10m/pixel (Max Zoom)</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-microchip panel-icon"></i> IoT Ground Sensor</div><div class="panel-val" style="font-size:32px; margin-top:14px;">ONLINE</div><div class="panel-sub">แบตเตอรี่: 98% | อุณหภูมิดิน: 28.5°C</div></div>', unsafe_allow_html=True)

# --- 6. MAP RENDERING (ปลดล็อก MAX ZOOM = 22) ---
tab1, tab2 = st.tabs(["🔥 1. Heatmap Dispersion (ความหนาแน่นก๊าซ)", "📐 2. Cadastral Boundary (ขอบเขตแปลงเกษตรแม่นยำ)"])

# จุดศูนย์กลางแผนที่ ซูมเข้าไปใกล้ๆ ทันที
map_center = [18.6172, 98.8915]

with tab1:
    # ปลดล็อก max_zoom=22 ให้ซูมลึกสุดใจ
    m1 = folium.Map(location=map_center, zoom_start=19, max_zoom=22, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google Maps Satellite")
    HeatMap(heat_points, radius=20, blur=15, gradient={0.2:'#64FFDA', 0.5:'#FFEA00', 0.8:'#F47B20', 1.0:'#FF3D00'}, max_zoom=22).add_to(m1)
    st_folium(m1, width=1200, height=550, key="heat_map_view", returned_objects=[])

with tab2:
    # ปลดล็อก max_zoom=22 เหมือนกัน
    m2 = folium.Map(location=map_center, zoom_start=19, max_zoom=22, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google Maps Satellite")
    
    for key, plot in PLOT_DATABASE.items():
        # วาดกรอบสี่เหลี่ยมทับแปลงนา
        folium.Polygon(
            locations=plot["polygon"],
            color=plot["color"],
            weight=3,
            fill_color=plot["color"],
            fill_opacity=0.3,
            tooltip=f"{plot['name']}"
        ).add_to(m2)
        
        # ปักหมุดตรงกลาง
        folium.Marker(
            location=plot["center"],
            popup=folium.Popup(f"<div style='font-family:Kanit; width:150px;'><b>{plot['name']}</b><br>มีเทน: {plot['flux']} mg/m²/h</div>", max_width=200),
            icon=folium.Icon(color="black", icon_color=plot["color"], icon="info-sign")
        ).add_to(m2)
        
    st_folium(m2, width=1200, height=550, key="polygon_map_view", returned_objects=[])
