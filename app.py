import streamlit as st
import pandas as pd

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Placement Score Predictor", layout="centered")

st.title("🎓 Student Placement Score Predictor")
st.markdown("### 🔐 Check Your Personal Placement Score")

# -------------------------------
# GOOGLE SHEET CSV LINK
# -------------------------------
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRzjhu63Op-IqthN82hju7bIy9vmeohNuWFQgf5l0Kt_cY4eMxBzLx9-tz7qI0KwMsuvZH7DEd3-PQ8/pub?output=csv"

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data(ttl=10)
def load_data():
    return pd.read_csv(url)

data = load_data()

# Clean column names
data.columns = data.columns.str.strip().str.replace(" ", "_")

# -------------------------------
# USER INPUT (EMAIL)
# -------------------------------
st.subheader("📧 Enter your email to get your result")
email = st.text_input("Email Address")

# -------------------------------
# SAFE NUMBER CONVERSION FUNCTION
# -------------------------------
def get_value(row, col):
    try:
        return float(row.get(col, 0))
    except:
        return 0

# -------------------------------
# SCORE CALCULATION
# -------------------------------
def calculate_score(row):
    score = 0

    score += get_value(row, 'CGPA') * 10
    score += get_value(row, 'Projects') * 5
    score += get_value(row, 'Internships') * 10
    score += get_value(row, 'Certifications') * 2
    score += get_value(row, 'Programming') * 5
    score += get_value(row, 'Aptitude') * 3
    score += get_value(row, 'Communication') * 3
    score += get_value(row, 'GD') * 2

    return min(score, 100)

# -------------------------------
# BUTTON ACTION
# -------------------------------
if st.button("🔍 Get My Result"):

    if email.strip() == "":
        st.warning("⚠️ Please enter your email")
        st.stop()

    # Check if column exists
    if 'Email_Address' not in data.columns:
        st.error("❌ Email column not found in data. Check Google Form.")
        st.stop()

    # Filter user data
    user_data = data[data['Email_Address'].str.strip().str.lower() == email.strip().lower()]

    if user_data.empty:
        st.error("❌ No record found. Please fill the Google Form first.")
    else:
        latest = user_data.tail(1)
        student = latest.iloc[0]

        score = calculate_score(student)

        # -------------------------------
        # RESULT
        # -------------------------------
        st.subheader("🎯 Your Placement Score")
        st.write(f"📈 Score: {score:.2f} / 100")

        # Performance level
        if score >= 80:
            st.success("🔥 Excellent – High chances of placement")
        elif score >= 60:
            st.warning("👍 Good – Moderate chances")
        elif score >= 40:
            st.warning("⚠️ Average – Need improvement")
        else:
            st.error("❌ Low – Work on your skills")

        # -------------------------------
        # SUGGESTIONS
        # -------------------------------
        st.subheader("📌 Personalized Suggestions")

        if get_value(student, 'Internships') < 1:
            st.write("👉 Do at least 1 internship")

        if get_value(student, 'Projects') < 2:
            st.write("👉 Build more real-world projects")

        if get_value(student, 'Programming') < 6:
            st.write("👉 Improve coding skills")

        if get_value(student, 'Communication') < 6:
            st.write("👉 Improve communication skills")

        if get_value(student, 'Aptitude') < 6:
            st.write("👉 Practice aptitude regularly")

        # -------------------------------
        # SHOW USER DATA (OPTIONAL)
        # -------------------------------
        with st.expander("📄 View Your Submitted Data"):
            st.write(latest)