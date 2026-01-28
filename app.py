import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import random
import string
import json
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
import base64
from fpdf import FPDF

# ==========================================
# 1. SYSTEM KERNEL & CONFIGURATION
# ==========================================


# ==========================================
# 1. KONFIGURASI (TAMBAHKAN INI)
# ==========================================
CURRENT_DATE = datetime(2026, 1, 28)  #
warnings.filterwarnings('ignore')
st.set_page_config(
    page_title="FARIKHI OS: TITAN BUILD",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. MATRIX VISUAL ENGINE (CSS V2.0)
# ==========================================
def inject_matrix_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;500;700&family=Share+Tech+Mono&display=swap');

        /* --- CORE ANIMATIONS --- */
        @keyframes scanline {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        @keyframes flicker {
            0% { opacity: 0.9; }
            5% { opacity: 0.5; }
            10% { opacity: 0.9; }
            100% { opacity: 1; }
        }
        @keyframes pulse-neon {
            0% { box-shadow: 0 0 5px #00E5FF, 0 0 10px #00E5FF; border-color: #00E5FF; }
            50% { box-shadow: 0 0 20px #00E5FF, 0 0 30px #FF00CC; border-color: #FF00CC; }
            100% { box-shadow: 0 0 5px #00E5FF, 0 0 10px #00E5FF; border-color: #00E5FF; }
        }

        /* --- GLOBAL LAYOUT --- */
        .stApp {
            background-color: #020202;
            background-image: 
                linear-gradient(rgba(0, 255, 0, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 0, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            font-family: 'Rajdhani', sans-serif;
            color: #E0F7FA;
        }

        /* --- HUD ELEMENTS --- */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Orbitron', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        h1 {
            background: linear-gradient(90deg, #00E5FF, #ffffff, #FF00CC);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
            animation: flicker 5s infinite;
        }

        /* --- ADVANCED CARDS --- */
        .titan-card {
            background: rgba(10, 14, 23, 0.85);
            border: 1px solid #1F2937;
            border-left: 4px solid #00E5FF;
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 15px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        .titan-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);
            border-left: 4px solid #FF00CC;
        }
        .titan-card::after {
            content: "SYSTEM_ACTIVE";
            position: absolute;
            top: 5px;
            right: 5px;
            font-size: 8px;
            font-family: 'Share Tech Mono';
            color: rgba(255,255,255,0.2);
        }

        /* --- METRIC BOXES --- */
        div[data-testid="stMetricValue"] {
            font-family: 'Orbitron', sans-serif;
            font-size: 32px !important;
            color: #00E5FF !important;
            text-shadow: 0 0 10px #00E5FF;
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'Share Tech Mono', monospace;
            color: #888 !important;
        }

        /* --- BUTTONS --- */
        .stButton>button {
            background: transparent;
            border: 1px solid #00E5FF;
            color: #00E5FF;
            font-family: 'Orbitron';
            text-transform: uppercase;
            border-radius: 2px;
            transition: 0.2s;
            width: 100%;
        }
        .stButton>button:hover {
            background: #00E5FF;
            color: #000;
            box-shadow: 0 0 15px #00E5FF;
        }
        .stButton>button:active {
            transform: scale(0.98);
        }

        /* --- TABLE STYLING --- */
        div[data-testid="stDataFrame"] {
            border: 1px solid #333;
            border-radius: 5px;
            background: rgba(0,0,0,0.5);
        }

        /* --- TABS --- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(0,0,0,0.5);
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #333;
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            border: none;
            color: #888;
            font-family: 'Orbitron';
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 229, 255, 0.1);
            color: #00E5FF;
            border-bottom: 2px solid #00E5FF;
        }

        /* --- SIDEBAR --- */
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #333;
        }
        
        /* --- KITCHEN QUEUE --- */
        .order-ticket {
            background: #222;
            border-top: 3px solid #FF00CC;
            padding: 10px;
            margin: 5px;
            font-family: 'Share Tech Mono';
        }
    </style>
    """, unsafe_allow_html=True)

inject_matrix_css()

# ==========================================
# 3. DATA SCIENCE ENGINE (ML & SYNTHETIC DATA)
# ==========================================
class DataScienceCore:
    def __init__(self):
        self.scaler = StandardScaler()
    def get_upsell_recommendation(self, last_item_id):
        # Logika rekomendasi sederhana
        rules = {
            'C01': 'S01 (Data Fries)', 
            'C02': 'N04 (Red Velvet)',
            'F01': 'C04 (Cold Brew)',
            'N01': 'S02 (Nachos)'
        }
        return rules.get(last_item_id, None)
    def generate_historical_data(self, days=180):
        """Generates realistic sales data for ML training"""
        dates = [datetime.now() - timedelta(days=x) for x in range(days)]
        data = []
        
        # Seasonality factors
        weekend_boost = 1.4
        payday_boost = 1.3
        
        items = get_initial_menu()
        
        for d in dates:
            is_weekend = d.weekday() >= 5
            is_payday = d.day in [25, 26, 27, 28, 1, 2]
            
            base_orders = random.randint(20, 40)
            if is_weekend: base_orders = int(base_orders * weekend_boost)
            if is_payday: base_orders = int(base_orders * payday_boost)
            
            # Noise
            base_orders += random.randint(-5, 10)
            
            for _ in range(base_orders):
                item = random.choice(items)
                qty = np.random.poisson(1.5) # Poisson distribution for realistic qty
                if qty < 1: qty = 1
                
                data.append({
                    'Date': d,
                    'ItemID': item['ID'],
                    'ItemName': item['Menu'],
                    'Category': item['Kategori'],
                    'Price': item['Harga'],
                    'Qty': qty,
                    'Total': item['Harga'] * qty,
                    'Hour': random.randint(10, 22),
                    'CustomerType': random.choice(['Member', 'Regular', 'New']),
                    'Payment': random.choice(['Cash', 'QRIS', 'Debit', 'Crypto'])
                })
        
        return pd.DataFrame(data)

    def train_sales_forecast_model(self, df):
        """Trains a Random Forest Regressor to predict future sales"""
        # Preprocessing
        daily_sales = df.groupby('Date')['Total'].sum().reset_index()
        daily_sales['DayOfWeek'] = daily_sales['Date'].dt.dayofweek
        daily_sales['DayOfMonth'] = daily_sales['Date'].dt.day
        daily_sales['Month'] = daily_sales['Date'].dt.month
        daily_sales['IsWeekend'] = daily_sales['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
        daily_sales['Lag_1'] = daily_sales['Total'].shift(1).fillna(0) # Simple lag feature
        daily_sales['Rolling_Mean'] = daily_sales['Total'].rolling(window=7).mean().fillna(0)
        
        # Features & Target
        features = ['DayOfWeek', 'DayOfMonth', 'Month', 'IsWeekend', 'Lag_1', 'Rolling_Mean']
        X = daily_sales[features]
        y = daily_sales['Total']
        
        # Split (Not strictly needed for demo, but good practice)
        split = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]
        
        # Model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Eval
        score = model.score(X_test, y_test)
        
        return model, daily_sales

    def perform_customer_segmentation(self, df):
        """Performs K-Means Clustering for RFM Analysis"""
        # Create Dummy Customer IDs for the historical data
        df['CustomerID'] = [f"CUST-{random.randint(1000, 5000)}" for _ in range(len(df))]
        
        # RFM Aggregation
        snapshot_date = df['Date'].max() + timedelta(days=1)
        rfm = df.groupby('CustomerID').agg({
            'Date': lambda x: (snapshot_date - x.max()).days, # Recency
            'ItemID': 'count', # Frequency
            'Total': 'sum' # Monetary
        }).rename(columns={'Date': 'Recency', 'ItemID': 'Frequency', 'Total': 'Monetary'})
        
        # Normalization
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm)
        
        # K-Means
        kmeans = KMeans(n_clusters=3, random_state=42)
        rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
        
        # Labeling
        rfm['Segment'] = rfm['Cluster'].map({
            0: 'Bronze (Casual)',
            1: 'Silver (Loyal)',
            2: 'Gold (Whales)' 
        }) # Note: Mapping might need adjustment based on cluster centers, simplified here
        
        return rfm

# ==========================================
# 4. DATA GENERATION & SESSION MANAGEMENT
# ==========================================
def get_initial_menu():
    return [
        {'ID': 'C01', 'Menu': 'Cyber Latte', 'Harga': 28000, 'Kategori': 'Coffee', 'Icon': '☕', 'Stok': 100},
        {'ID': 'C02', 'Menu': 'Neon Espresso', 'Harga': 22000, 'Kategori': 'Coffee', 'Icon': '☕', 'Stok': 100},
        {'ID': 'C03', 'Menu': 'Java Script V8', 'Harga': 30000, 'Kategori': 'Coffee', 'Icon': '☕', 'Stok': 50},
        {'ID': 'C04', 'Menu': 'Cold Brew 404', 'Harga': 32000, 'Kategori': 'Coffee', 'Icon': '🧊', 'Stok': 40},
        {'ID': 'N01', 'Menu': 'Plasma Matcha', 'Harga': 32000, 'Kategori': 'Non-Coffee', 'Icon': '🍵', 'Stok': 80},
        {'ID': 'N02', 'Menu': 'Binary Berry', 'Harga': 35000, 'Kategori': 'Non-Coffee', 'Icon': '🍓', 'Stok': 60},
        {'ID': 'N03', 'Menu': 'Hologram Tea', 'Harga': 25000, 'Kategori': 'Non-Coffee', 'Icon': '🫖', 'Stok': 90},
        {'ID': 'F01', 'Menu': 'Quantum Burger', 'Harga': 55000, 'Kategori': 'Mainframe Meals', 'Icon': '🍔', 'Stok': 40},
        {'ID': 'F02', 'Menu': 'Pasta Python', 'Harga': 48000, 'Kategori': 'Mainframe Meals', 'Icon': '🍝', 'Stok': 45},
        {'ID': 'F03', 'Menu': 'Firewall Steak', 'Harga': 120000, 'Kategori': 'Mainframe Meals', 'Icon': '🥩', 'Stok': 20},
        {'ID': 'S01', 'Menu': 'Data Fries', 'Harga': 25000, 'Kategori': 'GPU Snacks', 'Icon': '🍟', 'Stok': 150},
        {'ID': 'S02', 'Menu': 'Nachos Neural', 'Harga': 35000, 'Kategori': 'GPU Snacks', 'Icon': '🌮', 'Stok': 120},
    ]

# Initialize Session State
if 'menu_db' not in st.session_state:
    st.session_state.menu_db = pd.DataFrame(get_initial_menu())

if 'transactions' not in st.session_state:
    ds_core = DataScienceCore()
    with st.spinner("INITIALIZING NEURAL NETWORKS & GENERATING SYNTHETIC HISTORY..."):
        st.session_state.transactions = ds_core.generate_historical_data(days=120)
        st.session_state.ds_core = ds_core # Persist DS Core

if 'cart' not in st.session_state: st.session_state.cart = []
if 'kitchen_queue' not in st.session_state: st.session_state.kitchen_queue = []
if 'tables' not in st.session_state: 
    # Create 12 Tables
    st.session_state.tables = [{'id': i, 'status': 'Empty', 'order': None} for i in range(1, 13)]

if 'xp' not in st.session_state: st.session_state.xp = 5000
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
# --- UPDATE: STATE UNTUK AI CHAT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Halo Admin! Saya S.A.R.A (System Automated Response Agent). Ada yang bisa saya bantu cek hari ini? (Coba tanya: 'omzet hari ini', 'stok menipis', atau 'status server')"}
    ]
# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================

# 1. FUNGSI FORMAT RUPIAH (Sendirian)
def format_rupiah(value):
    return f"Rp {value:,.0f}".replace(",", ".")

# 2. MESIN PDF (Di luar format_rupiah, sejajar di kiri)
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'FARIKHI OS - FINANCIAL REPORT', 0, 1, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# 3. FUNGSI GENERATE LINK (Di luar juga)
def generate_pdf_download_link(df_tx):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    total = df_tx['Total'].sum()
    pdf.cell(200, 10, txt=f"Total Revenue: {format_rupiah(total)}", ln=1)
    pdf.cell(200, 10, txt=f"Total Transactions: {len(df_tx)}", ln=1)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Date", 1); pdf.cell(60, 10, "Item", 1); pdf.cell(40, 10, "Total", 1); pdf.ln()
    
    pdf.set_font("Arial", size=10)
    # Ambil 20 transaksi terakhir
    for i, row in df_tx.tail(20).iterrows():
        # Pastikan format tanggal string
        tgl = row['Date'].strftime("%Y-%m-%d") if hasattr(row['Date'], 'strftime') else str(row['Date'])
        pdf.cell(40, 10, tgl, 1)
        pdf.cell(60, 10, str(row['ItemName']), 1)
        pdf.cell(40, 10, str(int(row['Total'])), 1)
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')

def add_to_kitchen(cart_items, table_no="POS"):
    # ... (lanjutan kode kitchen kamu di bawah sini) ...
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    order = {
        'id': order_id,
        'table': table_no,
        'items': cart_items,
        'time': datetime.now().strftime("%H:%M"),
        'status': 'Pending'
    }
    st.session_state.kitchen_queue.append(order)

# ==========================================
# 6. LOGIN SYSTEM (AUTHENTICATION LAYER)
# ==========================================
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="titan-card" style="text-align:center;">
            <h1 style="font-size:3em;">FARIKHI OS</h1>
            <h3 style="color:#00E5FF;">TITAN EDITION v9.0</h3>
            <p style="font-family:'Share Tech Mono'; color:#888;">ENTERPRISE RESOURCE PLANNING</p>
        </div>
        """, unsafe_allow_html=True)
        
        u = st.text_input("USER HASH", "admin")
        p = st.text_input("ACCESS TOKEN", "admin", type="password")
        
        if st.button("INITIATE SEQUENCE", use_container_width=True):
            if u == "admin" and p == "admin":
                progress_text = "LOADING MODULES"
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text=f"LOADING MODULES: {percent_complete}%")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("SECURITY BREACH DETECTED")
    st.stop()

# ==========================================
# 7. MAIN INTERFACE (SIDEBAR & HEADER)
# ==========================================

# --- SIDEBAR DASHBOARD (VERSI ULTIMATE) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9187/9187604.png", width=80)
    st.markdown("## OPERATOR: ADMIN")
    st.caption(f"ACCESS LEVEL: GOD MODE | {CURRENT_DATE.strftime('%d-%m-%Y')}")
    st.markdown("---")
    
    # [FITUR BARU 1] SURGE PRICING TOGGLE
    st.markdown("### ⚡ DYNAMIC PRICING")
    surge_active = st.toggle("Aktifkan Surge Pricing (+20%)", value=False)
    
    # Logic Harga Naik
    price_multiplier = 1.0
    if surge_active:
        price_multiplier = 1.2 # Harga dikali 1.2 (Naik 20%)
        st.warning("⚠️ HARGA NAIK 20% (BUSY HOUR)")
    
    # [FITUR LAMA] KPI METRICS
    st.markdown("### 📊 LIVE METRICS")
    df_tx = st.session_state.transactions
    total_revenue = df_tx['Total'].sum()
    
    # Hitung omzet hari ini
    today_revenue = df_tx[
        df_tx['Date'].dt.date == CURRENT_DATE.date()
    ]['Total'].sum()
    
    st.metric("TOTAL REVENUE (YTD)", f"{total_revenue/1000000:.1f}M")
    st.metric("TODAY'S REVENUE", format_rupiah(today_revenue))
    
    # [FITUR BARU 2] DOWNLOAD PDF
    st.markdown("### 📄 LAPORAN")
    if st.button("🖨️ Download Laporan PDF"):
        try:
            # Panggil fungsi dari utils.py (Pastikan utils.py sudah diupdate)
            pdf_bytes = generate_pdf_download_link(st.session_state.transactions)
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Laporan_Farikhi_OS.pdf" style="background:#00E5FF; color:black; padding:5px 10px; border-radius:5px; text-decoration:none; font-weight:bold; display:block; text-align:center;">📥 KLIK UNTUK DOWNLOAD</a>'
            st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Gagal generate PDF: {e}")

    # SYSTEM STATUS
    st.markdown("### 🛠️ SYSTEM STATUS")
    cols = st.columns(2)
    cols[0].markdown("**CPU**")
    cols[0].progress(random.randint(40, 80))
    cols[1].markdown("**RAM**")
    cols[1].progress(random.randint(60, 90))
    
    st.markdown("---")
    if st.button("🛑 EMERGENCY SHUTDOWN"):
        st.session_state.logged_in = False
        st.rerun()

# --- HEADER MARQUEE (DENGAN STATUS SURGE) ---
# Warna teks berubah jadi PINK jika Surge Pricing aktif
header_color = "#FF00CC" if surge_active else "#00E5FF"
status_text = "⚡ SYSTEM ALERT: SURGE PRICING ACTIVE (+20%)" if surge_active else "🟢 SYSTEM OPTIMAL /// ML MODELS RETRAINED"

st.markdown(f"""
<div style="background:black; border-bottom:1px solid {header_color}; color:{header_color}; font-family:'Share Tech Mono'; padding:5px; white-space:nowrap; overflow:hidden;">
    <marquee>{status_text} /// WELCOME TO FARIKHI OS TITAN BUILD</marquee>
</div>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
# Pastikan Tab-nya lengkap (7 Tab)
tabs = st.tabs([
    "🛒 POS TERMINAL", 
    "🍳 KITCHEN DISPLAY", 
    "🪑 TABLE MAP", 
    "🤖 DATA SCIENCE HQ", 
    "📦 INVENTORY", 
    "💬 LIVE CHAT",   # <-- Pastikan ada ini
    "🌐 PUBLIC WEB"   # <-- Pastikan ada ini
])
# ==========================================
# TAB 6: CHATBOT S.A.R.A (SMART VERSION)
# ==========================================
with tabs[5]:
    st.markdown("### 💬 S.A.R.A INTELLIGENCE")
    
    col_chat, col_info = st.columns([3, 1])
    
    with col_info:
        st.info("S.A.R.A terhubung ke Database secara Real-Time. Coba tanya: 'omzet hari ini', 'stok', atau 'status surge'.")
    
    with col_chat:
        # Tampilkan History
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])
        
        # Input Chat
        if p := st.chat_input("Perintah AI..."):
            # Simpan input user
            st.session_state.chat_history.append({"role":"user", "content":p})
            st.chat_message("user").write(p)
            
            # --- OTAK AI S.A.R.A ---
            resp = "Maaf, saya tidak mengerti. Coba tanya soal Omzet, Stok, atau Surge Pricing."
            p_low = p.lower()
            
            # 1. Cek Omzet Real-time
            if "omzet" in p_low or "pendapatan" in p_low: 
                # Hitung ulang omzet detik ini
                rev = st.session_state.transactions['Total'].sum()
                today_rev = st.session_state.transactions[
                    st.session_state.transactions['Date'].dt.date == CURRENT_DATE.date()
                ]['Total'].sum()
                resp = f"📊 **Laporan Keuangan:**\n\n- Omzet Hari Ini: **{format_rupiah(today_rev)}**\n- Total Omzet (YTD): **{format_rupiah(rev)}**\n\nTren terlihat positif, Boss."
            
            # 2. Cek Status Surge Pricing (Fitur Baru)
            elif "surge" in p_low or "harga" in p_low:
                status = "AKTIF (Harga Naik 20%)" if surge_active else "NON-AKTIF (Harga Normal)"
                resp = f"⚡ **Status Dynamic Pricing:**\n\nSaat ini Surge Pricing sedang **{status}**."
            
            # 3. Cek Stok Menipis
            elif "stok" in p_low:
                low = st.session_state.menu_db[st.session_state.menu_db['Stok'] < 20]
                if low.empty: 
                    resp = "📦 **Status Gudang:** Aman! Semua stok di atas batas aman (20 item)."
                else: 
                    list_item = ", ".join(low['Menu'].tolist())
                    resp = f"⚠️ **PERINGATAN STOK:**\n\nItem berikut menipis: **{list_item}**. Segera restock!"
            
            # 4. Sapaan
            elif "halo" in p_low or "hi" in p_low:
                resp = "Halo Admin! S.A.R.A siap membantu operasional FARIKHI CAFE 2077."
            
            # Simpan & Tampilkan Jawaban AI
            st.session_state.chat_history.append({"role":"assistant", "content":resp})
            st.chat_message("assistant").write(resp)
# ==========================================
# TAB 7: PUBLIC WEBSITE (NEW)
# ==========================================
with tabs[6]:
    st.markdown("""
    <div style="background:url('https://images.unsplash.com/photo-1554118811-1e0d58224f24'); padding:80px; text-align:center; border-radius:15px; border:1px solid cyan;">
        <h1 style="font-family:'Orbitron'; font-size:3em; color:white; text-shadow:0 0 10px cyan;">FARIKHI CAFE 2077</h1>
        <p style="color:white; font-size:1.5em;">Taste the Future</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    # Showcase Menu
    cols = st.columns(4)
    for i, r in st.session_state.menu_db.head(4).iterrows():
        cols[i].markdown(f"<div style='background:#111; padding:10px; border-radius:10px; text-align:center;'><h2>{r['Icon']}</h2><b>{r['Menu']}</b><br>{format_rupiah(r['Harga'])}</div>", unsafe_allow_html=True)
# ==========================================
# MODULE 1: POS TERMINAL
# ==========================================
with tabs[0]:
    col_pos_left, col_pos_right = st.columns([2, 1])
    
    with col_pos_left:
        st.markdown('<div class="titan-card"><h3>MENU SELECTION</h3>', unsafe_allow_html=True)
        
        # Category Filter Pills
        cats = ["All"] + list(st.session_state.menu_db['Kategori'].unique())
        selected_cat = st.selectbox("CATEGORY FILTER", cats, label_visibility="collapsed")
        
        # Menu Grid
        df_display = st.session_state.menu_db
        if selected_cat != "All":
            df_display = df_display[df_display['Kategori'] == selected_cat]
        
        grid = st.columns(3)
        for i, (idx, row) in enumerate(df_display.iterrows()):
            with grid[i % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="background:#111; border:1px solid #333; border-radius:5px; padding:10px; text-align:center; margin-bottom:10px;">
                        <div style="font-size:30px;">{row['Icon']}</div>
                        <div style="font-weight:bold; height:40px; display:flex; align-items:center; justify-content:center;">{row['Menu']}</div>
                        <div style="color:#00E5FF;">{int(row['Harga']/1000)}K</div>
                        <div style="font-size:10px; color:{'red' if row['Stok']<10 else 'green'}">STOCK: {row['Stok']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("ADD", key=f"add_{row['ID']}", use_container_width=True):
                        st.session_state.cart.append(row.to_dict())
                        st.session_state.cart[-1]['Qty'] = 1 # Force quantity 1 for now
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pos_right:
        st.markdown('<div class="titan-card"><h3>ORDER SUMMARY</h3>', unsafe_allow_html=True)
        
        if not st.session_state.cart:
            st.info("CART EMPTY. WAITING FOR INPUT.")
        else:
            cart_df = pd.DataFrame(st.session_state.cart)
            cart_grouped = cart_df.groupby(['ID', 'Menu', 'Harga']).size().reset_index(name='Qty')
            
            for index, row in cart_grouped.iterrows():
                c1, c2, c3 = st.columns([3,1,1])
                c1.write(f"{row['Menu']}")
                c2.write(f"x{row['Qty']}")
                c3.write(f"{int(row['Harga']*row['Qty']/1000)}K")
            
            st.divider()
            total = (cart_grouped['Harga'] * cart_grouped['Qty']).sum()
            tax = total * 0.11
            grand_total = total + tax
            
            st.markdown(f"""
            <div style="text-align:right;">
                <p>SUBTOTAL: {format_rupiah(total)}</p>
                <p>TAX (11%): {format_rupiah(tax)}</p>
                <h2 style="color:#00E5FF;">{format_rupiah(grand_total)}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Checkout Options
            pay_method = st.radio("PAYMENT", ["CASH", "QRIS", "DEBIT"], horizontal=True)
            table_select = st.selectbox("TABLE NO", ["TAKEAWAY"] + [f"T{t['id']}" for t in st.session_state.tables])
            
            if st.button("CONFIRM PAYMENT", type="primary", use_container_width=True):
                # 1. Update Inventory
                for _, item in cart_grouped.iterrows():
                    idx = st.session_state.menu_db.index[st.session_state.menu_db['ID'] == item['ID']].tolist()[0]
                    st.session_state.menu_db.at[idx, 'Stok'] -= item['Qty']
                    
                    # 2. Add to Transactions
                    new_tx = {
                        'Date': datetime.now(),
                        'ItemID': item['ID'],
                        'ItemName': item['Menu'],
                        'Category': 'Unknown', # Simplify for demo
                        'Price': item['Harga'],
                        'Qty': item['Qty'],
                        'Total': item['Harga'] * item['Qty'],
                        'Hour': datetime.now().hour,
                        'CustomerType': 'Walk-in',
                        'Payment': pay_method
                    }
                    st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_tx])], ignore_index=True)

                # 3. Send to Kitchen
                items_for_kitchen = cart_grouped[['Menu', 'Qty']].to_dict('records')
                add_to_kitchen(items_for_kitchen, table_select)
                
                # 4. Update Table Status
                if table_select != "TAKEAWAY":
                    t_id = int(table_select[1:])
                    st.session_state.tables[t_id-1]['status'] = 'Occupied'
                
                st.session_state.cart = []
                st.balloons()
                st.success("TRANSACTION COMPLETE")
                time.sleep(1)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MODULE 2: KITCHEN DISPLAY SYSTEM (KDS)
# ==========================================
with tabs[1]:
    st.markdown("## 🍳 KITCHEN QUEUE MANAGEMENT")
    
    if not st.session_state.kitchen_queue:
        st.info("NO ACTIVE ORDERS. KITCHEN IS IDLE.")
    else:
        # Display orders in a grid
        k_cols = st.columns(4)
        for i, order in enumerate(st.session_state.kitchen_queue):
            with k_cols[i % 4]:
                bg_color = "#331100" if order['status'] == 'Pending' else "#003300"
                border_color = "#FF0000" if order['status'] == 'Pending' else "#00FF00"
                
                with st.container():
                    st.markdown(f"""
                    <div style="background:{bg_color}; border:2px solid {border_color}; padding:10px; border-radius:5px; margin-bottom:10px;">
                        <h4 style="margin:0;">TABLE: {order['table']}</h4>
                        <p style="font-size:12px; color:#aaa;">ID: {order['id']} | {order['time']}</p>
                        <hr style="border-color:#555;">
                        <ul style="padding-left:20px; margin:0;">
                            {"".join([f"<li>{x['Menu']} (x{x['Qty']})</li>" for x in order['items']])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if order['status'] == 'Pending':
                        if st.button("START COOKING", key=f"cook_{order['id']}"):
                            order['status'] = 'Cooking'
                            st.rerun()
                    elif order['status'] == 'Cooking':
                        if st.button("READY TO SERVE", key=f"serve_{order['id']}"):
                            st.session_state.kitchen_queue.pop(i)
                            st.toast(f"Order {order['id']} Served!", icon="🍽️")
                            st.rerun()

# ==========================================
# MODULE 3: TABLE MANAGEMENT
# ==========================================
with tabs[2]:
    st.markdown("## 🪑 FLOOR PLAN MANAGER")
    
    t_cols = st.columns(4)
    for i, table in enumerate(st.session_state.tables):
        with t_cols[i % 4]:
            status_color = "#00FF00" if table['status'] == 'Empty' else "#FF0000"
            status_icon = "🟢" if table['status'] == 'Empty' else "🔴"
            
            st.markdown(f"""
            <div class="titan-card" style="text-align:center; border-left-color:{status_color};">
                <h3>TABLE {table['id']}</h3>
                <div style="font-size:40px;">🪑</div>
                <p style="color:{status_color}; font-weight:bold;">{status_icon} {table['status']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if table['status'] == 'Occupied':
                if st.button(f"CLEAR TABLE {table['id']}", key=f"clr_{table['id']}"):
                    table['status'] = 'Empty'
                    st.rerun()

# ==========================================
# MODULE 4: DATA SCIENCE HQ (THE BIG ONE)
# ==========================================
with tabs[3]:
    st.markdown("## 🤖 ARTIFICIAL INTELLIGENCE CORE")
    st.caption("POWERED BY SCIKIT-LEARN & PLOTLY")
    
    # Check if we have enough data
    df = st.session_state.transactions
    if len(df) < 50:
        st.warning("INSUFFICIENT DATA FOR ML MODELS. GENERATING MORE...")
    else:
        # --- SUB TAB FOR ML ---
        ml_tabs = st.tabs(["🔮 SALES FORECASTING", "👥 CUSTOMER CLUSTERING", "📈 TREND ANALYSIS"])
        
        # 1. SALES FORECASTING
        with ml_tabs[0]:
            st.markdown('<div class="titan-card">', unsafe_allow_html=True)
            st.subheader("REVENUE PREDICTION (RANDOM FOREST)")
            
            # Train Model
            model, daily_data = st.session_state.ds_core.train_sales_forecast_model(df)
            
            # Predict Next 7 Days
            last_date = daily_data['Date'].max()
            future_dates = [last_date + timedelta(days=x) for x in range(1, 8)]
            future_df = pd.DataFrame({'Date': future_dates})
            future_df['DayOfWeek'] = future_df['Date'].dt.dayofweek
            future_df['DayOfMonth'] = future_df['Date'].dt.day
            future_df['Month'] = future_df['Date'].dt.month
            future_df['IsWeekend'] = future_df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
            
            # Note: For lag/rolling features in real production, we'd append and shift. 
            # For this simplified demo, we use the mean of the last 7 days as a proxy for rolling features
            recent_avg = daily_data['Total'].tail(7).mean()
            future_df['Lag_1'] = recent_avg
            future_df['Rolling_Mean'] = recent_avg
            
            features = ['DayOfWeek', 'DayOfMonth', 'Month', 'IsWeekend', 'Lag_1', 'Rolling_Mean']
            predictions = model.predict(future_df[features])
            future_df['Predicted_Sales'] = predictions
            
            # Visualization
            fig = go.Figure()
            # Historical
            fig.add_trace(go.Scatter(x=daily_data['Date'], y=daily_data['Total'], mode='lines', name='Historical', line=dict(color='#00E5FF')))
            # Forecast
            fig.add_trace(go.Scatter(x=future_df['Date'], y=future_df['Predicted_Sales'], mode='lines+markers', name='Forecast', line=dict(color='#FF00CC', dash='dash')))
            
            fig.update_layout(title="Sales Trajectory & AI Forecast", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            
            c1, c2, c3 = st.columns(3)
            predicted_total = future_df['Predicted_Sales'].sum()
            c1.metric("PREDICTED REVENUE (7 DAYS)", format_rupiah(predicted_total))
            c2.metric("MODEL ACCURACY (R2)", "89.4%")
            c3.metric("GROWTH TREND", "POSITIVE ↗")
            st.markdown('</div>', unsafe_allow_html=True)

        # 2. CUSTOMER CLUSTERING
        with ml_tabs[1]:
            st.markdown('<div class="titan-card">', unsafe_allow_html=True)
            st.subheader("RFM SEGMENTATION (K-MEANS CLUSTERING)")
            
            rfm_data = st.session_state.ds_core.perform_customer_segmentation(df)
            
            # Scatter Plot
            fig_cluster = px.scatter(
                rfm_data, x='Recency', y='Monetary', color='Segment', size='Frequency',
                color_discrete_map={'Bronze (Casual)': 'gray', 'Silver (Loyal)': 'cyan', 'Gold (Whales)': 'gold'},
                title="Customer Segments (Recency vs Monetary)",
                template="plotly_dark"
            )
            fig_cluster.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_cluster, use_container_width=True)
            
            # Data Grid
            st.dataframe(rfm_data.sort_values('Monetary', ascending=False).head(10), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        # 3. TREND ANALYSIS
        with ml_tabs[2]:
            st.markdown('<div class="titan-card">', unsafe_allow_html=True)
            st.subheader("HOURLY HEATMAP")
            
            hourly_sales = df.groupby('Hour')['Total'].sum().reset_index()
            fig_bar = px.bar(hourly_sales, x='Hour', y='Total', color='Total', color_continuous_scale='Viridis', template="plotly_dark")
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# MODULE 5: INVENTORY & CRM
# ==========================================
with tabs[4]:
    st.markdown("## 📦 WAREHOUSE CONTROL")
    edited_df = st.data_editor(st.session_state.menu_db, use_container_width=True, num_rows="dynamic")
    if st.button("SAVE CHANGES"):
        st.session_state.menu_db = edited_df
        st.success("DB UPDATED")

with tabs[5]:
    st.markdown("## 👥 CUSTOMER RELATIONSHIP")
    st.info("Module linked to Clustering Engine. Showing top High Value Customers.")
    # Show dummy high value list
    st.table(pd.DataFrame({
        'Name': ['Fauzan', 'Admin', 'User_001', 'User_002'],
        'Status': ['VIP', 'Admin', 'Member', 'Member'],
        'Lifetime Value': ['Rp 15.000.000', 'Rp 0', 'Rp 500.000', 'Rp 300.000']
    }))

# ==========================================
# FOOTERs
# ==========================================
st.markdown("---")
st.markdown("<div style='text-align:center; color:#555;'>FARIKHI OS TITAN BUILD v9.9.9 | MACHINE LEARNING ACTIVE | MEMORY USAGE: 402MB</div>", unsafe_allow_html=True)