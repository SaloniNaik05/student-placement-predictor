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

# Clean column names
data.columns = data.columns.str.strip().str.replace(" ", "_")

# -------------------------------
# DEBUG (REMOVE LATER)
# -------------------------------
# st.write(data.columns)

# -------------------------------
# USER INPUT
# -------------------------------
email = st.text_input("📧 Enter your Email Address")

# -------------------------------
# SAFE NUMBER FUNCTION (VERY IMPORTANT)
# -------------------------------
def get_val(row, col):
    try:
        value = row.get(col, 0)

        # Handle missing values
        if pd.isna(value):
            return 0

        # Convert string to number safely
        value = str(value).strip()

        # Remove unwanted characters
        value = value.replace("%", "")

        return float(value)

    except:
        return 0

# -------------------------------
# NORMALIZATION FUNCTIONS
# -------------------------------
def normalize(val, max_val):
    return min(val / max_val, 1)

# -------------------------------
# SMART SCORE FUNCTION
# -------------------------------
def calculate_score(row):

    cgpa = get_val(row, 'CGPA')
    projects = get_val(row, 'Projects')
    internships = get_val(row, 'Internships')
    certifications = get_val(row, 'Certifications')
    programming = get_val(row, 'Programming')
    aptitude = get_val(row, 'Aptitude')
    communication = get_val(row, 'Communication')
    gd = get_val(row, 'GD')

    score = 0

    score += normalize(cgpa, 10) * 20
    score += normalize(projects, 5) * 15
    score += normalize(internships, 3) * 20
    score += normalize(programming, 10) * 15
    score += normalize(aptitude, 10) * 10
    score += normalize(communication, 10) * 10
    score += normalize(certifications, 5) * 5
    score += normalize(gd, 5) * 5

    return round(score, 2)

# -------------------------------
# BUTTON
# -------------------------------
if st.button("🔍 Get My Result"):

    if email.strip() == "":
        st.warning("⚠️ Please enter your email")
        st.stop()

    # Check email column exists
    if 'Email_Address' not in data.columns:
        st.error("❌ Email column not found. Check Google Form.")
        st.stop()

    # Filter user data (case-insensitive)
    user_data = data[data['Email_Address'].astype(str).str.strip().str.lower() == email.strip().lower()]

    if user_data.empty:
        st.error("❌ No record found. Please fill the form first.")
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
        # DEBUG VALUES (VERY IMPORTANT)
        # -------------------------------
        st.write("🔎 Debug Values:")
        st.write({
            "Internships": get_val(student, 'Internships'),
            "Projects": get_val(student, 'Projects'),
            "Programming": get_val(student, 'Programming')
        })

        # -------------------------------
        # SUGGESTIONS (NOW CORRECT)
        # -------------------------------
        st.subheader("📌 Personalized Suggestions")

        if get_val(student, 'Internships') < 1:
            st.write("👉 Add at least 1 internship")

        if get_val(student, 'Projects') < 2:
            st.write("👉 Build more projects")

        if get_val(student, 'Programming') < 6:
            st.write("👉 Improve coding skills")

        if get_val(student, 'Communication') < 6:
            st.write("👉 Improve communication")

        if get_val(student, 'Aptitude') < 6:
            st.write("👉 Practice aptitude")

        # -------------------------------
        # USER DATA
        # -------------------------------
        with st.expander("📄 Your Submitted Data"):
            st.write(latest)