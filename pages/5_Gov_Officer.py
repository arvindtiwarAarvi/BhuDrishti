import streamlit as st
from blockchain_module import get_ledger_summary, verify_record
from extract import get_plot_coordinates
from geo_utils import create_geodataframe, get_area_sqm
from ai_report import generate_ai_report
from fertility_water import estimate_fertility, detect_water_resources
from aasia import summarize_page

st.set_page_config(page_title="Gov Officer | BhuDrishti", layout="wide")
st.title("🏛️ Government Officer Desk")
st.caption("Ledger overview · Verification support · Transparency tools")

summary = get_ledger_summary()
st.metric("Total locked records", summary.get("total_blocks", 0))

st.subheader("Recent ledger entries")
entries = summary.get("entries", [])
if not entries:
    st.info("No locked records yet. Citizens/Real Estate desks se Lock karke entries aayengi.")
else:
    for e in reversed(entries[-10:]):
        st.write(f"**Block #{e.get('index')}** | {e.get('plot_key')} | `{e.get('hash')}` | {e.get('time')}")
        st.write("---")

st.subheader("Quick verify a plot")
c1, c2, c3, c4 = st.columns(4)
with c1:
    district = st.text_input("District", "Prayagraj", key="g_d")
with c2:
    tehsil = st.text_input("Tehsil", "Koraon", key="g_t")
with c3:
    village = st.text_input("Village", "Koodar", key="g_v")
with c4:
    plot_no = st.text_input("Plot No", "30", key="g_p")

if st.button("Run verification", type="primary"):
    coords = get_plot_coordinates(district, tehsil, village, plot_no)
    gdf = create_geodataframe(coords, plot_no)
    area = get_area_sqm(gdf)
    fert = estimate_fertility(coords)
    water = detect_water_resources(coords)
    report = generate_ai_report(plot_no, fert, water)
    s = report.get("summary", "") if isinstance(report, dict) else str(report)
    v = verify_record(district, tehsil, village, plot_no, coords, area, s)
    if v.get("authentic"):
        st.success(f"AUTHENTIC — {v.get('message')}")
    else:
        st.warning(f"{v.get('status')} — {v.get('message')}")

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Officer page"):
    st.success(summarize_page("Gov Officer"))
