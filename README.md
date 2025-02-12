# Sentiment Analysis App

This repository contains a **sentiment analysis application** built using **FastAPI** (backend) and **React** (frontend) with Tailwind CSS. The system supports two models for sentiment classification:

- **Custom Fine-Tuned Model**: A DistilBERT-based model fine-tuned on the IMDB dataset.
- **Llama 3**: A large language model accessed via Groq Cloud API.

## **Installation and Setup**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/sentiment-analysis.git
cd sentiment-analysis
```

## **Backend (FastAPI) Setup**

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv sentiment_env
source sentiment_env/bin/activate  # On macOS/Linux
sentiment_env\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**
```bash
cd backend  # Navigate to the backend folder
pip install -r requirements.txt
```

### **4️⃣ Run the FastAPI Server**
```bash
uvicorn main:app --reload
```
Once running, access the API documentation at:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## **Frontend (React) Setup**

### **5️⃣ Install Frontend Dependencies**
```bash
cd ../sentiment-ui  # Navigate to the frontend folder
npm install
```

### **6️⃣ Start the React Application**
```bash
npm run dev
```
The UI should now be accessible at:  
[http://localhost:5173/](http://localhost:5173/)

## **API Endpoints**

### **1️⃣ Sentiment Analysis**
**POST** `/analyze/`  
Analyzes sentiment using either the custom model or Llama 3.

#### **Example Request**
```json
{
  "text": "This movie was amazing!",
  "model": "custom"
}
```

#### **Example Response**
```json
{
  "sentiment": "positive",
  "confidence": 0.97
}
```

| Method | Endpoint  | Description |
|--------|----------|-------------|
| `POST` | `/analyze/` | Analyzes sentiment of input text |

## **License**
This project is open-source under the **MIT License**.

