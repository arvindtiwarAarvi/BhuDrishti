import streamlit as st
from extract import get_plot_coordinates
from geo_utils import create_geodataframe, get_centroid, get_area_sqm
from ai_report import generate_ai_report
from fertility_water import estimate_fertility, detect_water_resources
from blockchain_module import lock_on_chain, verify_record
from aasia import summarize_page, summarize_result

st.set_page_config(page_title="Real Estate | BhuDrishti", layout="wide")
st.title("🏢 Real Estate Desk")
st.caption("Plot overview · Area · Authenticity check before deal")

if "re_data" not in st.session_state:
    st.session_state.re_data = None

c1, c2, c3, c4 = st.columns(4)
with c1:
    district = st.text_input("District", "Prayagraj", key="re_d")
with c2:
    tehsil = st.text_input("Tehsil", "Koraon", key="re_t")
with c3:
    village = st.text_input("Village", "Koodar", key="re_v")
with c4:
    plot_no = st.text_input("Plot No", "30", key="re_p")

if st.button("Check Plot", type="primary", use_container_width=True):
    coords = get_plot_coordinates(district, tehsil, village, plot_no)
    gdf = create_geodataframe(coords, plot_no)
    area = get_area_sqm(gdf)
    lat, lon = get_centroid(gdf)
    fert = estimate_fertility(coords)
    water = detect_water_resources(coords)
    report = generate_ai_report(plot_no, fert, water)
    st.session_state.re_data = {
        "district": district, "tehsil": tehsil, "village": village, "plot_no": plot_no,
        "coords": coords, "area": area, "lat": lat, "lon": lon, "report": report,
    }

if st.session_state.re_data:
    r = st.session_state.re_data
    m1, m2, m3 = st.columns(3)
    m1.metric("Village", r["village"])
    m2.metric("Plot", r["plot_no"])
    m3.metric("Area", f"{r['area']:,.0f} sq.m")
    st.write(f"Centroid: **{r['lat']:.6f}, {r['lon']:.6f}**")
    if isinstance(r["report"], dict):
        st.success(r["report"].get("summary", ""))

    summary = r["report"].get("summary", "") if isinstance(r["report"], dict) else str(r["report"])
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Lock snapshot on chain", use_container_width=True):
            locked = lock_on_chain(r["district"], r["tehsil"], r["village"], r["plot_no"], r["coords"], r["area"], summary)
            st.session_state.re_lock = locked
            st.success(f"LOCKED Block #{locked.get('index')}")
            st.code(locked.get("hash", ""))
            st.info(summarize_result("lock", locked))
    with b2:
        if st.button("Verify authenticity", use_container_width=True):
            v = verify_record(r["district"], r["tehsil"], r["village"], r["plot_no"], r["coords"], r["area"], summary)
            if v.get("authentic"):
                st.success(f"AUTHENTIC — {v.get('message')}")
            else:
                st.error(f"{v.get('status')} — {v.get('message')}")
            st.info(summarize_result("verify", v))

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Real Estate page"):
    st.success(summarize_page("Real Estate"))
