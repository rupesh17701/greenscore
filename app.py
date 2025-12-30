import streamlit as st
import pandas as pd
import numpy as np

# ------------------ PAGE ------------------
st.set_page_config(page_title="GreenScore.ai", layout="wide")

# ------------------ STYLE ------------------
st.markdown("""
<style>
body {background-color:#f7f9fc;}
.card {
    background:white;
    padding:18px;
    border-radius:12px;
    box-shadow:0 4px 12px rgba(0,0,0,0.05);
}
.big {font-size:32px;font-weight:700;}
.green {color:#2ecc71;}
.red {color:#e74c3c;}
.grey {color:#7f8c8d;}
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🌍 GreenScore.ai")
currency = st.sidebar.selectbox("Currency", ["₹ INR", "$ USD"])
user_type = st.sidebar.radio("User Type", ["Home", "Hostel", "Company"])

symbol = "₹" if currency=="₹ INR" else "$"
rate = 1 if currency=="₹ INR" else 0.012

st.sidebar.markdown("---")
st.sidebar.markdown("### What matters in your score")
st.sidebar.markdown("• CO₂ per person")
st.sidebar.markdown("• CO₂ per area")

# ------------------ HEADER ------------------
st.markdown("## 🌱 GreenScore.ai")
st.markdown("Your **Sustainability Credit Score** for Homes, Campuses & Companies")

# ------------------ ENGINE ------------------
def green_score(co2):
    if co2 <= 2: return 95
    elif co2 <= 4: return 80
    elif co2 <= 6: return 65
    elif co2 <= 10: return 40
    else: return 20

def esg(score):
    if score>=85: return "A+"
    elif score>=70: return "A"
    elif score>=55: return "B"
    elif score>=40: return "C"
    else: return "D"

def money(score):
    if score>=80: return 5000
    elif score>=60: return 0
    elif score>=40: return -2000
    else: return -5000

# ------------------ INPUT ------------------
st.markdown("### Step 1 — Enter your data")

colA, colB, colC = st.columns(3)
with colA:
    units = st.number_input("Electricity used (kWh)",0.0)
with colB:
    people = st.number_input("People (optional)",0)
with colC:
    area = st.number_input("Area (sq.m) (optional)",0.0)

if st.button("Analyze my sustainability"):

    # ---------------- CALCULATION ----------------
    total_co2 = units * 0.82

    per_person = total_co2 / people if people>0 else total_co2
    per_area = total_co2 / area if area>0 else total_co2

    effective = (per_person + per_area) / 2

    score = green_score(effective)
    grade = esg(score)
    cash = money(score)*rate

    # ---------------- KPIs ----------------
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Total CO₂ (kg)", round(total_co2,2))
    k2.metric("CO₂ / person", round(per_person,2))
    k3.metric("CO₂ / area", round(per_area,2))
    k4.metric("Green Score", score)

    # ---------------- STORY ----------------
    st.markdown("### 🌍 Your Sustainability Story")

    if score>=80:
        st.success("You are greener than most users.")
    elif score>=60:
        st.info("You are average. Small improvements will help.")
    else:
        st.error("You are a heavy polluter. Action is required.")

    st.progress(score/100)

    # ---------------- MONEY ----------------
    if cash>=0:
        st.success(f"🌱 You earn {symbol}{round(cash,2)} in green incentives")
    else:
        st.error(f"🔥 You must pay {symbol}{abs(round(cash,2))} as carbon cost")

    # ---------------- INSIGHTS ----------------
    st.markdown("### 🔍 Smart Insights")

    if per_person>5:
        st.warning("Your per-person emissions are high. Reduce appliance usage.")
    if per_area>5:
        st.warning("Your building is energy-inefficient. Improve insulation.")

    if score>=80:
        st.success("You qualify for green loans and government subsidies.")
    elif score<40:
        st.error("You may face higher electricity tariffs in the future.")

    # ---------------- ACTIONS ----------------
    st.markdown("### 🚀 What should you do next?")

    a1,a2,a3 = st.columns(3)
    with a1:
        st.button("🌞 Install Solar")
        st.caption("Reduce CO₂ up to 40%")
    with a2:
        st.button("🏦 Apply Green Loan")
        st.caption("Lower interest for green users")
    with a3:
        st.button("📄 Download ESG Report")
        st.caption("Submit to govt / college")

# ------------------ GROUP ------------------
st.markdown("## 🏢 Step 2 — Compare Hostels or Companies")

file = st.file_uploader("Upload CSV or Excel (Name, Units, People, Area)",type=["csv","xlsx"])

if file:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df["CO2"] = df["Units"]*0.82
    df["PerPerson"] = df["CO2"]/df["People"]
    df["PerArea"] = df["CO2"]/df["Area"]
    df["Effective"] = (df["PerPerson"]+df["PerArea"])/2
    df["Score"] = df["Effective"].apply(green_score)
    df["ESG"] = df["Score"].apply(esg)

    df = df.sort_values("Score",ascending=False)
    df["Rank"] = range(1,len(df)+1)

    st.dataframe(df[["Rank","Name","Score","ESG","CO2","PerPerson","PerArea"]])

    st.markdown("### 📊 GreenScore comparison")
    st.bar_chart(df.set_index("Name")["Score"])



