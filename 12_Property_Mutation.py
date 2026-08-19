"""
BhuDrishti — Property Mutation & Transfer Centre
Demo workflow inspired by Registration Act / TPA / State revenue process
NOT a legal substitute for Bhulekh / Sub-Registrar
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json
import hashlib
from datetime import datetime, timezone

import streamlit as st
import folium
from streamlit_folium import st_folium

from bhunaksha_client import list_districts, list_tehsils, fetch_plot_real
from geo_utils import create_geodataframe, get_centroid, get_area_sqm

st.set_page_config(
    page_title="Property Mutation | BhuDrishti",
    page_icon="📜",
    layout="wide",
)

st.markdown(
    """
<style>
.mut-hero {
  background: linear-gradient(90deg, #0a1f44 0%, #1565c0 50%, #138808 100%);
  color: #fff !important; padding: 18px 20px; border-radius: 12px; margin-bottom: 12px;
}
.mut-hero h2, .mut-hero div { color: #fff !important; margin: 0 0 6px 0; }
.warn {
  background: #0a1f44 !important; color: #fff !important;
  border-left: 6px solid #FF9933; padding: 12px 14px; border-radius: 8px; margin-bottom: 12px;
}
.card {
  background: #f7fafc; border: 1px solid #cbd5e1; border-radius: 10px;
  padding: 14px; margin-bottom: 10px; color: #102a43 !important;
}
.ok { background: #e8f5e9; border: 1px solid #138808; border-radius: 10px; padding: 12px; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="mut-hero">
  <h2>📜 Property Mutation & Transfer Centre</h2>
  <div>Sell · Buy · Gift · Inheritance · Lease · Partition · Status · Encumbrance · Timeline (Demo workflow)</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="warn">
  <b>Legal notice:</b> Yeh page <b>process understanding + demo integrity trail</b> ke liye hai.
  Asli mutation / registry sirf competent authority (Revenue / Sub-Registrar) + Bhulekh / Registration Act ke under hoti hai.
  BhuDrishti legal title issue / transfer nahi karta.
</div>
""",
    unsafe_allow_html=True,
)

# session stores
if "mut_plot" not in st.session_state:
    st.session_state.mut_plot = None
if "mut_timeline" not in st.session_state:
    st.session_state.mut_timeline = []  # local demo timeline (not legal registry)


def add_event(event_type, detail, meta=None):
    st.session_state.mut_timeline.insert(
        0,
        {
            "time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "type": event_type,
            "detail": detail,
            "meta": meta or {},
        },
    )


def demo_hash(obj):
    raw = json.dumps(obj, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


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


# ---------- SECTION A: LOAD PROPERTY ----------
st.markdown("### A) Property identify (Live Bhunaksha)")

districts = load_districts()
d_labels = list(districts.keys())
d_default = 0
for i, lab in enumerate(d_labels):
    if "175" in lab or "प्रयाग" in lab:
        d_default = i
        break
d_label = st.selectbox("District", d_labels, index=d_default, key="mut_d")
d_code = districts[d_label]

tehsils = load_tehsils(d_code)
if tehsils:
    t_labels = list(tehsils.keys())
    t_default = 0
    for i, lab in enumerate(t_labels):
        if "00895" in lab or "कोरांव" in lab:
            t_default = i
            break
    t_label = st.selectbox("Tehsil", t_labels, index=min(t_default, len(t_labels) - 1), key="mut_t")
    t_code = tehsils[t_label]
else:
    t_code = st.text_input("Tehsil code", "00895", key="mut_tc")
    t_label = t_code

v_code = st.text_input("Village code", "163668", key="mut_vc")
v_name = st.text_input("Village name", "कूदर", key="mut_vn")
plot_no = st.text_input("Plot No", "29", key="mut_pn")

if st.button("Load property from Bhunaksha", type="primary", use_container_width=True):
    try:
        with st.spinner("Live fetch..."):
            data = fetch_plot_real(
                str(d_code).strip(), str(t_code).strip(),
                str(v_code).strip(), str(plot_no).strip(),
            )
            coords = [[float(lo), float(la)] for lo, la in data["coordinates"]]
            gdf = create_geodataframe(coords, plot_no)
            area = get_area_sqm(gdf)
            lat, lon = get_centroid(gdf)
            parcel_id = f"{data.get('gis_code')}|{plot_no}"
            st.session_state.mut_plot = {
                "parcel_id": parcel_id,
                "district": d_label,
                "tehsil": t_label,
                "village": v_name or v_code,
                "plot_no": str(plot_no),
                "gis_code": data.get("gis_code"),
                "coords": coords,
                "area": area,
                "lat": lat,
                "lon": lon,
                "info_text": data.get("info_text") or "",
                "source": data.get("source"),
                "status": "FREE",  # FREE / UNDER_MUTATION / DISPUTED
                "encumbrances": [],
                "owners_demo": ["Current holder (from enquiry / ROR — verify offline)"],
            }
            add_event("LOAD", f"Property loaded from Bhunaksha: {parcel_id}", {"gis": data.get("gis_code")})
    except Exception as e:
        st.error(f"Load failed: {e}")

if not st.session_state.mut_plot:
    st.info("Pehle property load karo.")
    st.stop()

p = st.session_state.mut_plot

st.success(f"Parcel ID: `{p['parcel_id']}` · Status: **{p['status']}** · {p.get('source')}")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Village", p["village"])
c2.metric("Plot", p["plot_no"])
c3.metric("Area", f"{p['area']:,.0f} sq.m")
c4.metric("Status", p["status"])

with st.expander("Bhunaksha details", expanded=True):
    st.write(f"**GIS:** `{p.get('gis_code')}`")
    st.write(f"**Centroid:** {p['lat']:.6f}, {p['lon']:.6f}")
    st.text(p.get("info_text") or "(no extra owner text from portal)")

latlon = [[la, lo] for lo, la in p["coords"]]
m = folium.Map(
    location=[p["lat"], p["lon"]],
    zoom_start=18,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
)
folium.Polygon(latlon, color="#0a1f44", weight=3, fill=True, fill_color="#42a5f5", fill_opacity=0.35).add_to(m)
st_folium(m, height=320, key=f"mut_map_{p['parcel_id']}")

# ---------- SECTION B: STATUS & ENCUMBRANCE ----------
st.markdown("### B) Status flags & encumbrances")
st.markdown('<div class="card">', unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    new_status = st.selectbox(
        "Status flag",
        ["FREE", "UNDER_MUTATION", "DISPUTED"],
        index=["FREE", "UNDER_MUTATION", "DISPUTED"].index(p.get("status", "FREE")),
    )
    if st.button("Update status (demo)"):
        p["status"] = new_status
        st.session_state.mut_plot = p
        add_event("STATUS", f"Status set to {new_status}")
        st.rerun()
with col_b:
    enc = st.multiselect(
        "Encumbrances",
        ["Mortgage", "Litigation", "ROFR", "Lease active", "Court stay", "Bank lien"],
        default=p.get("encumbrances") or [],
    )
    if st.button("Save encumbrances (demo)"):
        p["encumbrances"] = enc
        st.session_state.mut_plot = p
        add_event("ENCUMBRANCE", f"Encumbrances: {', '.join(enc) if enc else 'None'}")
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION C: TRANSFER MODES ----------
st.markdown("### C) How property can move (Transfer modes)")

mode = st.selectbox(
    "Select mode",
    [
        "Sell (whole)",
        "Sell (part) — new parcel token idea",
        "Gift",
        "Inheritance",
        "Exchange",
        "Partition",
        "Release deed",
        "Lease (no ownership transfer)",
    ],
)

st.markdown('<div class="card">', unsafe_allow_html=True)
party_from = st.text_input("From party (demo name)", "Holder A")
party_to = st.text_input("To party (demo name)", "Holder B")
doc_ref = st.text_input("Document ref (sale deed / will / gift deed no.)", "DOC-DEMO-001")
notes = st.text_area("Notes / conditions", "")

part_fraction = None
if mode.startswith("Sell (part)"):
    part_fraction = st.slider("Part share (demo %)", 5, 95, 50)
    st.caption("Idea: whole sell → same property token to buyer; part sell → new token for new part (demo only).")

if mode.startswith("Lease"):
    st.info("Lease = right to use for a period · ownership transfer nahi hota.")
    lease_months = st.number_input("Lease period (months)", 1, 360, 11)
else:
    lease_months = None

if st.button("Record transfer event (demo trail)", type="primary", use_container_width=True):
    if p["status"] == "DISPUTED" and not mode.startswith("Lease"):
        st.error("Status DISPUTED hai — demo transfer block (pehle dispute clear flag).")
    else:
        event = {
            "mode": mode,
            "from": party_from,
            "to": party_to,
            "doc_ref": doc_ref,
            "notes": notes,
            "part_percent": part_fraction,
            "lease_months": lease_months,
            "parcel_id": p["parcel_id"],
            "gis_code": p.get("gis_code"),
            "plot_no": p["plot_no"],
            "area": p["area"],
            "coords_fingerprint": demo_hash(p["coords"])[:16],
        }
        event["event_hash"] = demo_hash(event)
        if not mode.startswith("Lease"):
            p["status"] = "UNDER_MUTATION"
            p["owners_demo"] = [party_to]
            st.session_state.mut_plot = p
        add_event("TRANSFER", f"{mode}: {party_from} → {party_to}", event)
        st.success("Demo event recorded in timeline (not legal mutation).")
        st.code(event["event_hash"])
st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION D: TOKEN IDEA (demo) ----------
st.markdown("### D) Two-token idea (from notebook — demo view)")
st.markdown('<div class="card">', unsafe_allow_html=True)
t1, t2 = st.columns(2)
with t1:
    st.markdown("**① Person / Entity token**")
    st.write("Individual / group / organisation identity side (private access idea).")
    person_token = st.text_input("Person token ID (demo)", "PERSON-DEMO-001")
with t2:
    st.markdown("**② Property token**")
    st.write("Parcel public-ish: owner timeline, status, dispute flag.")
    prop_token = f"PROP-{p['parcel_id']}"
    st.code(prop_token)
if st.button("Link tokens in timeline (demo)"):
    add_event(
        "TOKEN_LINK",
        f"Linked {person_token} ↔ {prop_token}",
        {"person_token": person_token, "property_token": prop_token},
    )
    st.success("Linked in demo timeline.")
st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION E: TIMELINE ----------
st.markdown("### E) History timeline (demo)")
if not st.session_state.mut_timeline:
    st.info("No events yet.")
else:
    for ev in st.session_state.mut_timeline:
        st.markdown(
            f"""
<div class="card">
  <b>{ev['type']}</b> · {ev['time']}<br>
  {ev['detail']}
</div>
""",
            unsafe_allow_html=True,
        )
        if ev.get("meta"):
            with st.expander("Event detail"):
                st.json(ev["meta"])

if st.button("Clear demo timeline"):
    st.session_state.mut_timeline = []
    st.rerun()

st.markdown("---")
st.markdown(
    """
#### Process reminder (real world)
1. Document (sale deed / gift / will…)  
2. Registration where required  
3. Mutation / Dakhil Kharij on revenue record (Bhulekh)  
4. BhuDrishti = optional **integrity snapshot** after official steps  
"""
)
st.caption("BhuDrishti Mutation Centre · Demo workflow · Not official registry")