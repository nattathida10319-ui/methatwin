import streamlit as st
import pandas as pd
import numpy as np
import datetime
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import time

# --- 1. SET UP THE UI THEME (โทนส้ม-ดำ สไตล์พรรคประชาชน) ---
st.set_page_config(page_title="MethaTwin | AI New Gen", layout="wide", page_icon="🌾")

st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    
    /* การ์ดข้อมูล โทนดำตัดขอบส้ม */
    .metric-card {
        background-color: #1E1E1E;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 10px rgba(244, 123, 32, 0.1);
        border-top: 4px solid #F47B20; /* สีส้มพรรคประชาชน */
        margin-bottom: 20px;
    }
    
    .card-title { color: #A0AEC0; font-size: 14px; font-weight: 600; }
    .card-value { color: #F47B20; font-size: 38px; font-weight: 700; margin: 10px 0; }
    .card-status { font-size: 15px; font-weight: 500; color: #E2E8F0; }
    
    /* หัวข้อหลัก */
    h1, h2, h3 { color: #F47B20 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA ENGINE (จำลองจุดข้อมูลให้เป็นกลุ่มควัน) ---
CENTER_LAT, CENTER_LON = 18.6235, 98.8964

@st.cache_data(ttl=10)
def generate_heatmap_data(mode):
    np.random.seed(int(time.time()) % 100)
    # สร้างจุดข้อมูล 500 จุด ให้ดูเนียนเป็นกลุ่มควัน
    lats = np.random.normal(CENTER_LAT, 0.0015, 500)
    lons = np.random.normal(CENTER_LON, 0.0015, 500)
    
    if mode == "น้ำท่วมขัง (วิกฤต)":
        weights = np.random.uniform(0.6, 1.0, 500) # น้ำขัง มีเทนเข้มข้น (สีแดง/ส้ม)
    else:
        weights = np.random.uniform(0.1, 0.4, 500) # AWD มีเทนเจือจาง (สีเขียว/เหลือง)
        
    return [[lat, lon, weight] for lat, lon, weight in zip(lats, lons, weights)]

# --- 3. SIDEBAR (เมนูควบคุม) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=70)
    st.markdown("## 🌾 METHATWIN AI")
    st.markdown("### AI NEW GEN")
    st.markdown("---")
    
    menu = st.radio("เมนูหลัก", ["🎯 แดชบอร์ดติดตามแปลงนา", "🚜 คู่มือปฏิบัติการแกล้งข้าว (AWD)"])
    st.markdown("---")
    
    st.markdown("**🎛️ จำลองสถานการณ์น้ำในนา**")
    water_mode = st.selectbox("เลือกโหมด:", ["จัดการน้ำแบบ AWD (แกล้งข้าว)", "น้ำท่วมขัง (วิกฤต)"])

heat_data = generate_heatmap_data(water_mode)

# --- 4. RENDER MODULES ---

if menu == "🎯 แดชบอร์ดติดตามแปลงนา":
    st.markdown("# 🛰️ ระบบติดตามความหนาแน่นก๊าซมีเทน (Digital Twin)")
    st.caption("📍 พื้นที่: แปลงวิจัยที่ 3 ศูนย์วิจัยข้าวเชียงใหม่ อ.สันป่าตอง | 📡 แผนที่: Google Maps Satellite (Real-time Heatmap)")
    
    # --- ส่วนที่เน้นการทำนา (Farming Status) ---
    st.markdown("### 🚜 สถานะการเพาะปลูกปัจจุบัน (Farming Status)")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.info("**🌱 ระยะการเติบโต:** ระยะแตกกอสูงสุด (Maximum Tillering)")
    with col_f2:
        st.warning("**📅 อายุข้าว:** 45 วัน หลังปักดำ")
    with col_f3:
        if "AWD" in water_mode:
            st.success("**💧 สถานะน้ำ:** อยู่ในช่วงระบายน้ำออก (แกล้งข้าว)")
        else:
            st.error("**💧 สถานะน้ำ:** น้ำท่วมขัง (ต้องรีบระบายออก!)")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- การ์ดตัวเลข ---
    c1, c2, c3, c4 = st.columns(4)
    if "AWD" in water_mode:
        c1.markdown('<div class="metric-card"><div class="card-title">มีเทนเฉลี่ยสะสม</div><div class="card-value" style="color:#00E676;">14.2</div><div class="card-status">mg/m²/h (เกณฑ์ปลอดภัย)</div></div>', unsafe_allow_html=True)
        c2.markdown('<div class="metric-card"><div class="card-title">ระดับน้ำใต้ดิน</div><div class="card-value" style="color:#00B0FF;">-10 cm</div><div class="card-status">กำลังระบายน้ำ (AWD)</div></div>', unsafe_allow_html=True)
        c3.markdown('<div class="metric-card"><div class="card-title">คาร์บอนเครดิต</div><div class="card-value">0.42</div><div class="card-status">tCO₂e / ไร่</div></div>', unsafe_allow_html=True)
        c4.markdown('<div class="metric-card"><div class="card-title">AI แนะนำชาวนา</div><div class="card-value" style="font-size:24px; color:#A0AEC0;">ปล่อยแห้งต่อ</div><div class="card-status">อีก 3 วัน ค่อยเติมน้ำ</div></div>', unsafe_allow_html=True)
    else:
        c1.markdown('<div class="metric-card"><div class="card-title">มีเทนเฉลี่ยสะสม</div><div class="card-value" style="color:#FF3D00;">78.5</div><div class="card-status">mg/m²/h (อันตราย!)</div></div>', unsafe_allow_html=True)
        c2.markdown('<div class="metric-card"><div class="card-title">ระดับน้ำใต้ดิน</div><div class="card-value" style="color:#00B0FF;">+8 cm</div><div class="card-status">ท่วมขังต่อเนื่อง 10 วัน</div></div>', unsafe_allow_html=True)
        c3.markdown('<div class="metric-card"><div class="card-title">คาร์บอนเครดิต</div><div class="card-value" style="color:#FF3D00;">0.00</div><div class="card-status">ไม่ผ่านเกณฑ์ MRV</div></div>', unsafe_allow_html=True)
        c4.markdown('<div class="metric-card"><div class="card-title">AI แนะนำชาวนา</div><div class="card-value" style="font-size:24px; color:#FF3D00;">สูบน้ำออกทันที!</div><div class="card-status">เสี่ยงโรคและมีเทนพุ่ง</div></div>', unsafe_allow_html=True)

    # --- แผนที่ Heatmap ไล่สีควันเนียนๆ บน Google Maps ---
    st.markdown("### 🗺️ แผนที่เรดาร์ก๊าซมีเทน (Methane Radar Overlay)")
    
    # ดึงแผนที่ Google Maps แบบดาวเทียม (Hybrid: เห็นหลังคา เห็นแปลงนา)
    m = folium.Map(
        location=[CENTER_LAT, CENTER_LON], 
        zoom_start=17, 
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", 
        attr="Google Maps Satellite",
        control_scale=True
    )
    
    # ตั้งค่าสีของควัน (ถ้าปลอดภัยจะเป็นสีเขียว/เหลือง, ถ้าวิกฤตจะเป็นสีส้ม/แดง)
    if "AWD" in water_mode:
        grad = {0.2: 'lime', 0.5: 'green', 1.0: 'yellow'}
    else:
        grad = {0.4: 'yellow', 0.6: 'orange', 1.0: 'red'}

    # ใส่ Layer ควัน (Heatmap)
    HeatMap(
        heat_data, 
        radius=25,       # ขนาดความฟุ้งของควัน
        blur=20,         # ความเบลอให้ดูเนียน
        gradient=grad,   # สีที่ตั้งไว้
        max_zoom=17
    ).add_to(m)
    
    # แสดงผลใน Streamlit
    st_folium(m, width=1200, height=500, returned_objects=[])
    
elif menu == "🚜 คู่มือปฏิบัติการแกล้งข้าว (AWD)":
    st.markdown("# 🚜 ปฏิทินปฏิบัติการแกล้งข้าว (Actionable Farming)")
    st.write("บอกชาวนาแบบเจาะจงเลยว่า วันนี้ต้องทำอะไร เพื่อลดคาร์บอนและเพิ่มผลผลิต!")
    
    st.markdown('<div class="metric-card" style="border-top: 4px solid #00B0FF;">', unsafe_allow_html=True)
    st.markdown("### 💧 เฟส 1: ข้าวตั้งตัว (อายุ 0-20 วัน)")
    st.write("**การจัดการน้ำ:** รักษาระดับน้ำให้ท่วมผิวดิน 2-5 ซม. เพื่อควบคุมวัชพืช")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card" style="border-top: 4px solid #F47B20;">', unsafe_allow_html=True)
    st.markdown("### 🌤️ เฟส 2: ระยะแตกกอ / แกล้งข้าว (อายุ 20-45 วัน) 👈 **(คุณอยู่ที่นี่)**")
    st.write("**การจัดการน้ำ (AWD):** ปล่อยน้ำให้แห้งไปจนระดับน้ำใต้ดินลดลงไปถึง **-15 ซม.** (วัดจากท่อ PVC) ดินจะเริ่มแตกแตง ออกซิเจนลงสู่ราก จุลินทรีย์สร้างมีเทนจะตายลง")
    st.write("🔥 **คำแนะนำจาก AI วันนี้:** ระดับน้ำปัจจุบันอยู่ที่ -10 ซม. สามารถรอให้แห้งต่อได้อีก 3-5 วัน")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card" style="border-top: 4px solid #00E676;">', unsafe_allow_html=True)
    st.markdown("### 🌾 เฟส 3: ข้าวตั้งท้อง-ออกรวง (อายุ 45-80 วัน)")
    st.write("**การจัดการน้ำ:** เติมน้ำกลับเข้าแปลงให้สูง 5 ซม. ตลอดช่วงนี้ เพื่อให้ข้าวผสมเกสรและสร้างเมล็ดอย่างสมบูรณ์")
    st.markdown('</div>', unsafe_allow_html=True)
