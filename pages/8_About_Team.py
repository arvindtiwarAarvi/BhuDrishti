import streamlit as st
from aasia import summarize_page

st.set_page_config(page_title="About | BhuDrishti", layout="wide")
st.title("👥 About BhuDrishti")
st.caption("Mission · Problem · Team")

st.markdown(
    """
### Mission
**BhuDrishti: A Descriptive Analysis of Blockchain-Enabled Plot Authentication**

BhuDrishti ka aim hai land plot ko **dikhana, samjhana aur verify** karna —
satellite context + descriptive insights + blockchain-style integrity ke saath.

### Problem focus (SIH PS-28 aligned)
Land records aksar fragmented ya tamper-prone hote hain. BhuDrishti:
- plot boundary + satellite view deta hai
- simple land insights (fertility/water/AI summary) deta hai
- snapshot ko hash karke lock/verify karta hai

### Who can use
- **Citizens** — basic plot check
- **Farmers** — field insights
- **Lekhpal** — boundary + coordinates
- **Real Estate** — pre-deal overview
- **Gov Officers** — ledger / verification support

### Important note
Yeh portal awareness aur verification-support ke liye hai.
Official ownership / mutation ke liye state revenue systems (jaise Bhulekh) hi authoritative hain.
"""
)

st.subheader("Team")
st.write("**Lead / Documentation:** ARVIND KUMAR TIWARI")
st.write("B.Tech 2nd year CSE (AI/ML)")
st.write("Team members: (names yahan add karein)")

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize About page"):
    st.success(summarize_page("About"))
