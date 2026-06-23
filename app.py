import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pydeck as pdk
import time

# --- 1. ตั้งค่าหน้าจอแบบ Full Dashboard ---
st.set_page_config(page_title="MethaTwin | AI New Gen", layout="wide", page_icon="🌾")

# --- CSS ตกแต่งให้เป็นเหมือนหน้าปัดยานอวกาศ (Dark UI) ---
st.markdown("""
    <style>
    /* พื้นหลังและฟอนต์ */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* กล่องการ์ดสำหรับใส่ข้อมูล */
    .metric-card {
        background-color: #1E2129;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 5px solid #00FF7F;
    }
    .metric-card-danger { border-left: 5px solid #FF4B4B; }
    
    /* ตัวหนังสือในกล่อง */
    .metric-title { font-size: 14px; color: #A0AEC0; margin-bottom: 5px; }
    .metric-value { font-size: 32px; font-weight: bold; margin: 0; }
    .metric-delta { font-size: 14px; color: #00FF7F; }
    .metric-delta-danger { color: #FF4B4B; }
    </style>
""", unsafe_allow_html=True)

# --- 2. ข้อมูลพิกัดและโมเดลจำลองแปลงนา ---
# พิกัดจำลองแปลงนา A1 (สมมติเป็นรูปทรงเจาะจงคล้ายหัวใจ/หลายเหลี่ยม ที่ อ.สันป่าตอง)
CENTER_LAT = 18.6235
CENTER_LON = 98.8964

# วาดขอบเขตแปลงนา (Polygon)
polygon_data = pd.DataFrame([{
    "contours": [
        [98.8940, 18.6250], # บนซ้าย
        [98.8964, 18.6270], # บนกลาง (รอยหยักหัวใจ)
        [98.8988, 18.6250], # บนขวา
        [98.8980, 18.6210], # ล่างขวา
        [98.8964, 18.6190], # ล่างสุดแหลมๆ
        [98.8948, 18.6210], # ล่างซ้าย
    ],
    "name": "แปลงนาวิจัย A1 (รูปทรงหัวใจ)"
}])

@st.cache_data(ttl=5) # ข้อมูลอัปเดตใหม่ทุก 5 วินาที
def get_sensor_data(scenario):
    np.random.seed(int(time.time()))
    # สุ่มจุดข้อมูล "เฉพาะภายในรัศมีขอบเขตแปลงนา"
    lats = np.random.uniform(18.6195, 18.6265, 300)
    lons = np.random.uniform(98.8945, 98.8985, 300)
    
    if scenario == "AWD (เปียกสลับแห้ง)":
        # โหมด AWD มีเทนต่ำ (เขียวเยอะ)
        methane = np.random.uniform(5, 35, 300)
    else:
        # โหมดน้ำท่วมขัง มีเทนพุ่ง (แดงเยอะ)
        methane = np.random.uniform(30, 85, 300)
        
    return pd.DataFrame({'lat': lats, 'lon': lons, 'methane': methane})

# --- 3. ระบบนำทางด้านข้าง (Sidebar Navigation เสถียร 100%) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1892/1892747.png", width=60)
    st.markdown("### 🌾 MethaTwin AI")
    st.caption("AI New Gen Project")
    st.markdown("---")
    
    page = st.radio("เมนูหลัก (Navigation)", [
        "🎯 แดชบอร์ด (Live Map)", 
        "🤖 การวิเคราะห์จาก AI", 
        "📊 คาร์บอนเครดิต (MRV)"
    ])
    
    st.markdown("---")
    st.markdown("**⚙️ ตั้งค่าสถานการณ์จำลอง**")
    scenario = st.selectbox("โหมดการจัดการน้ำ:", ["AWD (เปียกสลับแห้ง)", "น้ำท่วมขัง (Flooded)"])

# โหลดข้อมูลตามสถานการณ์ที่เลือก
df_points = get_sensor_data(scenario)

# --- 4. การแสดงผลแต่ละหน้า ---

if page == "🎯 แดชบอร์ด (Live Map)":
    # Header
    st.markdown("## 🛰️ ศูนย์บัญชาการแปลงนาอัจฉริยะ (Digital Twin)")
    st.caption(f"📍 พิกัด: แปลงนาวิจัย A1 อ.สันป่าตอง จ.เชียงใหม่ | 🕒 เวลาสถานี: {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    
    # 4 ตัวเลขสถานะแบบการ์ดสวยๆ
    c1, c2, c3, c4 = st.columns(4)
    if scenario == "AWD (เปียกสลับแห้ง)":
        c1.markdown('<div class="metric-card"><div class="metric-title">ค่ามีเทนเฉลี่ย (CH₄ Flux)</div><p class="metric-value">18.4 <span style="font-size:16px;">mg/m²/h</span></p><p class="metric-delta">⬇ 45% (เทียบกับเมื่อวาน)</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="metric-card"><div class="metric-title">ดัชนีความเสี่ยงมีเทน</div><p class="metric-value">22 / 100</p><p class="metric-delta">🟢 ความเสี่ยงต่ำ</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="metric-card"><div class="metric-title">ระดับน้ำในนา (Water Level)</div><p class="metric-value">-5.2 <span style="font-size:16px;">cm</span></p><p class="metric-delta">อยู่ในช่วงแกล้งข้าว</p></div>', unsafe_allow_html=True)
        c4.markdown('<div class="metric-card"><div class="metric-title">ความชื้นดิน (Soil Moisture)</div><p class="metric-value">68 <span style="font-size:16px;">%</span></p><p class="metric-delta">เหมาะสม</p></div>', unsafe_allow_html=True)
    else:
        c1.markdown('<div class="metric-card metric-card-danger"><div class="metric-title">ค่ามีเทนเฉลี่ย (CH₄ Flux)</div><p class="metric-value">65.8 <span style="font-size:16px;">mg/m²/h</span></p><p class="metric-delta-danger">⬆ 18% (สูงเกินเกณฑ์)</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="metric-card metric-card-danger"><div class="metric-title">ดัชนีความเสี่ยงมีเทน</div><p class="metric-value">78 / 100</p><p class="metric-delta-danger">🔴 ความเสี่ยงสูงมาก!</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="metric-card metric-card-danger"><div class="metric-title">ระดับน้ำในนา (Water Level)</div><p class="metric-value">8.5 <span style="font-size:16px;">cm</span></p><p class="metric-delta-danger">น้ำท่วมขังต่อเนื่อง</p></div>', unsafe_allow_html=True)
        c4.markdown('<div class="metric-card metric-card-danger"><div class="metric-title">ความชื้นดิน (Soil Moisture)</div><p class="metric-value">96 <span style="font-size:16px;">%</span></p><p class="metric-delta-danger">ดินขาดออกซิเจน</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- แผนที่ 3D (PyDeck) แบบกำหนดพื้นที่ ---
    st.markdown("### 🗺️ แผนที่ระบุโซนความเสี่ยงระดับแปลง (Methane Heatmap)")
    st.write("*(ซูมเข้า/ออก และใช้เมาส์คลิกขวาหรือคลิกซ้ายค้างเพื่อหมุนดูมุมมอง 3 มิติในขอบเขตแปลงนา)*")

    # 1. เลเยอร์เส้นขอบแปลงนา (Polygon)
    polygon_layer = pdk.Layer(
        "PolygonLayer",
        polygon_data,
        get_polygon="contours",
        filled=True,
        extruded=False,
        wireframe=True,
        get_fill_color=[255, 255, 255, 20],
        get_line_color=[0, 255, 127, 255],
        line_width_min_pixels=3,
    )

    # 2. เลเยอร์แท่งรังผึ้ง 3 มิติ (HexagonLayer) โชว์ความหนาแน่นมีเทน
    hexagon_layer = pdk.Layer(
        "HexagonLayer",
        df_points,
        get_position=["lon", "lat"],
        radius=25, # ขนาดรังผึ้ง
        elevation_scale=3, # ความสูง
        elevation_range=[0, 300],
        color_range=[
            [50, 255, 50, 200],   # เขียว (ต่ำ)
            [255, 255, 50, 200],  # เหลือง (กลาง)
            [255, 150, 50, 200],  # ส้ม (ค่อนข้างสูง)
            [255, 50, 50, 200],   # แดง (สูง/วิกฤต)
        ],
        extrude=True,
        coverage=0.9,
    )

    # มุมกล้องตั้งต้น
    view_state = pdk.ViewState(
        latitude=CENTER_LAT, longitude=CENTER_LON,
        zoom=16, pitch=45, bearing=0
    )

    # แสดงแผนที่ (ปรับพื้นหลังเป็นแบบดาวเทียมมืดให้ดูขลัง)
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v11",
        layers=[polygon_layer, hexagon_layer],
        initial_view_state=view_state,
        tooltip={"text": "ความหนาแน่นจุดปล่อยก๊าซมีเทน"}
    ))

elif page == "🤖 การวิเคราะห์จาก AI":
    st.markdown("## 🧠 ระบบผู้เชี่ยวชาญ AI (AI Recommendation)")
    st.write("ดึงข้อมูลจากโมเดล Machine Learning เพื่อพยากรณ์และแนะนำเกษตรกร")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📈 แนวโน้มการปล่อยมีเทน 7 วันล่วงหน้า")
        dates = pd.date_range(start=datetime.datetime.today(), periods=7).strftime('%d %b')
        if scenario == "AWD (เปียกสลับแห้ง)":
            trend = [22, 20, 18, 15, 12, 10, 8]
        else:
            trend = [65, 68, 70, 75, 78, 80, 82]
        
        df_chart = pd.DataFrame({'วันที่': dates, 'ฟลักซ์มีเทนคาดการณ์': trend}).set_index('วันที่')
        st.line_chart(df_chart, color="#FF4B4B" if scenario == "น้ำท่วมขัง (Flooded)" else "#00FF7F")
        
    with col2:
        st.subheader("💡 คำแนะนำจาก AI")
        if scenario == "AWD (เปียกสลับแห้ง)":
            st.success("**คำแนะนำปัจจุบัน:**\n\nระดับน้ำอยู่ในเกณฑ์แกล้งข้าว (AWD) สมบูรณ์แบบ แนะนำให้คงสภาพดินแห้งต่อไปอีก 4 วัน ก่อนปล่อยน้ำเข้าแปลงรอบถัดไปเพื่อรักษาระดับผลผลิต")
        else:
            st.error("**คำแนะนำฉุกเฉิน:**\n\nพบน้ำท่วมขังและจุลินทรีย์ผลิตมีเทนทำงานหนัก! แนะนำให้ **ระบายน้ำออกทันที** จนกว่าระดับน้ำจะลดลงถึง -5 cm ใต้ผิวดิน เพื่อตัดวงจรการเกิดมีเทน")

elif page == "📊 คาร์บอนเครดิต (MRV)":
    st.markdown("## 🌿 ประเมินคาร์บอนเครดิตสะสม (MRV Estimation)")
    st.write("คำนวณจากส่วนต่างของสถานการณ์ฐาน (Baseline) และโครงการจริง (Project Scenario)")
    
    st.markdown('<div class="metric-card" style="text-align:center;"><div class="metric-title">คาร์บอนที่ลดได้สะสม (ตั้งแต่เริ่มฤดูกาล)</div><p class="metric-value" style="font-size:48px;">0.42 tCO₂e</p><p class="metric-delta">มูลค่าประเมินเบื้องต้น: 210 บาท / ไร่</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📌 **หมายเหตุ:** ข้อมูลนี้เป็นการคำนวณเบื้องต้นด้วย Digital Twin Model สำหรับเวทีประกวด AI New Gen")
