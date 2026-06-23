import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time
import datetime

# --- 1. PAGE INITIALIZATION ---
st.set_page_config(page_title="METHATWIN AI | COMMAND CENTER", layout="wide")

# --- 2. PREMIUM NAVY-ORANGE TECH UI (CSS INJECTION) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&family=Michroma&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { font-family: 'Kanit', sans-serif; }
        
        /* Deep Navy Background Architecture */
        .stApp { background-color: #0A192F; color: #E6F1FF; }
        
        /* Glow Logo METHATWIN */
        .brand-logo {
            font-family: 'Michroma', sans-serif;
            font-size: 46px;
            color: #F47B20;
            text-shadow: 0px 0px 20px rgba(244, 123, 32, 0.6);
            margin-bottom: 0px;
            letter-spacing: 3px;
            font-weight: bold;
        }
        .brand-sub { font-size: 12px; color: #8892B0; letter-spacing: 5px; margin-top: -5px; margin-bottom: 30px; text-transform: uppercase; }
        
        /* Control Panels & Metric Cards */
        .glass-panel {
            background-color: #112240;
            border: 1px solid #233554;
            border-left: 5px solid #F47B20;
            border-radius: 8px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.5);
            transition: 0.3s ease;
        }
        .glass-panel:hover { border-left: 5px solid #64FFDA; transform: translateY(-2px); }
        
        .panel-icon { color: #64FFDA; font-size: 20px; margin-right: 10px; }
        .panel-title { color: #8892B0; font-size: 13px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 500; }
        .panel-val { font-size: 36px; font-weight: 700; color: #FFFFFF; margin: 10px 0 5px 0; line-height: 1.1; }
        .panel-sub { font-size: 13px; color: #CCD6F6; margin-top: 5px; }
        
        /* Dynamic Status Colors */
        .text-accent { color: #F47B20 !important; }
        .text-ice { color: #64FFDA !important; }
        .text-danger { color: #FF3D00 !important; }
        .text-warning { color: #FFEA00 !important; }
        
        /* Streamlit Element Overrides */
        .stTabs [data-baseweb="tab"] { color: #8892B0 !important; font-size: 16px; font-weight: 500; }
        .stTabs [aria-selected="true"] { color: #F47B20 !important; border-bottom-color: #F47B20 !important; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. CORE DATABASE: ข้อมูลแปลงนาจริงพิกัดศูนย์วิจัยข้าวเชียงใหม่ (สันป่าตอง) ---
# กำหนดพิกัดกรอบสี่เหลี่ยมรอบแปลงนาจริงเพื่อไม่ให้หลุดไปโดนหมู่บ้าน
PLOT_DATABASE = {
    "PLOT_A": {
        "name": "แปลงทดลอง A1 (ระบบน้ำอัจฉริยะ AWD)",
        "polygon": [[18.6178, 98.8912], [18.6178, 98.8924], [18.6171, 98.8924], [18.6171, 98.8912]],
        "center": [18.61745, 98.8918],
        "agency": "กองวิจัยพัฒนาข้าว กรมการข้าว ร่วมกับ สถาบันวิจัยข้าวระหว่างประเทศ (IRRI)",
        "manager": "ดร.อานนท์ รัตนวิจิตร (ผู้เชี่ยวชาญนิเวศวิทยาข้าว)",
        "flux": 12.4,
        "accumulated": "124.5 kg CH4 / Hectare / Season (ต่ำกว่าค่าเกณฑ์ 72%)",
        "status": "SAFE",
        "color": "#64FFDA",
        "schedule": {
            "current_state": "ช่วงระบายน้ำออก (แกล้งข้าวเพื่อให้รากเดินลึก)",
            "next_action": "ไขน้ำเข้าแปลง (เติมน้ำบำรุงต้น)",
            "countdown": "อีก 3 วัน (กำหนดการ: 26 มิถุนายน 2569)",
            "past_action": "ระบายน้ำออกสำเร็จเมื่อ 7 วันก่อน (16 มิถุนายน 2569)"
        }
    },
    "PLOT_B": {
        "name": "แปลงควบคุม B1 (ระบบดั้งเดิม - น้ำท่วมขังขีดสุด)",
        "polygon": [[18.6178, 98.8928], [18.6178, 98.8940], [18.6171, 98.8940], [18.6171, 98.8928]],
        "center": [18.61745, 98.8934],
        "agency": "สถานีวิจัยข้าวเชียงใหม่ (แปลงศึกษาเปรียบเทียบผลกระทบสิ่งแวดล้อม)",
        "manager": "คุณจิรภัทร นามวงศ์ (นักวิชาการเกษตรชำนาญการ)",
        "flux": 85.2,
        "accumulated": "612.8 kg CH4 / Hectare / Season (วิกฤต! สูงกว่าแปลงทดลอง 4.9 เท่า)",
        "status": "CRITICAL",
        "color": "#FF3D00",
        "schedule": {
            "current_state": "น้ำท่วมขังต่อเนื่อง (ระดับผิวน้ำ +8 cm จนดินขาดออกซิเจน)",
            "next_action": "ไม่มีนโยบายระบายน้ำ (รักษาเสถียรภาพแปลง Baseline)",
            "countdown": "ระงับการสั่งการ (แปลงปล่อยก๊าซเรือนกระจกสูง)",
            "past_action": "ขังน้ำนิ่งถาวรตั้งแต่วันปักดำ"
        }
    },
    "PLOT_C": {
        "name": "แปลงเครือข่าย C1 (แปลงใหญ่เกษตรกร ต.มะขามหลวง)",
        "polygon": [[18.6167, 98.8912], [18.6167, 98.8924], [18.6160, 98.8924], [18.6160, 98.8912]],
        "center": [18.61635, 98.8918],
        "agency": "สำนักงานเกษตรอำเภอสันป่าตอง ร่วมกับ สหกรณ์แปลงใหญ่",
        "manager": "ผู้ใหญ่สมศักดิ์ แก้วมณี (ประธานกลุ่มผู้ปลูกข้าวสันป่าตอง)",
        "flux": 41.8,
        "accumulated": "285.3 kg CH4 / Hectare / Season (อยู่ในเกณฑ์เฝ้าระวัง)",
        "status": "WARNING",
        "color": "#F47B20",
        "schedule": {
            "current_state": "ดินเริ่มแห้งเกินเกณฑ์ความชื้นวิกฤต (ต่อน้ำซึมลดลงเร็วเกินไป)",
            "next_action": "เปิดประตูระบายเพื่อปล่อยน้ำเข้าควบคุมระดับน้ำ",
            "countdown": "อีก 1 วัน (กำหนดการ: 24 มิถุนายน 2569)",
            "past_action": "ปล่อยน้ำแห้งตามธรรมชาติเข้าสู่วันที่ 12"
        }
    }
}

# --- 4. MAP DATA GENERATOR (จำลองควันมีเทนให้อยู่เฉพาะในกรอบนาจริง) ---
@st.cache_data(ttl=5)
def generate_precise_heatmap(selected_plot):
    np.random.seed(int(time.time()) % 100)
    points = []
    
    # ดึงขอบเขตของแปลงนาที่เลือกมาจำลองควันให้ฟุ้งกระจายภายในกรอบเท่านั้น
    poly = PLOT_DATABASE[selected_plot]["polygon"]
    lat_min, lat_max = min(p[0] for p in poly), max(p[0] for p in poly)
    lon_min, lon_max = min(p[1] for p in poly), max(p[1] for p in poly)
    
    # สร้างจุดควันหนาแน่น 600 จุดภายในแปลงนาจริง
    lats = np.random.uniform(lat_min, lat_max, 600)
    lons = np.random.uniform(lon_min, lon_max, 600)
    
    if selected_plot == "PLOT_B":
        weights = np.random.uniform(0.75, 1.0, 600) # แดงจัด ควันหนาแน่น
    elif selected_plot == "PLOT_C":
        weights = np.random.uniform(0.45, 0.70, 600) # ส้ม/เหลือง
    else:
        weights = np.random.uniform(0.10, 0.35, 600) # เขียว/ฟ้า ปลอดภัย
        
    for lat, lon, w in zip(lats, lons, weights):
        points.append([lat, lon, w])
        
    # บังคับขอบเขตสีเรดาร์
    points.extend([[0, 0, 1.0], [0, 0, 0.0]])
    return points

# --- 5. SIDEBAR MANAGEMENT CONTROL ---
with st.sidebar:
    st.markdown('<h1 class="brand-logo" style="font-size:26px;">METHATWIN</h1><div class="brand-sub">San Pa Tong Rice Research</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown('<div class="panel-title" style="margin-bottom:10px; color:#F47B20;"><i class="fa-solid fa-crosshairs"></i> SELECT TARGET PLOT</div>', unsafe_allow_html=True)
    plot_key = st.radio(
        "เลือกแปลงนาที่ต้องการตรวจสอบ:",
        ["PLOT_A", "PLOT_B", "PLOT_C"],
        format_func=lambda x: PLOT_DATABASE[x]["name"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<div class="panel-title" style="margin-bottom:10px; color:#64FFDA;"><i class="fa-solid fa-server"></i> TELEMETRY NETWORK</div>', unsafe_allow_html=True)
    st.caption("📡 IoT Node 01 - AWD Field: Connected\n📡 IoT Node 02 - Baseline Field: Connected\n🛰️ Sentinel-2 Image Layer: Synced (June 2026)")

# โหลดข้อมูลตามปุ่มเลือกด้านข้าง
active_plot = PLOT_DATABASE[plot_key]
heat_points = generate_precise_heatmap(plot_key)

# --- 6. DASHBOARD MAIN INTERFACE ---
st.markdown('<h1 class="brand-logo">METHATWIN AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">High-Resolution Digital Twin Platform for Carbon Credit Verification</div>', unsafe_allow_html=True)

# 4 แผงข้อมูลหลักเชิงลึกของแปลงนาที่เลือก
c1, c2, c3, c4 = st.columns(4)

with c1:
    flux_color = "text-ice" if active_plot["status"] == "SAFE" else ("text-danger" if active_plot["status"] == "CRITICAL" else "text-warning")
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-gauge-high panel-icon"></i> Methane Flux</div><div class="panel-val {flux_color}">{active_plot["flux"]}</div><div class="panel-sub">mg/m²/h ({active_plot["status"]})</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-calendar-check panel-icon"></i> Next Action Schedule</div><div class="panel-val text-accent" style="font-size:20px; margin-top:22px; font-weight:500;">{active_plot["schedule"]["next_action"]}</div><div class="panel-sub">{active_plot["schedule"]["countdown"]}</div></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-chart-line panel-icon"></i> Methane Accumulated</div><div class="panel-val" style="font-size:18px; margin-top:25px; color:#FFFFFF;">{active_plot["accumulated"]}</div><div class="panel-sub">ปริมาณสะสมประจำฤดูกาล</div></div>', unsafe_allow_html=True)

with c4:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-building-shield panel-icon"></i> Governing Agency</div><div class="panel-val" style="font-size:15px; margin-top:15px; font-weight:400; color:#CCD6F6;">{active_plot["agency"]}</div><div class="panel-sub">ผู้ดูแล: {active_plot["manager"]}</div></div>', unsafe_allow_html=True)

# --- 7. DUAL FUNCTION LAYERS (ระบบสลับหน้าฟังก์ชันแผนที่) ---
st.markdown('<div style="margin-top:10px; margin-bottom:5px; color:#8892B0; font-size:13px; letter-spacing:1px; text-transform:uppercase;"><i class="fa-solid fa-map"></i> SELECT GEOSPATIAL LAYER FUNCTION</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["เลเยอร์วิเคราะห์กลุ่มควันความหนาแน่นก๊าซมีเทน", "เลเยอร์พิกัดขอบเขตแปลงนาและตารางจัดการน้ำ"])

# ตัวตั้งค่าแผนที่ฐานจากดาวเทียม Google Maps (มองเห็นความลึก ร่องคันนา ชัดเจน)
map_center = [18.6170, 98.8925]

with tab1:
    st.write("ฟังก์ชันวิเคราะห์ภาพการกระจายตัวและการสะสมของก๊าซเรือนกระจกรายพิกัดแปลงในรูปแบบกลุ่มควันความร้อน (Dispersion Heatmap)")
    
    m1 = folium.Map(location=map_center, zoom_start=17, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google Maps Satellite")
    
    # เรดาร์ไล่ระดับสีตามลักษณะควันธรรมชาติ (ฟ้าเขียว -> เหลือง -> ส้ม -> แดงวิกฤต)
    gradient_config = { 0.2: '#64FFDA', 0.4: '#FFEA00', 0.7: '#F47B20', 1.0: '#FF3D00' }
    
    HeatMap(heat_points, radius=28, blur=18, gradient=gradient_config, max_zoom=18).add_to(m1)
    st_folium(m1, width=1200, height=500, key="map_layer_heatmap", returned_objects=[])

with tab2:
    st.write("ฟังก์ชันการจัดการที่ดิน แสดงพิกัดอาณาเขต (Cadastral Boundary) และแผนปฏิบัติการไขน้ำวิศวกรรมเกษตรรายแปลง")
    
    m2 = folium.Map(location=map_center, zoom_start=17, tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", attr="Google Maps Satellite")
    
    # วาดรูปปิดกรอบแปลงนา (Polygon) ทุกแปลงลงบนแผนที่จริงเพื่อแสดงอาณาเขตชัดเจน
    for key, plot in PLOT_DATABASE.items():
        folium.Polygon(
            locations=plot["polygon"],
            color=plot["color"],
            weight=3,
            fill_color=plot["color"],
            fill_opacity=0.25,
            tooltip=f"คลิกดูรายละเอียดเชิงลึก {plot['name']}"
        ).add_to(m2)
        
        # ปักหมุดระบุศูนย์กลางของแต่ละแปลงเพื่อให้กดดู Pop-up รายละเอียดได้
        popup_content = f"""
        <div style="font-family: 'Kanit', sans-serif; color: #0A192F; width:280px;">
            <h4 style="margin:0 0 5px 0; color:#F47B20;">{plot['name']}</h4>
            <b>ผู้ดูแล:</b> {plot['manager']}<br>
            <b>สถานะน้ำ:</b> {plot['schedule']['current_state']}<br>
            <b>แผนการถัดไป:</b> {plot['schedule']['next_action']} ({plot['schedule']['countdown']})<br>
            <b>ปริมาณก๊าซสะสม:</b> {plot['accumulated']}
        </div>
        """
        folium.Marker(
            location=plot["center"],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color="orange" if key=="PLOT_C" else ("red" if key=="PLOT_B" else "cadetblue"), icon="info-sign")
        ).add_to(m2)
        
    st_folium(m2, width=1200, height=500, key="map_layer_cadastral", returned_objects=[])

# --- 8. DETAILED WATER ACTION TIMELINE (ตารางปฏิทินปฏิบัติการเชิงลึก) ---
st.markdown("### <i class='fa-solid fa-clock-history text-accent'></i> แผนกำหนดการวิศวกรรมการจัดการน้ำรายสัปดาห์ (Water Control Logs)", unsafe_allow_html=True)
st.write(f"ตารางควบคุมและพยากรณ์การจัดการน้ำสำหรับแปลงเป้าหมายปัจจุบัน: **{active_plot['name']}**")

df_timeline = pd.DataFrame({
    "สถานะและภารกิจ": ["อดีต (ดำเนินการแล้ว)", "ปัจจุบัน (Real-time)", "เป้าหมายถัดไป (AI Plan)", "ระยะยาว (พยากรณ์ล่วงหน้า)"],
    "กิจกรรมการจัดการน้ำ": [active_plot["schedule"]["past_action"], active_plot["schedule"]["current_state"], active_plot["schedule"]["next_action"], "เข้าสู่เฟสทำดินแห้งรอบที่สองเพื่อกระตุ้นจุลินทรีย์ชนิดดี"],
    "ระยะเวลาคำนวณถอยหลัง": ["เรียบร้อยแล้ว", "กำลังทำงาน", active_plot["schedule"]["countdown"], "อีก 14 วันข้างหน้า"],
    "หน่วยตรวจสอบพารามิเตอร์": ["เซนเซอร์วัดความชื้นผิวดิน", "เซนเซอร์ระดับน้ำ Ultrasonic ในท่อ PVC", "แบบจำลอง AI Predictor", "ข้อมูลพยากรณ์อากาศกรมอุตุนิยมวิทยาประกอบดาวเทียม NDVI"]
})
st.table(df_timeline)
