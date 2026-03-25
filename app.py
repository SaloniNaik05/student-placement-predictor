import streamlit as st
import pandas as pd

# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(page_title="Placement Predictor", layout="centered")

st.title("🎓 Smart Placement Predictor")
st.markdown("### 🔐 Get Your Personalized Placement Score")

# -------------------------------
# GOOGLE SHEET CSV LINK
# -------------------------------
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRzjhu63Op-IqthN82hju7bIy9vmeohNuWFQgf5l0Kt_cY4eMxBzLx9-tz7qI0KwMsuvZH7DEd3-PQ8/pub?output=csv"

@st.cache_data(ttl=10)
def load_data():
    return pd.read_csv(url)

data = load_data()

# Clean column names (VERY IMPORTANT)
data.columns = data.columns.str.strip().str.replace(" ", "_").str.replace("/", "_")

# -------------------------------
# USER INPUT
# -------------------------------
email = st.text_input("📧 Enter your Email Address")

# -------------------------------
# SAFE NUMBER FUNCTION
# -------------------------------
def get_val(row, col):
    try:
        value = row.get(col, 0)

        if pd.isna(value):
            return 0

        value = str(value).strip().replace("%", "")
        return float(value)

    except:
        return 0

# -------------------------------
# NORMALIZATION
# -------------------------------
def normalize(val, max_val):
    return min(val / max_val, 1)

# -------------------------------
# SCORE FUNCTION (MATCHED COLUMNS)
# -------------------------------
def calculate_score(row):

    score = 0

    score += normalize(get_val(row, 'Current_CGPA'), 10) * 20
    score += normalize(get_val(row, 'Number_of_Projects_Done'), 5) * 15
    score += normalize(get_val(row, 'Number_of_Internships'), 3) * 20
    score += normalize(get_val(row, 'Programming_Skill_Level'), 10) * 15
    score += normalize(get_val(row, 'Aptitude_Skill_Level'), 10) * 10
    score += normalize(get_val(row, 'Communication_Skills'), 10) * 10
    score += normalize(get_val(row, 'Number_of_Certifications'), 5) * 5
    score += normalize(get_val(row, 'Number_of_Group_Discussions_(GD)_Attended'), 5) * 5

    return round(score, 2)

# -------------------------------
# BUTTON
# -------------------------------
if st.button("🔍 Get My Result"):

    if email.strip() == "":
        st.warning("⚠️ Please enter your email")
        st.stop()

    if 'Email_Address' not in data.columns:
        st.error("❌ Email column missing")
        st.stop()

    user_data = data[data['Email_Address'].astype(str).str.strip().str.lower() == email.strip().lower()]

    if user_data.empty:
        st.error("❌ No record found. Fill the form first.")
    else:
        latest = user_data.tail(1)
        student = latest.iloc[0]

        score = calculate_score(student)

        # -------------------------------
        # RESULT
        # -------------------------------
        st.subheader("🎯 Your Placement Score")
        st.write(f"📈 Score: {score} %")

        if score >= 80:
            st.success("🔥 Excellent – Strong chances")
        elif score >= 65:
            st.info("👍 Good – On track")
        elif score >= 50:
            st.warning("⚠️ Average – Improve more")
        else:
            st.error("❌ Low – Needs improvement")

        # -------------------------------
        # DEBUG (CHECK VALUES)
        # -------------------------------
        st.write("🔎 Debug Values:")
        st.write({
            "Internships": get_val(student, 'Number_of_Internships'),
            "Projects": get_val(student, 'Number_of_Projects_Done')
        })

        # -------------------------------
        # SUGGESTIONS (NOW FIXED ✅)
        # -------------------------------
        st.subheader("📌 Personalized Suggestions")

        if get_val(student, 'Number_of_Internships') < 1:
            st.write("👉 Add at least 1 internship")

        if get_val(student, 'Number_of_Projects_Done') < 2:
            st.write("👉 Build more projects")

        if get_val(student, 'Programming_Skill_Level') < 6:
            st.write("👉 Improve coding skills")

        if get_val(student, 'Communication_Skills') < 6:
            st.write("👉 Improve communication")

        if get_val(student, 'Aptitude_Skill_Level') < 6:
            st.write("👉 Practice aptitude")

        # -------------------------------
        # USER DATA
        # -------------------------------
        with st.expander("📄 Your Submitted Data"):
            st.write(latest)