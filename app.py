import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ==========================================
# 1. PENGAMAN SIDEBAR & LAYOUT (WAJIB DI ATAS)
# ==========================================
st.set_page_config(
    page_title="AquaChem IKA Pro V3.0",
    layout="wide",
    initial_sidebar_state="expanded"  # Mengunci menu kiri agar tidak hilang di HP
)

# Custom CSS untuk tema gelap biosfer kuantum
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .metric-box {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HEADER UTAMA (Sesuai Screenshot)
# ==========================================
st.markdown("<h3 style='color: #00d4ff;'>⚡ e⁻ &nbsp; [OH]⁻ &nbsp; [H]⁺ &nbsp; 🦠</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='color: #00ffa3; letter-spacing: 2px;'>BIO-CHEMICAL REDOKS MATRIX V3.0</h5>", unsafe_allow_html=True)
st.title("AquaChem IKA Pro")
st.write(
    "Aplikasi analisis kimia air kuantum untuk melacak indeks kualitas air, "
    "keseimbangan anion-kation (aktivitas elektron bebas), serta beban organik "
    "mikrobial (bakteri) via pH, BOD, dan COD."
)
st.markdown("<h5 style='color: #a3a3a3;'>✨ [Ca]²⁺ &nbsp;&nbsp; [SO₄]²⁻ &nbsp;&nbsp; 🔬</h5>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 3. SIDEBAR PERMANEN (INPUT PARAMETER)
# ==========================================
st.sidebar.markdown("### 🔬 Parameter Sampel")
st.sidebar.write("Silakan input data analisis laboratorium:")

# Metadata Sampel
nama_sampel = st.sidebar.text_input("ID Sampel Aktif:", value="SAMPEL-001")

# Parameter Fisika-Kimia Dasar
st.sidebar.markdown("**📊 Parameter Dasar**")
ph = st.sidebar.slider("Derajat Keasaman (pH):", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
bod = st.sidebar.number_input("BOD (Biological Oxygen Demand) mg/L:", min_value=0.0, value=15.4, step=0.1)
cod = st.sidebar.number_input("COD (Chemical Oxygen Demand) mg/L:", min_value=0.0, value=42.1, step=0.1)

# Konsentrasi Ion Eksperimental (meq/L)
st.sidebar.markdown("**🧪 Komposisi Ion (meq/L)**")
kation_ca = st.sidebar.number_input("Kation [Ca]²⁺:", min_value=0.0, value=5.5, step=0.1)
kation_mg = st.sidebar.number_input("Kation [Mg]²⁺:", min_value=0.0, value=2.1, step=0.1)
kation_na = st.sidebar.number_input("Kation [Na]⁺:", min_value=0.0, value=1.8, step=0.1)

anion_so4 = st.sidebar.number_input("Anion [SO₄]²⁻:", min_value=0.0, value=4.8, step=0.1)
anion_cl = st.sidebar.number_input("Anion [Cl]⁻:", min_value=0.0, value=2.5, step=0.1)
anion_hco3 = st.sidebar.number_input("Anion [HCO₃]⁻:", min_value=0.0, value=2.0, step=0.1)

# ==========================================
# 4. ENGINE KALKULASI (RUMUS MATRIKS KIMIA)
# ==========================================
# Perhitungan Aktivitas Elektron Bebas (pE) teoritis berbasis pH kuantum
pe_teoritis = 13.2 - ph  

# Perhitungan Rasio Bebas Organik (BOD/COD)
if cod > 0:
    rasio_biodegradabilitas = bod / cod
else:
    rasio_biodegradabilitas = 0.0

# Total Kation & Anion untuk mengecek Keseimbangan Muatan (Ion Balance)
total_kation = kation_ca + kation_mg + kation_na
total_anion = anion_so4 + anion_cl + anion_hco3

if (total_kation + total_anion) > 0:
    ion_balance_error = ((total_kation - total_anion) / (total_kation + total_anion)) * 100
else:
    ion_balance_error = 0.0

# Prediksi Beban Mikrobial (Simulasi Kuantum)
beban_mikrobial = (bod * 1.5) + (ph * 0.8)

# ==========================================
# 5. TAMPILAN INTERFACE UTAMA (TABS NAVIGASI)
# ==========================================
tab1, tab2 = st.tabs(["📊 Live Analytics Dashboard", "🗃️ Database Multi-Sampel"])

with tab1:
    st.markdown(f"#### 📍 Hasil Analisis Sampel Aktif: <span style='color:#00ffa3;'>{nama_sampel}</span>", unsafe_allow_html=True)
    
    # Grid Informasi Utama (Metrics)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Derajat Keasaman (pH)", value=f"{ph}", delta=f"{ph-7.0:.1f} dari Netral")
    with col2:
        st.metric(label="Potensial Redoks (pE)", value=f"{pe_teoritis:.2f} eq")
    with col3:
        st.metric(label="Rasio BOD/COD", value=f"{rasio_biodegradabilitas:.2f}", delta="Biodegradable" if rasio_biodegradabilitas > 0.5 else "Persisten")
    with col4:
        st.metric(label="Keseimbangan Muatan", value=f"{ion_balance_error:.2f} %", delta="Stabil" if abs(ion_balance_error) <= 5 else "Tidak Seimbang", delta_color="normal" if abs(ion_balance_error) <= 5 else "inverse")

    st.markdown("---")
    
    # Layout Baris Kedua: Grafik & Detail Matriks
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Matrix Keseimbangan Anion - Kation (meq/L)")
        
        # Grafik Bar Interaktif Plotly
        fig = go.Figure()
        
        # Data Kation
        fig.add_trace(go.Bar(
            name='Kation (Muatan +)',
            x=['[Ca]²⁺', '[Mg]²⁺', '[Na]⁺'],
            y=[kation_ca, kation_mg, kation_na],
            marker_color='#00d4ff'
        ))
        
        # Data Anion
        fig.add_trace(go.Bar(
            name='Anion (Muatan -)',
            x=['[SO₄]²⁻', '[Cl]⁻', '[HCO₃]⁻'],
            y=[anion_so4, anion_cl, anion_hco3],
            marker_color='#ff007f'
        ))
        
        fig.update_layout(
            barmode='group',
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=20, b=20, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Status Kuantum")
        st.write(f"**Total Kation:** {total_kation:.2f} meq/L")
        st.write(f"**Total Anion:** {total_anion:.2f} meq/L")
        
        # Alert Box Dinamis berdasarkan hasil perhitungan
        if abs(ion_balance_error) > 5:
            st.error("⚠️ Peringatan: Selisih kation dan anion melebihi batas standar 5%! Periksa kembali akurasi alat uji.")
        else:
            st.success("✅ Validasi Kimia: Keseimbangan ion air memenuhi hukum elektroneutralitas.")
            
        st.info(f"🧬 **Estimasi Densitas Organik:** {beban_mikrobial:.1f} unit/mL berdasarkan korelasi aktivitas reduktor kimia.")

with tab2:
    st.subheader("🗃️ Database Registrasi Multi-Sampel")
    st.write("Berikut adalah arsip data sampel aktif dan log simulasi laboratorium sebelumnya:")
    
    # Membuat representasi tabel data historis
    data_log = {
        "ID Sampel": [nama_sampel, "SAMPEL-002", "SAMPEL-003", "SAMPEL-004"],
        "pH": [ph, 6.5, 8.1, 7.0],
        "BOD (mg/L)": [bod, 10.2, 4.5, 22.1],
        "COD (mg/L)": [cod, 30.0, 15.2, 65.0],
        "Total Kation": [total_kation, 6.2, 8.5, 12.1],
        "Total Anion": [total_anion, 6.0, 8.2, 11.9],
        "Error (%)": [round(ion_balance_error, 2), 1.64, 1.80, 0.83]
    }
    df_database = pd.DataFrame(data_log)
    st.dataframe(df_database, use_container_width=True)
