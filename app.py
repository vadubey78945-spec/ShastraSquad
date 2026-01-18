
import streamlit as st
import time
import datetime
import pandas as pd
import random
import os
import google.generativeai as genai
from typing import List, Dict, Any

# --- CONFIGURATION ---
st.set_page_config(
    page_title="ShastraShield AI - Autonomous IoT Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini AI
if "API_KEY" in os.environ:
    genai.configure(api_key=os.environ["API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    model = None

# --- CUSTOM THEMING (ORANGE) ---
st.markdown("""
    <style>
    :root {
        --primary: #f97316;
        --bg-dark: #020617;
    }
    .stApp {
        background-color: #020617;
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        border-right: 1px solid rgba(249, 115, 22, 0.2);
    }
    .stButton>button {
        background-color: #f97316;
        color: #020617;
        font-weight: 800;
        text-transform: uppercase;
        border-radius: 12px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #fb923c;
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(249, 115, 22, 0.4);
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.4);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(249, 115, 22, 0.1);
        text-align: center;
    }
    .orange-glow {
        color: #f97316;
        text-shadow: 0 0 10px rgba(249, 115, 22, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)   # <--- Change 'stdio' to 'html'
# --- SESSION STATE INITIALIZATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'devices' not in st.session_state:
    st.session_state.devices = [
        {"id": "d1", "name": "Core Gateway", "type": "Router", "ip": "192.168.1.1", "status": "Secure", "anomaly": 0.02, "criticality": 10},
        {"id": "d2", "name": "Front Door Lock", "type": "Smart Lock", "ip": "192.168.1.42", "status": "Secure", "anomaly": 0.05, "criticality": 9},
        {"id": "d3", "name": "Backyard Cam", "type": "Camera", "ip": "192.168.1.55", "status": "Secure", "anomaly": 0.08, "criticality": 8},
    ]
if 'threat_history' not in st.session_state:
    st.session_state.threat_history = []
if 'protection_mode' not in st.session_state:
    st.session_state.protection_mode = "Protection"

# --- LOGIN PAGE ---
def login_page():
    st.markdown("<h1 style='text-align: center; text-transform: uppercase; font-weight: 900;'>ShastraShield AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; letter-spacing: 0.3em; text-transform: uppercase; font-size: 10px;'>Autonomous Security Agent</p>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)
            identity = st.text_input("Agent Identity", placeholder="Email or UID")
            password = st.text_input("Secret Key", type="password")
            if st.button("Establish Link", use_container_width=True):
                if identity and password: # Simple simulation
                    st.session_state.authenticated = True
                    st.session_state.user = identity
                    st.rerun()
                else:
                    st.error("Invalid Credentials Vault")

# --- AI AGENT SERVICES ---
def get_ai_explanation(threat_type, device_name):
    if not model:
        return "Anomaly neutralized via edge-level hardware baseline. Integrity Score: Optimal."
    
    prompt = f"Explain this IoT threat: {threat_type} targeting {device_name}. Keep it under 40 words, sound like an AI security agent."
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Behavioral drift detected. Automated isolation active."

# --- SIDEBAR & REAL-TIME CLOCK ---
def sidebar():
    with st.sidebar:
        st.markdown("<h2 class='orange-glow'>SHASTRA</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Real-time Clock
        clock_placeholder = st.empty()
        
        menu = ["Safety Hub", "Neural Hub", "IoT Inventory", "Adaptive Firewall", "Mitigation Center"]
        choice = st.radio("Navigation", menu)
        
        st.markdown("---")
        st.markdown(f"**Mode:** `{st.session_state.protection_mode}`")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
            
    return choice, clock_placeholder

# --- DASHBOARD SECTIONS ---
def dashboard():
    st.markdown("<h1 style='font-weight: 900;'>SAFETY HUB</h1>", unsafe_allow_html=True)
    
    # Top Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='metric-card'><h4>Integrity</h4><h2 style='color:#10b981'>98%</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h4>Active Nodes</h4><h2>{len(st.session_state.devices)}</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='metric-card'><h4>Threats</h4><h2 style='color:#f43f5e'>0</h2></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='metric-card'><h4>Latency</h4><h2 style='color:#f97316'>12ms</h2></div>", unsafe_allow_html=True)

    st.markdown("### Live Network Topology")
    # Simulation of a Network Graph using columns for layout
    col_net1, col_net2 = st.columns([2, 1])
    with col_net1:
        st.info("Neural Mesh active. Monitoring encrypted L3/L4 headers across 3 local subnets.")
        # Graphviz for topology
        import graphviz
        dot = graphviz.Digraph()
        dot.attr(bgcolor='transparent', fontcolor='white')
        dot.node('R', 'Router', color='#f97316', fontcolor='#f97316', style='bold')
        for d in st.session_state.devices:
            if d['type'] != 'Router':
                dot.node(d['id'], d['name'], color='#64748b', fontcolor='white')
                dot.edge('R', d['id'], color='#f9731633')
        st.graphviz_chart(dot)
    
    with col_net2:
        st.markdown("### Protection Controls")
        mode = st.toggle("Autonomous Protection", value=True)
        st.session_state.protection_mode = "Protection" if mode else "Learning"
        
        if st.button("Run Security Drill", use_container_width=True):
            with st.spinner("Simulating attack vector..."):
                time.sleep(2)
                st.toast("🚨 Anomaly detected on Backyard Cam!", icon="🔥")
                new_threat = {
                    "time": datetime.datetime.now().strftime("%H:%M:%S"),
                    "type": "Brute Force",
                    "target": "Backyard Cam",
                    "status": "Neutralized"
                }
                st.session_state.threat_history.insert(0, new_threat)

def inventory():
    st.markdown("<h1 style='font-weight: 900;'>IOT INVENTORY</h1>", unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.devices)
    st.table(df)
    
    with st.expander("Provision New Node"):
        name = st.text_input("Device Name")
        dtype = st.selectbox("Type", ["Camera", "Smart Lock", "Light", "TV", "NAS"])
        ip = st.text_input("Static IP", value="192.168.1.XX")
        if st.button("Link to Mesh"):
            new_dev = {"id": f"d{len(st.session_state.devices)+1}", "name": name, "type": dtype, "ip": ip, "status": "Secure", "anomaly": 0.0, "criticality": 5}
            st.session_state.devices.append(new_dev)
            st.success(f"{name} provisioned successfully.")
            st.rerun()

def neural_hub():
    st.markdown("<h1 style='font-weight: 900;'>NEURAL EVOLUTION</h1>", unsafe_allow_html=True)
    st.markdown("#### Local Neural Maturity: `Adaptive`")
    st.progress(0.88, text="Immunity Score: 88%")
    
    st.markdown("### Adaptation Log")
    log = [
        {"time": "14:22", "action": "Sync", "desc": "Fetched 12 new IoT CVE signatures."},
        {"time": "12:10", "action": "Learn", "desc": "Solidified baseline for Smart Lock."},
        {"time": "09:45", "action": "Drift", "desc": "Corrected clock skew on Core Router."}
    ]
    st.write(pd.DataFrame(log))

# --- MAIN APP ROUTING ---
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        choice, clock_placeholder = sidebar()
        
        # Keep clock ticking
        now = datetime.datetime.now()
        clock_placeholder.markdown(f"""
            <div style='text-align: center;'>
                <h3 style='color: #f97316; margin-bottom: 0;'>{now.strftime("%H:%M:%S")}</h3>
                <p style='color: #64748b; font-size: 10px;'>{now.strftime("%d %b %Y")}</p>
            </div>
        """, unsafe_allow_html=True)

        if choice == "Safety Hub":
            dashboard()
        elif choice == "IoT Inventory":
            inventory()
        elif choice == "Neural Hub":
            neural_hub()
        else:
            st.info(f"The {choice} module is running in background autonomous mode.")
            
        # Global Threat Monitor (Mini-feed)
        if st.session_state.threat_history:
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 🚨 Critical Alerts")
            for t in st.session_state.threat_history[:3]:
                st.sidebar.error(f"**{t['type']}** @ {t['target']}\n\n*Auto-{t['status']}*")

if __name__ == "__main__":
    main()
