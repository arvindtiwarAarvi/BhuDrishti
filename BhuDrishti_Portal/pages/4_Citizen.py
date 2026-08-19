import streamlit as st
import folium
from streamlit_folium import st_folium

from extract import get_plot_coordinates
from geo_utils import create_geodataframe, get_centroid, get_area_sqm
from fertility_water import estimate_fertility, detect_water_resources
from ai_report import generate_ai_report
from blockchain_module import lock_on_chain, verify_record
from aasia import summarize_page, summarize_result

st.set_page_config(page_title="Citizen Desk | BhuDrishti", layout="wide")
st.title("👤 Citizen Desk")
st.caption("Simple plot check · Satellite view · Lock & Verify")

if "cit" not in st.session_state:
    st.session_state.cit = None
if "cit_map" not in st.session_state:
    st.session_state.cit_map = None

c1, c2, c3, c4 = st.columns(4)
with c1:
    district = st.text_input("District", "Prayagraj", key="c_d")
with c2:
    tehsil = st.text_input("Tehsil", "Koraon", key="c_t")
with c3:
    village = st.text_input("Village", "Koodar", key="c_v")
with c4:
    plot_no = st.text_input("Plot No", "30", key="c_p")

if st.button("Analyze My Plot", type="primary", use_container_width=True):
    coords = get_plot_coordinates(district, tehsil, village, plot_no)
    gdf = create_geodataframe(coords, plot_no)
    area = get_area_sqm(gdf)
    lat, lon = get_centroid(gdf)
    fert = estimate_fertility(coords)
    water = detect_water_resources(coords)
    report = generate_ai_report(plot_no, fert, water)
    latlon = [[a, b] for b, a in coords]
    m = folium.Map(
        location=[lat, lon], zoom_start=18,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
    )
    folium.Polygon(latlon, color="red", weight=3, fill=True, fill_color="yellow", fill_opacity=0.35).add_to(m)
    st.session_state.cit = {
        "district": district, "tehsil": tehsil, "village": village, "plot_no": plot_no,
        "coords": coords, "area": area, "report": report, "fert": fert, "water": water,
    }
    st.session_state.cit_map = m

if st.session_state.cit:
    r = st.session_state.cit
    st.success(f"Plot {r['plot_no']} · {r['village']} · {r['area']:,.0f} sq.m")
    left, right = st.columns([1.2, 1])
    with left:
        if st.session_state.cit_map is not None:
            st_folium(st.session_state.cit_map, height=380, key="cit_map")
    with right:
        if isinstance(r["report"], dict):
            st.write(r["report"].get("summary", ""))
        if isinstance(r["fert"], dict):
            st.info(f"Fertility: {r['fert'].get('level', '-')}")
        if isinstance(r["water"], dict):
            st.write(f"Water: {r['water'].get('nearby_water', '-')}")

    summary = r["report"].get("summary", "") if isinstance(r["report"], dict) else str(r["report"])
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Lock on Chain", use_container_width=True):
            locked = lock_on_chain(r["district"], r["tehsil"], r["village"], r["plot_no"], r["coords"], r["area"], summary)
            st.code(locked.get("hash", ""))
            st.success(summarize_result("lock", locked))
    with b2:
        if st.button("Verify Authenticity", use_container_width=True):
            v = verify_record(r["district"], r["tehsil"], r["village"], r["plot_no"], r["coords"], r["area"], summary)
            if v.get("authentic"):
                st.success(summarize_result("verify", v))
            else:
                st.error(summarize_result("verify", v))

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Citizen page"):
    st.success(summarize_page("Citizen"))
