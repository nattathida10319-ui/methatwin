import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

# --- 1. PAGE INITIALIZATION ---
st.set_page_config(page_title="METHATWIN AI | PRECISION", layout="wide")

# --- 2. PREMIUM CSS (แก้ตัวอักษรอ่านยาก + ลูกเล่น Hover ไอคอนส้ม->เขียว) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&family=Michroma&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { font-family: 'Kanit', sans-serif; }
        
        .stApp { background-color: #0A192F; color: #FFFFFF; } /* ปรับสีตัวอักษรหลักเป็นขาวสว่าง */
        
        .brand-logo {
            font-family: 'Michroma', sans-serif;
            font-size: 42px;
            color: #F47B20;
            text-shadow: 0px 0px 20px rgba(244, 123, 32, 0.8);
            margin-bottom: 0px;
        }
        .brand-sub { font-size: 13px; color: #E6F1FF; letter-spacing: 3px; margin-bottom: 25px; text-transform: uppercase; }
        
        /* การ์ดข้อมูล */
        .glass-panel {
            background-color: #112240;
            border: 1px solid #495670; /* ปรับขอบให้สว่างขึ้นนิดนึง */
            border-left: 5px solid #F47B20;
            border-radius: 10px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.6);
            transition: all 0.3s ease;
        }
        
        /* โฮเวอร์ที่การ์ดแล้วไอคอนขยับและเปลี่ยนสี */
        .glass-panel:hover { 
            border-left: 5px solid #00E676; 
            transform: translateY(-5px); 
            box-shadow: 0 12px 30px rgba(0, 230, 118, 0.2);
        }
        .glass-panel:hover .panel-icon {
            color: #00E676 !important; /* เปลี่ยนเป็นสีเขียว */
            transform: scale(1.3) rotate(-10deg); /* ขยับและหมุนนิดๆ */
        }
        
        /* ตั้งค่า Default ของไอคอนให้เป็นสีส้ม */
        .panel-icon { 
            color: #F47B20; 
            font-size: 22px; 
            margin-right: 12px; 
            display: inline-block;
            transition: all 0.3s ease; /* ทำให้การเปลี่ยนสีนุ่มนวล */
        }
        
        /* ปรับสีตัวอักษรให้อ่านง่ายขึ้นชัดเจน */
        .panel-title { color: #E6F1FF; font-size: 14px; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; }
        .panel-val { font-size: 38px; font-weight: 700; color: #FFFFFF; margin: 12px 0 5px 0; }
        .panel-sub { font-size: 14px; color: #A8B2D1; font-weight: 400; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE: วาด Polygon แบบเป๊ะๆ (สามเหลี่ยมและสี่เหลี่ยมคางหมูตามพื้นที่จริง) ---
PLOT_DATABASE = {
    "PLOT_A": {
        "name": "แปลงทดลอง A1 (รูปสามเหลี่ยมเฉียง)",
        # วาดพิกัดให้เป็นรูปสามเหลี่ยมเป๊ะๆ ตามแนวถนน/คันนา
        "polygon": [[18.6185, 98.8910], [18.6170, 98.8905], [18.6175, 98.8925]],
        "center": [18.6176, 98.8913],
        "status": "SAFE (กำลังระบายน้ำ)", "flux": 12.4, "color": "#00E676"
    },
    "PLOT_B": {
        "name": "แปลงควบคุม B1 (รูปหลายเหลี่ยมตามภูมิประเทศ)",
        # วาดพิกัดให้เป็นสี่เหลี่ยมเบี้ยวๆ (Irregular Polygon)
        "polygon": [[18.6190, 98.8930], [18.6195, 98.8945], [18.6180, 98.8950], [18.6175, 98.8935]],
        "center": [18.6185, 98.8940],
        "status": "CRITICAL (ท่วมขัง)", "flux": 85.2, "color": "#FF3D00"
    },
    "PLOT_C": {
        "name": "แปลงเครือข่าย C1 (สี่เหลี่ยมคางหมู)",
        # วาดพิกัดให้เป็นรูปสี่เหลี่ยมคางหมู
        "polygon": [[18.6165, 98.8920], [18.6168, 98.8940], [18.6155, 98.8935], [18.6152, 98.8915]],
        "center": [18.6160, 98.8927],
        "status": "WARNING (เฝ้าระวัง)", "flux": 41.8, "color": "#F47B20"
    }
}

@st.cache_data(ttl=5)
def generate_focused_heatmap(selected_plot):
    np.random.seed(int(time.time()) % 100)
    # จุดควันจะเกาะกลุ่มหนาแน่นเฉพาะจุดศูนย์กลางของแปลงนาที่เลือก ไม่ฟุ้งไปบ้านคน
    center_lat, center_lon = PLOT_DATABASE[selected_plot]["center"]
    
    lats = np.random.normal(center_lat, 0.0004, 400) # บีบรัศมีความฟุ้งให้แคบลง
    lons = np.random.normal(center_lon, 0.0004, 400)
    
    if selected_plot == "PLOT_B": weights = np.random.uniform(0.7, 1.0, 400)
    elif selected_plot == "PLOT_C": weights = np.random.uniform(0.4, 0.7, 400)
    else: weights = np.random.uniform(0.1, 0.3, 400)
        
    points = [[lat, lon, w] for lat, lon, w in zip(lats, lons, weights)]
    points.extend([[0, 0, 1.0], [0, 0, 0.0]]) # ล็อกสี
    return points

# --- 4. SIDEBAR & SETTINGS MENU ---
with st.sidebar:
    st.markdown('<h1 class="brand-logo" style="font-size:24px;">METHATWIN</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # เมนูเลือกแปลง
    st.markdown('<div class="panel-title" style="color:#FFFFFF;"><i class="fa-solid fa-map-location-dot" style="color:#F47B20; margin-right:8px;"></i> SELECT PLOT</div>', unsafe_allow_html=True)
    plot_key = st.radio("", ["PLOT_A", "PLOT_B", "PLOT_C"], format_func=lambda x: PLOT_DATABASE[x]["name"], label_visibility="collapsed")
    
    st.markdown("---")
    
    # ⚙️ เพิ่มฟีเจอร์ "การตั้งค่าระบบ" (System Settings) แบบกดขยายได้
    with st.expander("⚙️ การตั้งค่าระบบ (SYSTEM SETTINGS)"):
        st.write("**การแจ้งเตือน (Notifications)**")
        st.toggle("เปิดเสียงเตือนเมื่อก๊าซวิกฤต", value=True)
        st.toggle("ส่ง SMS ให้ผู้ดูแลแปลง", value=False)
        st.divider()
        st.write("**การปรับเทียบ (Calibration)**")
        st.slider("ความไวของเซนเซอร์ระดับน้ำ (Sensivity)", 1, 10, 5)
        st.selectbox("ความถี่ในการดึงภาพดาวเทียม", ["ทุก 3 วัน", "ทุก 5 วัน (ค่าเริ่มต้น)", "ทุก 10 วัน"])
        if st.button("บันทึกการตั้งค่า"):
            st.toast("บันทึกการตั้งค่าลงระบบคลาวด์สำเร็จ! ☁️")

active_plot = PLOT_DATABASE[plot_key]
heat_points = generate_focused_heatmap(plot_key)

# --- 5. MAIN DASHBOARD ---
st.markdown('<h1 class="brand-logo">METHATWIN AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">PRECISION AGRICULTURE & HIGH-RESOLUTION DIGITAL TWIN</div>', unsafe_allow_html=True)

# แผงข้อมูล (เอาเมาส์ไปชี้ไอคอนจะเด้งและเป็นสีเขียว!)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-cloud-bolt panel-icon"></i> Methane Flux</div><div class="panel-val">{active_plot["flux"]} <span style="font-size:18px; color:{active_plot["color"]};">mg/m²/h</span></div><div class="panel-sub">สถานะ: <strong style="color:{active_plot["color"]};">{active_plot["status"]}</strong></div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-satellite-dish panel-icon"></i> Data Sync Status</div><div class="panel-val" style="font-size:32px;">REAL-TIME</div><div class="panel-sub">อัปเดตล่าสุด: เมื่อ 2 นาทีที่แล้ว</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-mobile-screen-button panel-icon"></i> IoT Sensor ID</div><div class="panel-val" style="font-size:32px; color:#F8F9FA;">N-{plot_key[-1]}</div><div class="panel-sub">แบตเตอรี่โซลาร์เซลล์: 98% ⚡</div></div>', unsafe_allow_html=True)

# --- 6. MAP RENDERING (โชว์ทั้งควันและกรอบที่เป๊ะขึ้น) ---
tab1, tab2 = st.tabs(["🔥 แผนที่ความร้อนก๊าซมีเทน (Heatmap)", "📐 แผนที่ขอบเขตแปลงเกษตรแม่นยำ (Cadastral Polygons)"])

map_center = [18.6175, 98.8925]

with tab1:
    m1 = folium.Map(location=map_center, zoom_start=17, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google Maps Satellite")
    HeatMap(heat_points, radius=25, blur=15, gradient={0.2:'#00E676', 0.5:'#FFEA00', 0.8:'#F47B20', 1.0:'#FF3D00'}, max_zoom=18).add_to(m1)
    st_folium(m1, width=1200, height=500, key="heat_map_view", returned_objects=[])

with tab2:
    m2 = folium.Map(location=map_center, zoom_start=17, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google Maps Satellite")
    
    for key, plot in PLOT_DATABASE.items():
        # วาดรูปทรงตามพิกัดเป๊ะๆ
        folium.Polygon(
            locations=plot["polygon"],
            color=plot["color"],
            weight=4,
            fill_color=plot["color"],
            fill_opacity=0.35,
            tooltip=f"{plot['name']}"
        ).add_to(m2)
        
        # ปักหมุดกลางแปลง
        folium.Marker(
            location=plot["center"],
            popup=folium.Popup(f"<b style='font-family: Kanit;'>{plot['name']}</b>", max_width=200),
            icon=folium.Icon(color="black", icon_color=plot["color"], icon="info-sign")
        ).add_to(m2)
        
    st_folium(m2, width=1200, height=500, key="polygon_map_view", returned_objects=[])
