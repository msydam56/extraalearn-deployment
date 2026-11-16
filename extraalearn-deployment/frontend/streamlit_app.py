import os

import requests
import streamlit as st

backend_url = os.getenv("BACKEND_URL", "http://localhost:5000").rstrip("/")

st.title("ExtraaLearn Lead Conversion")
st.write("Enter one lead’s details to estimate their chance of becoming a paid customer.")

with st.form("lead_form"):
    lead = {
        "age": st.number_input("Age", min_value=0, value=35),
        "current_occupation": st.selectbox(
            "Current occupation", ["Professional", "Unemployed", "Student"]
        ),
        "first_interaction": st.selectbox(
            "First interaction", ["Website", "Mobile App"]
        ),
        "profile_completed": st.selectbox(
            "Profile completion", ["Low", "Medium", "High"]
        ),
        "website_visits": st.number_input("Website visits", min_value=0, value=3),
        "time_spent_on_website": st.number_input(
            "Total time on website (seconds)", min_value=0, value=376
        ),
        "page_views_per_visit": st.number_input(
            "Average pages viewed per visit", min_value=0.0, value=2.79, step=0.1
        ),
        "last_activity": st.selectbox(
            "Most recent activity",
            ["Email Activity", "Phone Activity", "Website Activity"],
        ),
    }

    for field, label in {
        "print_media_type1": "Saw a newspaper ad",
        "print_media_type2": "Saw a magazine ad",
        "digital_media": "Saw a digital ad",
        "educational_channels": "Heard about ExtraaLearn through an educational channel",
        "referral": "Heard about ExtraaLearn through a referral",
    }.items():
        lead[field] = st.selectbox(label, ["No", "Yes"], key=field)

    submitted = st.form_submit_button("Predict conversion")

if submitted:
    try:
        response = requests.post(f"{backend_url}/predict", json=lead, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        st.error(f"The prediction request failed. {error}")
    else:
        result = response.json()
        prediction_label = "Likely to convert" if result["prediction"] == 1 else "Unlikely to convert"

        st.success(prediction_label)
        st.metric("Estimated conversion probability", f"{result['conversion_probability']:.1%}")
