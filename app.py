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

# ==========================================
# 1. HYPER-SPACE UI CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="UNICORN OS: OMEGA",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEMES & CSS GILA-GILAAN ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&family=Orbitron:wght@400;900&display=swap');

    /* Global Cyberpunk Reset */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1614850523296-d8c1af93d400?q=80&w=2070&auto=format&fit=crop');
        background-size: cover;
        color: #00ffcc;
        font-family: 'Fira Code', monospace;
    }

    /* Scanline Effect ala Monitor Jadul */
    .stApp::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 2;
        background-size: 100% 4px, 3px 100%;
        pointer-events: none;
    }

    /* Glassmorphism Card Ultra */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 204, 0.2);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 204, 0.1);
        margin-bottom: 20px;
    }

    /* Neon Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc !important;
        text-shadow: 0 0 10px #00ffcc;
    }

    /* Custom Header */
    .cyber-header {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 5px;
        background: linear-gradient(to right, #00ffcc, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA ENGINE (Gak Berubah, Tetap Solid) ---
DB_FILE = 'cafe_database.csv'
MENU_FILE = 'menu_database.csv'

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

def load_data():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    else:
        df = pd.DataFrame(columns=['Tanggal', 'Menu', 'Harga', 'HPP', 'Qty', 'Omset', 'Profit', 'Kategori', 'Pelanggan'])
    
    if os.path.exists(MENU_FILE):
        df_menu = pd.read_csv(MENU_FILE)
    else:
        menu_data = [{'Menu': 'Kopi Python', 'Harga': 25000, 'HPP': 8000, 'Kategori': 'Minuman', 'Img': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=400'}]
        df_menu = pd.DataFrame(menu_data)
        df_menu.to_csv(MENU_FILE, index=False)
    return df, df_menu

def save_transaksi(new_row):
    df_old, _ = load_data()
    df_new = pd.concat([df_old, pd.DataFrame([new_row])], ignore_index=True)
    df_new.to_csv(DB_FILE, index=False)

# ==========================================
# 2. LOGIN PROTOCOL
# ==========================================
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    lottie_coding = load_lottie("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    st.markdown('<h1 class="cyber-header">UNICORN OS ACCESS</h1>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st_lottie(lottie_coding, height=200)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        u = st.text_input("IDENT_USER")
        p = st.text_input("SECRET_PASS", type="password")
        if st.button("🔓 DECRYPT & ENTER", use_container_width=True):
            if u == "admin" and p == "admin":
                st.session_state.logged_in, st.session_state.role = True, "CEO"
                st.rerun()
            elif u == "kasir" and p == "kasir":
                st.session_state.logged_in, st.session_state.role = True, "STAFF"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. MAIN INTERFACE
# ==========================================
else:
    df, df_menu = load_data()
    
    with st.sidebar:
        st.markdown(f"### ⚡ SYSTEM: {st.session_state.role}")
        st.caption(f"📅 {datetime.now().strftime('%A, %d %B %Y')}")
        st.divider()
        if st.session_state.role == "CEO":
            nav = st.sidebar.selectbox("COMMAND:", ["🛰️ Overview", "🧠 Neural Prediction", "⚙️ Data Matrix"])
        else:
            nav = st.sidebar.selectbox("COMMAND:", ["🏪 POS Terminal"])
        
        if st.sidebar.button("🔌 TERMINATE SESSION"):
            st.session_state.logged_in = False
            st.rerun()

    # --- TAB: OVERVIEW (DASHBOARD) ---
    if nav == "🛰️ Overview":
        st.markdown('<h1 class="cyber-header">Global Analytics</h1>', unsafe_allow_html=True)
        
        # Floating Metrics
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("TOTAL_OMSET", f"Rp {df['Omset'].sum():,.0f}", "+12%")
        with col2: st.metric("NET_PROFIT", f"Rp {df['Profit'].sum():,.0f}", "+5%")
        with col3: st.metric("NODES_ACTIVE", f"{len(df)} Units")

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Temporal Flux (Revenue)")
        daily = df.groupby('Tanggal')['Omset'].sum().reset_index()
        fig = px.area(daily, x='Tanggal', y='Omset', color_discrete_sequence=['#00ffcc'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#fff", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB: AI PREDICTION (MATH EXPERT) ---
    elif nav == "🧠 Neural Prediction":
        st.markdown('<h1 class="cyber-header">Neural Forecast</h1>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("### 📐 Mathematical Kernel")
        st.latex(r"Y_{forecast} = \alpha + \beta X + \epsilon")
        st.caption("Linear Regression Model - Scikit-Learn Engine")
        
        if st.button("🌀 INITIATE DEEP LEARNING"):
            daily = df.groupby('Tanggal')['Omset'].sum().reset_index()
            if len(daily) < 3:
                st.error("INSUFFICIENT DATA: Zan, minimal 3 hari jualan!")
            else:
                daily['X'] = np.arange(len(daily))
                model = LinearRegression().fit(daily[['X']], daily['Omset'])
                
                # Prediksi 30 Hari (Gila-gilaan!)
                future_x = np.array([len(daily) + i for i in range(30)]).reshape(-1, 1)
                preds = model.predict(future_x)
                f_dates = [daily['Tanggal'].max() + timedelta(days=i) for i in range(1, 31)]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=daily['Tanggal'], y=daily['Omset'], name="Past Realities", line=dict(color='#00ffcc', width=4)))
                fig.add_trace(go.Scatter(x=f_dates, y=preds, name="AI Future Cloud", fill='tonexty', line=dict(color='#ff00ff', dash='dot')))
                fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
                
                st.success(f"LEARNING COMPLETE | ACCURACY: {model.score(daily[['X']], daily['Omset'])*100:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB: POS TERMINAL (UI/UX DEWA) ---
    elif nav == "🏪 POS Terminal":
        st.markdown('<h1 class="cyber-header">Transaction Hub</h1>', unsafe_allow_html=True)
        c1, c2 = st.columns([1.8, 1])
        
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🛒 Grid System Menu")
            cols = st.columns(2)
            for idx, row in df_menu.iterrows():
                with cols[idx % 2]:
                    with st.container():
                        st.image(row['Img'] if 'Img' in row else "https://via.placeholder.com/150", use_container_width=True)
                        if st.button(f"SELECT {row['Menu']}", key=f"pos_{idx}", use_container_width=True):
                            if 'cart' not in st.session_state: st.session_state.cart = []
                            st.session_state.cart.append(row.to_dict())
                            st.toast(f"Synchronizing {row['Menu']}...")
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("📋 Buffer Cart")
            if 'cart' in st.session_state and st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.table(cart_df[['Menu', 'Harga']])
                total = cart_df['Harga'].sum()
                st.markdown(f"## TOTAL: Rp {total:,.0f}")
                if st.button("🔥 DEPLOY TO DATABASE", use_container_width=True, type="primary"):
                    for _, r in cart_df.iterrows():
                        save_transaksi({'Tanggal': datetime.now(), 'Menu': r['Menu'], 'Harga': r['Harga'], 'HPP': r['HPP'], 'Qty': 1, 'Omset': r['Harga'], 'Profit': r['Harga']-r['HPP'], 'Kategori': r['Kategori'], 'Pelanggan': 'Guest'})
                    st.session_state.cart = []
                    st.success("DATA SECURED."); st.balloons(); time.sleep(1); st.rerun()
            else:
                st.write("BUFFER EMPTY")
            st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER TERMINAL ---
st.markdown("<br><center><p style='font-family:Orbitron; color:rgba(0,255,204,0.3)'>[ SYSTEM V5.0 OMEGA PROTOCOL | DEV: ZAN GUNADARMA ]</p></center>", unsafe_allow_html=True)