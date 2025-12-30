import streamlit as st
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="GreenScore.ai", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
body {background-color:#f8f9fb;}
.card {
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0 4px 10px rgba(0,0,0,0.05);
}
.green {color:#2ecc71;font-weight:bold;}
.red {color:#e74c3c;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 GreenScore.ai")
currency = st.sidebar.selectbox("Currency", ["₹ INR", "$ USD"])
user_type = st.sidebar.radio("User Type", ["Home", "Hostel", "Company"])

rate = 1 if currency == "₹ INR" else 0.012
symbol = "₹" if currency == "₹ INR" else "$"

# ---------------- HEADER ----------------
st.markdown("## 🌱 GreenScore.ai")
st.markdown("### Your sustainability credit score")

# ---------------- ENGINE ----------------
def green_score(co2):
    if co2 <= 100: return 90
    elif co2 <= 200: return 75
    elif co2 <= 300: return 60
    elif co2 <= 500: return 40
    else: return 20

def esg(score):
    if score >= 80: return "A+"
    elif score >= 65: return "A"
    elif score >= 50: return "B"
    elif score >= 35: return "C"
    else: return "D"

def money(score):
    if score >= 80: return 5000
    elif score >= 60: return 0
    elif score >= 40: return -2000
    else: return -5000

# ---------------- USER JOURNEY ----------------
st.markdown("## Step 1 – Enter your energy data")

units = st.number_input("Electricity used (kWh)", 0.0)
people = st.number_input("People (optional)", 0)
area = st.number_input("Area sq.m (optional)", 0.0)

if st.button("Analyze My Sustainability"):

    # Step 2 – Calculate
    co2 = units * 0.82
    effective = co2
    if people > 0: effective /= people
    if area > 0: effective /= area

    score = green_score(effective)
    grade = esg(score)
    cash = money(score) * rate

    # ---------------- KPI CARDS ----------------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CO₂ (kg)", round(co2,2))
    c2.metric("Effective CO₂", round(effective,2))
    c3.metric("Green Score", score)
    c4.metric("ESG Grade", grade)

    # ---------------- STORY ----------------
    st.markdown("## 🌍 Your Sustainability Story")

    if score >= 80:
        st.success("You are greener than most users. You qualify for rewards.")
    elif score >= 60:
        st.info("You are average. Small improvements can save money.")
    else:
        st.error("You are a heavy polluter. Action is required.")

    st.progress(score/100)

    # ---------------- MONEY ----------------
    if cash >= 0:
        st.success(f"🌱 You earned {symbol}{round(cash,2)} in green incentives")
    else:
        st.error(f"🔥 You owe {symbol}{abs(round(cash,2))} as carbon tax")

    # ---------------- INSIGHTS ----------------
    st.markdown("## 🔍 Smart Insights")

    if score < 50:
        st.warning("Your emissions are high compared to similar users.")
    else:
        st.success("You are performing better than most comparable users.")

    # ---------------- ACTIONS ----------------
    st.markdown("## 🚀 What should you do next?")

    colA, colB, colC = st.columns(3)

    with colA:
        st.button("🌞 Install Solar")
        st.caption("Reduce CO₂ by up to 40%")

    with colB:
        st.button("🏦 Apply for Green Loan")
        st.caption("Lower interest if you stay green")

    with colC:
        st.button("📄 Download ESG Report")
        st.caption("Submit to government or college")

# ---------------- GROUP ----------------
st.markdown("## 🏢 Step 2 – Compare Hostels / Companies")

file = st.file_uploader("Upload CSV or Excel (Hostel, Units)", type=["csv","xlsx"])

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df["CO2"] = df["Units"] * 0.82
    df["Score"] = df["CO2"].apply(green_score)
    df["ESG"] = df["Score"].apply(esg)

    df = df.sort_values("Score", ascending=False)
    df["Rank"] = range(1,len(df)+1)

    st.dataframe(df)

    st.markdown("### 📊 Who is green and who is polluting?")
    st.bar_chart(df.set_index("Hostel")["Score"])

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("GreenScore.ai – The Sustainability Credit Score for the World")


