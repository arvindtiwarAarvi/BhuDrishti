"""
BhuDrishti Portal — Home
Government-style multi-user land intelligence portal
"""

import streamlit as st

st.set_page_config(
    page_title="BhuDrishti Portal",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- GOI-inspired CSS ----
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

html, body, [class*="css"] {
  font-family: 'Roboto', sans-serif;
}
.stApp {
  background: linear-gradient(180deg, #0b1f3a 0%, #0b1f3a 120px, #f4f7fb 120px, #f4f7fb 100%);
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.goi-header {
  background: linear-gradient(90deg, #ff9933 0%, #ff9933 33%, #ffffff 33%, #ffffff 66%, #138808 66%, #138808 100%);
  height: 6px;
  width: 100%;
  margin-bottom: 0;
}
.navy-bar {
  background: #0b1f3a;
  color: white;
  padding: 12px 18px;
  border-radius: 0 0 8px 8px;
  margin-bottom: 18px;
}
.navy-bar h1 {
  margin: 0;
  font-size: 1.8rem;
  letter-spacing: 0.5px;
}
.navy-bar p {
  margin: 4px 0 0 0;
  opacity: 0.9;
  font-size: 0.95rem;
}
.hero-card {
  background: white;
  border: 1px solid #d9e2ec;
  border-radius: 12px;
  padding: 22px;
  box-shadow: 0 4px 14px rgba(11,31,58,0.08);
}
.service-card {
  background: white;
  border-top: 4px solid #0b1f3a;
  border-radius: 10px;
  padding: 16px;
  height: 100%;
  box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.service-card h4 { margin: 0 0 8px 0; color: #0b1f3a; }
.service-card p { margin: 0; color: #445; font-size: 0.9rem; }
.aasia-box {
  background: linear-gradient(135deg, #e8f5e9, #e3f2fd);
  border-left: 5px solid #138808;
  border-radius: 10px;
  padding: 14px 16px;
  margin-top: 12px;
}
.badge {
  display: inline-block;
  background: #0b1f3a;
  color: white;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  margin-right: 6px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="goi-header"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="navy-bar">
  <h1>🗺️ BhuDrishti</h1>
  <p>A Descriptive Analysis of Blockchain-Enabled Plot Authentication · Digital Land Intelligence Portal</p>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([2.2, 1])

with left:
    st.markdown(
        """
<div class="hero-card">
  <span class="badge">PUBLIC SERVICE</span>
  <span class="badge">TRANSPARENT</span>
  <span class="badge">SECURE</span>
  <h2 style="color:#0b1f3a;margin-top:12px;">Land Intelligence for Every Citizen</h2>
  <p style="color:#334;line-height:1.55;">
    BhuDrishti helps citizens, farmers, lekhpals, real-estate users and officers
    view plot boundaries on satellite imagery, understand land context, and
    verify record authenticity using blockchain-style integrity checks.
  </p>
  <p style="color:#334;"><b>Transparent · Efficient · Citizen-Centric Land Services</b></p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")
    st.subheader("Select your desk")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """<div class="service-card"><h4>Lekhpal Desk</h4>
            <p>Satellite view, plot search, corner Lat-Long.</p></div>""",
            unsafe_allow_html=True,
        )
        st.page_link("pages/1_Lekhpal.py", label="Open Lekhpal", icon="🛰️")
    with c2:
        st.markdown(
            """<div class="service-card"><h4>Farmers Desk</h4>
            <p>Fertility, water resources, field insights.</p></div>""",
            unsafe_allow_html=True,
        )
        st.page_link("pages/2_Farmers.py", label="Open Farmers", icon="🌾")
    with c3:
        st.markdown(
            """<div class="service-card"><h4>Real Estate</h4>
            <p>Plot area, location, authenticity check.</p></div>""",
            unsafe_allow_html=True,
        )
        st.page_link("pages/3_Real_Estate.py", label="Open Real Estate", icon="🏢")

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown(
            """<div class="service-card"><h4>Citizen Desk</h4>
            <p>Simple plot check + blockchain verify.</p></div>""",
            unsafe_allow_html=True,
        )
        st.page_link("pages/4_Citizen.py", label="Open Citizen", icon="👤")
    with c5:
        st.markdown(
            """<div class="service-card"><h4>Gov Officer</h4>
            <p>Ledger overview & verification support.</p></div>""",
            unsafe_allow_html=True,
        )
        st.page_link("pages/5_Gov_Officer.py", label="Open Officer", icon="🏛️")
    with c6:
        st.markdown(
            """<div class="service-card"><h4>Database</h4>
            <p>Locked records & hash history.</p></div>""",
            unsafe_allow_html=True,
        )
        st.page_link("pages/9_Database.py", label="Open Database", icon="🗄️")

    st.write("")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.page_link("pages/6_Feedback.py", label="Feedback", icon="💬")
    with d2:
        st.page_link("pages/7_Related_Portals.py", label="Related Portals", icon="🔗")
    with d3:
        st.page_link("pages/8_About_Team.py", label="About Team", icon="👥")
    st.page_link("pages/10_Dashboard.py", label="User Dashboard", icon="📋")

with right:
    st.markdown("### 🇮🇳 Portal highlights")
    st.info("Secure & Transparent land snapshot")
    st.info("Satellite-assisted boundary view")
    st.info("Blockchain-style authenticity lock")
    st.success("Enter any desk from the left menu")

    # AASIA
    st.markdown("### 🤖 AASIA")
    st.caption("Automated Assistance for Spatial & Integrity Analysis")
    if st.button("Summarize this page", key="aasia_home"):
        from aasia import summarize_page
        st.markdown(
            f'<div class="aasia-box"><b>AASIA says:</b><br>{summarize_page("Home")}</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption("BhuDrishti · Digital Land Intelligence · For public awareness & verification support · Not a replacement for official revenue mutation")
