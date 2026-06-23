import streamlit as st
import streamlit.components.v1 as components

# --- 1. INITIALIZATION & CONFIG ---
st.set_page_config(page_title="METHATWIN AI | RICE RESEARCH PRECISION", layout="wide")

# --- 2. DEEP NAVY PREMIUM UI STYLING ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&family=Michroma&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { font-family: 'Kanit', sans-serif; }
        .stApp { background-color: #0A192F; color: #E6F1FF; }
        
        .brand-logo {
            font-family:import streamlit as st
import streamlit.components.v1 as components

# --- 1. INITIALIZATION & CONFIG ---
st.set_page_config(page_title="METHATWIN AI | DIGITAL TWIN PLATFORM", layout="wide", initial_sidebar_state="expanded")

# --- 2. DEEP NAVY PREMIUM UI STYLING ---
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

        // ฐานข้อมูลแปลงนามีการเปลี่ยนชื่อแปลง (Flooded, AWD, Control) และเพิ่ม Methane Flux
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
                <div class='pop-row'><span class='pop-label'>Water Management Type:</span><span class='pop-val' style='color:${p.color};'>${p.management}</span></div>
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
            font-size: 42px;
            color: #F47B20;
            text-shadow: 0px 0px 15px rgba(244, 123, 32, 0.6);
            margin-bottom: 0px;
        }
        .brand-sub { font-size: 13px; color: #8892B0; letter-spacing: 4px; margin-top: -5px; margin-bottom: 25px; text-transform: uppercase; }
        
        /* Dashboard Control Cards */
        .glass-panel {
            background-color: #112240;
            border: 1px solid #233554;
            border-left: 5px solid #F47B20;
            border-radius: 8px;
            padding: 20px;
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
        .panel-icon { color: #F47B20; font-size: 20px; margin-right: 10px; transition: all 0.3s ease; }
        .panel-title { color: #8892B0; font-size: 14px; text-transform: uppercase; font-weight: 500; }
        .panel-val { font-size: 34px; font-weight: 700; color: #FFFFFF; margin-top: 5px; }
        .panel-sub { font-size: 12px; color: #CCD6F6; margin-top: 5px; }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR CONTROL ---
with st.sidebar:
    st.markdown('<h1 class="brand-logo" style="font-size:26px;">METHATWIN</h1><div class="brand-sub">GeoJSON Engine v3</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🛰️ ศูนย์วิจัยข้าวเชียงใหม่ (ฝั่งขวา)")
    st.caption("ย้ายตำแหน่งพิกัดเข้าสู่พื้นที่บล็อกนาข้าวจริงฝั่งขวาเรียบร้อยแล้ว ไม่ทับสิ่งปลูกสร้างหรือถนนสาธารณะตามเงื่อนไข")
    st.divider()
    st.info("💡 แนะนำ: คลิกซ้ายที่พื้นที่ Polygon ของแปลงนาแต่ละสีโดยตรง เพื่อเปิดดูค่าวิเคราะห์และคำแนะนำจาก AI")

# --- 4. CORE DASHBOARD HEADERS ---
st.markdown('<h1 class="brand-logo">METHATWIN AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">High-Resolution Leaflet.js Mapping Architecture & Core Data Systems</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-map-location-dot panel-icon"></i> Core Coordinates</div><div class="panel-val" style="font-size: 24px; margin-top:10px;">18.6143722, 98.8976491</div><div class="panel-sub">พิกัดศูนย์กลางพื้นที่วิจัยหลัก</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-layer-group panel-icon"></i> Cadastral System</div><div class="panel-val" style="font-size: 24px; margin-top:10px;">Pure Real-Grid Polygon</div><div class="panel-sub">ขอบเขตล็อกนาจริง (No Markers)</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-clock panel-icon"></i> System Telemetry</div><div class="panel-val" style="font-size: 24px; margin-top:10px;">ONLINE</div><div class="panel-sub">อัปเดตระบบพิกัดดาวเทียมปัจจุบันสำเร็จ</div></div>', unsafe_allow_html=True)

# --- 5. EMBEDDED LEAFLET.JS ENGINE WITH REAL RICE FIELD COORDINATES ---
st.markdown("### 📐 ระบบแผนที่แสดงอาณาเขตและค่าวิเคราะห์ก๊าซเรือนกระจกรายแปลง (Leaflet Precision Engine)")

# โค้ด HTML/JS เจาะพิกัดเข้าล็อกแปลงนาข้าวด้านขวาของศูนย์วิจัยข้าวเชียงใหม่
leaflet_html_code = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body { margin: 0; padding: 0; background: #0A192F; }
        #map { width: 100%; height: 520px; border-radius: 8px; border: 1px solid #233554; }
        
        .leaflet-popup-content-wrapper { background: #112240 !important; color: #E6F1FF !important; border: 1px solid #233554; border-radius: 6px; font-family: 'sans-serif'; }
        .leaflet-popup-tip { background: #112240 !important; }
        .leaflet-popup-content { margin: 12px; font-size: 13px; line-height: 1.6; min-width: 260px; }
        .pop-title { font-size: 16px; font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #233554; padding-bottom: 4px; }
        .pop-row { display: flex; justify-content: space-between; margin-bottom: 3px; }
        .pop-label { color: #8892B0; }
        .pop-val { font-weight: bold; }
        .pop-ai { color: #64FFDA; margin-top: 6px; padding-top: 6px; border-top: 1px dashed #233554; font-style: italic; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // โฟกัสศูนย์กลางไปที่บริเวณกลุ่มแปลงนาด้านขวาของศูนย์วิจัย
        var map = L.map('map', { center: [18.6145, 98.8988], zoom: 19, maxZoom: 21 });
        
        // ใช้ภาพดาวเทียมความละเอียดสูงจาก Esri Satellite
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 21
        }).addTo(map);

        // คำนวณพิกัด GeoJSON ใหม่ย้ายเข้าสู่บล็อกนาข้าวสีเขียวฝั่งขวา ขนาดเท่ากัน และเรียงต่อกันตามคันนาจริง
        var geojsonFeatureCollection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot 1",
                        "management": "Flooded",
                        "ndvi": "0.76",
                        "ndwi": "0.58",
                        "waterLevel": "+10 cm",
                        "soilMoisture": "100%",
                        "methaneRisk": "High Critical",
                        "aiRec": "แนะนำ: ระดับน้ำสูงขังนาน กระตุ้นแก๊สมีเทน ควรเปิดประตูระบายน้ำออกทันที",
                        "color": "#FF3D00"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [98.8985, 18.6148],
                            [98.8988, 18.6148],
                            [98.8988, 18.6144],
                            [98.8985, 18.6144],
                            [98.8985, 18.6148]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot 2",
                        "management": "AWD",
                        "ndvi": "0.78",
                        "ndwi": "-0.08",
                        "waterLevel": "-5 cm",
                        "soilMoisture": "48%",
                        "methaneRisk": "Low Safe",
                        "aiRec": "แนะนำ: อยู่ในเกณฑ์แกล้งข้าวที่ดี ดินแห้งช่วยลดการปล่อยมีเทนได้ถึง 80%",
                        "color": "#00E676"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [98.8989, 18.6148],
                            [98.8992, 18.6148],
                            [98.8992, 18.6144],
                            [98.8989, 18.6144],
                            [98.8989, 18.6148]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot 3",
                        "management": "Reference",
                        "ndvi": "0.75",
                        "ndwi": "0.22",
                        "waterLevel": "+3 cm",
                        "soilMoisture": "75%",
                        "methaneRisk": "Moderate Warning",
                        "aiRec": "แนะนำ: แปลงอ้างอิงรักษาระดับน้ำตามเกณฑ์มาตรฐาน ควบคุมความชื้นต่อเนื่อง",
                        "color": "#FFEA00"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [98.8985, 18.6143],
                            [98.8992, 18.6143],
                            [98.8992, 18.6139],
                            [98.8985, 18.6139],
                            [98.8985, 18.6143]
                        ]]
                    }
                }
            ]
        };

        function styleStructure(feature) {
            return {
                fillColor: feature.properties.color,
                weight: 2.5,
                opacity: 1,
                color: feature.properties.color,
                fillOpacity: 0.35
            };
        }

        function bindInteractions(feature, layer) {
            var props = feature.properties;
            var content = `
                <div class='pop-title' style='color:${props.color};'>${props.plotName}</div>
                <div class='pop-row'><span class='pop-label'>Water Management:</span><span class='pop-val' style='color:${props.color};'>${props.management}</span></div>
                <div class='pop-row'><span class='pop-label'>NDVI:</span><span class='pop-val'>${props.ndvi}</span></div>
                <div class='pop-row'><span class='pop-label'>NDWI:</span><span class='pop-val'>${props.ndwi}</span></div>
                <div class='pop-row'><span class='pop-label'>Water Level:</span><span class='pop-val'>${props.waterLevel}</span></div>
                <div class='pop-row'><span class='pop-label'>Soil Moisture:</span><span class='pop-val'>${props.soilMoisture}</span></div>
                <div class='pop-row'><span class='pop-label'>Methane Risk:</span><span class='pop-val'>${props.methaneRisk}</span></div>
                <div class='pop-ai'><b>🤖 AI Recommendation:</b><br>${props.aiRec}</div>
            `;
            layer.bindPopup(content);
            
            layer.on('mouseover', function () { this.setStyle({ fillOpacity: 0.60, weight: 4 }); });
            layer.on('mouseout', function () { this.setStyle({ fillOpacity: 0.35, weight: 2.5 }); });
        }

        L.geoJSON(geojsonFeatureCollection, {
            style: styleStructure,
            onEachFeature: bindInteractions
        }).addTo(map);
    </script>
</body>
</html>
"""

# แสดงผลแผนที่ Leaflet ในจุดที่ถูกต้อง
components.html(leaflet_html_code, height=530, scrolling=False)

st.markdown("---")
st.caption("ระบบความปลอดภัยสูง © 2026 METHATWIN PLATFORM - พิกัดถูกล็อกเข้าแปลงนาเกษตรแม่นยำเรียบร้อยแล้ว")
