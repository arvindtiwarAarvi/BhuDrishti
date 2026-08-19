import streamlit as st
from extract import get_plot_coordinates
from geo_utils import create_geodataframe, get_area_sqm
from fertility_water import estimate_fertility, detect_water_resources
from ai_report import generate_ai_report
from aasia import summarize_page

st.set_page_config(page_title="Farmers Desk | BhuDrishti", layout="wide")
st.title("🌾 Farmers Desk")
st.caption("Fertility (Upjau) · Water resources · Simple land guidance")

c1, c2, c3, c4 = st.columns(4)
with c1:
    district = st.text_input("District", "Prayagraj", key="f_d")
with c2:
    tehsil = st.text_input("Tehsil", "Koraon", key="f_t")
with c3:
    village = st.text_input("Village", "Koodar", key="f_v")
with c4:
    plot_no = st.text_input("Plot No", "30", key="f_p")

if st.button("Get Farm Insights", type="primary", use_container_width=True):
    coords = get_plot_coordinates(district, tehsil, village, plot_no)
    gdf = create_geodataframe(coords, plot_no)
    area = get_area_sqm(gdf)
    fert = estimate_fertility(coords)
    water = detect_water_resources(coords)
    report = generate_ai_report(plot_no, fert, water)

    st.success(f"Insights ready for Plot {plot_no} · Area {area:,.0f} sq.m")

    a, b = st.columns(2)
    with a:
        st.subheader("🌱 Fertility / Upjau")
        if isinstance(fert, dict):
            st.info(f"Level: **{fert.get('level', '-')}**")
            st.write(fert.get("reason", ""))
            st.caption(fert.get("ndvi_note", ""))
        else:
            st.write(fert)
    with b:
        st.subheader("💧 Water resources")
        if isinstance(water, dict):
            st.write(f"**Nearby:** {water.get('nearby_water', '-')}")
            st.write(water.get("note", ""))
            st.caption(water.get("irrigation_hint", ""))
        else:
            st.write(water)

    st.subheader("📋 Land summary")
    if isinstance(report, dict):
        st.write(f"**Land use:** {report.get('land_use', '-')}")
        st.success(report.get("summary", ""))
    st.warning("Note: These are guidance insights for awareness — not official lab certificates.")

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Farmers page"):
    st.success(summarize_page("Farmers"))
