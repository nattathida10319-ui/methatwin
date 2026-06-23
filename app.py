<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>METHATWIN AI | Leaflet Precision Map</title>
    
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&family=Michroma&display=swap" rel="stylesheet">

    <style>
        body { margin: 0; padding: 0; background-color: #0A192F; }
        #map { width: 100vw; height: 100vh; }
        
        /* UI Overlay ล้ำๆ ด้านบนซ้าย */
        .ui-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: rgba(17, 34, 64, 0.85);
            border-left: 4px solid #F47B20;
            padding: 15px 25px;
            border-radius: 8px;
            color: #E6F1FF;
            font-family: 'Kanit', sans-serif;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }
        .brand { font-family: 'Michroma', sans-serif; font-size: 24px; color: #F47B20; margin: 0 0 5px 0; text-shadow: 0 0 10px rgba(244,123,32,0.5); }
        .sub-brand { font-size: 12px; color: #8892B0; letter-spacing: 2px; text-transform: uppercase; margin: 0; }

        /* Custom Popup สไตล์ Futuristic Navy/Orange */
        .leaflet-popup-content-wrapper {
            background-color: #112240;
            border: 1px solid #233554;
            border-radius: 8px;
            color: #E6F1FF;
            font-family: 'Kanit', sans-serif;
            box-shadow: 0 8px 25px rgba(0,0,0,0.8);
        }
        .leaflet-popup-tip { background-color: #112240; }
        .leaflet-popup-content { margin: 15px; line-height: 1.5; font-size: 14px; min-width: 220px; }
        
        /* จัดรูปแบบข้อมูลใน Popup */
        .pop-title { font-size: 18px; font-weight: 600; margin-bottom: 10px; border-bottom: 1px solid #233554; padding-bottom: 5px; }
        .pop-item { display: flex; justify-content: space-between; margin-bottom: 5px; }
        .pop-label { color: #8892B0; }
        .pop-val { font-weight: 600; }
        
        /* สีตัวหนังสือใน Popup ตามสถานะ */
        .text-red { color: #FF3D00; }
        .text-green { color: #00E676; }
        .text-yellow { color: #FFEA00; }
        .text-ai { color: #64FFDA; margin-top: 10px; font-style: italic; border-top: 1px dashed #233554; padding-top: 8px;}
    </style>
</head>
<body>

    <div class="ui-panel">
        <h1 class="brand">METHATWIN</h1>
        <p class="sub-brand">GeoJSON Precision Map</p>
    </div>

    <div id="map"></div>

    <script>
        // 1. กำหนดจุดศูนย์กลางแผนที่ตามที่คุณระบุ
        const mapCenter = [18.6143722, 98.8976491];
        
        // สร้าง Map Object (ซูมลึกสุดถึงระดับ 20)
        const map = L.map('map', {
            center: mapCenter,
            zoom: 18,
            maxZoom: 20
        });

        // 2. ใช้ Base Map เป็น Satellite ภาพถ่ายดาวเทียมความละเอียดสูง (Esri World Imagery)
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            maxZoom: 20
        }).addTo(map);

        // 3. ฐานข้อมูลแปลงนาในรูปแบบ GeoJSON (สามารถเปลี่ยนพิกัด Coordinates ให้ตรงกับงานเซอร์เวย์จริงได้เลย)
        // ** พิกัดใน GeoJSON ต้องเรียงแบบ [Longitude, Latitude] เสมอ **
        const ricePlotsGeoJSON = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot A",
                        "management": "Flooded",
                        "ndvi": "0.68",
                        "ndwi": "0.45",
                        "soilMoisture": "100%",
                        "methaneRisk": "85.2 (Critical)",
                        "aiRec": "DANGER: Drain water immediately to reduce CH4.",
                        "fillColor": "#FF3D00" // แดง
                    },
                    "geometry": {
                        "type": "Polygon",
                        // หมายเหตุ: แทนที่อาร์เรย์พิกัดด้านล่างด้วยพิกัดแปลงจริงของคุณ
                        "coordinates": [[
                            [98.897000, 18.614800],
                            [98.897500, 18.614800],
                            [98.897500, 18.614300],
                            [98.897000, 18.614300],
                            [98.897000, 18.614800]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot B",
                        "management": "AWD",
                        "ndvi": "0.72",
                        "ndwi": "-0.15",
                        "soilMoisture": "45%",
                        "methaneRisk": "12.4 (Safe)",
                        "aiRec": "OPTIMAL: Maintain current dry-wet cycle.",
                        "fillColor": "#00E676" // เขียว
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [98.897600, 18.614800],
                            [98.898200, 18.614800],
                            [98.898200, 18.614300],
                            [98.897600, 18.614300],
                            [98.897600, 18.614800]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "plotName": "Plot C",
                        "management": "Control",
                        "ndvi": "0.70",
                        "ndwi": "0.10",
                        "soilMoisture": "70%",
                        "methaneRisk": "41.8 (Warning)",
                        "aiRec": "WARNING: Monitor soil moisture. Prepare for drainage.",
                        "fillColor": "#FFEA00" // เหลือง
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [98.897000, 18.614200],
                            [98.898200, 18.614200],
                            [98.898200, 18.613800],
                            [98.897000, 18.613800],
                            [98.897000, 18.614200]
                        ]]
                    }
                }
            ]
        };

        // 4. ฟังก์ชันดึงสีจาก GeoJSON Properties
        function stylePlot(feature) {
            return {
                fillColor: feature.properties.fillColor,
                weight: 2,
                opacity: 1,
                color: feature.properties.fillColor, // สีเส้นขอบ
                fillOpacity: 0.35 // ความโปร่งใสของสีพื้น
            };
        }

        // 5. ฟังก์ชันสร้าง Popup ตอนคลิกที่ Polygon (ไม่มี Marker)
        function onEachPlot(feature, layer) {
            if (feature.properties) {
                const p = feature.properties;
                
                // กำหนดสีของข้อความ Methane Risk ตามประเภท
                let methaneColorClass = "";
                if(p.management === "Flooded") methaneColorClass = "text-red";
                else if(p.management === "AWD") methaneColorClass = "text-green";
                else methaneColorClass = "text-yellow";

                // จัดหน้าตา Popup ด้วย HTML 
                const popupContent = `
                    <div class="pop-title" style="color: ${p.fillColor};">${p.plotName}</div>
                    
                    <div class="pop-item">
                        <span class="pop-label">Management:</span>
                        <span class="pop-val" style="color: ${p.fillColor};">${p.management}</span>
                    </div>
                    <div class="pop-item">
                        <span class="pop-label">NDVI:</span>
                        <span class="pop-val">${p.ndvi}</span>
                    </div>
                    <div class="pop-item">
                        <span class="pop-label">NDWI:</span>
                        <span class="pop-val">${p.ndwi}</span>
                    </div>
                    <div class="pop-item">
                        <span class="pop-label">Soil Moisture:</span>
                        <span class="pop-val">${p.soilMoisture}</span>
                    </div>
                    <div class="pop-item">
                        <span class="pop-label">Methane Risk:</span>
                        <span class="pop-val ${methaneColorClass}">${p.methaneRisk}</span>
                    </div>
                    
                    <div class="text-ai">
                        <i class="fa-solid fa-robot"></i> <b>AI Action:</b> ${p.aiRec}
                    </div>
                `;
                layer.bindPopup(popupContent);
                
                // ลูกเล่น: เอาเมาส์ไปชี้แล้วเส้นขอบสว่างขึ้น
                layer.on('mouseover', function (e) {
                    this.setStyle({ fillOpacity: 0.6, weight: 3 });
                });
                layer.on('mouseout', function (e) {
                    this.setStyle({ fillOpacity: 0.35, weight: 2 });
                });
            }
        }

        // 6. วาด GeoJSON ลงแผนที่
        L.geoJSON(ricePlotsGeoJSON, {
            style: stylePlot,
            onEachFeature: onEachPlot
        }).addTo(map);

    </script>
</body>
</html>
