import streamlit as st
import pandas as pd
import numpy as np

# ---------------- CONFIG ----------------
st.set_page_config(page_title="GreenScore.ai", layout="wide")

# ---------------- THEME ----------------
theme = st.sidebar.radio("Theme", ["🌙 Dark", "☀ Light"])
if theme == "🌙 Dark":
    st.markdown("""<style>body{background-color:#0E1117;color:white}</style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>body{background-color:white;color:black}</style>""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("## 🌱 GreenScore.ai")
st.markdown("### AI Powered Carbon, Finance & Sustainability Platform")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Climate_change_icon.svg/512px-Climate_change_icon.svg.png", width=120)

# ---------------- GREEN SCORE ENGINE ----------------
def green_score(co2):
    if co2 <= 100: return 95
    elif co2 <= 200: return 80
    elif co2 <= 300: return 65
    elif co2 <= 500: return 40
    else: return 20

def govt_benefit(score):
    if score >= 80: return "₹5000 Green Subsidy + ESG Certificate"
    elif score >= 60: return "Normal Tariff"
    elif score >= 40: return "Energy Warning"
    elif score >= 20: return "₹2000 Carbon Penalty"
    else: return "₹5000 Heavy Carbon Tax"

def bank_interest(score):
    if score >= 80: return "Green Loan @ 5% interest"
    elif score >= 60: return "Normal Loan @ 8%"
    elif score >= 40: return "Loan @ 12%"
    else: return "High Risk – 18% interest"

# ---------------- MODE SELECTION ----------------
mode = st.radio("Select Mode", ["👤 Personal User", "🏢 Hostel / Group Upload"])

# ---------------- PERSONAL MODE ----------------
if mode == "👤 Personal User":
    st.subheader("👤 Personal Carbon Calculator")

    name = st.text_input("Your Name")
    units = st.number_input("Electricity Used (kWh)", min_value=0)
    people = st.number_input("People in house", min_value=1)
    area = st.number_input("House area (sq.m)", min_value=1)

    if st.button("Calculate My Green Score"):
        co2 = units * 0.82
        co2_person = co2 / people
        co2_area = co2 / area
        score = green_score(co2_person)

        st.metric("Total CO₂ (kg)", round(co2,2))
        st.metric("CO₂ per person", round(co2_person,2))
        st.metric("Green Score", score)

        st.success("Government: " + govt_benefit(score))
        st.info("Bank: " + bank_interest(score))

# ---------------- GROUP MODE ----------------
if mode == "🏢 Hostel / Group Upload":
    st.subheader("🏢 Hostel / Campus Green Score")

    file = st.file_uploader("Upload Excel or CSV (Hostel, Units)", type=["csv","xlsx"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        df["CO2"] = df["Units"] * 0.82
        df["Green Score"] = df["CO2"].apply(green_score)

        df["Govt Incentive"] = df["Green Score"].apply(govt_benefit)
        df["Bank Interest"] = df["Green Score"].apply(bank_interest)

        df = df.sort_values("Green Score", ascending=False)
        df["Rank"] = range(1,len(df)+1)

        st.dataframe(df)

        st.bar_chart(df.set_index("Hostel")["CO2"])
        st.bar_chart(df.set_index("Hostel")["Green Score"])

        best = df.iloc[0]
        worst = df.iloc[-1]

        st.success(f"🌿 Best Hostel: {best['Hostel']} (Score {best['Green Score']})")
        st.error(f"🔥 Worst Hostel: {worst['Hostel']} (Score {worst['Green Score']})")

# ---------------- ESG DOWNLOAD ----------------
st.subheader("📄 Download ESG Report")
st.download_button("Download Green Report", "GreenScore AI Report", "report.txt")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("🌍 GreenScore.ai — Sustainability meets Finance")
st.markdown("Built by Rupesh Mishra")
