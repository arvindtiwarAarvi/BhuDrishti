import streamlit as st
from blockchain_module import get_ledger_summary
from aasia import summarize_page

st.set_page_config(page_title="Dashboard | BhuDrishti", layout="wide")
st.title("📋 User Dashboard")
st.caption("Profile · Quick links · Activity snapshot")

# Simple local profile (demo)
if "profile" not in st.session_state:
    st.session_state.profile = {"name": "", "role": "Citizen", "district": "Prayagraj"}

with st.form("profile_form"):
    name = st.text_input("Your name", st.session_state.profile.get("name", ""))
    role = st.selectbox(
        "Preferred desk",
        ["Citizen", "Farmer", "Lekhpal", "Real Estate", "Gov Officer"],
        index=["Citizen", "Farmer", "Lekhpal", "Real Estate", "Gov Officer"].index(
            st.session_state.profile.get("role", "Citizen")
        ),
    )
    district = st.text_input("Home district", st.session_state.profile.get("district", "Prayagraj"))
    if st.form_submit_button("Save profile"):
        st.session_state.profile = {"name": name, "role": role, "district": district}
        st.success("Profile saved (this browser session)")

p = st.session_state.profile
st.info(f"Welcome **{p.get('name') or 'User'}** · Role: **{p.get('role')}** · District: **{p.get('district')}**")

st.subheader("Quick links")
c1, c2, c3 = st.columns(3)
with c1:
    st.page_link("pages/1_Lekhpal.py", label="Lekhpal Desk", icon="🛰️")
    st.page_link("pages/2_Farmers.py", label="Farmers Desk", icon="🌾")
with c2:
    st.page_link("pages/3_Real_Estate.py", label="Real Estate", icon="🏢")
    st.page_link("pages/4_Citizen.py", label="Citizen Desk", icon="👤")
with c3:
    st.page_link("pages/5_Gov_Officer.py", label="Gov Officer", icon="🏛️")
    st.page_link("pages/9_Database.py", label="Database", icon="🗄️")

st.subheader("Activity snapshot")
ledger = get_ledger_summary()
st.write(f"Locked records in system: **{ledger.get('total_blocks', 0)}**")
entries = ledger.get("entries", [])
if entries:
    last = entries[-1]
    st.write(f"Last lock: Block #{last.get('index')} · {last.get('plot_key')} · {last.get('time')}")

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Dashboard"):
    st.success(summarize_page("Dashboard"))
