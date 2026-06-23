import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pydeck as pdk
import time

# --- 1. ตั้งค่าคอนฟิกหลักของเว็บขั้นสุด ---
st.set_page_config(page_title="MethaTwin Pro | Command Center", layout="wide", page_icon="🌍")

st.markdown("""
    <style>
    .big-font { font-size:38px !important; font-weight: bold; color: #00FF7F; }
    </style>
""", unsafe_allow_html=True)

# --- 2. ฟังก์ชันจำลองข้อมูล (Dataset & Live Data) ---
@st.cache_data
def load_simulated_dataset():
    dates = [datetime.date(2026, 5, 19) + datetime.timedelta(days=i) for i in range(10)]
    df_flooded = pd.DataFrame({
        'วันที่': dates, 'ระดับน้ำ (cm)': [5.0, 5.5, 6.0, 6.8, 7.2, 7.8, 8.0, 8.0, 7.8, 7.8],
        'ฟลักซ์มีเทน (mg/m²/h)': [15.2, 18.5, 22.1, 25.4, 28.0, 31.2, 34.5, 36.8, 37.5, 37.6]
    })
    df_awd = pd.DataFrame({
        'วันที่': dates, 'ระดับน้ำ (cm)': [5.0, 3.5, 1.2, -1.5, -4.0, -7.5, -7.5, -3.0, 2.0, 5.0],
        'ฟลักซ์มีเทน (mg/m²/h)': [15.2, 16.0, 14.1, 11.5, 9.2, 8.0, 8.5, 10.2, 14.5, 22.4]
    })
    return df_flooded, df_awd

df_flooded, df_awd = load_simulated_dataset()

@st.cache_data(ttl=60)
def generate_live_map_data():
    np.random.seed(int(time.time()) % 100)
    num_points = 150
    lats = np.random.uniform(18.6180, 18.6290, num_points)
    lons = np.random.uniform(98.8900, 98.9020, num_points)
    methane_flux = np.random.uniform(10, 80, num_points)
    
    colors = []
    for flux in methane_flux:
        if flux >= 50: colors.append([255, 50, 50, 200])   # แดง (เสี่ยง)
        elif flux >= 30: colors.append([255, 200, 50, 200]) # เหลือง
        else: colors.append([50, 255, 50, 200])             # เขียว (ปลอดภัย)
            
    return pd.DataFrame({'lat': lats, 'lon': lons, 'methane': methane_flux, 'color': colors})

df_map = generate_live_map_data()

# --- 3. หน้าแดชบอร์ดหลัก (Command Center) ---
def page_main_dashboard():
    col_logo, col_title = st.columns([1, 8])
    with col_logo:
        st.image("https://cdn-icons-png.flaticon.com/512/1892/1892747.png", width=80)
    with col_title:
        st.markdown('<p class="big-font">🌍 MethaTwin: Live Command Center</p>', unsafe_allow_html=True)
        st.caption(f"📍 พิกัด: ศูนย์วิจัยข้าวเชียงใหม่ อ.สันป่าตอง | 🕒 อัปเดตล่าสุด: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    st.markdown("---")
    scenario = st.selectbox("🎛️ เลือกระบบจัดการน้ำ (Scenario):", ["🌿 ระบบจัดการน้ำอัจฉริยะแบบเปียกสลับแห้ง (AWD)", "💧 การทำนาแบบน้ำท่วมขังดั้งเดิม (Flooded)"])

    col1, col2, col3, col4 = st.columns(4)
    if "AWD" in scenario:
        col1.metric("ดัชนีมีเทนภาพรวม", "18.4 mg/m²", "-45%", delta_color="inverse")
        col2.metric("ระดับน้ำเฉลี่ย", "-5.2 cm", "-2.1 cm")
        col3.metric("ความชื้นในดิน", "68%", "-5%")
        col4.metric("สถานะพื้นที่", "🟢 ปลอดภัย")
        df_map['methane'] = df_map['methane'] * 0.4
        df_map['color'] = df_map['methane'].apply(lambda x: [50, 255, 50, 200] if x < 30 else [255, 200, 50, 200])
    else:
        col1.metric("ดัชนีมีเทนภาพรวม", "54.2 mg/m²", "+12%", delta_color="inverse")
        col2.metric("ระดับน้ำเฉลี่ย", "8.5 cm", "+1.0 cm")
        col3.metric("ความชื้นในดิน", "96%", "+2%")
        col4.metric("สถานะพื้นที่", "🔴 วิกฤต")

    st.markdown("### 🗺️ แผนที่ระบุโซนความเสี่ยงมีเทนแบบ 3 มิติ (Methane Heatmap)")
    st.write("*(ใช้เมาส์คลิกซ้ายค้างไว้เพื่อหมุนมุมมอง 3 มิติ)*")
    
    layer = pdk.Layer(
        'ColumnLayer',
        data=df_map, get_position='[lon, lat]', get_elevation='methane',
        elevation_scale=4, radius=30, get_fill_color='color',
        pickable=True, auto_highlight=True,
    )
    view_state = pdk.ViewState(latitude=18.6235, longitude=98.8964, zoom=15, pitch=50, bearing=10)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "ค่ามีเทน: {methane} mg/m²/h"}))

# --- 4. หน้าวิเคราะห์ภาพถ่ายดาวเทียม ---
def page_satellite():
    st.markdown('<h1 style="color:#00FF7F;">🛰️ วิเคราะห์ภาพถ่ายดาวเทียม Sentinel-2</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://scx2.b-cdn.net/gfx/news/2021/a-new-method-that-uses.jpg", caption="NDVI Analysis")
    with col2:
        st.subheader("แนวโน้มดัชนีพืชพรรณ")
        st.line_chart(pd.DataFrame(np.random.randn(20, 2) * 0.1 + [0.6, 0.4], columns=['Flooded', 'AWD']))

# --- 5. หน้าประเมินคาร์บอนเครดิต (MRV) ---
def page_mrv():
    st.markdown('<h1 style="color:#00FF7F;">📊 รายงานคาร์บอนเครดิต (MRV)</h1>', unsafe_allow_html=True)
    st.info("💡 การจัดการน้ำแบบ AWD ช่วยลดก๊าซมีเทนสะสม คิดเป็นคาร์บอนเครดิต **0.42 tCO2e** (มูลค่าประมาณ 1,260 บาท/ไร่)")
    st.subheader("📉 เปรียบเทียบฟลักซ์ก๊าซมีเทน (Methane Flux Trend)")
    chart_methane = pd.DataFrame({
        'วันที่': df_awd['วันที่'], 'แบบน้ำท่วมขัง (Flooded)': df_flooded['ฟลักซ์มีเทน (mg/m²/h)'], 'แบบเปียกสลับแห้ง (AWD)': df_awd['ฟลักซ์มีเทน (mg/m²/h)']
    }).set_index('วันที่')
    st.line_chart(chart_methane)

# --- 6. หน้าคลังข้อมูลดิบ ---
def page_dataset():
    st.markdown('<h1 style="color:#00FF7F;">📁 คลังข้อมูลดิบ (Raw Dataset)</h1>', unsafe_allow_html=True)
    st.subheader("ตารางข้อมูลแบบจำลองเปียกสลับแห้ง (AWD)")
    st.dataframe(df_awd, use_container_width=True)

# --- 7. ระบบเปิดเมนูหลายหน้า (Navigation) ---
pg = st.navigation([
    st.Page(page_main_dashboard, title="Live 3D Dashboard", icon="🌍"),
    st.Page(page_satellite, title="Satellite Analysis", icon="🛰️"),
    st.Page(page_mrv, title="Carbon Credit (MRV)", icon="📊"),
    st.Page(page_dataset, title="Raw Dataset", icon="📁")
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌾 โครงงาน สสวท.")
st.sidebar.info("**ชื่อโครงงาน:** MethaTwin\n\n**พื้นที่:** อ.สันป่าตอง จ.เชียงใหม่")

pg.run()
pg.run()
