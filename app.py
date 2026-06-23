import streamlit as st
import streamlit.components.v1 as components

# --- 1. INITIALIZATION & CONFIG ---
st.set_page_config(page_title="METHATWIN AI | DIGITAL TWIN PLATFORM", layout="wide", initial_sidebar_state="expanded")

# --- 2. DEEP NAVY PREMIUM UI STYLING ---
# สังเกตตรงนี้ครับ ต้องมีเครื่องหมาย """ เปิดและปิดเสมอ
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&family=Michroma&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { font-family: 'Kanit', sans-serif; }
        .stApp { background-color: #0A192F; color: #E6F1FF; }
        
        /* Glow Logo */
        .brand-logo {
            font-family: 'Michroma', sans-serif;
            font-size: 38px;
            color: #F47B20;
            text-shadow: 0px 0px 15px rgba(244, 123, 32, 0.6);
            margin-bottom: 0px;
        }
        .brand-sub { font-size: 13px; color: #8892B0; letter-spacing: 3px; margin-top: -5px; margin-bottom: 25px; text-transform: uppercase; }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] { background-color: #112240; border-right: 1px solid #233554; }
        .sidebar-menu-title { color: #8892B0; font-size: 12px; letter-spacing: 2px; margin-bottom: 10px; text-transform: uppercase; }
        
        /* Dashboard Control Cards */
        .glass-panel {
            background-color: #112240;
            border: 1px solid #233554;
            border-left: 5px solid #F47B20;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            transition: all 0.3s ease;
        }
        .glass-panel:hover { 
            border-left: 5px solid #00E676; 
            transform: translateY(-3px); 
            box-shadow: 0 8px 25px rgba(0, 230, 118, 0.2);
            background-color: #1A2D4F;
        }
        .glass-panel:hover .panel-icon { color: #00E676 !important; transform: scale(1.2); }
        .panel-icon { color: #F47B20; font-size: 22px; margin-right: 10px; transition: all 0.3s ease; }
        .panel-title { color: #8892B0; font-size: 13px; text-transform: uppercase; font-weight: 500; }
        .panel-val { font-size: 32px; font-weight: 700; color: #FFFFFF; margin-top: 5px; }
        .panel-sub { font-size: 12px; color: #CCD6F6; margin-top: 5px; }
        
        /* Text Colors */
        .text-danger { color: #FF3D00; }
        .text-success { color: #00E676; }
        .text-warning { color: #FFEA00; }
        .text-info { color: #64FFDA; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<h1 class="brand-logo" style="font-size:24px;">METHATWIN</h1><div class="brand-sub">Digital Twin Platform</div>', unsafe_allow_html=True)
    st.divider()
    
    st.markdown('<div class="sidebar-menu-title">PLATFORM MODULES</div>', unsafe_allow_html=True)
    selected_menu = st.radio(
        "",
        [
            "📊 Dashboard", 
            "🗺️ Field Map", 
            "🌐 Digital Twin", 
            "🤖 AI Recommendation", 
            "💨 Methane Analytics", 
            "🍃 Carbon Credit", 
            "📅 Forecast", 
            "📑 Report"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.info("💡 **Digital Twin Engine Active**\nระบบกำลังซิงค์ข้อมูลจากดาวเทียมและเซนเซอร์ภาคพื้นดินแบบเรียลไทม์")

# --- 4. TOP DASHBOARD (4 METRICS) ---
st.markdown('<h1 class="brand-logo">DIGITAL TWIN PLATFORM</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="brand-sub">Current Module: {selected_menu[2:]} | Chiang Mai Rice Research Center</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-triangle-exclamation panel-icon"></i> Methane Risk Index</div><div class="panel-val text-warning">46.4 <span style="font-size:14px; color:#8892B0;">Avg</span></div><div class="panel-sub">สถานะภาพรวม: <strong class="text-warning">เฝ้าระวัง</strong></div></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-leaf panel-icon"></i> Carbon Reduction</div><div class="panel-val text-success">-24.5 <span style="font-size:14px; color:#8892B0;">tCO2e</span></div><div class="panel-sub">เทียบกับฐานข้อมูล Baseline</div></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-water panel-icon"></i> Water Status</div><div class="panel-val text-info">AWD-Active</div><div class="panel-sub">ระบบชลประทาน: ควบคุมได้</div></div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-cloud-sun panel-icon"></i> Forecast 7 Days</div><div class="panel-val">Dry <i class="fa-solid fa-sun text-warning" style="font-size:24px;"></i></div><div class="panel-sub">ฝนทิ้งช่วง เหมาะแก่การระบายน้ำ</div></div>', unsafe_allow_html=True)

# --- 5. EMBEDDED LEAFLET.JS (FIELD MAP & DIGITAL TWIN) ---
st.markdown("### 📐 ระบบแสดงขอบเขตแปลงดิจิทัลทวิน (Field Digital Twin)")

# โค้ดส่วนนี้เป็น HTML ก็ต้องมี """ ครอบเปิด-ปิดเช่นกัน
leaflet_html_code = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body { margin: 0; padding: 0; background: #0A192F; }
        #map { width: 100%; height: 500px; border-radius: 8px; border: 1px solid #233554; }
        
        .leaflet-popup-content-wrapper { background: #112240 !important; color: #E6F1FF !important; border: 1px solid #233554; border-radius: 6px; font-family: 'sans-serif'; }
        .leaflet-popup-tip { background: #112240 !important; }
        .leaflet-popup-content { margin: 15px; font-size: 13px; line-height: 1.6; min-width: 270px; }
        .pop-title { font-size: 17px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #233554; padding-bottom: 5px; text-transform: uppercase; }
        .pop-row { display: flex; justify-content: space-between; margin-bottom: 4px; }
        .pop-label { color: #8892B0; }
        .pop-val { font-weight: bold; }
        .pop-ai { color: #64FFDA; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #233554; font-style: italic; line-height: 1.4; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map', { center: [18.6145, 98.8988], zoom: 19, maxZoom: 21 });
        
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 21
        }).addTo(map);

        var geojsonFeatureCollection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Flooded Plot",
                        "management": "Flooded",
                        "ndvi": "0.76",
                        "ndwi": "0.58",
                        "waterLevel": "+10 cm",
                        "soilMoisture": "100%",
                        "methaneFlux": "85.2 mg/m²/h",
                        "methaneRisk": "High Critical",
                        "aiRec": "CRITICAL: ระดับน้ำขังต่อเนื่อง กระตุ้นก๊าซมีเทนรุนแรง ระบบ Digital Twin แนะนำให้เปิดประตูระบายน้ำทันที",
                        "color": "#FF3D00"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[98.8985, 18.6148], [98.8988, 18.6148], [98.8988, 18.6144], [98.8985, 18.6144], [98.8985, 18.6148]]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "AWD Plot",
                        "management": "AWD (แกล้งดิน)",
                        "ndvi": "0.78",
                        "ndwi": "-0.08",
                        "waterLevel": "-5 cm",
                        "soilMoisture": "48%",
                        "methaneFlux": "12.4 mg/m²/h",
                        "methaneRisk": "Low Safe",
                        "aiRec": "OPTIMAL: สภาวะดินแห้งสลับเปียกสมบูรณ์แบบ แพลตฟอร์มคาดการณ์ว่าจะลดก๊าซเรือนกระจกได้กว่า 55% ในรอบนี้",
                        "color": "#00E676"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[98.8989, 18.6148], [98.8992, 18.6148], [98.8992, 18.6144], [98.8989, 18.6144], [98.8989, 18.6148]]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Control Plot",
                        "management": "Control",
                        "ndvi": "0.75",
                        "ndwi": "0.22",
                        "waterLevel": "+3 cm",
                        "soilMoisture": "75%",
                        "methaneFlux": "41.8 mg/m²/h",
                        "methaneRisk": "Moderate Warning",
                        "aiRec": "MONITORING: แปลงควบคุมมีแนวโน้มก๊าซมีเทนสะสม เฝ้าระวังความชื้นของดินในช่วง 7 วันข้างหน้า",
                        "color": "#FFEA00"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[98.8985, 18.6143], [98.8992, 18.6143], [98.8992, 18.6139], [98.8985, 18.6139], [98.8985, 18.6143]]]
                    }
                }
            ]
        };

        function styleStructure(feature) {
            return { fillColor: feature.properties.color, weight: 2.5, opacity: 1, color: feature.properties.color, fillOpacity: 0.35 };
        }

        function bindInteractions(feature, layer) {
            var p = feature.properties;
            var content = `
                <div class='pop-title' style='color:${p.color};'>${p.plotName}</div>
                <div class='pop-row'><span class='pop-label'>Water Management:</span><span class='pop-val' style='color:${p.color};'>${p.management}</span></div>
                <div class='pop-row'><span class='pop-label'>NDVI:</span><span class='pop-val'>${p.ndvi}</span></div>
                <div class='pop-row'><span class='pop-label'>NDWI:</span><span class='pop-val'>${p.ndwi}</span></div>
                <div class='pop-row'><span class='pop-label'>Water Level:</span><span class='pop-val'>${p.waterLevel}</span></div>
                <div class='pop-row'><span class='pop-label'>Soil Moisture:</span><span class='pop-val'>${p.soilMoisture}</span></div>
                <div class='pop-row'><span class='pop-label'>Methane Flux:</span><span class='pop-val'>${p.methaneFlux}</span></div>
                <div class='pop-row'><span class='pop-label'>Methane Risk Index:</span><span class='pop-val'>${p.methaneRisk}</span></div>
                <div class='pop-ai'><b>🤖 AI Recommendation:</b><br>${p.aiRec}</div>
            `;
            layer.bindPopup(content);
            
            layer.on('mouseover', function () { this.setStyle({ fillOpacity: 0.60, weight: 4 }); });
            layer.on('mouseout', function () { this.setStyle({ fillOpacity: 0.35, weight: 2.5 }); });
        }

        L.geoJSON(geojsonFeatureCollection, { style: styleStructure, onEachFeature: bindInteractions }).addTo(map);
    </script>
</body>
</html>
"""

components.html(leaflet_html_code, height=510, scrolling=False)
