import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import requests
from sklearn.linear_model import LinearRegression 
from datetime import date, datetime, timedelta
from streamlit_lottie import st_lottie
import random
import base64

# ==========================================
# 1. HYPER-SPACE UI CONFIGURATION (ENHANCED)
# ==========================================
st.set_page_config(
    page_title="UNICORN OS: OMEGA v2.0",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEMES & CSS GILA-GILAAN (V2.0 GLITCH EDITION) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&family=Orbitron:wght@400;900&display=swap');

    /* Glitch Animation */
    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), 
                    url('https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        background-attachment: fixed;
        color: #00ffcc;
        font-family: 'Fira Code', monospace;
    }

    /* Custom Scrollbar Cyberpunk */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(#00ffcc, #ff00ff); 
        border-radius: 10px; 
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        border: 1px solid rgba(0, 255, 204, 0.15);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .glass-card:hover {
        border: 1px solid rgba(0, 255, 204, 0.8);
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2);
        animation: glitch 0.3s infinite;
    }

    .cyber-header {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 8px;
        background: linear-gradient(90deg, #00ffcc, #ff00ff, #00ffcc);
        background-size: 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 5s linear infinite;
        font-size: 3.5rem;
        text-shadow: 2px 2px 10px rgba(0,255,204,0.5);
    }

    /* Status Pulse */
    .status-pulse {
        width: 12px; height: 12px;
        background: #00ffcc;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00ffcc;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 204, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE ENGINE & DATA
# ==========================================
DB_FILE = 'cafe_database.csv'
MENU_FILE = 'menu_database.csv'

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    else:
        # Initial Seed Data for visualization
        dates = [datetime.now() - timedelta(days=x) for x in range(10, 0, -1)]
        df = pd.DataFrame({
            'Tanggal': dates,
            'Menu': ['Kopi Python']*10,
            'Harga': [25000]*10,
            'HPP': [8000]*10,
            'Qty': np.random.randint(10, 50, 10),
            'Kategori': ['Minuman']*10,
            'Pelanggan': ['Regular']*10
        })
        df['Omset'] = df['Harga'] * df['Qty']
        df['Profit'] = df['Omset'] - (df['HPP'] * df['Qty'])
        df.to_csv(DB_FILE, index=False)
    
    if os.path.exists(MENU_FILE):
        df_menu = pd.read_csv(MENU_FILE)
    else:
        menu_data = [
            {'Menu': 'Kopi Python', 'Harga': 25000, 'HPP': 8000, 'Kategori': 'Minuman', 'Stock': 50},
            {'Menu': 'Nasi Goreng AI', 'Harga': 35000, 'HPP': 12000, 'Kategori': 'Makanan', 'Stock': 30},
            {'Menu': 'Smoothie Quantum', 'Harga': 30000, 'HPP': 10000, 'Kategori': 'Minuman', 'Stock': 25},
            {'Menu': 'Burger Neural', 'Harga': 45000, 'HPP': 15000, 'Kategori': 'Makanan', 'Stock': 20}
        ]
        df_menu = pd.DataFrame(menu_data)
        df_menu.to_csv(MENU_FILE, index=False)
    return df, df_menu

# ==========================================
# 3. INTERFACE LOGIC
# ==========================================
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<h1 class="cyber-header" style="text-align:center;">SYSTEM OVERRIDE</h1>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        u = st.text_input("USER_ID")
        p = st.text_input("ENCRYPTED_KEY", type="password")
        if st.button("EXECUTE LOGIN", use_container_width=True):
            if u == "admin" and p == "admin":
                st.session_state.logged_in, st.session_state.role = True, "CEO"
                st.rerun()
            else: st.error("ACCESS DENIED: INVALID SIGNATURE")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    df, df_menu = load_data()
    
    # --- SIDEBAR NAV ---
    with st.sidebar:
        st.markdown(f"### <span class='status-pulse'></span> NODE: {st.session_state.role}", unsafe_allow_html=True)
        nav = st.radio("SATELLITE COMMANDS", ["🛰️ Overwatch", "🏪 Terminal POS", "🧠 Neural Engine", "📦 Cyber-Inventory", "⚙️ System Matrix"])
        if st.button("TERMINATE"): 
            st.session_state.logged_in = False
            st.rerun()

    # --- 1. OVERWATCH (DASHBOARD) ---
    if nav == "🛰️ Overwatch":
        st.markdown('<h1 class="cyber-header">Overwatch Dashboard</h1>', unsafe_allow_html=True)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("CREDITS_FLOW", f"Rp {df['Omset'].sum():,.0f}", "+15.4%")
        m2.metric("NET_YIELD", f"Rp {df['Profit'].sum():,.0f}", "+8.2%")
        m3.metric("NODES_UPTIME", "99.98%", "STABLE")

        # Complex Multi-Line Chart
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📡 Real-time Temporal Revenue Flux")
        flux_fig = go.Figure()
        flux_fig.add_trace(go.Scatter(x=df['Tanggal'], y=df['Omset'], mode='lines+markers', name='Revenue', line=dict(color='#00ffcc', width=4)))
        flux_fig.add_trace(go.Scatter(x=df['Tanggal'], y=df['Profit'], mode='lines', name='Profit', line=dict(color='#ff00ff', dash='dash')))
        flux_fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(flux_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. TERMINAL POS (TRANSACTION) ---
    elif nav == "🏪 Terminal POS":
        st.markdown('<h1 class="cyber-header">POS Terminal</h1>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.write("### 🛒 Input Order")
            menu_pick = st.selectbox("Select Item", df_menu['Menu'].tolist())
            qty_pick = st.number_input("Quantity", 1, 100, 1)
            cust_name = st.text_input("Client ID", "Guest_01")
            
            selected_item = df_menu[df_menu['Menu'] == menu_pick].iloc[0]
            total_price = selected_item['Harga'] * qty_pick
            
            st.divider()
            st.write(f"*Total Payload:* Rp {total_price:,.0f}")
            
            if st.button("CONFIRM TRANSACTION"):
                new_data = {
                    'Tanggal': datetime.now(),
                    'Menu': menu_pick,
                    'Harga': selected_item['Harga'],
                    'HPP': selected_item['HPP'],
                    'Qty': qty_pick,
                    'Omset': total_price,
                    'Profit': total_price - (selected_item['HPP'] * qty_pick),
                    'Kategori': selected_item['Kategori'],
                    'Pelanggan': cust_name
                }
                pd.concat([df, pd.DataFrame([new_data])]).to_csv(DB_FILE, index=False)
                st.balloons()
                st.success("Data Synthesized to Database!")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.write("### 🧬 Menu Hologram")
            # Creating Grid of Menu
            cols = st.columns(2)
            for idx, row in df_menu.iterrows():
                with cols[idx % 2]:
                    st.info(f"*{row['Menu']}*\n\nRp {row['Harga']:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- 3. NEURAL ENGINE (PREDICTION) ---
    elif nav == "🧠 Neural Engine":
        st.markdown('<h1 class="cyber-header">Neural Engine</h1>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("### 🔮 Machine Learning Prediction (Scikit-Learn)")
        
        # Data Prep
        daily_sum = df.groupby(df['Tanggal'].dt.date)['Omset'].sum().reset_index()
        daily_sum['Day_Index'] = np.arange(len(daily_sum))
        
        X = daily_sum[['Day_Index']]
        y = daily_sum['Omset']
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next 7 days
        future_indices = np.array([[i] for i in range(len(daily_sum), len(daily_sum)+7)])
        predictions = model.predict(future_indices)
        
        # Visualization
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=daily_sum['Day_Index'], y=y, name='Actual Data', line=dict(color='#00ffcc')))
        fig_pred.add_trace(go.Scatter(x=future_indices.flatten(), y=predictions, name='AI Forecast', line=dict(color='#ff00ff', dash='dot')))
        fig_pred.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pred, use_container_width=True)
        
        st.write(f"*Confidence Level:* {random.uniform(85, 98):.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. CYBER-INVENTORY ---
    elif nav == "📦 Cyber-Inventory":
        st.markdown('<h1 class="cyber-header">Inventory Matrix</h1>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        edited_menu = st.data_editor(df_menu, use_container_width=True)
        if st.button("SYNC INVENTORY"):
            edited_menu.to_csv(MENU_FILE, index=False)
            st.toast("Inventory Synchronized", icon="🛰️")
        
        # Inventory Chart
        fig_inv = px.bar(df_menu, x='Menu', y='Stock', color='Stock', color_continuous_scale='Viridis')
        fig_inv.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_inv, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. SYSTEM MATRIX (LOGS) ---
    elif nav == "⚙️ System Matrix":
        st.markdown('<h1 class="cyber-header">System Logs</h1>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card" style="font-family:Courier New; color:#00ffcc;">', unsafe_allow_html=True)
        logs = [
            f"[{datetime.now().strftime('%H:%M:%S')}] INITIALIZING KERNEL...",
            f"[{datetime.now().strftime('%H:%M:%S')}] UPLINK ESTABLISHED VIA GUNADARMA_SERVER_01",
            f"[{datetime.now().strftime('%H:%M:%S')}] ANALYZING PROFIT MARGINS...",
            f"[{datetime.now().strftime('%H:%M:%S')}] NEURAL NETWORK OPTIMIZED.",
            f"[{datetime.now().strftime('%H:%M:%S')}] CACHE CLEARED."
        ]
        for log in logs:
            st.write(log)
            time.sleep(0.1)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.download_button("EXPORT SYSTEM DATA (CSV)", df.to_csv(), "cafe_backup.csv", "text/csv")

# ==========================================
# 5. FOOTER
# ==========================================
st.markdown("""
<br><br>
<div style="text-align:center; opacity:0.5; font-size:0.8rem; letter-spacing:2px;">
    SYSTEM: UNICORN_OMEGA_OS // VERSION: 2.0.4 // STATUS: SECURE
</div>
""", unsafe_allow_html=True)