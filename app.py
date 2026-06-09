import os
import csv
from datetime import datetime
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration with premium layout set to wide for true mockup layout matching
st.set_page_config(
    page_title="FinanceGuru - Investment Strategy & Tax Planning Portal",
    page_icon="💰",
    layout="wide"
)

# Custom premium CSS to match the high-fidelity FinanceGuru Luxury UI Colors palette
st.markdown("""
<style>
    /* Hide default Streamlit header, footer, and borders for a clean white-label appearance */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden; height: 0px !important;}
    .stDecoration {display: none !important;}
    
    /* Luxury dark background */
    .stApp {
        background: #0f0f11 !important;
    }

    /* Main body text color (Cream/Off-White) and standard font family */
    .main, .main h1, .main h2, .main h3, .main p, .main span, .main li {
        color: #eaeaea !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Top Navbar simulator matching the header in right chat area */
    .chat-header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(223, 186, 107, 0.1);
        padding-bottom: 14px;
        margin-bottom: 24px;
    }
    
    .chat-header-title {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* Target Streamlit chat message containers and override styling */
    .stChatMessage {
        border-radius: 18px !important;
        margin-bottom: 16px !important;
        padding: 16px 20px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        max-width: 85%;
    }
    
    /* User chat bubble: Champagne-Gold gradient with dark text */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background: linear-gradient(135deg, #dfba6b 0%, #c5a059 100%) !important;
        border-top-right-radius: 4px !important;
        float: right !important;
        clear: both;
    }
    .stChatMessage[data-testid="stChatMessageUser"] * {
        color: #0d0d0f !important;
        font-weight: 500 !important;
    }
    
    /* Assistant chat bubble: Charcoal background with soft white text */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #1e1e21 !important;
        border-top-left-radius: 4px !important;
        float: left !important;
        clear: both;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] * {
        color: #eaeaea !important;
    }
    
    /* Custom CSS to format the circular gold letter avatar icons */
    div[data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #dfba6b 0%, #c5a059 100%) !important;
        color: #0d0d0f !important;
    }
    div[data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #dfba6b 0%, #c5a059 100%) !important;
        color: #0d0d0f !important;
        box-shadow: 0 0 10px rgba(223, 186, 107, 0.3) !important;
    }
    
    /* Custom styles for sidebar elements specifically */
    section[data-testid="stSidebar"] {
        background-color: #18181a !important;
        border-right: 1px solid rgba(223, 186, 107, 0.08) !important;
    }
    section[data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide standard sidebar widgets to make room for custom layout */
    section[data-testid="stSidebar"] div.stMarkdown {
        margin-bottom: 0px;
    }
    
    /* Sidebar user profile card */
    .sidebar-profile-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #222224;
        border: 1px solid rgba(223, 186, 107, 0.08);
        padding: 12px 14px;
        border-radius: 12px;
        margin-bottom: 24px;
        margin-top: 10px;
    }
    
    .user-avatar-container {
        position: relative;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #111;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1.5px solid #dfba6b;
    }
    
    .user-status-dot {
        position: absolute;
        bottom: 0;
        right: 0;
        width: 9px;
        height: 9px;
        background-color: #4caf50;
        border: 2px solid #222224;
        border-radius: 50%;
    }
    
    .profile-info {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        margin-left: 12px;
    }
    .profile-name {
        font-weight: 600;
        color: #ffffff;
        font-size: 13.5px;
    }
    .profile-tier {
        font-size: 11px;
        color: #dfba6b;
        font-weight: 500;
    }
    
    .profile-chevron {
        color: #8e887d;
        font-size: 12px;
        font-weight: bold;
    }

    /* Menu label headers */
    .menu-header {
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #8e887d;
        margin: 24px 0 10px 0;
        text-transform: uppercase;
    }
    
    /* Chat items */
    .menu-item {
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 13.5px;
        color: #8e887d;
        margin-bottom: 6px;
        border: 1px solid transparent;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .menu-item:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.02);
    }
    .menu-item.active {
        background: rgba(223, 186, 107, 0.03) !important;
        border: 1px solid rgba(223, 186, 107, 0.25) !important;
        color: #dfba6b !important;
        font-weight: 600;
        box-shadow: 0 0 10px rgba(223, 186, 107, 0.05);
    }
    
    .chat-icon-svg {
        width: 16px;
        height: 16px;
        fill: currentColor;
    }

    /* Gold balance widget with custom sparkline */
    .sidebar-widget {
        background: #222224;
        border: 1px solid rgba(223, 186, 107, 0.08);
        padding: 16px;
        border-radius: 14px;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .widget-title {
        font-size: 12px;
        color: #8e887d;
    }
    .widget-value {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .widget-sparkline {
        height: 48px;
        width: 100%;
        margin-top: 6px;
    }

    /* Market watch items */
    .market-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-size: 13px;
    }
    .market-ticker {
        color: #eaeaea;
    }
    .market-change {
        color: #4caf50;
        font-weight: 600;
    }
    
    /* Custom styling for text area input inside the sidebar (API Key validation) */
    section[data-testid="stSidebar"] div[data-baseweb="input"] {
        background-color: #1e1e21 !important;
        border: 1px solid rgba(223, 186, 107, 0.15) !important;
        border-radius: 10px !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="input"] input {
        color: #eaeaea !important;
        background-color: transparent !important;
    }
    
    /* Glowing chat input bar at bottom */
    .stChatInputContainer {
        border-color: rgba(223, 186, 107, 0.25) !important;
        background-color: #111113 !important;
        box-shadow: 0 0 15px rgba(223, 186, 107, 0.08) !important;
        border-radius: 30px !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #dfba6b !important;
        box-shadow: 0 0 20px rgba(223, 186, 107, 0.15) !important;
    }
    .stChatInput textarea {
        color: #ffffff !important;
    }
    
    /* Gold-gradient buttons overrides for the suggested topic chips */
    div.stButton > button {
        background: linear-gradient(135deg, #dfba6b 0%, #c5a059 100%) !important;
        color: #0d0d0f !important;
        border: none !important;
        border-radius: 24px !important;
        font-size: 13px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(223, 186, 107, 0.25) !important;
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
api_key = os.getenv("GEMINI_API_KEY")

# Sidebar setup matching high-fidelity layout
with st.sidebar:
    # Header Branding
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #dfba6b 0%, #c5a059 100%); display: flex; align-items: center; justify-content: center; font-weight: 800; color: #0d0d0f; font-size: 16px;">F</div>
            <span style="font-size: 19px; font-weight: 700; color: #ffffff; letter-spacing: 0.5px;">FinanceGuru</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Active user profile card
    st.markdown("""
        <div class="sidebar-profile-card">
            <div class="user-avatar-container">
                <span style="font-size: 18px; color: #ffffff;">👤</span>
                <div class="user-status-dot"></div>
            </div>
            <div class="profile-info">
                <span class="profile-name">Alex R.</span>
                <span class="profile-tier">Premium User</span>
            </div>
            <span class="profile-chevron">&gt;</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("""
        <div class="menu-header">ACTIVE CHATS</div>
        <div class="menu-item active">
            <svg class="chat-icon-svg" viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" fill="#dfba6b" /></svg>
            <span style="margin-left: 8px;">Investment Strategy</span>
        </div>
        <div class="menu-item">
            <svg class="chat-icon-svg" viewBox="0 0 24 24"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z" fill="#8e887d" /></svg>
            <span style="margin-left: 8px;">Tax Planning</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Widgets
    st.markdown("""
        <div class="menu-header">WIDGETS</div>
        <div class="sidebar-widget">
            <span class="widget-title">Portfolio Balance</span>
            <span class="widget-value">$1,245,670</span>
            <div class="widget-sparkline">
                <svg width="100%" height="100%" viewBox="0 0 100 30" preserveAspectRatio="none">
                    <defs>
                        <linearGradient id="gold-spark-grad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#dfba6b" stop-opacity="0.35"/>
                            <stop offset="100%" stop-color="#dfba6b" stop-opacity="0"/>
                        </linearGradient>
                    </defs>
                    <path d="M0,25 Q15,20 30,22 T60,5 T85,15 L100,10 L100,30 L0,30 Z" fill="url(#gold-spark-grad)" />
                    <path d="M0,25 Q15,20 30,22 T60,5 T85,15 L100,10" fill="none" stroke="#dfba6b" stroke-width="1.5" />
                </svg>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Market Watch
    st.markdown("""
        <div class="menu-header">MARKET WATCH</div>
        <div class="market-row">
            <span class="market-ticker">S&P 500</span>
            <span class="market-change">+0.72%</span>
        </div>
        <div class="market-row">
            <span class="market-ticker">BTC</span>
            <span class="market-change">+1.2%</span>
        </div>
    """, unsafe_allow_html=True)

    # API key setup fallback
    if not api_key:
        st.warning("⚠️ API key missing in environment (.env)")
        api_key_input = st.text_input("Enter Gemini Key manually:", type="password")
        if api_key_input:
            api_key = api_key_input
            st.success("API Key loaded!")
    else:
        st.caption("🟢 Connection: Active")

# Configure generative AI client if key exists
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
else:
    model = None

# Main Chat Header Bar
st.markdown("""
    <div class="chat-header-bar">
        <span class="chat-header-title">Investment Strategy Discussion</span>
        <div style="display: flex; gap: 16px; color: #8e887d;">
            <span style="cursor: pointer;">💬</span>
            <span style="cursor: pointer;">•••</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize conversation history in Session State
if "messages" not in st.session_state:
    # Pre-populate with a greeting matching the mock sequence if empty
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello Alex! I've analyzed your portfolio against the current market data. Here are tailored insights... Would you like to review specific sectors or risk adjustments?"}
    ]

# Display conversation history
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        # Add feedback logging buttons to Assistant messages
        if msg["role"] == "assistant" and idx > 0:
            if idx == len(st.session_state.messages) - 1:
                col_f1, col_f2, col_f3 = st.columns([0.05, 0.05, 0.9])
                with col_f1:
                    if st.button("👍", key=f"up_{idx}"):
                        log_feedback(st.session_state.messages[idx-1]["content"], msg["content"], 5)
                        st.toast("Feedback logged!", icon="✨")
                with col_f2:
                    if st.button("👎", key=f"down_{idx}"):
                        log_feedback(st.session_state.messages[idx-1]["content"], msg["content"], 1)
                        st.toast("Feedback logged!", icon="📝")

# Feedback logging function
def log_feedback(query, response, score):
    file_path = "feedback_log.csv"
    file_exists = os.path.exists(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "User Query", "Bot Response", "Score (1-5)"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query, response, score])

# Suggested Topic Chips container aligned on bottom right
st.markdown("<div style='margin-top: 16px; margin-bottom: 8px; font-size:11px; color:#8e887d; font-weight:700; letter-spacing:1px; text-transform:uppercase;'>Action Presets</div>", unsafe_allow_html=True)
col_chip1, col_chip2, col_chip3 = st.columns(3)

with col_chip1:
    if st.button("Tech Performance", key="btn_tech"):
        st.session_state.messages.append({"role": "user", "content": "Please show me the tech sector performance first."})
        st.rerun()
with col_chip2:
    if st.button("Healthcare Sector", key="btn_health"):
        st.session_state.messages.append({"role": "user", "content": "What is the outlook and tax impact for the healthcare sector?"})
        st.rerun()
with col_chip3:
    if st.button("Risk Tolerance Review", key="btn_risk"):
        st.session_state.messages.append({"role": "user", "content": "Let's review my risk tolerance and asset allocation guidelines."})
        st.rerun()

# Text input for chat
user_query = st.chat_input("Ask FinanceGuru about your investments...")

if user_query:
    with st.chat_message("user"):
        st.write(user_query)
        
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    if not model:
        with st.chat_message("assistant"):
            st.error("Please configure your Gemini API Key in the sidebar or .env file to activate the chatbot.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Market Insights..."):
                try:
                    chat = model.start_chat(history=[])
                    history_contents = []
                    for m in st.session_state.messages[:-1]:
                        role_name = "user" if m["role"] == "user" else "model"
                        history_contents.append({"role": role_name, "parts": [m["content"]]})
                    chat.history = history_contents
                    
                    response = chat.send_message(user_query)
                    bot_response = response.text
                    st.write(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error calling Gemini API: {str(e)}")
