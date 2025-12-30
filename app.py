import streamlit as st
import pandas as pd

st.set_page_config(page_title="GreenScore.ai", layout="wide")

st.title("🌱 GreenScore.ai")
st.write("Upload electricity data to calculate CO₂, Green Score and incentives")

uploaded_file = st.file_uploader("Upload Hostel Electricity Data", type=["xlsx","csv"])

def get_green_score(co2):
    if co2 <= 100:
        return 95
    elif co2 <= 200:
        return 80
    elif co2 <= 300:
        return 65
    elif co2 <= 500:
        return 40
    else:
        return 20

def get_benefits(score):
    if score >= 80:
        return "🌳 ₹5000 Green Subsidy + Green Hostel Certificate"
    elif score >= 60:
        return "✅ Normal electricity tariff"
    elif score >= 40:
        return "⚠ Improve energy efficiency"
    elif score >= 20:
        return "💰 Carbon Penalty ₹2000"
    else:
        return "🔴 Heavy Carbon Tax ₹5000"

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📄 Uploaded Data")
    st.dataframe(df)

    df["CO2"] = df["Units"] * 0.82
    df["Green Score"] = df["CO2"].apply(get_green_score)

    total_co2 = df["CO2"].sum()
    avg_score = df["Green Score"].mean()

    col1, col2 = st.columns(2)
    col1.metric("Total CO₂ (kg)", round(total_co2,2))
    col2.metric("Average Green Score", round(avg_score,1))

    st.subheader("🌱 Incentive / Penalty")
    st.info(get_benefits(avg_score))

    st.subheader("🏆 Hostel Leaderboard")
    df = df.sort_values("Green Score", ascending=False)
    df["Rank"] = range(1, len(df)+1)
    st.dataframe(df[["Rank","Hostel","Units","CO2","Green Score"]])

    st.subheader("📈 CO₂ Comparison")
    st.bar_chart(df.set_index("Hostel")["CO2"])
  
