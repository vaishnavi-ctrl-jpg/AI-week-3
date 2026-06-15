# Accessibility roles and clean CSS styling references.
# The styling must remain exactly identical to preserve the user's hard-designed layout.

CUSTOM_CSS = """
<style>
    /* Hide default Streamlit menus and footers but preserve the top header container for the sidebar toggle */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Make the header bar transparent and click-through, but preserve the toggle button on the left */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    /* Hide top-right Streamlit developer toolbar buttons (Deploy, Settings, etc.) */
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
    }
    
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
    
    /* --- CUSTOM HIGH-FIDELITY CHAT CONTAINER & BUBBLES --- */
    .chat-container-custom {
        display: flex;
        flex-direction: column;
        gap: 18px;
        margin-bottom: 20px;
    }
    
    .msg-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        max-width: 80%;
    }
    
    .msg-row.bot {
        align-self: flex-start;
    }
    
    .msg-row.user {
        align-self: flex-end;
        flex-direction: row-reverse;
    }
    
    .msg-avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #dfba6b 0%, #c5a059 100%);
        color: #0d0d0f;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 14px;
        box-shadow: 0 0 12px rgba(223, 186, 107, 0.35);
        flex-shrink: 0;
        margin-top: 2px;
    }
    
    .msg-bubble {
        padding: 14px 18px;
        border-radius: 18px;
        font-size: 14.5px;
        line-height: 1.55;
    }
    
    .msg-row.bot .msg-bubble {
        background-color: #1e1e21;
        border: 1px solid rgba(223, 186, 107, 0.06);
        color: #eaeaea;
        border-top-left-radius: 4px;
    }
    
    .msg-row.user .msg-bubble {
        background: linear-gradient(135deg, #dfba6b 0%, #c5a059 100%);
        color: #0d0d0f;
        border-top-right-radius: 4px;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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
    
    /* Chat items links */
    .menu-item {
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 13.5px;
        color: #8e887d !important;
        margin-bottom: 6px;
        border: 1px solid transparent;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        text-decoration: none !important;
        transition: all 0.2s ease;
    }
    .menu-item:hover {
        color: #ffffff !important;
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
    
    .progress-bar-container {
        background: #0f0f11;
        height: 6px;
        border-radius: 3px;
        overflow: hidden;
        margin: 4px 0;
    }
    .progress-bar-fill {
        background: linear-gradient(90deg, #c5a059, #dfba6b);
        height: 100%;
        border-radius: 3px;
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

    /* Premium Logo & Text Shimmer Styles */
    @keyframes spin-slow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    @keyframes pulse-gentle {
        0%, 100% { transform: scale(1); filter: drop-shadow(0 0 2px rgba(223,186,107,0.3)); }
        50% { transform: scale(1.04); filter: drop-shadow(0 0 10px rgba(223,186,107,0.6)); }
    }
    @keyframes node-pulse {
        0%, 100% { transform: scale(1); opacity: 0.6; }
        50% { transform: scale(1.4); opacity: 1; }
    }
    @keyframes line-draw {
        0% { stroke-dasharray: 0 40; stroke-dashoffset: 0; }
        50% { stroke-dasharray: 40 40; stroke-dashoffset: 0; }
        100% { stroke-dasharray: 40 40; stroke-dashoffset: -40; }
    }
    @keyframes gold-shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    .rotating-ring {
        transform-origin: 20px 20px;
        animation: spin-slow 25s linear infinite;
    }
    .premium-logo-svg {
        animation: pulse-gentle 4s ease-in-out infinite;
    }
    .pulse-node-1 {
        transform-origin: 13px 24px;
        animation: node-pulse 2s infinite ease-in-out;
    }
    .pulse-node-2 {
        transform-origin: 20px 18px;
        animation: node-pulse 2s infinite ease-in-out 0.4s;
    }
    .pulse-node-3 {
        transform-origin: 27px 14px;
        animation: node-pulse 2s infinite ease-in-out 0.8s;
    }
    .draw-line {
        stroke-dasharray: 40;
        animation: line-draw 4s infinite ease-in-out;
    }
    .shimmer-text {
        background: linear-gradient(90deg, #ffffff 0%, #dfba6b 25%, #f5e0a3 50%, #dfba6b 75%, #ffffff 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gold-shimmer 4s linear infinite;
    }
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 24px;
        margin-top: 5px;
        padding: 8px 12px;
        border-radius: 14px;
        background: rgba(223, 186, 107, 0.02);
        border: 1px solid rgba(223, 186, 107, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: inset 0 0 12px rgba(223, 186, 107, 0.03);
    }
    .logo-container:hover {
        background: rgba(223, 186, 107, 0.05);
        border-color: rgba(223, 186, 107, 0.25);
        box-shadow: 0 4px 20px rgba(223, 186, 107, 0.1), inset 0 0 16px rgba(223, 186, 107, 0.05);
        transform: translateY(-1px);
    }
</style>
"""
