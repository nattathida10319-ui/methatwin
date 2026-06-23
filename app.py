import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time

# --- 1. ตั้งค่าหน้าจอแบบ Full Dashboard ---
st.set_page_config(page_title="MethaTwin | AI New Gen", layout="wide", page_icon="🌾")

# --- CSS ตกแต่งให้เป็นเหมือนหน้าปัดยานอวกาศ (Dark UI) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .metric-card {
        background-color: #1E2129;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 5px solid #00FF7F;
    }
    .metric-card-danger { border-left: 5px solid #FF4B4B; }
    .metric-title { font-size: 14px; color: #A0AEC0; margin-bottom: 5px; }
    .metric-value { font-size: 32px; font-weight: bold; margin: 0; }
    .metric-delta { font-size: 14px; color: #00FF7F; }
    .metric-delta-danger { color: #FF4B4B; }
    </style>
""", unsafe_allow_html=True)

# --- 2. ข้อมูลพิกัดและโมเดลจำลองแปลงนา ---
# พิกัดแปลงนาวิจัย ศูนย์วิจัยข้าวเชียงใหม่ อ.สันป่าตอง
CENTER_LAT = 18.6235
CENTER_LON = 98.8964

@st.cache_data(ttl=5)
def get_sensor_data(scenario):
    np.random.seed(int(time.time()) % 100)
    num_points = 200
    
    # สุ่มพิกัดให้กระจายตัวอยู่ภายในแปลงนาจริงๆ (รูปทรงกรอบสี่เหลี่ยมรอบพิกัดหลัก)
    lats = np.random.uniform(18.6210, 18.6260, num_points)
    lons = np.random.uniform(98.8930, 98.8990, num_points)
    
    if scenario == "AWD (เปียกสลับแห้ง)":
        # มีเทนต่ำ -> สีเขียวเยอะ
        color_r = 0
        color_g = 255
    else:
        # มีเทนสูง -> สีแดงเยอะ
        color_r = 255
        color_g = 0
        
    return pd.DataFrame({
        'latitude': lats, 
        'longitude': lons, 
        'r': color_r,
        'g': color_g,
        'b': 0,
        'a': 180
    })

# --- 3. ระบบนำทางด้านข้าง (Sidebar Navigation) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1892/1892747.png", width=60)
    st.markdown("### 🌾 MethaTwin AI")
    st.caption("AI New Gen Project")
    st.markdown("---")
    
    page = st.sidebar.selectbox("เมนูหลัก (Navigation)", [
        "🎯 แดชบอร์ด (Live Map)", 
        "🤖 การวิเคราะห์จาก AI", 
        "📊 คาร์บอนเครดิต (MRV)"
    ])
    
    st.markdown("---")
    st.markdown("**⚙️ ตั้งค่าสถานการณ์จำลอง**")
    scenario = st.selectbox("โหมดการจัดการน้ำ:", ["AWD (เปียกสลับแห้ง)", "น้ำท่วมขัง (Flooded)"])

# โหลดข้อมูลตามสถานการณ์
df_points = get_sensor_data(scenario)

# --- 4. การแสดงผลแต่ละหน้า ---

if page == "🎯 แดชบอร์ด (Live Map)":
    st.markdown("## 🛰️ ศูนย์บัญชาการแปลงนาอัจฉริยะ (Digital Twin)")
    st.caption(f"📍 พิกัด: แปลงนาวิจัย A1 ศูนย์วิจัยข้าวเชียงใหม่ อ.สันป่าตอง | 🕒 อัปเดตล่าสุด: {datetime.datetime.now().strftime('%d %B %Y %H:%M:%S')}")
    
    # 4 ตัวเลขสถานะแบบการ์ดสไตล์ Dark UI เหมือนต้นฉบับ
    c1, c2, c3, c4 = st.columns(4)
    if scenario == "AWD (เปียกสลับแห้ง)":
        c1.markdown('<div class="metric-card"><div class="metric-title">ค่ามีเทนเฉลี่ย (CH₄ Flux)</div><p class="metric-value">12.4 <span style="font-size:16px;">mg/m²/h</span></p><p class="metric-delta">⬇ 45% (ลดลงจากการแกล้งข้าว)</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="metric-card"><div class="metric-title">ดัชนีความเสี่ยงมีเทน</div><p class="metric-value">15 / 100</p><p class="metric-delta">🟢 ความเสี่ยงต่ำ (ปลอดภัย)</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="metric-card"><div class="metric-title">ระดับน้ำในนา (Water Level)</div><p class="metric-value">-7.5 <span style="font-size:16px;">cm</span></p><p class="metric-delta">อยู่ในช่วงแกล้งข้าว</p></div>', unsafe_allow_html=True)
        c4.markdown('<div class="metric-card"><div class="metric-title">ความชื้นดิน (Soil Moisture)</div><p class="metric-value">68 <span style="font-size:16px;">%</span></p><p class="metric-delta">เหมาะสม</p></div>', unsafe_allow_html=True)
    else:
        c1.markdown('<div class="metric-card metric-card-danger"><div class="metric-title">ค่ามีเทนเฉลี่ย (CH₄ Flux)</div><p class="metric-value">54.2 <span style="font-size:16px;">mg/m²/h</span></p><p class="metric-delta-danger">⬆ 18% (สูงเกินเกณฑ์)</p></div>', unsafe_allow_html=True)
        c2.markdown('<div class="metric-card metric-card-danger"><div class="metric-title">ดัชนีความเสี่ยงมีเทน</div><p class="metric-value">78 / 100</p><p class="metric-delta-danger">🔴 ความเสี่ยงสูง (วิกฤต)</p></div>', unsafe_allow_html=True)
        c3.markdown('<div class="metric-card metric-card-danger"><div class="metric-title">ระดับน้ำในนา (Water Level)</div><p class="metric-value">8.5 <span style="font-size:16px;">cm</span></p><p class="metric-delta-danger">น้ำท่วมขังต่อเนื่อง</p></div>', unsafe_allow_html=True)
        c4.markdown('<div class="metric-card metric-card-danger"><div class="metric-title">ความชื้นดิน (Soil Moisture)</div><p class="metric-value">96 <span style="font-size:16px;">%</span></p><p class="metric-delta-danger">ดินขาดออกซิเจน</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- แผนที่ความเสี่ยงระดับแปลง (Real-time Heatmap) ---
    st.markdown("### 🗺️ แผนที่พิกัดแปลงนาและการปล่อยก๊าซมีเทนแยกโซน")
    st.write("แสดงพิกัดจริง ณ **อ.สันป่าตอง จ.เชียงใหม่** ข้อมูลแยกโซนตามค่าความชื้นและเซนเซอร์")
    
    # ใช้ระบบแผนที่มาตรฐานของ Streamlit ที่เสถียรและแสดงภาพดาวเทียม
    st.map(df_points, latitude=CENTER_LAT, longitude=CENTER_LON, zoom=15, color=None, size=20)
    st.caption("💡 แผนที่จะแสดงจุดเซนเซอร์ย่อยภายในแปลงนา: สีเขียว = ปล่อยมีเทนต่ำมาก | สีแดง = จุดสะสมแก๊สมีเทนสูง")

elif page == "🤖 การวิเคราะห์จาก AI":
    st.markdown("## 🧠 ระบบผู้เชี่ยวชาญ AI (AI Recommendation)")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📈 แนวโน้มการปล่อยมีเทน 7 วันล่วงหน้า")
        dates = pd.date_range(start=datetime.datetime.today(), periods=7).strftime('%d %b')
        trend = [22, 20, 18, 15, 12, 10, 8] if scenario == "AWD (เปียกสลับแห้ง)" else [65, 68, 70, 75, 78, 80, 82]
        st.line_chart(pd.DataFrame({'วันที่': dates, 'ฟลักซ์มีเทนคาดการณ์': trend}).set_index('วันที่'))
    with col2:
        st.subheader("💡 คำแนะนำจาก AI")
        if scenario == "AWD (เปียกสลับแห้ง)":
            st.success("**ควรปล่อยน้ำแห้งต่ออีก 4 วัน**\n\nระดับน้ำใต้ดินเหมาะสมกับการทำนาแบบเปียกสลับแห้ง คาดว่าจะลดการปล่อยมีเทนได้ถึง 18%")
        else:
            st.error("**คำแนะนำฉุกเฉิน:**\n\nพบน้ำท่วมขังเกินเกณฑ์ แนะนำให้ระบายน้ำออกทันทีเพื่อตัดวงจรจุลินทรีย์โบราณที่ผลิตแก๊สมีเทน")

elif page == "📊 คาร์บอนเครดิต (MRV)":
    st.markdown("## 🌿 ประเมินคาร์บอนเครดิตสะสม (MRV Estimation)")
    st.markdown('<div class="metric-card" style="text-align:center;"><div class="metric-title">คาร์บอนที่ลดได้สะสม (ฤดูกาลปัจจุบัน)</div><p class="metric-value" style="font-size:48px;">0.42 tCO₂e</p><p class="metric-delta">มูลค่าประเมินเบื้องต้น: 1,260 บาท</p></div>', unsafe_allow_html=True)
