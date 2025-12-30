import streamlit as st
import pandas as pd

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="GreenScore.ai",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- THEME SWITCH ----------------
theme = st.sidebar.radio("🌗 Theme", ["Dark", "Light"])

if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, span, label {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        h1, h2, h3, h4, h5, h6, p, span, label {
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🌱 GreenScore.ai")
st.caption("AI Powered Carbon, Finance & Sustainability Platform")

st.image("https://cdn-icons-png.flaticon.com/512/2909/2909767.png", width=120)

# ---------------- ENGINE ----------------
def green_score(co2):
    if co2 <= 100: return 95
    elif co2 <= 200: return 80
    elif co2 <= 300: return 65
    elif co2 <= 500: return 40
    else: return 20

def govt(score):
    if score >= 80: return "₹5000 Green Subsidy + ESG Certificate"
    elif score >= 60: return "Normal Tariff"
    elif score >= 40: return "Energy Warning"
    elif score >= 20: return "₹2000 Carbon Penalty"
    else: return "₹5000 Heavy Carbon Tax"

def bank(score):
    if score >= 80: return "Green Loan @ 5%"
    elif score >= 60: return "Loan @ 8%"
    elif score >= 40: return "Loan @ 12%"
    else: return "High Risk Loan @ 18%"

# ---------------- MODE ----------------
mode = st.radio("Select Mode", ["Personal User", "Hostel / Group Upload"])

# ---------------- PERSONAL MODE ----------------
if mode == "Personal User":
    st.subheader("👤 Personal Carbon Calculator")

    units = st.number_input("Electricity Used (kWh)", min_value=0.0)
    people = st.number_input("People in house (optional)", min_value=0)
    area = st.number_input("House area sq.m (optional)", min_value=0.0)

    if st.button("Calculate"):
        co2 = units * 0.82

        final_co2 = co2
        if people > 0:
            final_co2 /= people
        if area > 0:
            final_co2 /= area

        score = green_score(final_co2)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total CO₂ (kg)", round(co2,2))
        col2.metric("Effective CO₂", round(final_co2,2))
        col3.metric("Green Score", score)

        st.success("Government: " + govt(score))
        st.info("Bank: " + bank(score))

# ---------------- GROUP MODE ----------------
if mode == "Hostel / Group Upload":
    st.subheader("🏢 Hostel / Campus Green Score")

    file = st.file_uploader("Upload Excel or CSV (Hostel, Units)", type=["csv","xlsx"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        df["CO2"] = df["Units"] * 0.82
        df["Green Score"] = df["CO2"].apply(green_score)
        df["Govt"] = df["Green Score"].apply(govt)
        df["Bank"] = df["Green Score"].apply(bank)

        df = df.sort_values("Green Score", ascending=False)
        df["Rank"] = range(1, len(df)+1)

        st.dataframe(df)

        st.subheader("📊 CO₂ Comparison")
        st.bar_chart(df.set_index("Hostel")["CO2"])

        st.subheader("📊 Green Score Comparison")
        st.bar_chart(df.set_index("Hostel")["Green Score"])

        best = df.iloc[0]
        worst = df.iloc[-1]

        st.success(f"🌿 Best Hostel: {best['Hostel']} (Score {best['Green Score']})")
        st.error(f"🔥 Worst Hostel: {worst['Hostel']} (Score {worst['Green Score']})")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("GreenScore.ai | Sustainability meets Finance")

