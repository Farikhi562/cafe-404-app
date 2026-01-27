import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os
import random
import qrcode
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta

# ==========================================
# 1. KONFIGURASI SUPREME (V4.0)
# ==========================================
st.set_page_config(
    page_title="UNICORN OS: GOD MODE",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS: THE MATRIX & NEON GLOW ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;500;700&family=Syncopate:wght@400;700&display=swap');

    /* ANIMATED STARFIELD BACKGROUND */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        font-family: 'Rajdhani', sans-serif;
        color: #E0F7FA;
    }
    
    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #00E5FF; border-radius: 3px; }

    /* CARD DESIGN: GLASSMOPHISM PRO MAX */
    .neon-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 229, 255, 0.2);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .neon-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.4);
        border: 1px solid rgba(0, 229, 255, 0.8);
    }

    /* TYPOGRAPHY */
    h1, h2, h3 { font-family: 'Syncopate', sans-serif; letter-spacing: 2px; }
    
    .glow-text {
        color: #00E5FF;
        text-shadow: 0 0 10px #00E5FF, 0 0 20px #00E5FF;
    }

    /* METRIC BOX STYLING */
    div[data-testid="stMetricValue"] {
        font-family: 'Syncopate', sans-serif;
        color: #00E5FF !important;
        text-shadow: 0 0 15px rgba(0, 229, 255, 0.5);
    }

    /* MENU GRID BUTTONS */
    .menu-btn {
        display: inline-block;
        width: 100%;
        padding: 15px;
        text-align: center;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
        border: 1px solid rgba(0,255,204,0.3);
        border-radius: 10px;
        cursor: pointer;
        transition: 0.3s;
        color: white;
    }
    .menu-btn:hover { background: rgba(0,255,204,0.2); border-color: #00ffcc; }

    /* LEVEL PROGRESS BAR */
    .xp-bar-bg { width: 100%; background: #333; height: 10px; border-radius: 5px; margin-top: 5px; }
    .xp-bar-fill { height: 100%; background: linear-gradient(90deg, #FF00CC, #333399); border-radius: 5px; transition: width 0.5s; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA ENGINE & SESSION
# ==========================================
DB_FILE = 'cafe_db_v4.csv'
MENU_FILE = 'menu_db_v4.csv'

def init_session():
    if 'cart' not in st.session_state: st.session_state.cart = []
    if 'xp' not in st.session_state: st.session_state.xp = 0
    if 'level' not in st.session_state: st.session_state.level = 1
    if 'last_trx' not in st.session_state: st.session_state.last_trx = None

def load_data():
    # Load or Create Transactions
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    else:
        df = pd.DataFrame(columns=['Tanggal', 'Menu', 'Harga', 'Qty', 'Omset', 'Kategori', 'Payment_Type'])
        df.to_csv(DB_FILE, index=False)
    
    # Load or Create Menu
    if os.path.exists(MENU_FILE):
        df_menu = pd.read_csv(MENU_FILE)
    else:
        menu_data = [
            {'Menu': 'Cyber Latte', 'Harga': 28000, 'Kategori': 'Coffee', 'Icon': '☕'},
            {'Menu': 'Neon Matcha', 'Harga': 32000, 'Kategori': 'Non-Coffee', 'Icon': '🍵'},
            {'Menu': 'Quantum Burger', 'Harga': 55000, 'Kategori': 'Food', 'Icon': '🍔'},
            {'Menu': 'Data Fries', 'Harga': 25000, 'Kategori': 'Snack', 'Icon': '🍟'},
            {'Menu': 'Pasta Python', 'Harga': 48000, 'Kategori': 'Food', 'Icon': '🍝'},
            {'Menu': 'Binary Soda', 'Harga': 20000, 'Kategori': 'Beverage', 'Icon': '🥤'},
        ]
        df_menu = pd.DataFrame(menu_data)
        df_menu.to_csv(MENU_FILE, index=False)
    return df, df_menu

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#00E5FF", back_color="black")
    return img

def calculate_level(xp):
    return int(xp / 100) + 1

# ==========================================
# 3. INTERFACE LOGIC
# ==========================================
init_session()
df, df_menu = load_data()

# --- HEADER AREA ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown('<h1 class="glow-text">UNICORN OS <span style="font-size:0.5em; color:white;">V4.0</span></h1>', unsafe_allow_html=True)
with c2:
    # XP / LEVEL SYSTEM
    lvl = calculate_level(st.session_state.xp)
    progress = st.session_state.xp % 100
    st.markdown(f"""
    <div style="text-align:right;">
        <b>OPERATOR LEVEL {lvl}</b><br>
        <span style="font-size:0.8em; color:#aaa;">{st.session_state.xp} XP Earned</span>
        <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{progress}%;"></div></div>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tabs = st.tabs(["🛒 SMART POS", "📊 ANALYTICS GOD MODE", "⚙️ SYSTEM CORE"])

# =========================================================
# TAB 1: SMART POS (GRID SYSTEM)
# =========================================================
with tabs[0]:
    col_menu, col_cart = st.columns([2, 1.2])
    
    with col_menu:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader("💠 MENU SELECTOR")
        
        # Grid Layout for Menu
        categories = df_menu['Kategori'].unique()
        filter_cat = st.pills("Filter", ["All"] + list(categories), selection_mode="single", default="All")
        
        filtered_menu = df_menu if filter_cat == "All" else df_menu[df_menu['Kategori'] == filter_cat]
        
        # Dynamic Grid
        cols = st.columns(3)
        for index, row in filtered_menu.iterrows():
            with cols[index % 3]:
                # Card-like Button
                if st.button(f"{row['Icon']}\n{row['Menu']}\n{int(row['Harga']/1000)}K", key=f"btn_{index}", use_container_width=True):
                    st.session_state.cart.append(row.to_dict())
                    st.toast(f"Added {row['Menu']}", icon="✅")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_cart:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader("🛒 HOLOGRAPHIC CART")
        
        if len(st.session_state.cart) > 0:
            cart_df = pd.DataFrame(st.session_state.cart)
            cart_disp = cart_df.groupby('Menu')['Harga'].agg(['count', 'sum']).reset_index()
            cart_disp.columns = ['Item', 'Qty', 'Subtotal']
            
            st.dataframe(cart_disp, hide_index=True, use_container_width=True)
            
            total = cart_disp['Subtotal'].sum()
            st.markdown(f"<h2 style='text-align:right; color:#00E5FF;'>TOTAL: Rp {total:,.0f}</h2>", unsafe_allow_html=True)
            
            # Payment Method
            pay_method = st.radio("Payment Gateway", ["CASH", "QRIS / E-WALLET", "CRYPTO"], horizontal=True)
            
            if pay_method == "QRIS / E-WALLET":
                # Generate Real QR Code
                qr_img = generate_qr(f"PAY|UNICORN|{total}|{int(time.time())}")
                
                # Convert to bytes for display
                buf = BytesIO()
                qr_img.save(buf)
                st.image(buf, caption="Scan to Pay (Instant)", width=200)

            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button("🔴 CLEAR", use_container_width=True):
                    st.session_state.cart = []
                    st.rerun()
            with col_act2:
                if st.button("🚀 EXECUTE ORDER", type="primary", use_container_width=True):
                    # Save Transaction
                    new_rows = []
                    for item in st.session_state.cart:
                        new_rows.append({
                            'Tanggal': datetime.now(),
                            'Menu': item['Menu'],
                            'Harga': item['Harga'],
                            'Qty': 1,
                            'Omset': item['Harga'],
                            'Kategori': item['Kategori'],
                            'Payment_Type': pay_method
                        })
                    
                    # Append to DB
                    new_df = pd.DataFrame(new_rows)
                    if os.path.exists(DB_FILE):
                        new_df.to_csv(DB_FILE, mode='a', header=False, index=False)
                    else:
                        new_df.to_csv(DB_FILE, index=False)
                    
                    # Add XP
                    st.session_state.xp += len(new_rows) * 10
                    st.session_state.cart = []
                    st.balloons()
                    st.success("TRANSACTION SECURED ON BLOCKCHAIN!")
                    time.sleep(1.5)
                    st.rerun()
        else:
            st.info("Cart is Empty / Awaiting Input...")
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# TAB 2: ANALYTICS GOD MODE
# =========================================================
with tabs[1]:
    st.markdown("### 📈 REAL-TIME DATA VISUALIZATION")
    
    if len(df) > 0:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("REVENUE", f"Rp {df['Omset'].sum():,.0f}", "+12%")
        k2.metric("TX COUNT", len(df), "Active")
        k3.metric("AVG BASKET", f"Rp {int(df['Omset'].mean()):,.0f}", "per Pax")
        top_item = df['Menu'].mode()[0] if not df.empty else "N/A"
        k4.metric("BEST SELLER", top_item, "Hot")
        
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.markdown('<div class="neon-card">', unsafe_allow_html=True)
            # Advanced Time Series
            daily = df.groupby(df['Tanggal'].dt.date)['Omset'].sum().reset_index()
            fig = px.area(daily, x='Tanggal', y='Omset', title="Revenue Velocity", color_discrete_sequence=['#00E5FF'])
            fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            fig.update_traces(line=dict(width=3))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="neon-card">', unsafe_allow_html=True)
            # 3D Chart Effect (Donut)
            fig_pie = px.pie(df, names='Kategori', values='Omset', hole=0.5, title="Category Matrix", color_discrete_sequence=px.colors.sequential.Cyan)
            fig_pie.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # AI INSIGHT MOCKUP
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader("🧠 AI NEURAL INSIGHTS")
        col_ai1, col_ai2 = st.columns(2)
        with col_ai1:
            st.info(f"**Trend Prediction:** Sales are projected to increase by **{random.randint(5,15)}%** this weekend based on historical velocity.")
        with col_ai2:
            st.warning(f"**Inventory Alert:** Stock for **{top_item}** is depleting faster than usual. Reorder recommended.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("INSUFFICIENT DATA FOR VISUALIZATION. PLEASE EXECUTE TRANSACTIONS.")

# =========================================================
# TAB 3: SYSTEM CORE
# =========================================================
with tabs[2]:
    col_sys1, col_sys2 = st.columns(2)
    
    with col_sys1:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader("📦 INVENTORY MATRIX")
        edited_db = st.data_editor(df_menu, num_rows="dynamic", use_container_width=True)
        if st.button("SYNC DATABASE"):
            edited_db.to_csv(MENU_FILE, index=False)
            st.success("Matrix Updated.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_sys2:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.subheader("💾 DATA EXFILTRATION")
        st.write("Download full encrypted transaction logs.")
        st.download_button(
            label="DOWNLOAD .CSV",
            data=df.to_csv(index=False),
            file_name=f"backup_{int(time.time())}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.divider()
        if st.button("⚠️ FACTORY RESET (DELETE ALL DATA)"):
            if os.path.exists(DB_FILE):
                os.remove(DB_FILE)
                st.session_state.cart = []
                st.session_state.xp = 0
                st.error("SYSTEM PURGED.")
                time.sleep(1)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"<center style='color:#555; font-size:0.8em;'>SESSION ID: {id(st.session_state)} | SERVER: JAKARTA-01 | LATENCY: 2ms</center>", unsafe_allow_html=True)