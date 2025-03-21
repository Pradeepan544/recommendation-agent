import streamlit as st
import requests

st.set_page_config(page_title="AI-Driven News Recommender", layout="centered")
st.title("🔹 AI-Driven Recommendation System")

# ✅ FastAPI Backend URL
API_URL = "http://localhost:8000"

# 🔹 User Profile Section
st.header("👤 Add User Profile")

# User Input Fields
user_id = st.text_input("🆔 User ID")
name = st.text_input("📛 Name")

# Dropdown for Structured Interests
interests_options = ["Technology", "Finance", "Sports", "Entertainment", "Health", "Education", "Business"]
selected_interests = st.multiselect("🎯 Interests", interests_options)

category = st.selectbox("📂 Preferred Category", interests_options)
relevance_score = st.slider("⭐ Relevance Score", 0.0, 1.0, 0.5)

if st.button("✅ Submit Profile"):
    with st.spinner("Adding user..."):
        user_data = {
            "user_id": user_id.strip(),
            "name": name.strip(),
            "interests": selected_interests,
            "metadata": {
                "category": category,
                "relevance_score": relevance_score
            }
        }
        
        try:
            response = requests.post(f"{API_URL}/add_user", json=user_data)
            response.raise_for_status()
            result = response.json()
            st.success(result.get("message", "User added successfully!"))
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to add user: {e}")

# 🔹 News Ingestion Section
st.header("📰 Fetch & Store News Articles")

news_category = st.selectbox("🌍 Select News Category", interests_options)

if st.button("📥 Fetch News"):
    with st.spinner("Fetching latest news..."):
        try:
            response = requests.post(f"{API_URL}/add_news/{user_id}?category={news_category}")
            response.raise_for_status()
            st.success(response.json()["message"])
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to fetch news: {e}")

# 🔹 AI-Driven News Recommendations
st.header("🤖 Get AI-Powered News Recommendations")

recommend_user_id = st.text_input("Enter User ID for Recommendations")

if st.button("📢 Get Recommendations"):
    with st.spinner("Generating AI recommendations..."):
        try:
            response = requests.get(f"{API_URL}/recommend/{recommend_user_id}")
            response.raise_for_status()
            recommendations = response.json().get("recommendations", "No recommendations found.")

            st.subheader("📌 AI Recommended News Articles:")
            st.write(recommendations)  # Displays AI-generated output
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Failed to get recommendations: {e}")
