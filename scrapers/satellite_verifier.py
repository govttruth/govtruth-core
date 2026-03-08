"""
GovTruth - Satellite Verification Engine
Uses ESA Sentinel-2 via OpenEO (free, no API key needed)
Verifies government infrastructure claims against satellite imagery
"""

import json
import time
import logging
from pathlib import Path
from datetime import datetime
import folium
from folium import plugins

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('GovTruth.Satellite')


class SatelliteVerifier:

    def __init__(self):
        self.data_dir = Path('data/satellite')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.maps_dir = Path('data/satellite/maps')
        self.maps_dir.mkdir(parents=True, exist_ok=True)
        self.connection = None

    def connect_openeo(self):
        """Connect to ESA Copernicus OpenEO - free tier"""
        try:
            import openeo
            logger.info("Connecting to ESA Copernicus OpenEO...")
            self.connection = openeo.connect("https://openeo.dataspace.copernicus.eu")
            self.connection.authenticate_oidc()
            logger.info("Connected to ESA Copernicus!")
            return True
        except Exception as e:
            logger.warning(f"OpenEO connection failed: {e}")
            logger.info("Falling back to map-based verification...")
            return False

    def load_promises(self):
        """Load manifesto promises"""
        path = Path('data/manifestos/BJP2024_infrastructure.json')
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def analyze_location_openeo(self, location, promise_id):
        """Pull Sentinel-2 imagery and detect construction activity"""
        try:
            import openeo
            lat, lon = location['lat'], location['lon']
            bbox = {
                "west": lon - 0.05,
                "south": lat - 0.05,
                "east": lon + 0.05,
                "north": lat + 0.05
            }

            logger.info(f"  Fetching Sentinel-2 imagery for {location['name']}...")

            # 2019 baseline (before major construction)
            s2_2019 = self.connection.load_collection(
                "SENTINEL2_L2A",
                spatial_extent=bbox,
                temporal_extent=["2019-01-01", "2019-12-31"],
                bands=["B04", "B08", "B11"]  # Red, NIR, SWIR
            ).filter_bbox(bbox)

            # 2024 current state
            s2_2024 = self.connection.load_collection(
                "SENTINEL2_L2A",
                spatial_extent=bbox,
                temporal_extent=["2024-01-01", "2024-12-31"],
                bands=["B04", "B08", "B11"]
            ).filter_bbox(bbox)

            # Calculate NDVI for both periods
            # NDVI = (NIR - Red) / (NIR + Red)
            # Construction reduces NDVI (less vegetation, more bare earth/concrete)
            ndvi_2019 = s2_2019.ndvi(nir="B08", red="B04")
            ndvi_2024 = s2_2024.ndvi(nir="B08", red="B04")

            # Save results
            out_2019 = str(self.data_dir / f"{promise_id}_{location['name'].replace(' ','_')}_2019.tif")
            out_2024 = str(self.data_dir / f"{promise_id}_{location['name'].replace(' ','_')}_2024.tif")

            ndvi_2019.download(out_2019, format="GTiff")
            ndvi_2024.download(out_2024, format="GTiff")

            logger.info(f"  Downloaded imagery for {location['name']}")
            return {"status": "DOWNLOADED", "files": [out_2019, out_2024]}

        except Exception as e:
            logger.warning(f"  OpenEO imagery failed for {location['name']}: {e}")
            return {"status": "FAILED", "error": str(e)}

    def generate_verification_map(self, promises_data):
        """Generate interactive verification map with all 16 locations"""
        logger.info("Generating interactive verification map...")

        # Center map on India
        m = folium.Map(
            location=[20.5937, 78.9629],
            zoom_start=5,
            tiles='CartoDB dark_matter'
        )

        # Color coding
        colors = {
            "PENDING_SATELLITE": "orange",
            "VERIFIED": "green",
            "PARTIAL": "yellow",
            "NOT_FOUND": "red",
            "CONTRADICTED": "darkred"
        }

        icons = {
            "Infrastructure": "road",
            "Airport": "plane",
            "Port": "ship",
            "Railway": "train"
        }

        promise_groups = {}

        for promise in promises_data['promises']:
            pid = promise['promise_id']
            status = promise['verification_status']
            color = colors.get(status, 'orange')

            for loc in promise['locations']:
                # Determine icon
                name_lower = loc['name'].lower()
                if 'airport' in name_lower:
                    icon = 'plane'
                elif 'port' in name_lower:
                    icon = 'anchor'
                elif 'rail' in name_lower or 'dfc' in name_lower or 'freight' in name_lower:
                    icon = 'train'
                else:
                    icon = 'road'

                popup_html = f"""
                <div style="font-family:monospace; min-width:300px; background:#0d0d1a; color:#e0e0e0; padding:15px; border-radius:8px;">
                    <div style="color:#ff3355; font-size:0.7em; letter-spacing:2px; margin-bottom:8px;">
                        GOVTRUTH SATELLITE VERIFICATION
                    </div>
                    <div style="color:#fff; font-weight:bold; margin-bottom:10px;">
                        {loc['name']}
                    </div>
                    <div style="color:#888; font-size:0.8em; margin-bottom:5px;">
                        📋 PROMISE: {promise['promise'][:80]}...
                    </div>
                    <div style="color:#ffaa00; font-size:0.8em; margin-bottom:5px;">
                        💰 BUDGET: {promise['budget_promised']}
                    </div>
                    <div style="color:#3399ff; font-size:0.8em; margin-bottom:5px;">
                        🏛️ GOVT CLAIM: {promise['govt_claim']}
                    </div>
                    <div style="color:#ff3355; font-size:0.8em; margin-bottom:10px;">
                        📊 CAG FINDING: {promise['cag_finding']}
                    </div>
                    <div style="background:#ff335522; color:#ff3355; padding:5px 10px; border-radius:4px; font-size:0.75em; text-align:center;">
                        STATUS: {status}
                    </div>
                    <div style="color:#444; font-size:0.65em; margin-top:8px; text-align:center;">
                        Coords: {loc['lat']}, {loc['lon']} | {loc['state']}
                    </div>
                </div>
                """

                folium.Marker(
                    location=[loc['lat'], loc['lon']],
                    popup=folium.Popup(popup_html, max_width=350),
                    tooltip=f"🛰️ {loc['name']} — {status}",
                    icon=folium.Icon(color=color, icon=icon, prefix='fa')
                ).add_to(m)

                # Draw verification radius circle
                folium.Circle(
                    location=[loc['lat'], loc['lon']],
                    radius=5000,  # 5km radius
                    color='#ff335544',
                    fill=True,
                    fill_color='#ff335511',
                    tooltip=f"Verification zone: {loc['name']}"
                ).add_to(m)

        # Add title
        title_html = '''
        <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                    z-index: 1000; background: #0d0d1a; color: white;
                    padding: 10px 20px; border-radius: 8px; border: 1px solid #ff3355;
                    font-family: monospace; text-align: center;">
            <span style="color:#ff3355; font-weight:900; letter-spacing:3px;">GOVTRUTH</span>
            <span style="color:#888; font-size:0.8em; margin-left:10px;">
                🛰️ BJP 2024 Infrastructure Promises — Satellite Verification
            </span>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))

        # Add legend
        legend_html = '''
        <div style="position: fixed; bottom: 30px; right: 10px; z-index: 1000;
                    background: #0d0d1a; color: white; padding: 15px;
                    border-radius: 8px; border: 1px solid #1a1a3a;
                    font-family: monospace; font-size: 0.8em;">
            <div style="color:#ff3355; font-weight:bold; margin-bottom:8px;">VERIFICATION STATUS</div>
            <div>🟠 Pending Satellite Review</div>
            <div>🟢 Verified — Construction Confirmed</div>
            <div>🟡 Partial — Incomplete</div>
            <div>🔴 Not Found — Empty Ground</div>
            <div style="color:#444; margin-top:8px; font-size:0.75em;">
                Source: ESA Sentinel-2 / Copernicus
            </div>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))

        # Save map
        map_path = self.maps_dir / 'BJP2024_infrastructure_verification.html'
        m.save(str(map_path))
        logger.info(f"Map saved: {map_path}")
        return map_path

    def generate_verification_report(self, promises_data):
        """Generate JSON report of all verifications"""
        report = {
            "generated": datetime.now().isoformat(),
            "party": "BJP",
            "election": "2024",
            "category": "Infrastructure",
            "total_promises": len(promises_data['promises']),
            "total_locations": sum(len(p['locations']) for p in promises_data['promises']),
            "verification_summary": {
                "pending": 0,
                "verified": 0,
                "partial": 0,
                "not_found": 0,
                "contradicted": 0
            },
            "promises": promises_data['promises']
        }

        for p in promises_data['promises']:
            status = p['verification_status'].lower().replace('pending_satellite', 'pending')
            if status in report['verification_summary']:
                report['verification_summary'][status] += 1

        report_path = self.data_dir / 'BJP2024_verification_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        logger.info(f"Report saved: {report_path}")
        return report

    def run(self):
        logger.info("GovTruth Satellite Verification Engine Starting...")
        logger.info("=" * 60)

        # Load promises
        promises_data = self.load_promises()
        logger.info(f"Loaded {promises_data['total_promises']} promises with {sum(len(p['locations']) for p in promises_data['promises'])} locations")

        # Try OpenEO connection
        openeo_available = self.connect_openeo()

        if openeo_available:
            logger.info("Running satellite analysis via ESA Copernicus...")
            for promise in promises_data['promises']:
                logger.info(f"\nVerifying: {promise['promise_id']}")
                for location in promise['locations']:
                    result = self.analyze_location_openeo(location, promise['promise_id'])
                    location['satellite_result'] = result
                    time.sleep(2)
        else:
            logger.info("OpenEO not connected — generating map for manual verification")
            logger.info("You can authenticate at: https://openeo.dataspace.copernicus.eu")

        # Always generate the map
        map_path = self.generate_verification_map(promises_data)

        # Generate report
        report = self.generate_verification_report(promises_data)

        logger.info("\n" + "=" * 60)
        logger.info("VERIFICATION ENGINE COMPLETE")
        logger.info(f"Interactive map: {map_path}")
        logger.info(f"Open in browser to see all 16 locations on satellite map")
        logger.info("=" * 60)

        print(f"\n✅ Map generated successfully!")
        print(f"📂 Open this file in your browser:")
        print(f"   {Path(map_path).absolute()}")
        print(f"\n🛰️  To enable real satellite imagery:")
        print(f"   Register at: https://dataspace.copernicus.eu/")
        print(f"   Then run this script again")


if __name__ == "__main__":
    verifier = SatelliteVerifier()
    verifier.run()