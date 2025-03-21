import requests
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
import google.generativeai as genai
from langgraph.graph import StateGraph
from typing import List
import os

# Initialize FastAPI
app = FastAPI()

# ✅ Connect to MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["usersDB"]
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")

# 🔹 Configure Gemini API
os.environ["GOOGLE_API_KEY"] = "enter gemini api key"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 🔹 Define Models
class Metadata(BaseModel):
    category: str
    relevance_score: float

class UserProfile(BaseModel):
    user_id: str
    name: str
    interests: List[str]
    metadata: Metadata  

class NewsArticle(BaseModel):
    user_id: str  # Added user_id
    title: str
    description: str
    url: str
    category: str
    keywords: List[str]
    relevance_score: float

# ✅ API to Add User Profile
@app.post("/add_user")
def add_user(user: UserProfile):
    existing_user = db["user_profiles"].find_one({"user_id": user.user_id})
    if existing_user:
        return {"message": "User already exists!"}
    db["user_profiles"].insert_one(user.model_dump())
    return {"message": "User added successfully!"}

# ✅ Fetch News from NewsAPI
NEWS_API_KEY = "enter news api key"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

def fetch_news(category: str = "technology", page_size: int = 5):
    params = {
        "apiKey": NEWS_API_KEY,
        "category": category,
        "pageSize": page_size,
        "country": "us",
    }
    response = requests.get(NEWS_API_URL, params=params)
    return response.json().get("articles", [])

# ✅ API to Fetch & Store News Articles (Now includes user_id)
@app.post("/add_news/{user_id}")
def add_news(user_id: str, category: str = "technology"):
    articles = fetch_news(category)

    if not articles:
        return {"message": f"No news found for category: {category}. Check API key and category name!"}

    for article in articles:
        news_data = {
            "user_id": user_id,  # Associate news with user
            "title": article.get("title", "No title"),
            "description": article.get("description", "No description"),
            "url": article.get("url", ""),
            "category": category,
            "keywords": article.get("title", "No title").split(),
            "relevance_score": 0.8
        }
        db["news"].insert_one(news_data)

    return {"message": f"{len(articles)} articles added for user {user_id}!"}

# ✅ Define LangGraph State
class RecommendationState(BaseModel):
    recommendations: List[str] = []

# ✅ AI-Driven News Recommendation (Now fetches news per user)
@app.get("/recommend/{user_id}")
def recommend(user_id: str):
    try:
        # 🔹 Fetch user profile
        user = db["user_profiles"].find_one({"user_id": user_id}, {"_id": 0})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # 🔹 Fetch relevant news articles for the user
        news_articles = list(db["news"].find({"user_id": user_id}, {"_id": 0}))
        if not news_articles:
            raise HTTPException(status_code=404, detail="No news articles found for user")
        
        print("User Data:", user)
        print("News Data:", news_articles)

        # ✅ LangGraph AI Recommendation
        def agent_function(state: RecommendationState):
            user_interests = user["interests"]  # Safe access
            articles_text = "\n".join(
                [f"- {article['title']} (Category: {article['category']})" for article in news_articles[:10]]
            )

            prompt = f"""
            User Interests: {', '.join(user_interests)}
            Available Articles:
            {articles_text}

            Based on the user's interests, generate the top recommendations based on the given news articles. Even if you have only a single genre article find necessary recommendation to it.
            """

            # Call the Generative AI model
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            # Extracting response text safely
            recommendations = response.text

            return RecommendationState(recommendations=[recommendations])

        # 🔹 Create LangGraph-based Agent
        sg = StateGraph(RecommendationState)
        sg.add_node("recommendation", agent_function)
        sg.set_entry_point("recommendation")
        graph = sg.compile()
        
        # ✅ Invoke LangGraph
        recommendation_result = graph.invoke({})  # Fixed issue
        print(recommendation_result)

        recommendations = recommendation_result.get("recommendations", [])

        # Ensure recommendations is a list of strings
        if not isinstance(recommendations, list):
            recommendations = [str(recommendations)]  # Convert to list if not already

        print("Recommendations:", recommendations)
        return {"recommendations": recommendations}  # Return in expected format

    except Exception as e:
        print("❌ Error:", e)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")