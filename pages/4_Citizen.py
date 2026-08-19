import streamlit as st
import folium
from streamlit_folium import st_folium

from bhunaksha_client import list_districts, list_tehsils, fetch_plot_real
from geo_utils import create_geodataframe, get_centroid, get_area_sqm
from blockchain_module import lock_on_chain, verify_record, get_ledger_summary

st.set_page_config(page_title="Citizen Desk | BhuDrishti", page_icon="👥", layout="wide")
st.title("👥 नागरिक डेस्क / Citizen Desk")
st.caption("Live Bhunaksha · Map · Property Authentication (Lock + Verify)")

for k in ["cit_result", "chain_result", "verify_result"]:
    if k not in st.session_state:
        st.session_state[k] = None

@st.cache_data(ttl=3600, show_spinner=False)
def load_districts():
    try:
        items = list_districts()
        return {f"{it.get('value')} ({it.get('code')})": str(it.get("code")) for it in items}
    except Exception:
        return {"प्रयागराज (175)": "175", "आगरा (146)": "146"}

@st.cache_data(ttl=1800, show_spinner=False)
def load_tehsils(district_code: str):
    try:
        items = list_tehsils(district_code)
        return {f"{it.get('value')} ({it.get('code')})": str(it.get("code")) for it in items}
    except Exception:
        return {}

st.markdown("### 1) Plot खोजें (Live Bhunaksha)")

districts = load_districts()
d_labels = list(districts.keys())
d_default = 0
for i, lab in enumerate(d_labels):
    if "175" in lab or "प्रयाग" in lab:
        d_default = i
        break
d_label = st.selectbox("District", d_labels, index=d_default)
d_code = districts[d_label]

tehsils = load_tehsils(d_code)
if tehsils:
    t_labels = list(tehsils.keys())
    t_default = 0
    for i, lab in enumerate(t_labels):
        if "00895" in lab or "कोरांव" in lab or "कोर" in lab:
            t_default = i
            break
    t_label = st.selectbox("Tehsil", t_labels, index=min(t_default, len(t_labels) - 1))
    t_code = tehsils[t_label]
else:
    t_code = st.text_input("Tehsil code", "00895")
    t_label = t_code

v_code = st.text_input("Village code", "163668")
v_name = st.text_input("Village name", "कूदर / Koodar")
plot_no = st.text_input("Plot No", "29")

if st.button("Search LIVE", type="primary", use_container_width=True):
    try:
        with st.spinner("Bhunaksha..."):
            data = fetch_plot_real(
                str(d_code).strip(), str(t_code).strip(),
                str(v_code).strip(), str(plot_no).strip(),
            )
            coords = [[float(lo), float(la)] for lo, la in data["coordinates"]]
            gdf = create_geodataframe(coords, plot_no)
            area = get_area_sqm(gdf)
            lat, lon = get_centroid(gdf)
            st.session_state.cit_result = {
                "district": d_label,
                "tehsil": t_label,
                "village": v_name or v_code,
                "plot_no": str(plot_no),
                "coords": coords,
                "area": area,
                "lat": lat,
                "lon": lon,
                "gis_code": data.get("gis_code"),
                "info_text": data.get("info_text", ""),
                "source": data.get("source", "UP Bhunaksha live API"),
            }
            st.session_state.chain_result = None
            st.session_state.verify_result = None
    except Exception as e:
        st.error(f"Live fetch failed: {e}")
        st.session_state.cit_result = None

if st.session_state.cit_result:
    r = st.session_state.cit_result
    st.success(f"LIVE · {r['source']} · GIS `{r.get('gis_code')}`")

    c1, c2, c3 = st.columns(3)
    c1.metric("Village", r["village"])
    c2.metric("Plot", r["plot_no"])
    c3.metric("Area", f"{r['area']:,.0f} sq.m")
    st.caption(f"Centroid: {r['lat']:.6f}, {r['lon']:.6f}")

    latlon = [[la, lo] for lo, la in r["coords"]]
    m = folium.Map(
        location=[r["lat"], r["lon"]],
        zoom_start=18,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
    )
    folium.Polygon(
        latlon, color="red", weight=3, fill=True, fill_color="yellow", fill_opacity=0.35
    ).add_to(m)

    left, right = st.columns([1.3, 1])
    with left:
        st.subheader("Satellite view")
        st_folium(m, height=400, key=f"cit_map_{r['plot_no']}_{r.get('gis_code')}")
    with right:
        st.subheader("Corner Lat-Long")
        for i, (lo, la) in enumerate(r["coords"], 1):
            st.write(f"**P{i}:** `{la:.6f}`, `{lo:.6f}`")
        if r.get("info_text"):
            st.text_area("Bhunaksha info", r["info_text"], height=100)

    st.markdown("---")
    st.markdown("### 2) 🔐 Property Authentication (Highlighted)")
    st.info("Live plot data ko lock karke baad mein verify kar sakte ho.")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("Lock on Blockchain", use_container_width=True, type="primary"):
            payload = {
                "district": r["district"],
                "tehsil": r["tehsil"],
                "village": r["village"],
                "plot_no": r["plot_no"],
                "gis_code": r.get("gis_code"),
                "coords": r["coords"],
                "area": r["area"],
                "lat": r["lat"],
                "lon": r["lon"],
                "source": r.get("source"),
            }
            st.session_state.chain_result = lock_on_chain(payload)
            st.session_state.verify_result = None
    with b2:
        if st.button("Verify Authenticity", use_container_width=True):
            payload = {
                "district": r["district"],
                "tehsil": r["tehsil"],
                "village": r["village"],
                "plot_no": r["plot_no"],
                "gis_code": r.get("gis_code"),
                "coords": r["coords"],
                "area": r["area"],
                "lat": r["lat"],
                "lon": r["lon"],
                "source": r.get("source"),
            }
            st.session_state.verify_result = verify_record(payload)

    if st.session_state.chain_result:
        ch = st.session_state.chain_result
        st.success(ch.get("message", "Locked"))
        st.write(f"**Hash:** `{ch.get('hash', ch.get('block_hash', ''))}`")
        st.caption(str(ch.get("timestamp", "")))

    if st.session_state.verify_result:
        v = st.session_state.verify_result
        if v.get("authentic") or str(v.get("status", "")).upper() == "AUTHENTIC":
            st.success(f"✅ AUTHENTIC — {v.get('message', '')}")
        else:
            st.error(f"❌ {v.get('status', 'NOT AUTHENTIC')} — {v.get('message', '')}")
        with st.expander("Verify details"):
            st.json(v)

    with st.expander("Ledger summary"):
        try:
            st.json(get_ledger_summary())
        except Exception as e:
            st.write(str(e))

st.caption("Not a replacement for official Bhulekh mutation / legal title.")