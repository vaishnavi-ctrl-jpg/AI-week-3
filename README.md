# AI Internship Week 3: FinanceGuru (Domain-Specific Chatbot)

An interactive, domain-specific AI chatbot specializing in **Indian Personal Finance & Tax Advisory**. The application demonstrates prompt engineering, multi-turn conversation memory, out-of-scope query guardrails, and a custom evaluation framework.

---

## 📌 Features

1. **Earthy Forest & Sage UI**: A premium custom-themed chat interface built with Streamlit.
2. **Conversation Memory**: Maintains multi-turn dialog context across queries.
3. **Structured System Prompt & Few-Shots**: Persona configured as a tax advisor with built-in rules for tax calculations (FY 2024-25).
4. **Out-of-Scope Guardrails**: Refuses queries regarding medicine, recipes, or coding with a standardized block message.
5. **Rating Feedback Logger**: Saves thumbs-up/thumbs-down user ratings directly to `feedback_log.csv` for usability analysis.
6. **20-Q&A Evaluation Framework**: Structured test cases covering Easy, Medium, and Hard scenarios to compute accuracy and safety.

---

## 🛠️ Tech Stack
* **Language**: Python 3
* **Interface**: Streamlit
* **AI Model**: Google Gemini 1.5 Flash (via `google-generativeai`)
* **Environment Configuration**: `python-dotenv`

---

## 📂 File Directory

```text
AI-WEEK-3/
├── app.py                # Main Streamlit Chat application
├── evaluation.py         # 20-Question test suite generator
├── feedback_log.csv      # Log file storing user ratings
├── reflection.md         # Reflection on LLM limitations & ethics
├── requirements.txt      # Dependency configurations
└── .env.example          # Environment variable template
```

---

## 🚀 How to Run Locally

### 1. Set Up Environment
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
Open `.env` and add your Google AI Studio API Key:
```text
GEMINI_API_KEY=AIzaSy...
```
*(If the `.env` file is missing, the application sidebar allows you to paste the key directly into the UI fallback input).*

### 3. Start the Application
Run the Streamlit application:
```bash
streamlit run app.py
```
Open the live interface at the address printed in your terminal (usually **`http://localhost:8501`**).

---

## 📊 Running the Evaluation Framework
Execute the programmatic evaluation suite to test all 20 scenarios:
```bash
python evaluation.py
```
This queries the Gemini API for all 20 test cases and saves them to `evaluation_results.csv` along with scoring columns. You can open this file in Excel to rate them (1-5 scale) on Accuracy, Relevance, and Safety.
