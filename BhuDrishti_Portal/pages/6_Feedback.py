import streamlit as st
import json
import os
from datetime import datetime
from aasia import summarize_page

st.set_page_config(page_title="Feedback | BhuDrishti", layout="wide")
st.title("💬 Feedback & Grievance")
st.caption("Aapka sujhav portal improve karne mein madad karega")

FEED_FILE = "feedback_store.json"

name = st.text_input("Name")
role = st.selectbox("You are", ["Citizen", "Farmer", "Lekhpal", "Real Estate", "Gov Officer", "Other"])
category = st.selectbox("Category", ["Suggestion", "Bug / Problem", "Complaint", "Appreciation"])
message = st.text_area("Your message", height=150)

if st.button("Submit feedback", type="primary"):
    if not message.strip():
        st.error("Please write a message.")
    else:
        entry = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "name": name or "Anonymous",
            "role": role,
            "category": category,
            "message": message.strip(),
        }
        data = []
        if os.path.exists(FEED_FILE):
            with open(FEED_FILE, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = []
        data.append(entry)
        with open(FEED_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        st.success("Feedback saved. Dhanyavaad!")

if os.path.exists(FEED_FILE):
    with st.expander("Recent feedback (local store)"):
        with open(FEED_FILE, "r", encoding="utf-8") as f:
            try:
                items = json.load(f)
            except Exception:
                items = []
        for item in reversed(items[-10:]):
            st.write(f"**{item.get('category')}** by {item.get('name')} ({item.get('role')}) — {item.get('time')}")
            st.write(item.get("message"))
            st.write("---")

st.divider()
st.markdown("### 🤖 AASIA")
if st.button("Summarize Feedback page"):
    st.success(summarize_page("Feedback"))
