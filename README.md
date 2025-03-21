# AI-Powered Recommendation Agent

## 📌 Overview
This project is an AI-powered recommendation agent that provides personalized recommendations based on user profiles and external news sources. Users can submit their profiles, fetch news data from an external API, and receive recommendations tailored to their interests.

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/news-recommendation.git
cd news-recommendation
```

### 2️⃣ Install Dependencies
Ensure you have Python installed (Python 3.8 or later recommended). Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up MongoDB
Ensure MongoDB is installed and running locally:
```bash
mongod --dbpath /path/to/your/db
```
Or use a cloud-based MongoDB service like [MongoDB Atlas](https://www.mongodb.com/atlas/database).

### 4️⃣ Set Up API Keys
Create a `.env` file and add the following API keys:
```env
GOOGLE_API_KEY=your-gemini-api-key
NEWS_API_KEY=your-newsapi-key
```
Replace `your-gemini-api-key` and `your-newsapi-key` with your actual API keys.

### 5️⃣ Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

## 🚀 Usage Instructions

### ➡️ Add a User Profile
```bash
curl -X POST "http://127.0.0.1:8000/add_user" -H "Content-Type: application/json" -d '{
    "user_id": "123",
    "name": "John Doe",
    "interests": ["Technology", "AI"],
    "metadata": {"category": "Tech", "relevance_score": 0.9}
}'
```

### ➡️ Fetch & Store News for a User
```bash
curl -X POST "http://127.0.0.1:8000/add_news/123?category=technology"
```

### ➡️ Get AI-Generated News Recommendations
```bash
curl -X GET "http://127.0.0.1:8000/recommend/123"
```

## 📌 Design Choices & Optimizations

1. **FastAPI for Scalability**: FastAPI was chosen for its speed, automatic validation, and async capabilities.
2. **MongoDB for Storage**: A NoSQL database was used to handle flexible user profiles and news data efficiently.
3. **Gemini AI Model**: Used Google Gemini to generate intelligent recommendations based on user interests and fetched news data.
4. **LangGraph for AI Workflow**: Ensured a structured AI pipeline for processing and generating recommendations.
5. **Efficient Querying**: Indexed MongoDB queries for faster retrieval of relevant user and news data.

## 🔗 API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/add_user` | Add a user profile |
| `POST` | `/add_news/{user_id}` | Fetch & store news articles for a user |
| `GET` | `/recommend/{user_id}` | Get AI-generated news recommendations |

## 📜 License
This project is open-source and available under the MIT License.

## 💡 Future Improvements
- Implement authentication for better security.
- Enhance recommendation algorithms with user feedback loops.
- Support multiple external news sources for a richer dataset.

---
💬 Feel free to contribute or raise an issue for improvements!
