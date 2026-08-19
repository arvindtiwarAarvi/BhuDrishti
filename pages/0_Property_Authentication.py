"""
BhuDrishti — Property Authentication
+ Bhunaksha details in lock
+ User-friendly ledger
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import hashlib
import json
from datetime import datetime, timezone

import streamlit as st
import folium
from streamlit_folium import st_folium

from bhunaksha_client import list_districts, list_tehsils, fetch_plot_real
from geo_utils import create_geodataframe, get_centroid, get_area_sqm
from blockchain_module import lock_on_chain, verify_record, get_ledger_summary

st.set_page_config(page_title="Property Authentication | BhuDrishti", page_icon="🔐", layout="wide")

st.markdown(
    """
<style>
.auth-hero {
  background: linear-gradient(90deg, #0a1f44, #138808);
  color: #fff !important; padding: 18px 20px; border-radius: 12px; margin-bottom: 14px;
}
.auth-hero h2, .auth-hero div { color: #fff !important; margin: 0 0 6px 0; }
.immutable {
  background: #0a1f44 !important; color: #fff !important;
  border-left: 6px solid #FF9933; padding: 14px 16px; margin: 10px 0; border-radius: 8px;
}
.immutable b { color: #ffe082 !important; }
.detail-card {
  background: #eef7ff; border: 1px solid #90caf9; border-radius: 10px;
  padding: 12px 14px; color: #0d47a1 !important; margin-bottom: 8px;
}
.demo-box {
  background: #e3f2fd; border: 2px solid #1565c0; border-radius: 12px;
  padding: 14px; color: #0d47a1 !important;
}
.lock-box {
  background: #fff3e0; border: 2px solid #ef6c00; border-radius: 12px;
  padding: 16px; color: #102a43 !important;
}
.auth-box {
  background: #e8f5e9; border: 2px solid #138808; border-radius: 12px;
  padding: 16px; color: #102a43 !important;
}
.ledger-card {
  background: #fafafa; border: 1px solid #cfd8dc; border-radius: 10px;
  padding: 12px; margin-bottom: 10px; color: #102a43 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="auth-hero">
  <h2>🔐 Property Authentication / प्लॉट प्रमाणीकरण</h2>
  <div>Live Bhunaksha details + Blockchain lock · Demo or permanent</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="immutable">
  <b>Rule:</b> Permanent LOCK ke baad snapshot (coords + area + Bhunaksha text) ka hash ledger mein rehta hai.
  Silent edit nahi. Demo mode save nahi karta. Yeh Bhulekh mutation ka legal substitute nahi hai.
</div>
""",
    unsafe_allow_html=True,
)

VALID_DEMO_IDS = {
    "LEKHPAL-001": "Lekhpal demo",
    "OFFICER-001": "Officer demo",
    "CITIZEN-001": "Citizen demo",
    "ADMIN-DEMO": "Admin demo",
}

for k in ["auth_result", "auth_chain", "auth_verify", "auth_demo", "auth_summary"]:
    if k not in st.session_state:
        st.session_state[k] = None


def build_summary(r, officer="-", purpose="-"):
    """Single canonical string for lock + verify (includes Bhunaksha details)."""
    info = (r.get("info_text") or "").strip().replace("\r\n", "\n")
    info_one_line = " | ".join([ln.strip() for ln in info.split("\n") if ln.strip()])
    return (
        f"AUTH_LOCK|officer={officer}|purpose={purpose}"
        f"|gis={r.get('gis_code')}|plot={r['plot_no']}"
        f"|village={r.get('village')}|district={r.get('district')}|tehsil={r.get('tehsil')}"
        f"|area={float(r['area']):.2f}|lat={float(r['lat']):.6f}|lon={float(r['lon']):.6f}"
        f"|source={r.get('source')}|bhunaksha={info_one_line}"
    )


def friendly_ledger(raw):
    """Convert ledger dict/list to user-friendly rows."""
    rows = []
    if raw is None:
        return rows
    if isinstance(raw, dict):
        entries = raw.get("entries") or raw.get("blocks") or raw.get("ledger") or raw.get("records")
        if entries is None and "hash" in raw:
            entries = [raw]
        if entries is None:
            # flatten key dicts
            for k, v in raw.items():
                if isinstance(v, list):
                    entries = v
                    break
            if entries is None:
                entries = [raw]
    elif isinstance(raw, list):
        entries = raw
    else:
        entries = [{"info": str(raw)}]

    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            rows.append({"#": i, "Detail": str(e)})
            continue
        rows.append({
            "#": e.get("index", e.get("block_index", i)),
            "Plot / Key": e.get("plot_key") or e.get("plot_no") or e.get("key") or "-",
            "Status": e.get("status") or e.get("message") or "LOCKED",
            "Hash (short)": str(e.get("hash") or e.get("block_hash") or e.get("current_hash") or "")[:18] + "…",
            "Time": str(e.get("time") or e.get("timestamp") or e.get("locked_at") or "-"),
        })
    return rows


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


st.markdown("### Step 1 — Live plot + Bhunaksha details")

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
        if "00895" in lab or "कोरांव" in lab:
            t_default = i
            break
    t_label = st.selectbox("Tehsil", t_labels, index=min(t_default, len(t_labels) - 1))
    t_code = tehsils[t_label]
else:
    t_code = st.text_input("Tehsil code", "00895")
    t_label = t_code

v_code = st.text_input("Village code", "163668")
v_name = st.text_input("Village name", "कूदर")
plot_no = st.text_input("Plot No", "29")

if st.button("1) Fetch Live Plot", type="primary", use_container_width=True):
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
            st.session_state.auth_result = {
                "district": d_label,
                "tehsil": t_label,
                "village": v_name or v_code,
                "plot_no": str(plot_no).strip(),
                "coords": coords,
                "area": area,
                "lat": lat,
                "lon": lon,
                "gis_code": data.get("gis_code"),
                "info_text": data.get("info_text", "") or "",
                "source": data.get("source", "UP Bhunaksha live API"),
                "bbox_utm": data.get("bbox_utm"),
            }
            st.session_state.auth_chain = None
            st.session_state.auth_verify = None
            st.session_state.auth_demo = None
            st.session_state.auth_summary = None
    except Exception as e:
        st.error(f"Fetch failed: {e}")
        st.session_state.auth_result = None

if not st.session_state.auth_result:
    st.stop()

r = st.session_state.auth_result
st.success(f"LIVE · {r['source']} · GIS `{r.get('gis_code')}`")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Village", r["village"])
m2.metric("Plot", r["plot_no"])
m3.metric("Area", f"{r['area']:,.0f} sq.m")
m4.metric("Lat", f"{r['lat']:.5f}")

# ---- Bhunaksha property details (show + later save in hash) ----
st.markdown("#### Bhunaksha property details")
st.markdown('<div class="detail-card">', unsafe_allow_html=True)
st.write(f"**GIS code:** `{r.get('gis_code')}`")
st.write(f"**District / Tehsil / Village:** {r['district']} · {r['tehsil']} · {r['village']}")
st.write(f"**Plot No:** {r['plot_no']}")
st.write(f"**Centroid:** {r['lat']:.6f}, {r['lon']:.6f}")
if r.get("bbox_utm"):
    st.write(f"**Extent (UTM):** `{r['bbox_utm']}`")
if r.get("info_text"):
    st.markdown("**Portal text (Khata / Owner / Area):**")
    st.text(r["info_text"])
else:
    st.caption("Is plot pe extra owner text empty aa sakta hai; extent + GIS phir bhi lock mein jayega.")
st.markdown("</div>", unsafe_allow_html=True)

latlon = [[la, lo] for lo, la in r["coords"]]
m = folium.Map(
    location=[r["lat"], r["lon"]],
    zoom_start=18,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
)
folium.Polygon(
    latlon, color="#0a1f44", weight=3, fill=True, fill_color="#ff9933", fill_opacity=0.35
).add_to(m)

c1, c2 = st.columns([1.3, 1])
with c1:
    st.subheader("Satellite")
    st_folium(m, height=360, key=f"auth_map_{r['plot_no']}_{r.get('gis_code')}")
with c2:
    st.subheader("Corners (in hash)")
    for i, (lo, la) in enumerate(r["coords"], 1):
        st.write(f"**P{i}:** `{la:.6f}`, `{lo:.6f}`")

# ---- DEMO ----
st.markdown("### Demo (one-time, no save)")
st.markdown('<div class="demo-box">', unsafe_allow_html=True)
if st.button("Run DEMO authenticate (no save)", use_container_width=True):
    raw = build_summary(r, officer="DEMO", purpose="demo-no-save")
    st.session_state.auth_demo = {
        "mode": "DEMO_ONLY",
        "saved": False,
        "hash": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "time": datetime.now(timezone.utc).isoformat(),
        "includes_bhunaksha": True,
        "message": "Demo OK — Bhunaksha details hashed in memory only. Not saved to ledger.",
        "preview_summary": raw[:300] + ("…" if len(raw) > 300 else ""),
    }
if st.session_state.auth_demo:
    d = st.session_state.auth_demo
    st.success(d["message"])
    st.code(d["hash"])
    st.caption(d.get("preview_summary", ""))
st.markdown("</div>", unsafe_allow_html=True)

# ---- PERMANENT LOCK ----
st.markdown("### Permanent Lock (Bhunaksha details + coords saved in hash)")
st.markdown('<div class="lock-box">', unsafe_allow_html=True)

st.markdown(
    """
**Valid demo IDs:** `LEKHPAL-001` · `OFFICER-001` · `CITIZEN-001` · `ADMIN-DEMO`
"""
)
officer = st.selectbox("Officer / User ID", ["— select —"] + list(VALID_DEMO_IDS.keys()))
purpose = st.selectbox(
    "Purpose",
    [
        "Integrity snapshot (demo)",
        "Pre-verification before mutation enquiry",
        "Citizen self-record check",
        "Officer audit trail",
    ],
)
confirm = st.checkbox("Confirm permanent append-only lock (Bhunaksha details included)")

if st.button("PERMANENT LOCK on Blockchain", type="primary", use_container_width=True):
    if officer not in VALID_DEMO_IDS:
        st.error("Sahi demo ID select karo (e.g. LEKHPAL-001).")
    elif not confirm:
        st.error("Confirmation tick karo.")
    else:
        summary = build_summary(r, officer=officer, purpose=purpose)
        st.session_state.auth_summary = summary
        st.session_state.auth_chain = lock_on_chain(
            r["district"],
            r["tehsil"],
            r["village"],
            r["plot_no"],
            r["coords"],
            r["area"],
            summary,
        )
        st.session_state.auth_verify = None

if st.session_state.auth_chain:
    ch = st.session_state.auth_chain
    st.success(ch.get("message", "LOCKED — Bhunaksha snapshot on ledger"))
    st.write("**Saved snapshot includes:** GIS, plot, area, coords, Bhunaksha info text, officer, purpose")
    with st.expander("Technical lock response"):
        st.json(ch)
    if st.session_state.auth_summary:
        with st.expander("Canonical summary (hash input)"):
            st.text(st.session_state.auth_summary)

st.markdown("</div>", unsafe_allow_html=True)

# ---- VERIFY ----
st.markdown("### Verify permanent lock")
st.markdown('<div class="auth-box">', unsafe_allow_html=True)
if st.button("VERIFY (ledger)", use_container_width=True):
    summary = st.session_state.auth_summary or build_summary(
        r, officer=officer if officer in VALID_DEMO_IDS else "verify", purpose="verify"
    )
    st.session_state.auth_verify = verify_record(
        r["district"],
        r["tehsil"],
        r["village"],
        r["plot_no"],
        r["coords"],
        r["area"],
        summary,
    )

if st.session_state.auth_verify:
    v = st.session_state.auth_verify
    ok = v.get("authentic") or str(v.get("status", "")).upper() == "AUTHENTIC"
    if ok:
        st.success(f"✅ AUTHENTIC — {v.get('message', '')}")
    else:
        st.error(f"❌ {v.get('status')} — {v.get('message', '')}")
    with st.expander("Technical verify response"):
        st.json(v)
st.markdown("</div>", unsafe_allow_html=True)

# ---- USER-FRIENDLY LEDGER ----
st.markdown("### Ledger report (user-friendly)")
try:
    raw = get_ledger_summary()
    rows = friendly_ledger(raw)
    if not rows:
        st.info("Abhi koi permanent lock nahi hai. Pehle PERMANENT LOCK karo (Demo ledger nahi likhta).")
    else:
        st.write(f"**Total records:** {len(rows)}")
        st.dataframe(rows, use_container_width=True)
        for row in rows:
            st.markdown(
                f"""
<div class="ledger-card">
  <b>#{row.get('#')}</b> &nbsp;|&nbsp; <b>Plot/Key:</b> {row.get('Plot / Key')}<br>
  <b>Status:</b> {row.get('Status')}<br>
  <b>Hash:</b> <code>{row.get('Hash (short)')}</code><br>
  <b>Time:</b> {row.get('Time')}
</div>
""",
                unsafe_allow_html=True,
            )
    with st.expander("Raw ledger (developer)"):
        st.json(raw)
except Exception as e:
    st.warning(f"Ledger load issue: {e}")

st.caption("BhuDrishti · Bhunaksha details are part of the locked snapshot · Not a Bhulekh substitute")