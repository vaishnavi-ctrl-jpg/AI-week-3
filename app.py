import os
import csv
from datetime import datetime
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration with premium layout
st.set_page_config(
    page_title="FinanceGuru - Indian Tax & Finance Advisor",
    page_icon="💰",
    layout="centered"
)

# Custom premium CSS to match our Luxury UI Colors palette (Black, Deep Charcoal, and Gold)
st.markdown("""
<style>
    /* Luxury background */
    .stApp {
        background: #0c0c0c !important;
    }

    /* Main body text color (Soft Gold/Cream) and fonts */
    .main, .main h1, .main h2, .main h3, .main p, .main span, .main li {
        color: #f5ebd5 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Card styling (Dark Charcoal Panel with Gold Border and Soft Gold Text) */
    .hero-card {
        background: #161616 !important;
        border-radius: 16px;
        padding: 24px;
        border: 1.5px solid #c5a880;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        margin-top: 15px;
        margin-bottom: 25px;
        animation: cardFloat 1.2s ease-out;
    }
    .hero-card h3 {
        color: #d8b17a !important;
        font-weight: 700 !important;
        font-size: 20px !important;
        margin-top: 0px !important;
    }
    .hero-card p {
        color: #f5ebd5 !important;
        line-height: 1.6;
        opacity: 0.95;
    }
    
    @keyframes cardFloat {
        from { transform: translateY(12px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Target Streamlit chat message containers */
    .stChatMessage {
        border-radius: 12px;
        margin-bottom: 15px;
        padding: 15px;
        border: 1.5px solid #8a6d3b !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* User chat bubble (Brushed Gold with Dark Text for high hierarchy contrast) */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #d8b17a !important;
        border: 1.5px solid #c5a880 !important;
    }
    .stChatMessage[data-testid="stChatMessageUser"] p {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    /* Assistant chat bubble (Deep Charcoal with Soft Gold Text) */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #161616 !important;
        border: 1.5px solid #8a6d3b !important;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] p {
        color: #f5ebd5 !important;
    }
    
    /* Sidebar text/headings readability (Soft Gold/Cream) */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] label {
        color: #f5ebd5 !important;
    }
    
    /* Force BaseWeb Input styling inside the sidebar specifically (Deep Charcoal with Gold border) */
    section[data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #161616 !important;
        border: 1.5px solid #8a6d3b !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="input"] input {
        color: #f5ebd5 !important;
        background-color: transparent !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="input"] button {
        background-color: transparent !important;
        color: #f5ebd5 !important;
        border: none !important;
    }
    
    /* Custom style for warnings/alerts inside sidebar */
    section[data-testid="stSidebar"] .stAlert {
        background-color: #161616 !important;
        border: 1px solid #8a6d3b !important;
    }
    section[data-testid="stSidebar"] .stAlert p {
        color: #f5ebd5 !important;
    }
    
    /* Input field styling (chat input textarea) */
    .stChatInputContainer {
        border-color: #c5a880 !important;
        background-color: #161616 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
    }
    .stChatInput textarea {
        color: #f5ebd5 !important;
    }
    
    /* Header logo SVG styling */
    .header-logo-svg {
        display: block;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .header-logo-svg:hover {
        transform: scale(1.1) rotate(5deg);
        filter: drop-shadow(0 0 12px rgba(216, 177, 122, 0.5));
    }

    /* --- SIDEBAR HIGH-FIDELITY DESIGN --- */
    .sidebar-profile-card {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #161616;
        border: 1.5px solid #8a6d3b;
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 20px;
        margin-top: 10px;
    }
    .profile-avatar {
        font-size: 22px;
        background: #0c0c0c;
        border-radius: 50%;
        width: 38px;
        height: 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1.5px solid #d8b17a;
    }
    .profile-info {
        display: flex;
        flex-direction: column;
    }
    .profile-name {
        font-weight: 600;
        color: #f5ebd5;
        font-size: 14px;
    }
    .profile-tier {
        font-size: 11px;
        color: #d8b17a;
        font-weight: 500;
    }
    .menu-header {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1px;
        color: #8a6d3b;
        margin: 18px 0 8px 0;
        text-transform: uppercase;
    }
    .menu-item {
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 13px;
        color: #f5ebd5;
        margin-bottom: 6px;
        border: 1px solid transparent;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .menu-item.active {
        background: #1a1712 !important;
        border: 1.5px solid #c5a880 !important;
        color: #d8b17a !important;
        font-weight: 600;
    }
    .sidebar-widget {
        background: #161616;
        border: 1.5px solid #8a6d3b;
        padding: 14px;
        border-radius: 12px;
        margin-bottom: 15px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .widget-title {
        font-size: 11px;
        color: #f5ebd5;
        opacity: 0.8;
    }
    .widget-value {
        font-size: 20px;
        font-weight: 700;
        color: #d8b17a;
        letter-spacing: 0.5px;
    }
    .progress-bar-container {
        background: #0c0c0c;
        height: 6px;
        border-radius: 3px;
        overflow: hidden;
        margin: 4px 0;
    }
    .progress-bar-fill {
        background: linear-gradient(90deg, #8a6d3b, #d8b17a);
        height: 100%;
        border-radius: 3px;
    }
    .market-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        font-size: 12px;
    }
    
    /* --- STREAMLIT PILL SUGGESTION CHIPS OVERRIDES --- */
    div.stButton > button {
        background-color: #161616 !important;
        color: #f5ebd5 !important;
        border: 1.5px solid #8a6d3b !important;
        border-radius: 24px !important;
        font-size: 13px !important;
        padding: 6px 18px !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #d8b17a !important;
        color: #1a1a1a !important;
        border-color: #c5a880 !important;
        box-shadow: 0 0 10px rgba(216, 177, 122, 0.3) !important;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 📂 SYSTEM PROMPT, FEW-SHOTS & GUARDRAILS SPEC
# ----------------------------------------------------
SYSTEM_PROMPT = """
You are "FinanceGuru", a highly sophisticated, professional, and friendly AI chatbot specializing in Indian Personal Finance, Income Tax (Direct and Indirect), Investments, Savings Schemes (e.g., PPF, NPS, Sukanya Samriddhi), and Financial Planning.

Your operations are strictly bound by the following rules:

1. Persona & Tone:
   - Speak in a clear, polite, and helpful professional tone.
   - Use simple analogies to explain complex tax concepts.
   - Always include a brief disclaimer at the end of tax calculations: "Please consult a registered Chartered Accountant (CA) or certified financial planner for final filings."

2. Domain Scope & Guardrails:
   - ONLY answer queries regarding Indian personal finance, income tax, savings, and investments.
   - Strictly REFUSE to answer queries regarding other domains (e.g., medical diagnoses, recipes, programming/coding, gaming, sports, history).
   - If a query is out-of-scope, answer with the exact sentence: "I apologize, but my expertise is strictly limited to Indian income tax, investments, and personal finance. I cannot assist with out-of-scope topics." Do not elaborate further or answer the out-of-scope question.

3. Accuracy Constraints:
   - Support calculations for both the Old Tax Regime and the New Tax Regime (specifically for Financial Year 2024-25 / Assessment Year 2025-26, and newer).
   - Clearly state deductions (such as Section 80C, 80D, 80TTA) where applicable under the Old Regime.

4. Few-Shot Context:
   Here are examples of how you must handle conversations:

   Query: "What is the deduction limit under Section 80C?"
   Response: "Under Section 80C of the Income Tax Act, you can claim a deduction of up to ₹1.5 Lakhs per financial year on eligible investments and expenses (such as PPF, ELSS, EPF, Life Insurance premium, and Principal repayment of Home Loan). Note: This deduction is only available if you opt for the Old Tax Regime. Disclaimer: Please consult a registered CA for personalized tax advice."

   Query: "Can you give me a recipe for Butter Chicken?"
   Response: "I apologize, but my expertise is strictly limited to Indian income tax, investments, and personal finance. I cannot assist with out-of-scope topics."
"""

# ----------------------------------------------------
# ⚙️ API KEY CONFIGURATION
# ----------------------------------------------------
# Retrieve API key
api_key = os.getenv("GEMINI_API_KEY")

# Sidebar for configuration and key validation fallback
with st.sidebar:
    st.markdown("### 🛠️ Configuration & Status")
    
    # If key is missing from environment, allow user to input it manually
    if not api_key:
        st.warning("⚠️ GEMINI_API_KEY not found in environment (.env).")
        api_key_input = st.text_input("Paste Gemini API Key:", type="password")
        if api_key_input:
            api_key = api_key_input
            st.success("API Key loaded successfully!")
    else:
        st.success("🤖 Gemini API Connection: ACTIVE")
        
    st.markdown("""
        <div class="sidebar-profile-card">
            <div class="profile-avatar">👨‍💻</div>
            <div class="profile-info">
                <span class="profile-name">Alex R.</span>
                <span class="profile-tier">AI Intern</span>
            </div>
        </div>
        
        <div class="menu-header">ACTIVE CHATS</div>
        <div class="menu-item active">💬 Tax Advisory</div>
        <div class="menu-item">📄 Financial Planning</div>
        
        <div class="menu-header">WIDGETS</div>
        <div class="sidebar-widget">
            <span class="widget-title">80C Tax-Saving Limit</span>
            <span class="widget-value">₹1,50,000</span>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: 80%;"></div>
            </div>
            <span style="font-size:10px; color:#8a6d3b; font-weight:500;">₹1,20,000 Saved (80% Achieved)</span>
        </div>
        
        <div class="menu-header">MARKET WATCH</div>
        <div class="market-row">
            <span style="color:#f5ebd5;">NIFTY 50</span>
            <span style="color:#4c7a41; font-weight:600;">22,493.50 (+0.72%)</span>
        </div>
        <div class="market-row">
            <span style="color:#f5ebd5;">SENSEX</span>
            <span style="color:#4c7a41; font-weight:600;">74,014.50 (+1.20%)</span>
        </div>
    """, unsafe_allow_html=True)

# Configure generative AI client if key exists
if api_key:
    genai.configure(api_key=api_key)
    # Using gemini-1.5-flash as the standard fast LLM model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
else:
    model = None

# Branded Glassmorphic Header
col1, col2 = st.columns([0.15, 0.85])
with col1:
    st.markdown('<svg class="header-logo-svg" viewBox="0 0 100 100" width="70" height="70" xmlns="http://www.w3.org/2000/svg"><path d="M50 10 C 25 15, 20 40, 20 60 C 20 75, 45 88, 50 90 C 55 88, 80 75, 80 60 C 80 40, 75 15, 50 10 Z" fill="#161616" stroke="#d8b17a" stroke-width="3" /><rect x="32" y="28" width="36" height="20" rx="6" fill="#0c0c0c" stroke="#8a6d3b" stroke-width="1.5" /><circle cx="43" cy="38" r="3" fill="#f5ebd5" /><circle cx="57" cy="38" r="3" fill="#f5ebd5" /><line x1="38" y1="58" x2="62" y2="58" stroke="#d8b17a" stroke-width="2" stroke-linecap="round" /><line x1="50" y1="52" x2="50" y2="72" stroke="#d8b17a" stroke-width="2" /><line x1="41" y1="58" x2="41" y2="67" stroke="#d8b17a" stroke-width="1" /><line x1="59" y1="58" x2="59" y2="67" stroke="#d8b17a" stroke-width="1" /><path d="M37 67 Q 41 71, 45 67" fill="none" stroke="#d8b17a" stroke-width="1.5" /><path d="M55 67 Q 59 71, 63 67" fill="none" stroke="#d8b17a" stroke-width="1.5" /><path d="M43 72 L 57 72" stroke="#d8b17a" stroke-width="2.5" stroke-linecap="round" /></svg>', unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div style='display: flex; flex-direction: column; justify-content: center; height: 70px;'>
            <h1 style='margin: 0; font-size: 32px; font-weight: 800; color: #f5ebd5; letter-spacing: 1.5px; font-family: "Space Grotesk", sans-serif;'>FINANCE<span style='color: #d8b17a;'>GURU</span></h1>
            <p style='margin: 0; font-size: 13px; color: #8a6d3b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Your Personal Indian Tax & Finance Assistant</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="hero-card">
        <h3 style='margin-top:0; font-family: "Space Grotesk", sans-serif; font-size: 20px; font-weight: 600; letter-spacing: 0.5px;'>Financial Oracle Hub</h3>
        <p style='margin:0; line-height: 1.6; font-size: 14px;'>Ask me anything about income tax slabs (Old vs New Regime), Section 80C/80D deductions, mutual funds, capital gains tax, or retirement savings. Our guidance is mapped directly to official Indian Income Tax regulations.</p>
    </div>
""", unsafe_allow_html=True)

# Initialize conversation history / memory in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        # Add feedback logging buttons to Assistant messages
        if msg["role"] == "assistant":
            # Avoid showing feedback buttons for older messages to keep UI clean
            if idx == len(st.session_state.messages) - 1:
                col1, col2, col3 = st.columns([0.1, 0.1, 0.8])
                with col1:
                    if st.button("👍", key=f"up_{idx}"):
                        log_feedback(st.session_state.messages[idx-1]["content"], msg["content"], 5)
                        st.toast("Feedback logged! Thank you.", icon="✨")
                with col2:
                    if st.button("👎", key=f"down_{idx}"):
                        log_feedback(st.session_state.messages[idx-1]["content"], msg["content"], 1)
                        st.toast("Feedback logged! We will improve.", icon="📝")

# Feedback logging function
def log_feedback(query, response, score):
    file_path = "feedback_log.csv"
    file_exists = os.path.exists(file_path)
    
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "User Query", "Bot Response", "Score (1-5)"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            query,
            response,
            score
        ])

# ----------------------------------------------------
# 💬 MULTI-TURN CHAT FLOW
# ----------------------------------------------------
# Suggestion Chips layout styled exactly as the mock pills
st.markdown("<div style='margin-bottom: 8px; font-size:11px; color:#8a6d3b; font-weight:600; letter-spacing:0.5px;'>SUGGESTED TOPICS</div>", unsafe_allow_html=True)
col_chip1, col_chip2, col_chip3 = st.columns(3)

# If clicked, append the message directly to trigger dialogue response on rerun
with col_chip1:
    if st.button("📈 Tech Performance", key="btn_tech"):
        st.session_state.messages.append({"role": "user", "content": "Explain the new tax slabs for FY 2024-25 and standard deduction."})
        st.rerun()
with col_chip2:
    if st.button("🏥 Healthcare Sector", key="btn_health"):
        st.session_state.messages.append({"role": "user", "content": "What are the tax deductions available for health insurance under Section 80D?"})
        st.rerun()
with col_chip3:
    if st.button("⚖️ Risk Tolerance", key="btn_risk"):
        st.session_state.messages.append({"role": "user", "content": "Explain how mutual fund investments are taxed in India."})
        st.rerun()

user_query = st.chat_input("Ask FinanceGuru about your investments...")

if user_query:
    # Render user bubble
    with st.chat_message("user"):
        st.write(user_query)
        
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Check if API is ready
    if not model:
        with st.chat_message("assistant"):
            st.error("Please configure your Gemini API Key in the sidebar or .env file to activate the chatbot.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Financial Guidelines..."):
                try:
                    # Construct conversational prompt for multi-turn dialogue memory
                    # We pass the history of the conversation to keep context
                    chat = model.start_chat(history=[])
                    
                    # Convert history format to GenAI Content objects
                    history_contents = []
                    for m in st.session_state.messages[:-1]:
                        role_name = "user" if m["role"] == "user" else "model"
                        history_contents.append({"role": role_name, "parts": [m["content"]]})
                    
                    chat.history = history_contents
                    
                    # Send message and receive response
                    response = chat.send_message(user_query)
                    bot_response = response.text
                    
                    st.write(bot_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.rerun()  # Rerun to refresh and present feedback buttons on latest response
                    
                except Exception as e:
                    st.error(f"Error calling LLM API: {str(e)}")
                    st.info("Check if your API Key is valid and you have sufficient quota.")
