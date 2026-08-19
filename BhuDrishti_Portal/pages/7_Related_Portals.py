import streamlit as st
from aasia import summarize_page

st.set_page_config(page_title="Related Portals | BhuDrishti", layout="wide")
st.title("🔗 Related Official Portals")
st.caption("Seedha sarkari / public services se judne ke liye links")

portals = [
    ("UP Bhulekh", "https://upbhulekh.gov.in/", "Uttar Pradesh land records (Khatauni / Khata)"),
    ("UP Bhunaksha", "https://upbhunaksha.gov.in/", "Cadastral maps / plot boundary maps"),
    ("UP Jansunwai", "https://jansunwai.up.nic.in/", "Public grievance / hearing related services"),
    ("Digital India", "https://www.digitalindia.gov.in/", "National digital governance programs"),
    ("India.gov.in", "https://www.india.gov.in/", "National government services portal"),
    ("NIC", "https://www.nic.gov.in/", "National Informatics Centre"),
]

for name, url, desc in portals:
    with st.container():
        st.subheader(name)
        st.write(desc)
        st.link_button(f"Open {name}", url, use_container_width=False)
        st.write("---")

st.info("BhuDrishti in portals ka alternative nahi hai — unke saath use karne layak support tool hai.")

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Related Portals page"):
    st.success(summarize_page("Related Portals"))
