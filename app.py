import os
import csv
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

from src.styles import CUSTOM_CSS
from src.config import SYSTEM_PROMPT, GUARDRAIL_ERROR_MESSAGE, get_generative_model
from src.gcp_services import record_feedback
from src.calculator import calculate_tax_old_regime, calculate_tax_new_regime

# Load environment variables
load_dotenv()

# Page configuration with premium layout: force sidebar to be open by default
st.set_page_config(
    page_title="FinanceGuru - Investment Strategy & Tax Planning Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom premium styles with accessibility classes
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------------------------------
# ⚙️ MULTI-ROOM CHAT & MEMORY SETUP
# ----------------------------------------------------
# Check query parameters for routing
chat_route = st.query_params.get("chat", "investment")

if chat_route == "tax":
    active_chat_title = "Tax Optimization & Planning Guide"
    active_chat_key = "tax"
else:
    active_chat_title = "Investment Strategy Discussion"
    active_chat_key = "investment"

# Initialize conversation history in Session State for both rooms
if "messages_investment" not in st.session_state:
    st.session_state.messages_investment = [
        {"role": "assistant", "content": "Hello Vaishnavi! I've analyzed your portfolio against the current market data. Here are tailored insights... Would you like to review specific sectors or risk adjustments?"}
    ]

if "messages_tax" not in st.session_state:
    st.session_state.messages_tax = [
        {"role": "assistant", "content": "Welcome to your Tax Planning portal, Vaishnavi! I can assist you with comparing Old vs New tax regimes, maximizing Section 80C/80D deductions, and planning your tax-saving deposits. What is your estimated total gross income?"}
    ]

# Select active messages set based on route
if active_chat_key == "tax":
    active_messages = st.session_state.messages_tax
else:
    active_messages = st.session_state.messages_investment

# ----------------------------------------------------
# ⚙️ API KEY CONFIGURATION & SIDEBAR
# ----------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")

# Sidebar setup matching high-fidelity layout
with st.sidebar:
    # Header Branding
    st.markdown("""
        <div class="logo-container" role="region" aria-label="FinanceGuru Brand Header">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" class="premium-logo-svg" role="img" aria-label="FinanceGuru Dotted Rotating Ring and Golden Hex Shield enclosing a growing investment graph line chart">
              <defs>
                <linearGradient id="gold-grad-1" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#dfba6b" />
                  <stop offset="50%" stop-color="#f5e0a3" />
                  <stop offset="100%" stop-color="#c5a059" />
                </linearGradient>
                <linearGradient id="gold-glow" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#dfba6b" stop-opacity="0.6"/>
                  <stop offset="100%" stop-color="#c5a059" stop-opacity="0.1"/>
                </linearGradient>
              </defs>
              <!-- Background Rotating Ring -->
              <circle cx="20" cy="20" r="17" stroke="url(#gold-glow)" stroke-width="1.2" fill="none" stroke-dasharray="3 3" class="rotating-ring" />
              <!-- Outer Hex Shield/Diamond -->
              <path d="M20 4 L36 12 L36 28 L20 36 L4 28 L4 12 Z" stroke="url(#gold-grad-1)" stroke-width="1.8" fill="none" />
              <!-- Inner geometric chart nodes and connecting line -->
              <path d="M13 24 L20 18 L27 14" stroke="url(#gold-grad-1)" stroke-width="1.8" stroke-linecap="round" fill="none" class="draw-line" />
              <circle cx="13" cy="24" r="2.5" fill="url(#gold-grad-1)" class="pulse-node-1" />
              <circle cx="20" cy="18" r="2.5" fill="url(#gold-grad-1)" class="pulse-node-2" />
              <circle cx="27" cy="14" r="2.5" fill="url(#gold-grad-1)" class="pulse-node-3" />
            </svg>
            <div style="display: flex; flex-direction: column;">
                <span class="shimmer-text" style="font-size: 20px; font-weight: 700; letter-spacing: 0.5px; line-height: 1.1;">FinanceGuru</span>
                <span style="font-size: 8.5px; font-weight: 600; color: #8e887d; letter-spacing: 2px; text-transform: uppercase; margin-top: 1.5px;">Wealth Portal</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Active user profile card
    st.markdown("""
        <div class="sidebar-profile-card" role="region" aria-label="User Profile">
            <div class="user-avatar-container" role="img" aria-label="Active Premium User profile status indicators">
                <span style="font-size: 18px; color: #ffffff;">👤</span>
                <div class="user-status-dot"></div>
            </div>
            <div class="profile-info">
                <span class="profile-name">Vaishnavi</span>
                <span class="profile-tier">Premium User</span>
            </div>
            <span class="profile-chevron">&gt;</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Active Chat Navigation Links (Working Routing via query parameters!)
    inv_class = "menu-item active" if active_chat_key == "investment" else "menu-item"
    tax_class = "menu-item active" if active_chat_key == "tax" else "menu-item"
    
    st.markdown(f"""
        <div class="menu-header" role="heading" aria-level="2">ACTIVE CHATS</div>
        <a href="/?chat=investment" target="_self" class="{inv_class}" role="link" aria-label="Navigate to Investment Strategy chat room">
            <svg class="chat-icon-svg" viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
            <span>Investment Strategy</span>
        </a>
        <a href="/?chat=tax" target="_self" class="{tax_class}" role="link" aria-label="Navigate to Tax Planning chat room">
            <svg class="chat-icon-svg" viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
            <span>Tax Planning</span>
        </a>
    """, unsafe_allow_html=True)
    
    # Widgets swap based on active page route
    st.markdown('<div class="menu-header">WIDGETS</div>', unsafe_allow_html=True)
    if active_chat_key == "investment":
        st.markdown("""
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
    else:
        st.markdown("""
            <div class="sidebar-widget">
                <span class="widget-title">80C Tax-Saving Limit</span>
                <span class="widget-value">₹1,50,000</span>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" style="width: 80%;"></div>
                </div>
                <span style="font-size:11px; color:#c5a059; font-weight:500; margin-top:2px; display:block;">₹1,20,000 Saved (80% Achieved)</span>
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

# Configure generative AI client if key exists using cached configuration
model = get_generative_model(api_key)

# Main Chat Header Bar showing active title route
st.markdown(f"""
    <div class="chat-header-bar">
        <span class="chat-header-title">{active_chat_title}</span>
        <div style="display: flex; gap: 16px; color: #8e887d; font-size: 18px;">
            <span style="cursor: pointer;">💬</span>
            <span style="cursor: pointer;">•••</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Render active chat history utilizing high-fidelity custom HTML design bubbles
chat_html = ""
for msg in active_messages:
    if msg["role"] == "assistant":
        chat_html += f"""
        <div class="msg-row bot">
            <div class="msg-avatar">F</div>
            <div class="msg-bubble">{msg["content"]}</div>
        </div>
        """
    else:
        chat_html += f"""
        <div class="msg-row user">
            <div class="msg-bubble">{msg["content"]}</div>
        </div>
        """

st.markdown(f'<div class="chat-container-custom">{chat_html}</div>', unsafe_allow_html=True)

# Feedback logging function
def log_feedback(query, response, score):
    record_feedback(query, response, score)

# Floating feedback triggers directly under the last bot message
if len(active_messages) > 1 and active_messages[-1]["role"] == "assistant":
    col_f1, col_f2, col_f3 = st.columns([0.05, 0.05, 0.9])
    with col_f1:
        if st.button("👍", key="up_feedback_main"):
            log_feedback(active_messages[-2]["content"], active_messages[-1]["content"], 5)
            st.toast("Feedback logged!", icon="✨")
    with col_f2:
        if st.button("👎", key="down_feedback_main"):
            log_feedback(active_messages[-2]["content"], active_messages[-1]["content"], 1)
            st.toast("Feedback logged!", icon="📝")

# Suggested Topic Chips container aligned on bottom right
st.markdown("<div style='margin-top: 24px; margin-bottom: 8px; font-size:11px; color:#8e887d; font-weight:700; letter-spacing:1px; text-transform:uppercase;'>Action Presets</div>", unsafe_allow_html=True)
col_chip1, col_chip2, col_chip3 = st.columns(3)

# Preset actions swap matching active page route
if active_chat_key == "investment":
    preset_1_text, preset_1_val = "Tech Performance", "Please show me the tech sector performance first."
    preset_2_text, preset_2_val = "Healthcare Sector", "What is the outlook and tax impact for the healthcare sector?"
    preset_3_text, preset_3_val = "Risk Tolerance Review", "Let's review my risk tolerance and asset allocation guidelines."
else:
    preset_1_text, preset_1_val = "New vs Old Regime", "Compare the New Tax Regime vs Old Tax Regime for ₹12 LPA gross salary."
    preset_2_text, preset_2_val = "Section 80C List", "What eligible investments can I make under Section 80C?"
    preset_3_text, preset_3_val = "Deduction Limits", "What is the maximum standard deduction and Section 80D limits?"

with col_chip1:
    if st.button(preset_1_text, key="btn_chip_1"):
        active_messages.append({"role": "user", "content": preset_1_val})
        st.rerun()
with col_chip2:
    if st.button(preset_2_text, key="btn_chip_2"):
        active_messages.append({"role": "user", "content": preset_2_val})
        st.rerun()
with col_chip3:
    if st.button(preset_3_text, key="btn_chip_3"):
        active_messages.append({"role": "user", "content": preset_3_val})
        st.rerun()

# Text input for chat
user_query = st.chat_input("Ask FinanceGuru about your investments...")

if user_query:
    # Append user question
    active_messages.append({"role": "user", "content": user_query})
    
    if not model:
        st.error("Please configure your Gemini API Key in the sidebar or .env file to activate the chatbot.")
    else:
        try:
            chat = model.start_chat(history=[])
            history_contents = []
            for m in active_messages[:-1]:
                role_name = "user" if m["role"] == "user" else "model"
                history_contents.append({"role": role_name, "parts": [m["content"]]})
            chat.history = history_contents
            
            response = chat.send_message(user_query)
            bot_response = response.text
            active_messages.append({"role": "assistant", "content": bot_response})
            st.rerun()
            
        except Exception as e:
            st.error(f"Error calling Gemini API: {str(e)}")
