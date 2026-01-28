import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

# ==========================================
# BAGIAN 1: KONFIGURASI & FISIKA (OTAKNYA)
# ==========================================

# Settingan Tampilan biar Tajam
plt.rcParams['figure.dpi'] = 100
plt.style.use('seaborn-v0_8-whitegrid')

def hitung_fisika(durasi_detik=3, fps=60, sudut_kemiringan=30):
    """
    Menghitung posisi benda menggunakan Hukum Newton II untuk Rotasi.
    Rumus a = (g * sin(theta)) / (1 + k)
    """
    g = 9.81
    theta = np.radians(sudut_kemiringan)
    
    # Bikin array waktu
    t = np.linspace(0, durasi_detik, durasi_detik * fps)
    
    # --- PESERTA 1: TAHU BULAT (Bola Pejal) ---
    # Inersia Bola Pejal: 2/5 mR^2 --> Konstanta k = 0.4
    k_tahu = 0.4 
    a_tahu = (g * np.sin(theta)) / (1 + k_tahu)
    pos_tahu = 0.5 * a_tahu * t**2 # Rumus S = 1/2 a t^2
    
    # --- PESERTA 2: KALENG BISKUIT (Silinder Pejal) ---
    # Inersia Silinder: 1/2 mR^2 --> Konstanta k = 0.5
    k_kaleng = 0.5
    a_kaleng = (g * np.sin(theta)) / (1 + k_kaleng)
    pos_kaleng = 0.5 * a_kaleng * t**2
    
    return t, pos_tahu, pos_kaleng

# ==========================================
# BAGIAN 2: VISUALISASI (GAMBARNYA)
# ==========================================

# Ambil data fisika
DURASI = 4
FPS = 60
t, p_tahu, p_kaleng = hitung_fisika(DURASI, FPS, sudut_kemiringan=25)

# Setup Canvas (Jendela Gambar)
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-1, 14)
ax.set_ylim(-2, 6)
ax.set_aspect('equal')
ax.set_title(f"🏁 GRAND PRIX: Tahu Bulat vs. Kaleng Biskuit 🏁", fontsize=16, fontweight='bold', color='darkblue')

# Gambar Bidang Miring (Jalanan)
sudut = 25
panjang_jalan = 18
x_alas = np.array([0, panjang_jalan])
y_alas = np.tan(np.radians(sudut)) * -x_alas + 5.5 # Persamaan garis miring
plt.plot(x_alas, y_alas, 'k-', lw=5, color='#5D4037') # Aspal
plt.fill_between(x_alas, y_alas, -5, color='#D7CCC8', alpha=0.5) # Tanah

# --- BIKIN KARAKTER ---
R = 0.6 # Jari-jari benda

# 1. Tahu Bulat (Merah Muda)
# Kita pakai Circle untuk badan, dan Wedge untuk mulut biar kayak Pacman
tahu_body = plt.Circle((0, 0), R, color='#FFAB91', ec='black', lw=2)
tahu_mata = patches.Circle((0, 0), R*0.15, color='black') # Mata
tahu_senyum = patches.Arc((0, 0), R, R, theta1=200, theta2=340, color='black', lw=2) # Mulut senyum

# 2. Kaleng Biskuit (Biru)
# Kita kasih garis silang di tengah biar kelihatan muter
kaleng_body = plt.Circle((0, 0), R, color='#4DD0E1', ec='black', lw=2)
kaleng_garis, = ax.plot([], [], 'w-', lw=3) # Jari-jari roda

# Fungsi Init (Posisi Awal)
def init():
    ax.add_patch(tahu_body)
    ax.add_patch(tahu_mata)
    ax.add_patch(tahu_senyum) # Arc harus ditambahkan sebagai patch
    ax.add_patch(kaleng_body)
    kaleng_garis.set_data([], [])
    return tahu_body, tahu_mata, tahu_senyum, kaleng_body, kaleng_garis

# ==========================================
# BAGIAN 3: ANIMASI (GERAKANNYA)
# ==========================================
def update(frame):
    # --- UPDATE TAHU BULAT ---
    jarak_t = p_tahu[frame]
    # Konversi jarak di bidang miring ke koordinat X, Y layar
    x_t = jarak_t * np.cos(np.radians(sudut))
    y_t = 5.5 - (jarak_t * np.sin(np.radians(sudut))) + R
    
    # Update posisi badan
    tahu_body.center = (x_t, y_t)
    
    # Update posisi mata (biar ikut gerak & muter dikit)
    # Tahu bulat itu bola, jadi muternya smooth.
    rotasi_t = -(jarak_t / R) # Sudut putar (radian)
    
    # Rumus rotasi titik (x,y)
    dx_mata = R*0.4 * np.cos(rotasi_t + np.pi/4) 
    dy_mata = R*0.4 * np.sin(rotasi_t + np.pi/4)
    tahu_mata.center = (x_t + dx_mata, y_t + dy_mata)
    
    # Update senyum (Arc agak tricky dipindah, jadi kita hide aja pas gerak biar simple, atau biarkan di pusat)
    # Trik: Kita bikin arc-nya statis relatif terhadap bola (agak advance), 
    # untuk simpelnya di VS Code: Senyumnya kita ganti jadi titik hidung biar gampang dirotasi
    
    # --- UPDATE KALENG BISKUIT ---
    jarak_k = p_kaleng[frame]
    # Kasih handicap start dikit (start di belakang tahu)
    jarak_k_adj = jarak_k - 1.5 
    
    x_k = jarak_k_adj * np.cos(np.radians(sudut))
    y_k = 5.5 - (jarak_k_adj * np.sin(np.radians(sudut))) + R
    
    kaleng_body.center = (x_k, y_k)
    
    # Efek Putaran Roda Kaleng
    rotasi_k = -(jarak_k_adj / R)
    # Bikin garis silang (+) yang muter
    gx = [x_k + R*np.sin(rotasi_k), x_k - R*np.sin(rotasi_k)]
    gy = [y_k + R*np.cos(rotasi_k), y_k - R*np.cos(rotasi_k)]
    kaleng_garis.set_data(gx, gy)
    
    return tahu_body, tahu_mata, kaleng_body, kaleng_garis

# Render Animasi
print("🎬 Sedang merender animasi... Tunggu jendela pop-up muncul ya!")
anim = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=1000/FPS)

# TAMPILKAN DI VS CODE (JENDELA BARU)
plt.show()