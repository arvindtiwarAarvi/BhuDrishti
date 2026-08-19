"""
BhuDrishti Portal — Hindi + English Home
"""

import os
import streamlit as st

ICON_PATH = os.path.join("assets", "bhudrishti_icon.png")
PAGE_ICON = ICON_PATH if os.path.exists(ICON_PATH) else "🗺️"

st.set_page_config(
    page_title="BhuDrishti | Digital Land Portal",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

if "lang" not in st.session_state:
    st.session_state["lang"] = "hi"  # default Hindi

def T(hi, en):
    return hi if st.session_state["lang"] == "hi" else en

if os.path.exists(ICON_PATH):
    st.logo(ICON_PATH, size="large")

HERO_BG = "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1600&q=80"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Noto+Sans+Devanagari:wght@400;700&display=swap');
html, body, [class*="css"] {{
  font-family: 'Noto Sans Devanagari', 'Roboto', sans-serif;
  color: #102a43 !important;
}}
.stApp {{ background: #f5f7fa !important; }}
.stMarkdown, .stMarkdown p, .stMarkdown li, .stCaption, label {{ color: #102a43 !important; }}
h1, h2, h3, h4 {{ color: #0a1f44 !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.tricolor {{
  height: 8px; width: 100%;
  background: linear-gradient(90deg, #FF9933 0%, #FF9933 33.3%, #FFFFFF 33.3%, #FFFFFF 66.6%, #138808 66.6%, #138808 100%);
}}
.topbar {{
  background: #0a1f44; color: #fff !important; padding: 12px 20px;
  display: flex; justify-content: space-between; align-items: center;
}}
.topbar .left, .topbar .right {{ color: #fff !important; font-size: 0.9rem; font-weight: 500; }}
.hero {{
  border-radius: 0 0 14px 14px; overflow: hidden; min-height: 300px;
  background:
    linear-gradient(100deg, rgba(6,20,45,0.92) 0%, rgba(6,20,45,0.82) 50%, rgba(6,20,45,0.55) 100%),
    url('{HERO_BG}');
  background-size: cover; background-position: center;
  color: #fff !important; padding: 40px 36px; margin-bottom: 20px;
  box-shadow: 0 8px 24px rgba(10,31,68,0.25);
}}
.hero * {{ color: #fff !important; }}
.hero h1 {{
  margin: 0; font-size: 2.5rem; font-weight: 700; color: #fff !important;
  text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}}
.hero .tag {{
  display: inline-block; margin-top: 8px; padding: 5px 12px;
  border: 1px solid #fff; border-radius: 20px; font-size: 0.8rem;
  background: rgba(0,0,0,0.25);
}}
.hero .sub {{
  margin-top: 12px; font-size: 1.05rem; max-width: 680px; line-height: 1.55;
  text-shadow: 0 1px 4px rgba(0,0,0,0.45);
}}
.hero .pill {{
  display: inline-block; background: rgba(255,255,255,0.2);
  border: 1px solid #fff; padding: 5px 12px; border-radius: 16px;
  margin-right: 8px; margin-bottom: 6px; font-size: 0.82rem; font-weight: 500;
}}
.section-title {{
  color: #0a1f44 !important; font-size: 1.3rem; font-weight: 700;
  margin: 10px 0 12px 0; border-left: 5px solid #FF9933; padding-left: 10px;
}}
.card {{
  background: #fff !important; border-radius: 12px; padding: 18px 16px;
  box-shadow: 0 3px 12px rgba(10,31,68,0.10); border-top: 4px solid #0a1f44;
  margin-bottom: 8px;
}}
.card h4 {{ margin: 0 0 8px 0; color: #0a1f44 !important; font-size: 1.05rem; }}
.card p {{ margin: 0; color: #243b53 !important; font-size: 0.92rem; line-height: 1.45; }}
.aasia {{
  background: #e8f5e9 !important; border-left: 5px solid #138808;
  border-radius: 10px; padding: 14px 16px; color: #102a43 !important;
}}
.footer-note {{
  text-align: center; color: #334e68 !important; font-size: 0.85rem;
  margin-top: 22px; padding: 14px; background: #fff; border-radius: 8px;
  border: 1px solid #d9e2ec;
}}
div[data-testid="stPageLink"] a {{
  display: block !important; background: #0a1f44 !important; color: #fff !important;
  padding: 10px 14px !important; border-radius: 8px !important; text-align: center !important;
  font-weight: 600 !important; border: 2px solid #0a1f44 !important; margin-top: 6px !important;
}}
div[data-testid="stPageLink"] a:hover {{
  background: #138808 !important; border-color: #138808 !important;
}}
div[data-testid="stPageLink"] span {{ color: #fff !important; }}
</style>
""",
    unsafe_allow_html=True,
)

# ---- Language toggle ----
c1, c2, c3 = st.columns([1, 1, 4])
with c1:
    if st.button("हिन्दी", use_container_width=True):
        st.session_state["lang"] = "hi"
        st.rerun()
with c2:
    if st.button("English", use_container_width=True):
        st.session_state["lang"] = "en"
        st.rerun()

st.markdown('<div class="tricolor"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
<div class="topbar">
  <div class="left">{T("भारत सरकार · सार्वजनिक सेवा पोर्टल", "GOVERNMENT OF INDIA STYLE PUBLIC SERVICE PORTAL")}</div>
  <div class="right">{T("डिजिटल भूमि जानकारी · विश्वसनीय सत्यापन", "Digital Land Intelligence · Trusted Verification")}</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="hero">
  <div class="tag">{T("सार्वजनिक डिजिटल सेवा", "PUBLIC DIGITAL SERVICE")}</div>
  <h1>BhuDrishti</h1>
  <div class="sub">
    {T(
      "ब्लॉकचेन-आधारित प्लाट प्रमाणीकरण का वर्णनात्मक विश्लेषण<br>उपग्रह दृश्य · भूमि जानकारी · हर नागरिक के लिए प्रमाणिकता जाँच",
      "A Descriptive Analysis of Blockchain-Enabled Plot Authentication<br>Satellite view · Land insights · Blockchain-style authenticity for every citizen",
    )}
  </div>
  <div style="margin-top:16px;">
    <span class="pill">{T("पारदर्शी", "Transparent")}</span>
    <span class="pill">{T("कुशल", "Efficient")}</span>
    <span class="pill">{T("नागरिक-केंद्रित", "Citizen-Centric")}</span>
    <span class="pill">{T("सुरक्षित सत्यापन", "Secure Verification")}</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

a, b = st.columns([2, 1])
with a:
    st.markdown(
        f'<div class="section-title">{T("पोर्टल में आपका स्वागत है", "Welcome to the portal")}</div>',
        unsafe_allow_html=True,
    )
    st.write(
        T(
            "BhuDrishti **नागरिकों, किसानों, लेखपालों, रियल एस्टेट उपयोगकर्ताओं और अधिकारियों** की मदद करता है — "
            "उपग्रह मानचित्र पर प्लाट सीमा देखने, भूमि की जानकारी समझने, और ब्लॉकचेन-शैली लॉक से "
            "रिकॉर्ड की प्रमाणिकता जाँचने में।",
            "BhuDrishti helps **citizens, farmers, lekhpals, real-estate users and officers** "
            "to view plot boundaries on satellite imagery, understand land context, and verify "
            "record authenticity using a blockchain-style integrity lock.",
        )
    )
with b:
    if os.path.exists(ICON_PATH):
        st.image(ICON_PATH, width=120)
    st.info(T("सुरक्षित और पारदर्शी", "Secure & Transparent"))
    st.success(T("उपग्रह-सहायता प्राप्त दृश्य", "Satellite-assisted view"))
    st.warning(T("आधिकारिक भूलेख म्यूटेशन का विकल्प नहीं", "Not a replacement for official Bhulekh mutation"))

st.markdown(
    f'<div class="section-title">{T("अपना डेस्क चुनें", "Select your desk")}</div>',
    unsafe_allow_html=True,
)

r1c1, r1c2, r1c3 = st.columns(3)
st.page_link(
    "pages/0_Property_Authentication.py",
    label="🔐 Property Authentication (Main) →",
    icon="🔐",
)
st.write("")
with r1c1:
    st.markdown(
        f'<div class="card"><h4>🗺️ {T("लेखपाल डेस्क", "Lekhpal Desk")}</h4>'
        f'<p>{T("उपग्रह मानचित्र, प्लाट खोज, हर कोने का Lat-Long।", "Satellite map, property search, every corner Lat-Long.")}</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Lekhpal.py", label=T("लेखपाल डेस्क खोलें →", "Open Lekhpal Desk →"), icon="🗺️")
with r1c2:
    st.markdown(
        f'<div class="card"><h4>🌿 {T("किसान डेस्क", "Farmers Desk")}</h4>'
        f'<p>{T("उर्वरता (उपजाऊ), जल संसाधन और खेत मार्गदर्शन।", "Fertility (Upjau), water resources and field guidance.")}</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Farmers.py", label=T("किसान डेस्क खोलें →", "Open Farmers Desk →"), icon="🌿")
with r1c3:
    st.markdown(
        f'<div class="card"><h4>🏠 {T("रियल एस्टेट", "Real Estate")}</h4>'
        f'<p>{T("क्षेत्रफल, स्थान सारांश और प्रमाणिकता जाँच।", "Plot area, location summary and authenticity check.")}</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/3_Real_Estate.py", label=T("रियल एस्टेट खोलें →", "Open Real Estate Desk →"), icon="🏠")

r2c1, r2c2, r2c3 = st.columns(3)
with r2c1:
    st.markdown(
        f'<div class="card"><h4>👥 {T("नागरिक डेस्क", "Citizen Desk")}</h4>'
        f'<p>{T("सरल प्लाट जाँच, लॉक और सत्यापन।", "Simple plot check, lock and verify for everyone.")}</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/4_Citizen.py", label=T("नागरिक डेस्क खोलें →", "Open Citizen Desk →"), icon="👥")
with r2c2:
    st.markdown(
        f'<div class="card"><h4>🏛️ {T("सरकारी अधिकारी", "Gov Officer")}</h4>'
        f'<p>{T("लेजर अवलोकन और सत्यापन सहायता।", "Ledger overview and verification support tools.")}</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/5_Gov_Officer.py", label=T("अधिकारी डेस्क खोलें →", "Open Officer Desk →"), icon="🏛️")
with r2c3:
    st.markdown(
        f'<div class="card"><h4>📊 {T("डेटाबेस", "Database")}</h4>'
        f'<p>{T("लॉक रिकॉर्ड, हैश इतिहास और ऑडिट ट्रेल।", "Locked records, hash history and audit trail.")}</p></div>',
        unsafe_allow_html=True,
    )
    st.page_link("pages/9_Database.py", label=T("डेटाबेस खोलें →", "Open Database →"), icon="📊")

st.write("")
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.page_link("pages/10_Dashboard.py", label=T("डैशबोर्ड →", "Dashboard →"), icon="📋")
with m2:
    st.page_link("pages/6_Feedback.py", label=T("प्रतिक्रिया →", "Feedback →"), icon="📝")
with m3:
    st.page_link("pages/7_Related_Portals.py", label=T("संबंधित पोर्टल →", "Related Portals →"), icon="🌐")
with m4:
    st.page_link("pages/8_About_Team.py", label=T("टीम के बारे में →", "About Team →"), icon="ℹ️")

# AASIA
st.markdown(
    f'<div class="section-title">{T("आसिया सहायक", "AASIA Assistant")}</div>',
    unsafe_allow_html=True,
)
st.caption(
    T(
        "स्थानिक और अखंडता विश्लेषण के लिए स्वचालित सहायता",
        "Automated Assistance for Spatial & Integrity Analysis",
    )
)

from aasia import summarize_page

if "aasia_home_msg" not in st.session_state:
    st.session_state["aasia_home_msg"] = ""

if st.button(T("इस पृष्ठ का सारांश", "Summarize this page"), use_container_width=True):
    st.session_state["aasia_home_msg"] = summarize_page("Home")

user_q = st.text_input(
    T("या आसिया से पूछें / खोजें", "Or ask / search with AASIA"),
    placeholder=T(
        "उदाहरण: लेखपाल डेस्क क्या करता है? उर्वरता क्या है?",
        "Example: what does lekhpal desk do? what is fertility?",
    ),
)

if st.button(T("आसिया से पूछें", "Ask AASIA"), type="primary", use_container_width=True):
    q = (user_q or "").strip().lower()
    if not q:
        st.session_state["aasia_home_msg"] = T("कृपया अपना प्रश्न लिखें।", "Please type your question.")
    elif "lekhpal" in q or "लेखपाल" in q or "lat" in q or "satellite" in q:
        st.session_state["aasia_home_msg"] = summarize_page("Lekhpal")
    elif "farmer" in q or "किसान" in q or "fertility" in q or "उपजाऊ" in q or "water" in q:
        st.session_state["aasia_home_msg"] = summarize_page("Farmers")
    elif "real" in q or "estate" in q or "रियल" in q:
        st.session_state["aasia_home_msg"] = summarize_page("Real Estate")
    elif "citizen" in q or "नागरिक" in q or "verify" in q or "blockchain" in q:
        st.session_state["aasia_home_msg"] = summarize_page("Citizen")
    elif "officer" in q or "अधिकारी" in q or "ledger" in q:
        st.session_state["aasia_home_msg"] = summarize_page("Gov Officer")
    elif "bhulekh" in q or "bhunaksha" in q or "भूलेख" in q or "भूनक्शा" in q:
        st.session_state["aasia_home_msg"] = summarize_page("Related Portals")
    elif "about" in q or "team" in q or "टीम" in q:
        st.session_state["aasia_home_msg"] = summarize_page("About")
    elif "database" in q or "डेटाबेस" in q or "hash" in q:
        st.session_state["aasia_home_msg"] = summarize_page("Database")
    else:
        st.session_state["aasia_home_msg"] = T(
            "आसिया: मैं BhuDrishti पोर्टल गाइड हूँ। लेखपाल, किसान, नागरिक, ब्लॉकचेन, भूलेख आदि के बारे में पूछ सकते हैं।",
            "AASIA: I guide the BhuDrishti portal. Ask about Lekhpal, Farmers, Citizen, Blockchain, Bhulekh, etc.",
        )

if st.session_state.get("aasia_home_msg"):
    st.markdown(
        f'<div class="aasia"><b>AASIA:</b><br>{st.session_state["aasia_home_msg"]}</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
<div class="footer-note">
  {T(
    "BhuDrishti · डिजिटल भूमि जानकारी पोर्टल · जन जागरूकता और सत्यापन सहायता<br>आधिकारिक भूलेख / म्यूटेशन प्रणाली का विकल्प नहीं",
    "BhuDrishti · Digital Land Intelligence Portal · Public awareness & verification support<br>Not a substitute for official Bhulekh / mutation systems",
  )}
</div>
""",
    unsafe_allow_html=True,
)