import streamlit as st
import streamlit.components.v1 as components
import datetime

# --- 1. INITIALIZATION & CONFIG ---
st.set_page_config(page_title="METHATWIN AI | CO2 & CH4 MANAGEMENT", layout="wide")

# --- 2. DEEP NAVY PREMIUM CSS CONTROL ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;700&family=Michroma&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { font-family: 'Kanit', sans-serif; }
        .stApp { background-color: #0A192F; color: #E6F1FF; }
        
        /* Glow Logo */
        .brand-logo {
            font-family: 'Michroma', sans-serif;
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
    st.markdown('<h1 class="brand-logo" style="font-size:26px;">METHATWIN</h1><div class="brand-sub">GeoJSON Engine v2</div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("### 🛰️ Live Telemetry Network")
    st.caption(f"ระบบฐานข้อมูลและผังวิเคราะห์เชิงพื้นที่ทำงานร่วมกับภาพถ่ายดาวเทียมความละเอียดสูงจากเครือข่าย OpenStreetMap Satellite ดึงข้อมูลพิกัดตรงผ่านระบบพิกัดอ้างอิงภูมิศาสตร์จริง")
    st.divider()
    st.info("💡 คำแนะนำ: นำเมาส์ไปคลิกที่ผืนพิกัด Polygon ในแผงแผนที่โดยตรง เพื่อเรียกดูชุดข้อมูลเชิงลึกและข้อเสนอแนะจาก AI รายแปลง")

# --- 4. CORE DASHBOARD HEADERS ---
st.markdown('<h1 class="brand-logo">METHATWIN AI</h1>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">High-Resolution Leaflet.js Mapping Architecture & Core Data Systems</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-map-location-dot panel-icon"></i> Core Coordinates</div><div class="panel-val" style="font-size: 24px; margin-top:10px;">18.6143722, 98.8976491</div><div class="panel-sub">พิกัดศูนย์กลางศูนย์วิจัยความแม่นยำสูง</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-layer-group panel-icon"></i> Cadastral System</div><div class="panel-val" style="font-size: 24px; margin-top:10px;">Pure GeoJSON Layer</div><div class="panel-sub">แสดงผลขอบเขตจริง (No Mid-Markers)</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="glass-panel"><div class="panel-title"><i class="fa-solid fa-clock panel-icon"></i> System Telemetry</div><div class="panel-val" style="font-size: 24px; margin-top:10px;">ONLINE</div><div class="panel-sub">สิงหาคม 2569 | ข้อมูลเป็นปัจจุบัน</div></div>', unsafe_allow_html=True)

# --- 5. EMBEDDED LEAFLET.JS ENGINE WITH GEOJSON ---
st.markdown("### 📐 ระบบแผนที่แสดงอาณาเขตและค่าวิเคราะห์ก๊าซเรือนกระจกรายแปลง (Leaflet Precision Engine)")

# โค้ดดิบ HTML/JS ของ Leaflet ที่รันแยกต่างหากเพื่อความปลอดภัย ไม่ขัดแย้งกับ Python
leaflet_html_code = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body { margin: 0; padding: 0; background: #0A192F; }
        #map { width: 100%; height: 520px; border-radius: 8px; border: 1px solid #233554; }
        
        /* Leaflet Pop-up Customization */
        .leaflet-popup-content-wrapper { background: #112240 !important; color: #E6F1FF !important; border: 1px solid #233554; border-radius: 6px; font-family: 'sans-serif'; }
        .leaflet-popup-tip { background: #112240 !important; }
        .leaflet-popup-content { margin: 12px; font-size: 13px; line-height: 1.6; min-width: 250px; }
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
        // ตั้งค่าพิกัดศูนย์กลางตามเงื่อนไขอย่างเคร่งครัด
        var map = L.map('map', { center: [18.6143722, 98.8976491], zoom: 18, maxZoom: 21 });
        
        // ใช้ OpenStreetMap Satellite (Esri World Imagery Map) ตามบรีฟ
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 21
        }).addTo(map);

        // โครงสร้างฐานข้อมูลยืดหยุ่นในรูปแบบ GeoJSON (พิกัดจัดวางให้เกาะกลุ่มรอบจุดศูนย์กลางตามขนาดรูปทรงนาจริง)
        var geojsonFeatureCollection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot A",
                        "management": "Flooded",
                        "ndvi": "0.68",
                        "ndwi": "0.52",
                        "soilMoisture": "100%",
                        "methaneRisk": "85.2 (Critical)",
                        "aiRec": "CRITICAL RISK: ปล่อยน้ำออกจากแปลงนาเพื่อขัดขวางจุลินทรีย์สร้างมีเทน ด่วน!",
                        "color": "#FF3D00"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [98.8971, 18.6147],
                            [98.8976, 18.6147],
                            [98.8976, 18.6143],
                            [98.8971, 18.6143],
                            [98.8971, 18.6147]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot B",
                        "management": "AWD",
                        "ndvi": "0.74",
                        "ndwi": "-0.12",
                        "soilMoisture": "42%",
                        "methaneRisk": "12.4 (Safe)",
                        "aiRec": "EXCELLENT: อยู่ในเกณฑ์แกล้งข้าว ดินแห้งกระตุ้นรากและลดมีเทนสมบูรณ์แบบ",
                        "color": "#00E676"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [98.8977, 18.6147],
                            [98.8982, 18.6147],
                            [98.8982, 18.6143],
                            [98.8977, 18.6143],
                            [98.8977, 18.6147]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot C",
                        "management": "Control",
                        "ndvi": "0.71",
                        "ndwi": "0.15",
                        "soilMoisture": "72%",
                        "methaneRisk": "41.8 (Warning)",
                        "aiRec": "NORMAL MONITORING: แปลงควบคุมตามเกณฑ์ปกติ เฝ้าระวังระดับน้ำหากสูงเกินกำหนด",
                        "color": "#FFEA00"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [98.8971, 18.6142],
                            [98.8982, 18.6142],
                            [98.8982, 18.6138],
                            [98.8971, 18.6138],
                            [98.8971, 18.6142]
                        ]]
                    }
                }
            ]
        };

        // ฟังก์ชันกำหนดรูปแบบเส้นขอบและสีพื้นตามกรรมสิทธิ์ใน GeoJSON
        function styleStructure(feature) {
            return {
                fillColor: feature.properties.color,
                weight: 3,
                opacity: 1,
                color: feature.properties.color,
                fillOpacity: 0.35
            };
        }

        // จัดการเหตุการณ์เมื่อคลิกเปิดฟังก์ชันพิกัดแต่ละแปลง
        function bindInteractions(feature, layer) {
            var props = feature.properties;
            var content = `
                <div class='pop-title' style='color:${props.color};'>${props.plotName}</div>
                <div class='pop-row'><span class='pop-label'>Water Management Type:</span><span class='pop-val' style='color:${props.color};'>${props.management}</span></div>
                <div class='pop-row'><span class='pop-label'>NDVI Value:</span><span class='pop-val'>${props.ndvi}</span></div>
                <div class='pop-row'><span class='pop-label'>NDWI Value:</span><span class='pop-val'>${props.ndwi}</span></div>
                <div class='pop-row'><span class='pop-label'>Soil Moisture:</span><span class='pop-val'>${props.soilMoisture}</span></div>
                <div class='pop-row'><span class='pop-label'>Methane Risk Index:</span><span class='pop-val'>${props.methaneRisk}</span></div>
                <div class='pop-ai'><b>🤖 AI Recommendation:</b> ${props.aiRec}</div>
            `;
            layer.bindPopup(content);
            
            layer.on('mouseover', function () { this.setStyle({ fillOpacity: 0.65, weight: 4 }); });
            layer.on('mouseout', function () { this.setStyle({ fillOpacity: 0.35, weight: 3 }); });
        }

        // วาดรูปทรงเรขาคณิตและจำลองพิกัดลงแผ่นที่โดยตรง
        L.geoJSON(geojsonFeatureCollection, {
            style: styleStructure,
            onEachFeature: bindInteractions
        }).addTo(map);
    </script>
</body>
</html>
"""

# ทำการฝังตัวแปลรหัส HTML ลงบนหน้าจอ Dashboard
components.html(leaflet_html_code, height=530, scrolling=False)

st.markdown("---")
st.caption("ระบบความปลอดภัยสูงสุด © 2026 METHATWIN PLATFORM - ข้อมูลพิกัดได้รับการคุ้มครองและตรวจสอบความถูกต้องผ่านสัญญากลุ่มวิจัยร่วม")
