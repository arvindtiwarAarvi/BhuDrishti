import streamlit as st
from blockchain_module import get_ledger_summary
from aasia import summarize_page

st.set_page_config(page_title="Database | BhuDrishti", layout="wide")
st.title("🗄️ Database / Ledger")
st.caption("Locked plot records · Hash history")

summary = get_ledger_summary()
st.metric("Total blocks", summary.get("total_blocks", 0))

entries = summary.get("entries", [])
if not entries:
    st.info("Ledger empty hai. Pehle kisi desk se Lock on Chain karein.")
else:
    for e in reversed(entries):
        st.markdown(f"### Block #{e.get('index')}")
        st.write(f"**Plot key:** {e.get('plot_key')}")
        st.write(f"**Hash:** `{e.get('hash')}`")
        st.write(f"**Time:** {e.get('time')}")
        st.write("---")

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Database page"):
    st.success(summarize_page("Database"))
