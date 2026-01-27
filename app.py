import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import random
import string
from datetime import datetime, timedelta
from io import BytesIO
import base64

# ==========================================
# 1. KONFIGURASI INTI & PAGE SETUP
# ==========================================
st.set_page_config(
    page_title="FARIKHI OS: GOD MODE",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CYBERPUNK CSS ENGINE (VISUAL EFFECTS)
# ==========================================
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');

        /* --- GLOBAL ANIMATIONS & BACKGROUND --- */
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        .stApp {
            background: linear-gradient(-45deg, #050505, #1a0b2e, #110f24, #000000);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            font-family: 'Rajdhani', sans-serif;
            color: #E0F7FA;
        }

        /* --- TYPOGRAPHY --- */
        h1, h2, h3 { 
            font-family: 'Orbitron', sans-serif !important; 
            letter-spacing: 3px; 
            text-transform: uppercase;
        }
        
        h1 {
            background: -webkit-linear-gradient(#00E5FF, #FF00CC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
        }

        /* --- GLASSMORPHISM CARDS --- */
        .neon-card {
            background: rgba(20, 20, 30, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 229, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        .neon-card::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            transition: 0.5s;
        }

        .neon-card:hover::before {
            left: 100%;
        }

        .neon-card:hover {
            transform: translateY(-5px) scale(1.01);
            border: 1px solid rgba(0, 229, 255, 0.5);
            box-shadow: 0 0 30px rgba(0, 229, 255, 0.2);
        }

        /* --- METRICS & KPI --- */
        div[data-testid="stMetricValue"] {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem !important;
            color: #00E5FF !important;
            text-shadow: 0 0 10px rgba(0, 229, 255, 0.8);
        }
        div[data-testid="stMetricLabel"] {
            color: #aaa !important;
            font-weight: bold;
        }

        /* --- BUTTONS --- */
        .stButton>button {
            background: linear-gradient(90deg, #001f3f, #003366);
            color: #00E5FF;
            border: 1px solid #00E5FF;
            border-radius: 4px;
            font-family: 'Orbitron', sans-serif;
            transition: 0.3s;
            text-transform: uppercase;
        }
        .stButton>button:hover {
            background: #00E5FF;
            color: black;
            box-shadow: 0 0 20px #00E5FF;
        }
        
        /* --- PROGRESS BAR (XP) --- */
        .xp-container {
            width: 100%;
            background-color: #111;
            border-radius: 10px;
            padding: 3px;
            border: 1px solid #333;
        }
        .xp-fill {
            height: 12px;
            background: linear-gradient(90deg, #FF00CC, #333399, #00E5FF);
            border-radius: 8px;
            width: 0%; /* Dynamic */
            transition: width 1s ease-in-out;
            box-shadow: 0 0 10px #FF00CC;
        }
        
        /* --- TABS --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: rgba(255,255,255,0.05);
            border-radius: 5px;
            color: white;
            font-family: 'Orbitron';
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 229, 255, 0.2);
            border: 1px solid #00E5FF;
            color: #00E5FF;
        }
        
        /* --- CUSTOM SCROLLBAR --- */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #000; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #00E5FF; }

    </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# 3. DATABASE & SESSION STATE
# ==========================================
# --- Helper: Generate Initial Menu ---
def get_initial_menu():
    return [
        # COFFEE
        {'ID': 'C01', 'Menu': 'Cyber Latte', 'Harga': 28000, 'Kategori': 'Coffee', 'Icon': '☕', 'Stok': 100},
        {'ID': 'C02', 'Menu': 'Neon Espresso', 'Harga': 22000, 'Kategori': 'Coffee', 'Icon': '☕', 'Stok': 100},
        {'ID': 'C03', 'Menu': 'Java Script', 'Harga': 30000, 'Kategori': 'Coffee', 'Icon': '☕', 'Stok': 50},
        # NON-COFFEE
        {'ID': 'N01', 'Menu': 'Plasma Matcha', 'Harga': 32000, 'Kategori': 'Non-Coffee', 'Icon': '🍵', 'Stok': 80},
        {'ID': 'N02', 'Menu': 'Binary Berry', 'Harga': 35000, 'Kategori': 'Non-Coffee', 'Icon': '🍓', 'Stok': 60},
        {'ID': 'N03', 'Menu': 'Hologram Tea', 'Harga': 25000, 'Kategori': 'Non-Coffee', 'Icon': '🫖', 'Stok': 90},
        # FOOD
        {'ID': 'F01', 'Menu': 'Quantum Burger', 'Harga': 55000, 'Kategori': 'Mainframe Meals', 'Icon': '🍔', 'Stok': 40},
        {'ID': 'F02', 'Menu': 'Pasta Python', 'Harga': 48000, 'Kategori': 'Mainframe Meals', 'Icon': '🍝', 'Stok': 45},
        {'ID': 'F03', 'Menu': 'Firewall Steak', 'Harga': 120000, 'Kategori': 'Mainframe Meals', 'Icon': '🥩', 'Stok': 20},
        # SNACK
        {'ID': 'S01', 'Menu': 'Data Fries', 'Harga': 25000, 'Kategori': 'GPU Snacks', 'Icon': '🍟', 'Stok': 150},
        {'ID': 'S02', 'Menu': 'Nachos Neural', 'Harga': 35000, 'Kategori': 'GPU Snacks', 'Icon': '🌮', 'Stok': 120},
        {'ID': 'S03', 'Menu': 'Cyber Wings', 'Harga': 40000, 'Kategori': 'GPU Snacks', 'Icon': '🍗', 'Stok': 60},
        # DESSERT
        {'ID': 'D01', 'Menu': 'Crypto Cake', 'Harga': 30000, 'Kategori': 'Crypto Desserts', 'Icon': '🍰', 'Stok': 30},
        {'ID': 'D02', 'Menu': 'Gelato Glitch', 'Harga': 28000, 'Kategori': 'Crypto Desserts', 'Icon': '🍦', 'Stok': 50},
    ]

# --- Helper: Initialize Session ---
if 'menu_db' not in st.session_state:
    st.session_state.menu_db = pd.DataFrame(get_initial_menu())

if 'transactions' not in st.session_state:
    # Dummy historical data for charts
    dates = [datetime.now() - timedelta(days=x) for x in range(30)]
    dummy_data = []
    for d in dates:
        for _ in range(random.randint(5, 15)):
            item = random.choice(get_initial_menu())
            dummy_data.append({
                'Tanggal': d,
                'ID': item['ID'],
                'Menu': item['Menu'],
                'Harga': item['Harga'],
                'Qty': random.randint(1, 3),
                'Total': item['Harga'] * random.randint(1, 3),
                'Kategori': item['Kategori'],
                'Payment': random.choice(['CASH', 'QRIS', 'CRYPTO'])
            })
    st.session_state.transactions = pd.DataFrame(dummy_data)

if 'cart' not in st.session_state: st.session_state.cart = []
if 'xp' not in st.session_state: st.session_state.xp = 1250 # Start with some XP
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'system_logs' not in st.session_state: st.session_state.system_logs = ["System Initialized...", "Connecting to Blockchain...", "Database Decrypted."]

# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================
def add_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.system_logs.insert(0, f"[{timestamp}] {message}")
    if len(st.session_state.system_logs) > 10:
        st.session_state.system_logs.pop()

def get_level_info(xp):
    if xp < 1000: return "SCRIPT KIDDIE", 1, xp/1000
    elif xp < 3000: return "NETRUNNER", 2, (xp-1000)/2000
    elif xp < 6000: return "SYSADMIN", 3, (xp-3000)/3000
    else: return "CYBER GOD", 4, 1.0

def format_rupiah(value):
    return f"Rp {value:,.0f}".replace(",", ".")

# ==========================================
# 5. LOGIN SCREEN (SIMULATION)
# ==========================================
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<div class="neon-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("<h1>FARIKHI OS</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#00E5FF; letter-spacing:2px;'>SECURE ACCESS TERMINAL</p>", unsafe_allow_html=True)
        
        username = st.text_input("USER IDENTIFIER", placeholder="Enter Admin ID...")
        password = st.text_input("ACCESS KEY", type="password", placeholder="••••••")
        
        if st.button("INITIATE HANDSHAKE", use_container_width=True):
            if username and password:
                placeholder = st.empty()
                with placeholder.container():
                    st.info("🔐 ENCRYPTING CHANNEL...")
                    time.sleep(1)
                    st.warning("👁️ SCANNING BIOMETRICS...")
                    time.sleep(1)
                    st.success("✅ ACCESS GRANTED. WELCOME BACK, OPERATOR.")
                    time.sleep(1)
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("ACCESS DENIED. INVALID CREDENTIALS.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 6. MAIN APPLICATION LAYOUT
# ==========================================
# --- SIDEBAR INFO ---
rank, lvl, progress = get_level_info(st.session_state.xp)
pct = int(progress * 100)

with st.sidebar:
    st.markdown(f"## 👤 OPERATOR: {rank}")
    st.markdown(f"**LEVEL {lvl}** | {st.session_state.xp} XP")
    st.markdown(f"""
        <div class="xp-container">
            <div class="xp-fill" style="width: {pct}%;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🖥️ SYSTEM LOGS")
    log_text = "<br>".join([f"<span style='color:#00ff00; font-family:monospace; font-size:10px;'>{log}</span>" for log in st.session_state.system_logs])
    st.markdown(f"<div style='background:black; padding:10px; border-radius:5px; border:1px solid #333;'>{log_text}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔴 TERMINATE SESSION"):
        st.session_state.logged_in = False
        st.rerun()

# --- HEADER ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown('<h1>🦄 FARIKHI OS <span style="font-size:0.4em; color:#FF00CC; vertical-align:super;">GOD MODE</span></h1>', unsafe_allow_html=True)
with col_head2:
    st.markdown(f"<div style='text-align:right; font-family:Orbitron; color:#00E5FF;'>{datetime.now().strftime('%d %B %Y')}<br><span style='font-size:1.5em;'>{datetime.now().strftime('%H:%M')}</span></div>", unsafe_allow_html=True)

# --- TABS NAVIGATION ---
tab1, tab2, tab3, tab4 = st.tabs(["🛒 HYPER POS", "📊 GOD ANALYTICS", "📦 QUANTUM INVENTORY", "⚙️ CORE SETTINGS"])

# ==========================================
# TAB 1: HYPER POS (POINT OF SALE)
# ==========================================
with tab1:
    col_menu, col_cart = st.columns([1.8, 1])
    
    # --- SECTION KIRI: MENU GRID ---
    with col_menu:
        # Filters
        categories = ["All"] + list(st.session_state.menu_db['Kategori'].unique())
        selected_cat = st.pills("FILTER PROTOCOL:", categories, default="All", selection_mode="single")
        
        search_query = st.text_input("🔍 SEARCH DATABASE", placeholder="Type item name...", label_visibility="collapsed")
        
        # Filtering Logic
        df_filtered = st.session_state.menu_db.copy()
        if selected_cat != "All":
            df_filtered = df_filtered[df_filtered['Kategori'] == selected_cat]
        if search_query:
            df_filtered = df_filtered[df_filtered['Menu'].str.contains(search_query, case=False)]
        
        # Grid Display
        st.markdown('<div style="height: 600px; overflow-y: scroll; padding-right:10px;">', unsafe_allow_html=True)
        
        # Create grid with columns
        grid_cols = st.columns(3)
        for idx, row in df_filtered.iterrows():
            with grid_cols[idx % 3]:
                # Dynamic Card Style
                stock_color = "#00ff00" if row['Stok'] > 20 else "#ff0000"
                
                with st.container():
                    st.markdown(f"""
                    <div class="neon-card" style="padding:15px; text-align:center; min-height:220px;">
                        <div style="font-size:40px; margin-bottom:10px;">{row['Icon']}</div>
                        <h4 style="margin:0; color:white;">{row['Menu']}</h4>
                        <p style="color:#00E5FF; font-weight:bold; font-size:1.2em;">{int(row['Harga']/1000)}K</p>
                        <p style="color:#aaa; font-size:0.8em;">STOCK: <span style="color:{stock_color}">{row['Stok']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Logic Button (Separate from HTML to keep Streamlit interactivity)
                    disabled = True if row['Stok'] <= 0 else False
                    btn_label = "ADD +" if not disabled else "OOS"
                    
                    if st.button(btn_label, key=f"add_{row['ID']}", disabled=disabled, use_container_width=True):
                        # Add to Cart Logic
                        existing_item = next((item for item in st.session_state.cart if item['ID'] == row['ID']), None)
                        if existing_item:
                            if existing_item['Qty'] < row['Stok']:
                                existing_item['Qty'] += 1
                                st.toast(f"Updated: {row['Menu']}", icon="⚡")
                            else:
                                st.error("Max stock reached!")
                        else:
                            st.session_state.cart.append({
                                'ID': row['ID'],
                                'Menu': row['Menu'],
                                'Harga': row['Harga'],
                                'Qty': 1,
                                'Kategori': row['Kategori']
                            })
                            st.toast(f"Added: {row['Menu']}", icon="✅")
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION KANAN: CART & CHECKOUT ---
    with col_cart:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("### 🛒 HOLOGRAPHIC CART")
        
        if not st.session_state.cart:
            st.info("WAITING FOR DATA INPUT...")
            st.markdown("<div style='text-align:center; font-size:50px; opacity:0.3;'>👾</div>", unsafe_allow_html=True)
        else:
            cart_df = pd.DataFrame(st.session_state.cart)
            
            # Display Cart Items
            for i, item in enumerate(st.session_state.cart):
                c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
                c1.write(f"**{item['Menu']}**")
                c2.write(f"x{item['Qty']}")
                c3.write(f"{int(item['Harga']*item['Qty']/1000)}K")
                if c4.button("🗑️", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            
            st.markdown("---")
            
            # Calculations
            subtotal = sum(item['Harga'] * item['Qty'] for item in st.session_state.cart)
            tax = subtotal * 0.11
            total = subtotal + tax
            
            r1, r2 = st.columns([2,1])
            r1.write("Subtotal")
            r2.write(format_rupiah(subtotal))
            r1.write("PPN (11%)")
            r2.write(format_rupiah(tax))
            
            st.markdown(f"""
            <div style="background:rgba(0,229,255,0.1); padding:15px; border-radius:10px; border:1px dashed #00E5FF; margin-top:10px;">
                <h2 style="text-align:right; margin:0; color:#00E5FF;">{format_rupiah(total)}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Payment Method
            payment = st.radio("PAYMENT GATEWAY", ["CASH", "QRIS", "CRYPTO (ETH/BTC)"], horizontal=True)
            
            if payment == "QRIS":
                st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=UNICORN_PAY_{int(total)}", caption="SCAN NEURAL LINK")
            
            # Action Buttons
            b1, b2 = st.columns(2)
            if b1.button("CLEAR MEMORY", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
            
            if b2.button("🚀 EXECUTE ORDER", type="primary", use_container_width=True):
                # 1. Update Inventory
                for item in st.session_state.cart:
                    idx = st.session_state.menu_db.index[st.session_state.menu_db['ID'] == item['ID']].tolist()[0]
                    st.session_state.menu_db.at[idx, 'Stok'] -= item['Qty']
                
                # 2. Record Transaction
                new_tx = []
                for item in st.session_state.cart:
                    new_tx.append({
                        'Tanggal': datetime.now(),
                        'ID': item['ID'],
                        'Menu': item['Menu'],
                        'Harga': item['Harga'],
                        'Qty': item['Qty'],
                        'Total': item['Harga'] * item['Qty'],
                        'Kategori': item['Kategori'],
                        'Payment': payment
                    })
                st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame(new_tx)], ignore_index=True)
                
                # 3. Gamification
                xp_gain = int(total / 1000)
                st.session_state.xp += xp_gain
                
                # 4. Success UI
                st.session_state.cart = []
                add_log(f"Order Executed. Revenue: {format_rupiah(total)}")
                
                st.balloons()
                st.markdown("""
                    <div style="position:fixed; top:50%; left:50%; transform:translate(-50%, -50%); 
                    background:rgba(0,0,0,0.9); padding:50px; border:2px solid #00E5FF; z-index:9999; border-radius:20px; text-align:center;">
                        <h1 style="color:#00E5FF;">TRANSACTION SECURED</h1>
                        <p>BLOCKCHAIN HASH: 0x{...}</p>
                        <p>XP GAINED: +""" + str(xp_gain) + """</p>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(2)
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 2: GOD ANALYTICS (VISUALIZATION)
# ==========================================
with tab2:
    st.markdown("### 📈 REAL-TIME DATA STREAMS")
    
    df_tx = st.session_state.transactions
    df_tx['Tanggal'] = pd.to_datetime(df_tx['Tanggal'])
    
    # KPI ROW
    k1, k2, k3, k4 = st.columns(4)
    total_rev = df_tx['Total'].sum()
    total_tx = len(df_tx)
    avg_ticket = df_tx['Total'].mean()
    top_item = df_tx['Menu'].mode()[0]
    
    k1.metric("TOTAL REVENUE", format_rupiah(total_rev), "100%")
    k2.metric("TRANSACTIONS", total_tx, "+5")
    k3.metric("AVG TICKET", format_rupiah(avg_ticket), "+2%")
    k4.metric("MVP ITEM", top_item, "Hot")
    
    st.markdown("---")
    
    # ROW 1: CHARTS
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("#### 🌊 REVENUE VELOCITY (Area Chart)")
        
        # Aggregate by Date
        daily_rev = df_tx.groupby(df_tx['Tanggal'].dt.date)['Total'].sum().reset_index()
        daily_rev.columns = ['Date', 'Revenue']
        
        fig_area = px.area(daily_rev, x='Date', y='Revenue', template="plotly_dark")
        fig_area.update_traces(line_color='#00E5FF', fill_color='rgba(0, 229, 255, 0.2)')
        fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Rajdhani"))
        st.plotly_chart(fig_area, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("#### 🍩 CATEGORY MATRIX (Sunburst)")
        
        fig_sun = px.sunburst(df_tx, path=['Kategori', 'Menu'], values='Total', color='Kategori',
                            color_discrete_sequence=px.colors.qualitative.Bold)
        fig_sun.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Orbitron"))
        st.plotly_chart(fig_sun, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ROW 2: AI PREDICTION
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.markdown("#### 🧠 NEURAL NETWORK FORECAST (AI SIMULATION)")
    
    # Generate Fake Forecast Data
    last_date = daily_rev['Date'].max()
    future_dates = [last_date + timedelta(days=x) for x in range(1, 8)]
    avg_last_3 = daily_rev['Revenue'].tail(3).mean()
    forecast_values = [avg_last_3 * (1 + random.uniform(-0.1, 0.2)) for _ in range(7)]
    
    df_forecast = pd.DataFrame({'Date': future_dates, 'Forecast': forecast_values})
    
    fig_fore = go.Figure()
    # Actual Data
    fig_fore.add_trace(go.Scatter(x=daily_rev['Date'], y=daily_rev['Revenue'], mode='lines+markers', name='Actual', line=dict(color='#00E5FF', width=3)))
    # Forecast Data
    fig_fore.add_trace(go.Scatter(x=df_forecast['Date'], y=df_forecast['Forecast'], mode='lines+markers', name='AI Prediction', line=dict(color='#FF00CC', dash='dot', width=3)))
    
    fig_fore.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title="Next 7 Days Revenue Projection")
    st.plotly_chart(fig_fore, use_container_width=True)
    
    col_insight1, col_insight2 = st.columns(2)
    col_insight1.info(f"**AI Insight:** Detected a {random.randint(10,30)}% potential spike this weekend.")
    col_insight2.warning("**Inventory Alert:** 'Coffee' beans supply might run low based on current trajectory.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 3: QUANTUM INVENTORY
# ==========================================
with tab3:
    c_inv1, c_inv2 = st.columns([2, 1])
    
    with c_inv1:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("### 📦 MATRIX DATABASE EDITOR")
        
        # Editable Dataframe
        edited_df = st.data_editor(
            st.session_state.menu_db,
            column_config={
                "Icon": st.column_config.TextColumn("Icon", width="small"),
                "Harga": st.column_config.NumberColumn("Price (Rp)", format="Rp %d"),
                "Stok": st.column_config.ProgressColumn("Stock Level", min_value=0, max_value=200, format="%f"),
            },
            num_rows="dynamic",
            use_container_width=True,
            height=500
        )
        
        if st.button("💾 SYNCHRONIZE DATABASE"):
            st.session_state.menu_db = edited_df
            add_log("Database Manual Update Logged.")
            st.success("DATA SAVED TO CORE MEMORY.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_inv2:
        st.markdown('<div class="neon-card">', unsafe_allow_html=True)
        st.markdown("### 📉 LOW STOCK ALERT")
        
        low_stock = st.session_state.menu_db[st.session_state.menu_db['Stok'] < 20]
        
        if not low_stock.empty:
            for i, row in low_stock.iterrows():
                st.error(f"⚠️ **{row['Menu']}**: ONLY {row['Stok']} LEFT!")
                if st.button(f"♻️ RESTOCK {row['Menu']}", key=f"restock_{i}"):
                    st.session_state.menu_db.at[i, 'Stok'] += 50
                    st.rerun()
        else:
            st.success("ALL SYSTEMS NOMINAL. INVENTORY HEALTHY.")
            
        st.markdown("---")
        st.markdown("### ➕ QUICK ADD")
        new_name = st.text_input("New Item Name")
        new_price = st.number_input("Price", min_value=0, step=1000)
        new_cat = st.selectbox("Category", categories[1:])
        
        if st.button("CREATE ITEM"):
            new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            new_row = {'ID': new_id, 'Menu': new_name, 'Harga': new_price, 'Kategori': new_cat, 'Icon': '❓', 'Stok': 50}
            st.session_state.menu_db = pd.concat([st.session_state.menu_db, pd.DataFrame([new_row])], ignore_index=True)
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 4: CORE SETTINGS (ADMIN)
# ==========================================
with tab4:
    st.markdown('<div class="neon-card">', unsafe_allow_html=True)
    st.markdown("## ⚙️ SYSTEM KERNEL ACCESS")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.subheader("DATA EXFILTRATION")
        st.caption("Download encrypted transaction logs (.csv)")
        
        csv = st.session_state.transactions.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ DOWNLOAD LOGS",
            data=csv,
            file_name=f"farikhi_logs_{int(time.time())}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_s2:
        st.subheader("DANGER ZONE")
        if st.button("☢️ FACTORY RESET SYSTEM", type="primary", use_container_width=True):
            st.session_state.clear()
            st.rerun()
            
    st.markdown("---")
    st.subheader("ABOUT FARIKHI OS")
    st.text("""
    VERSION: 5.0 (GOD MODE BUILD)
    KERNEL: PYTHON 3.9 + STREAMLIT
    GPU ACCELERATION: ACTIVE
    DEVELOPER: [YOUR NAME]
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br><div style='text-align:center; color:#555; font-size:12px;'>FARIKHI OS © 2077 | SECURED BY QUANTUM ENCRYPTION</div>", unsafe_allow_html=True)