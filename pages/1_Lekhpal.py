import streamlit as st
import folium
from streamlit_folium import st_folium

from bhunaksha_client import list_districts, list_tehsils, fetch_plot_real
from geo_utils import create_geodataframe, get_centroid, get_area_sqm, export_geojson

st.set_page_config(page_title="Lekhpal Desk | BhuDrishti", page_icon="🗺️", layout="wide")
st.title("🗺️ लेखपाल डेस्क / Lekhpal Desk")
st.caption("Direct live Bhunaksha · codes se · sample bypass")

if "lek_result" not in st.session_state:
    st.session_state.lek_result = None

@st.cache_data(ttl=3600, show_spinner=False)
def load_districts():
    try:
        items = list_districts()
        return {f"{it.get('value')} ({it.get('code')})": str(it.get("code")) for it in items}
    except Exception:
        return {"आगरा (146)": "146", "प्रयागराज (175)": "175"}

@st.cache_data(ttl=1800, show_spinner=False)
def load_tehsils(district_code: str):
    try:
        items = list_tehsils(district_code)
        return {f"{it.get('value')} ({it.get('code')})": str(it.get("code")) for it in items}
    except Exception:
        return {}

st.info("District/Tehsil dropdown Bhunaksha se. Village code + Plot zaroori. Demo codes pehle se bhare hain.")

districts = load_districts()
d_labels = list(districts.keys())
d_default = 0
for i, lab in enumerate(d_labels):
    if districts[lab] == "146":
        d_default = i
        break
d_label = st.selectbox("District", d_labels, index=d_default)
d_code = districts[d_label]

tehsils = load_tehsils(d_code)
if tehsils:
    t_labels = list(tehsils.keys())
    t_default = 0
    for i, lab in enumerate(t_labels):
        if tehsils[lab] == "00766":
            t_default = i
            break
    t_label = st.selectbox("Tehsil", t_labels, index=min(t_default, len(t_labels) - 1))
    t_code = tehsils[t_label]
else:
    t_code = st.text_input("Tehsil code", "00766")
    t_label = t_code

v_code = st.text_input("Village code", "124649")
v_name = st.text_input("Village name (display)", "अकबरपुर")
plot_no = st.text_input("Plot No", "1")

st.code(f"GIS = {d_code}{t_code}{v_code} | Plot = {plot_no}")

if st.button("Search LIVE Bhunaksha", type="primary", use_container_width=True):
    try:
        with st.spinner("Live fetch..."):
            # DIRECT live call — no extract name fallback path
            data = fetch_plot_real(
                str(d_code).strip(),
                str(t_code).strip(),
                str(v_code).strip(),
                str(plot_no).strip(),
            )
            # data["coordinates"] = [(lon, lat), ...]
            coords = [[float(lon), float(lat)] for lon, lat in data["coordinates"]]
            gdf = create_geodataframe(coords, plot_no)
            area = get_area_sqm(gdf)
            lat, lon = get_centroid(gdf)
            try:
                export_geojson(gdf, f"plot_{plot_no}.geojson")
            except Exception:
                pass

            st.session_state.lek_result = {
                "village": v_name or v_code,
                "plot_no": plot_no,
                "coords": coords,
                "area": area,
                "lat": lat,
                "lon": lon,
                "gis_code": data.get("gis_code"),
                "info_text": data.get("info_text", ""),
                "source": data.get("source", "UP Bhunaksha live API"),
                "bbox": data.get("bbox_utm"),
            }
    except Exception as e:
        st.session_state.lek_result = None
        st.error(f"Live fetch failed: {e}")

if st.session_state.lek_result:
    r = st.session_state.lek_result
    st.success(f"LIVE · {r.get('source')} · GIS `{r.get('gis_code')}`")
    st.write(f"**First corner Lon,Lat:** `{r['coords'][0]}`")
    st.caption("Live Bhunaksha extent (bbox → lat/lon). Plot badlo to numbers badalne chahiye.")
    m1, m2, m3 = st.columns(3)
    m1.metric("Village", r["village"])
    m2.metric("Plot", r["plot_no"])
    m3.metric("Area", f"{r['area']:,.0f} sq.m")

    latlon = [[lat, lon] for lon, lat in r["coords"]]
    m = folium.Map(
        location=[r["lat"], r["lon"]],
        zoom_start=18,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
    )
    folium.Polygon(
        latlon, color="red", weight=3, fill=True, fill_color="yellow", fill_opacity=0.35
    ).add_to(m)
    for i, (la, lo) in enumerate(latlon[:-1], 1):
        folium.CircleMarker(
            [la, lo], radius=4, color="white", fill=True, fill_color="red", popup=f"P{i}"
        ).add_to(m)

    left, right = st.columns([1.3, 1])
    with left:
        st.subheader("Satellite + Boundary")
        st_folium(m, height=420, key=f"map_{r['plot_no']}_{r.get('gis_code')}")
    with right:
        st.subheader("Corner Lat-Long")
        for i, (lo, la) in enumerate(r["coords"], 1):
            st.write(f"**Point {i}:** Lat `{la:.6f}` | Lon `{lo:.6f}`")
        if r.get("info_text"):
            st.text_area("Bhunaksha info", r["info_text"], height=120)

st.divider()
st.markdown("**Demo:** Village `124649` · Plot `1` / `2` / `5` — alag lat-lon aane chahiye.")