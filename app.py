import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Placement Predictor", layout="centered")

st.title("🎓 Student Placement Prediction System")
st.markdown("### 🚀 AI-Based Placement Predictor")

# -------------------------------
# GOOGLE SHEET CSV LINK
# -------------------------------
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRzjhu63Op-IqthN82hju7bIy9vmeohNuWFQgf5l0Kt_cY4eMxBzLx9-tz7qI0KwMsuvZH7DEd3-PQ8/pub?output=csv"

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(url)

data = load_data()

# -------------------------------
# SHOW DATA
# -------------------------------
st.subheader("📊 Latest Student Data")
st.write(data.tail())

# -------------------------------
# CLEAN COLUMN NAMES (IMPORTANT)
# -------------------------------
data.columns = data.columns.str.strip().str.replace(" ", "_")

# -------------------------------
# HANDLE MISSING VALUES
# -------------------------------
data = data.dropna()

# -------------------------------
# CHECK 'Placed' COLUMN
# -------------------------------
if 'Placed' not in data.columns:
    st.error("❌ Column 'Placed' not found. Check Google Form field name.")
    st.stop()

# Convert Yes/No → 1/0
data['Placed'] = data['Placed'].map({'Yes': 1, 'No': 0})

# -------------------------------
# CONVERT TEXT TO NUMBERS
# -------------------------------
data = pd.get_dummies(data)

# -------------------------------
# SPLIT FEATURES
# -------------------------------
X = data.drop("Placed", axis=1)
y = data["Placed"]

# -------------------------------
# TRAIN MODEL
# -------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# -------------------------------
# PREDICTION SECTION
# -------------------------------
st.subheader("🔍 Predict Placement")

if st.button("Predict for Latest Student"):

    latest_student = X.tail(1)

    prediction = model.predict(latest_student)
    prob = model.predict_proba(latest_student)

    probability = prob[0][1] * 100

    st.subheader("🎯 Prediction Result")

    st.write(f"📈 Placement Probability: {probability:.2f}%")

    if prediction[0] == 1:
        st.success("✅ High Chances of Placement")
    else:
        st.error("❌ Low Chances of Placement")

    # -------------------------------
    # SUGGESTIONS
    # -------------------------------
    if probability < 60:
        st.warning("⚠️ Suggestions to Improve:")
        st.write("- Do more internships")
        st.write("- Improve communication skills")
        st.write("- Practice aptitude")
        st.write("- Work on real-world projects")

    # -------------------------------
    # SHOW INPUT DATA
    # -------------------------------
    st.subheader("🧑 Student Details Used for Prediction")
    st.write(latest_student)