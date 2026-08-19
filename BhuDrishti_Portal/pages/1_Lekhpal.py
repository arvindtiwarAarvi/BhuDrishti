import streamlit as st
import folium
from streamlit_folium import st_folium

from extract import get_plot_coordinates
from geo_utils import create_geodataframe, get_centroid, get_area_sqm, export_geojson
from aasia import summarize_page, summarize_result

st.set_page_config(page_title="Lekhpal Desk | BhuDrishti", layout="wide")
st.title("🛰️ Lekhpal Desk")
st.caption("Satellite view · Plot boundary · Corner Lat-Long")

if "lek_result" not in st.session_state:
    st.session_state.lek_result = None
if "lek_map" not in st.session_state:
    st.session_state.lek_map = None

c1, c2, c3, c4 = st.columns(4)
with c1:
    district = st.text_input("District", "Prayagraj")
with c2:
    tehsil = st.text_input("Tehsil", "Koraon")
with c3:
    village = st.text_input("Village", "Koodar")
with c4:
    plot_no = st.text_input("Plot No", "30")

if st.button("Search Property", type="primary", use_container_width=True):
    with st.spinner("Loading plot..."):
        coords = get_plot_coordinates(district, tehsil, village, plot_no)
        gdf = create_geodataframe(coords, plot_no)
        area = get_area_sqm(gdf)
        lat, lon = get_centroid(gdf)
        export_geojson(gdf, f"plot_{plot_no}.geojson")

        latlon = [[a, b] for b, a in coords]
        m = folium.Map(
            location=[lat, lon],
            zoom_start=18,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri",
        )
        folium.Polygon(
            locations=latlon, color="red", weight=3, fill=True,
            fill_color="yellow", fill_opacity=0.35, popup=f"Plot {plot_no}",
        ).add_to(m)
        for i, (la, lo) in enumerate(latlon[:-1], 1):
            folium.CircleMarker([la, lo], radius=4, color="white", fill=True,
                                fill_color="red", popup=f"P{i}").add_to(m)

        st.session_state.lek_result = {
            "district": district, "tehsil": tehsil, "village": village,
            "plot_no": plot_no, "coords": coords, "area": area, "lat": lat, "lon": lon,
        }
        st.session_state.lek_map = m

if st.session_state.lek_result:
    r = st.session_state.lek_result
    m1, m2, m3 = st.columns(3)
    m1.metric("Location", f"{r['village']}, {r['tehsil']}")
    m2.metric("Plot", r["plot_no"])
    m3.metric("Area", f"{r['area']:,.0f} sq.m")

    left, right = st.columns([1.3, 1])
    with left:
        st.subheader("Satellite + Boundary")
        if st.session_state.lek_map is not None:
            st_folium(st.session_state.lek_map, height=420, key="lek_map")
    with right:
        st.subheader("Corner Lat-Long")
        for i, (lo, la) in enumerate(r["coords"], 1):
            st.write(f"**Point {i}:** Lat `{la}` | Lon `{lo}`")
        st.caption(f"Centroid: {r['lat']:.6f}, {r['lon']:.6f}")

    st.info(summarize_result("analyze", r))

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Lekhpal page"):
    st.success(summarize_page("Lekhpal"))
