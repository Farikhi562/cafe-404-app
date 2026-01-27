import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os
from datetime import date, datetime, timedelta

# ==========================================
# 1. KONFIGURASI HALAMAN & DATABASE ENGINE
# ==========================================
st.set_page_config(
    page_title="Cafe 404 Unicorn System",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --- FUNGSI GAMBAR OTOMATIS (HELPER) ---
def get_image_url(kategori):
    # Gambar diambil dari Unsplash (High Quality)
    if kategori == 'Minuman': 
        return "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=400&q=80"
    elif kategori == 'Makanan': 
        return "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=400&q=80"
    elif kategori == 'Snack':
        return "https://images.unsplash.com/photo-1621939514649-28b12e816751?auto=format&fit=crop&w=400&q=80"
    else: 
        return "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=400&q=80"
# File Database
DB_FILE = 'cafe_database.csv'
MENU_FILE = 'menu_database.csv'

# --- HIASAN CSS & BANNER ---
st.markdown("""
<style>
    /* Bikin Font Judul Lebih Gaul */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        color: #FF4B4B;
    }
    /* Card Menu Biar Lebih Pop-Up */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 10px;
    }
    /* Mode Gelap Friendly */
    @media (prefers-color-scheme: dark) {
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
            background-color: #262730;
        }
    }
</style>
""", unsafe_allow_html=True)

# HERO IMAGE (BANNER) - Taruh ini di dalam if nav == "Dashboard" atau Kasir
def show_hero():
    st.image("https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=1200&auto=format&fit=crop", 
            use_container_width=True, caption="Cafe 404: Debug Your Hunger")
# GANTI SELURUH def load_data(): DENGAN INI
def load_data():
    # 1. Load Transaksi (Biarin apa adanya)
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    else:
        # Dummy Transaksi
        dates = pd.date_range(end=date.today(), periods=7)
        data = []
        for d in dates:
            data.append({
                'Tanggal': d, 'Menu': 'Kopi Python', 'Harga': 20000, 
                'HPP': 6000, 'Qty': 5, 'Omset': 100000, 'Profit': 70000, 
                'Kategori': 'Minuman', 'Pelanggan': 'Guest'
            })
        df = pd.DataFrame(data)
        df.to_csv(DB_FILE, index=False)
    
    # 2. LOAD MENU (INI YANG KITA UPDATE BIAR GAMBARNYA BEDA-BEDA)
    if os.path.exists(MENU_FILE):
        df_menu = pd.read_csv(MENU_FILE)
    else:
        # DATABASE MENU "SULTAN" (GAMBAR SPESIFIK)
        menu_data = [
            # --- MINUMAN ---
            {'Menu': 'Kopi Python (Arabica)', 'Harga': 25000, 'HPP': 8000, 'Kategori': 'Minuman', 
            'Img': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?q=80&w=400&auto=format&fit=crop'},
            {'Menu': 'Iced Latte.js', 'Harga': 28000, 'HPP': 9000, 'Kategori': 'Minuman', 
            'Img': 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?q=80&w=400&auto=format&fit=crop'},
            {'Menu': 'Blue Screen Soda', 'Harga': 22000, 'HPP': 5000, 'Kategori': 'Minuman', 
            'Img': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=400&auto=format&fit=crop'},
            {'Menu': 'Matcha Learning', 'Harga': 30000, 'HPP': 12000, 'Kategori': 'Minuman', 
            'Img': 'https://images.unsplash.com/photo-1515825838458-f2a94b20105a?q=80&w=400&auto=format&fit=crop'},
            
            # --- MAKANAN ---
            {'Menu': 'Nasi Goreng Full Stack', 'Harga': 35000, 'HPP': 15000, 'Kategori': 'Makanan', 
            'Img': 'https://images.unsplash.com/photo-1603133872878-684f1084261d?q=80&w=400&auto=format&fit=crop'},
            {'Menu': 'RAM-en Special (Pedas)', 'Harga': 38000, 'HPP': 18000, 'Kategori': 'Makanan', 
            'Img': 'https://images.unsplash.com/photo-1552611052-33e04de081de?q=80&w=400&auto=format&fit=crop'},
            {'Menu': 'Burger Algorithm', 'Harga': 45000, 'HPP': 22000, 'Kategori': 'Makanan', 
            'Img': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=400&auto=format&fit=crop'},
            {'Menu': 'Spaghetti Code', 'Harga': 40000, 'HPP': 18000, 'Kategori': 'Makanan', 
            'Img': 'https://images.unsplash.com/photo-1622973536968-3ead9e780960?q=80&w=400&auto=format&fit=crop'},

            # --- SNACK ---
            {'Menu': 'French Fries.zip', 'Harga': 18000, 'HPP': 6000, 'Kategori': 'Snack', 
            'Img': 'https://images.unsplash.com/photo-1630384060421-cb20d0e0649d?q=80&w=400&auto=format&fit=crop'},
            {'Menu': 'Dimsum 404', 'Harga': 20000, 'HPP': 9000, 'Kategori': 'Snack', 
            'Img': 'https://images.unsplash.com/photo-1496116218417-1a781b1c423c?q=80&w=400&auto=format&fit=crop'},
        ]
        df_menu = pd.DataFrame(menu_data)
        df_menu.to_csv(MENU_FILE, index=False)
        
    return df, df_menu

def save_transaksi(new_row):
    # Load data lama, gabung, save ulang
    df_old, _ = load_data()
    df_new = pd.concat([df_old, pd.DataFrame([new_row])], ignore_index=True)
    df_new.to_csv(DB_FILE, index=False)
    return df_new

def save_menu_baru(new_menu_row):
    _, df_menu_old = load_data()
    df_new = pd.concat([df_menu_old, pd.DataFrame([new_menu_row])], ignore_index=True)
    df_new.to_csv(MENU_FILE, index=False)
    return df_new

# Load Data ke Memory
df, df_menu = load_data()

# CSS Styling
st.markdown("""
<style>
    .metric-card { background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #444; }
    .struk-font { font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# Inisialisasi Session
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user_role' not in st.session_state: st.session_state.user_role = ""

# ==========================================
# 2. SISTEM LOGIN
# ==========================================
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<h1 style='text-align:center;'>🦄 CAFE 404 UNICORN</h1>", unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("🚀 MASUK SISTEM", use_container_width=True):
                if u == "admin" and p == "admin":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "CEO"
                    st.success("Welcome CEO!"); time.sleep(0.5); st.rerun()
                elif u == "kasir" and p == "kasir":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Staff"
                    st.success("Semangat Kerja!"); time.sleep(0.5); st.rerun()
                else:
                    st.error("Login Gagal! (Hint: admin/admin atau kasir/kasir)")

# ==========================================
# 3. APLIKASI UTAMA
# ==========================================
else:
    # --- SIDEBAR ---
    with st.sidebar:
        st.title(f"Halo, {st.session_state.user_role}")
        if st.session_state.user_role == "CEO":
            nav = st.radio("Menu:", ["📊 Dashboard Real-time", "🔮 AI Forecasting", "⚙️ Manajemen Menu", "🚪 Logout"])
        else:
            nav = st.radio("Menu:", ["🏪 Mesin Kasir (POS)", "🚪 Logout"])
            
        if nav == "🚪 Logout":
            st.session_state.logged_in = False
            st.rerun()
        
        st.divider()
        st.caption("🟢 System Status: Online")
        st.caption(f"💾 Database: {DB_FILE}")

    # --- HALAMAN 1: DASHBOARD CEO ---
    if nav == "📊 Dashboard Real-time":
        st.title("📊 Unicorn Dashboard")
        
        # Reload data terbaru biar real-time
        df, _ = load_data()
        
        # Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Revenue", f"Rp {df['Omset'].sum():,.0f}")
        m2.metric("Net Profit", f"Rp {df['Profit'].sum():,.0f}")
        m3.metric("Total Order", f"{len(df)} Trx")
        m4.metric("Last Update", datetime.now().strftime("%H:%M:%S"))
        
        st.divider()
        
        # Grafik Omset
        c1, c2 = st.columns([2,1])
        with c1:
            st.subheader("📈 Tren Penjualan")
            daily = df.groupby('Tanggal')['Omset'].sum().reset_index()
            fig = px.area(daily, x='Tanggal', y='Omset', color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.subheader("🏆 Top Menu")
            top = df.groupby('Menu')['Qty'].sum().nlargest(5).reset_index()
            fig2 = px.bar(top, x='Qty', y='Menu', orientation='h', color='Qty')
            st.plotly_chart(fig2, use_container_width=True)

    # --- HALAMAN 2: REAL MACHINE LEARNING FORECASTING ---
    elif nav == "🔮 AI Forecasting":
        from sklearn.linear_model import LinearRegression # Import Otak AI
        
        st.title("🔮 AI Business Forecasting (ML Version)")
        st.info("Model: Linear Regression | Library: Scikit-Learn")

        if st.button("🤖 Jalankan Training & Prediksi"):
            with st.spinner("AI sedang mempelajari data histori..."):
                # 1. Ambil Data Histori
                df_history, _ = load_data()
                daily_sales = df_history.groupby('Tanggal')['Omset'].sum().reset_index()
                
                if len(daily_sales) < 3:
                    st.error("Data terlalu dikit Zan! Minimal butuh 3 hari jualan buat belajar.")
                else:
                    # 2. Persiapan Data (Feature Engineering)
                    # Kita ubah tanggal jadi urutan angka (0, 1, 2...) biar komputer ngerti
                    daily_sales['Hari_Ke'] = np.arange(len(daily_sales))
                    
                    X = daily_sales[['Hari_Ke']] # Input (Hari ke-berapa)
                    y = daily_sales['Omset']    # Target (Duit yang masuk)
                    
                    # 3. Training Model (Proses Belajar)
                    model = LinearRegression()
                    model.fit(X, y)
                    
                    # 4. Prediksi 7 Hari ke Depan
                    last_day = daily_sales['Hari_Ke'].max()
                    future_days = np.array([last_day + i for i in range(1, 8)]).reshape(-1, 1)
                    predictions = model.predict(future_days)
                    
                    # Buat Tanggal Masa Depan
                    last_date = daily_sales['Tanggal'].max()
                    future_dates = [last_date + timedelta(days=i) for i in range(1, 8)]
                    
                    df_pred = pd.DataFrame({'Tanggal': future_dates, 'Prediksi': predictions})

                    # 5. Visualisasi Hasil Belajar AI
                    st.success(f"Training Selesai! Akurasi Model: {model.score(X, y):.2f}")
                    
                    fig = go.Figure()
                    # Garis Data Asli
                    fig.add_trace(go.Scatter(x=daily_sales['Tanggal'], y=daily_sales['Omset'], 
                                        name='Data Histori (Kenyataan)', line=dict(color='cyan')))
                    # Garis Prediksi AI
                    fig.add_trace(go.Scatter(x=df_pred['Tanggal'], y=df_pred['Prediksi'], 
                                        name='Ramalan AI (Masa Depan)', line=dict(color='red', dash='dot')))
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 6. Business Insight
                    total_prediksi = predictions.sum()
                    st.markdown(f"""
                    ### 💡 Insight Buat Syahrul:
                    * *Estimasi Omset Seminggu Depan:* Rp {total_prediksi:,.0f}
                    * *Trend Bisnis:* {"🚀 Naik" if model.coef_[0] > 0 else "📉 Turun"}
                    * *Rekomendasi:* {"Siapkan stok lebih, permintaan naik!" if model.coef_[0] > 0 else "Hati-hati stok sisa, kurangi belanja."}
                    """)
    # --- HALAMAN 3: MANAJEMEN MENU ---
    elif nav == "⚙️ Manajemen Menu":
        st.title("⚙️ Kitchen Database")
        
        t1, t2 = st.tabs(["Daftar Menu", "Tambah Menu Baru"])
        
        with t1:
            st.dataframe(df_menu, use_container_width=True)
            
        with t2:
            with st.form("add_menu"):
                nm = st.text_input("Nama Menu")
                kat = st.selectbox("Kategori", ["Minuman", "Makanan", "Snack"])
                hrg = st.number_input("Harga Jual", 1000)
                hpp = st.number_input("Modal (HPP)", 1000)
                
                if st.form_submit_button("Simpan ke Database"):
                    new_m = {'Menu': nm, 'Harga': hrg, 'HPP': hpp, 'Kategori': kat}
                    save_menu_baru(new_m)
                    st.success(f"Menu {nm} tersimpan permanen!")
                    time.sleep(1); st.rerun()

    # --- HALAMAN 4: MESIN KASIR (POS) DENGAN GAMBAR ---
    elif nav == "🏪 Mesin Kasir (POS)":
        st.title("🏪 Unicorn POS")
        show_hero()
        c_menu, c_cart = st.columns([2, 1]) # Menu lebih lebar biar gambar enak diliat
        
        with c_menu:
            st.subheader("Katalog Menu")
            # Filter Kategori
            cat_filter = st.selectbox("Filter Kategori:", ["All", "Minuman", "Makanan", "Snack"])
            
            # Ambil data sesuai filter
            if cat_filter == "All":
                menu_view = df_menu
            else:
                menu_view = df_menu[df_menu['Kategori'] == cat_filter]
            
            
            # --- LOGIC GRID SYSTEM (UPDATED) ---
            cols = st.columns(3)
            for idx, row in menu_view.iterrows():
                with cols[idx % 3]:
                    with st.container(border=True):
                        # CEK APAKAH MENU PUNYA GAMBAR KHUSUS?
                        if 'Img' in row and pd.notna(row['Img']):
                            gambar = row['Img']
                        else:
                            # Fallback kalo gambar kosong (pake fungsi lama)
                            gambar = get_image_url(row['Kategori'])
                            
                        # TAMPILKAN GAMBAR (Pake use_container_width biar ga ada kotak kuning)
                        st.image(gambar, use_container_width=True)
                        
                        st.markdown(f"*{row['Menu']}*")
                        st.caption(f"Rp {row['Harga']:,.0f}")
                        
                        if st.button("Beli ➕", key=f"add_{idx}", use_container_width=True):
                            if 'cart' not in st.session_state: st.session_state.cart = []
                            st.session_state.cart.append(row.to_dict())
                            st.toast(f"✅ {row['Menu']} masuk keranjang!")
        with c_cart:
            st.subheader("🛒 Keranjang")
            
            if 'cart' not in st.session_state or len(st.session_state.cart) == 0:
                st.info("Belum ada pesanan.")
                st.image("https://cdn-icons-png.flaticon.com/512/2038/2038854.png", width=100)
            else:
                cart_df = pd.DataFrame(st.session_state.cart)
                # Grouping item biar gak panjang ke bawah
                cart_view = cart_df.groupby(['Menu', 'Harga', 'HPP', 'Kategori']).size().reset_index(name='Qty')
                cart_view['Subtotal'] = cart_view['Harga'] * cart_view['Qty']
                
                # Tabel Keranjang
                st.dataframe(cart_view[['Menu', 'Qty', 'Subtotal']], hide_index=True, use_container_width=True)
                
                total_bayar = cart_view['Subtotal'].sum()
                st.divider()
                st.markdown(f"### Total: Rp {total_bayar:,.0f}")
                
                pelanggan = st.text_input("Nama Pelanggan:", "Guest")
                metode = st.radio("Metode Bayar:", ["Tunai", "QRIS"], horizontal=True)
                
                if metode == "QRIS":
                    # Generate QR Code Asli sesuai Total Bayar (Simulasi)
                    st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=BayarRp{total_bayar}", caption="Scan QRIS")
                
                c_bayar, c_batal = st.columns(2)
                with c_bayar:
                    if st.button("✅ BAYAR", type="primary", use_container_width=True):
                        for _, row in cart_view.iterrows():
                            trx_data = {
                                'Tanggal': datetime.now(),
                                'Menu': row['Menu'], 'Harga': row['Harga'], 'HPP': row['HPP'],
                                'Qty': row['Qty'], 'Omset': row['Harga'] * row['Qty'],
                                'Profit': (row['Harga'] - row['HPP']) * row['Qty'],
                                'Kategori': row['Kategori'], 'Pelanggan': pelanggan
                            }
                            save_transaksi(trx_data)
                        st.session_state.cart = []
                        st.success("Lunas!"); st.balloons(); time.sleep(1); st.rerun()
                
                with c_batal:
                    if st.button("❌ Batal", use_container_width=True):
                        st.session_state.cart = []
                        st.rerun()