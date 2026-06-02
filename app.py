import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. KONFIGURASI HALAMAN WAJIB (Harus di baris paling atas)
# initial_sidebar_state="expanded" memaksa menu kiri selalu terbuka
st.set_page_config(
    page_title="AquaChem IKA Pro",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 2. DESAIN HEADER & DESKRIPSI UTAMA
st.markdown("### ⚡ e- [OH]- [H]+ 🦠")
st.markdown("#### BIO-CHEMICAL REDOKS MATRIX V3.0")
st.title("AquaChem IKA Pro")
st.write("Aplikasi analisis kimia air kuantum untuk melacak indeks kualitas air, keseimbangan anion-kation (aktivitas elektron bebas), serta beban organik mikrobial (bakteri) via pH, BOD, dan COD.")
st.markdown("✨ **[Ca]2+ &nbsp;&nbsp; [SO4]2-** 🔬")
st.markdown("---")

# 3. SIDEBAR - AREA INPUT DATA (Aman dari bug hilang)
st.sidebar.header("🔬 Input Data Sampel")
st.sidebar.write("Masukkan parameter air di bawah ini:")

# Variabel input langsung dideklarasikan agar menempel secara permanen
nama_sampel = st.sidebar.text_input("ID Sampel Aktif:", value="SAMPEL-001")
ph_value = st.sidebar.slider("Nilai pH:", min_value=0.0, max_value=14.0, value=7.2, step=0.1)
bod_value = st.sidebar.number_input("BOD (mg/L):", min_value=0.0, value=15.0)
cod_value = st.sidebar.number_input("COD (mg/L):", min_value=0.0, value=45.0)

st.sidebar.markdown("---")
st.sidebar.markdown("**Keseimbangan Ion (meq/L)**")
kation_ca = st.sidebar.number_input("Kation [Ca]2+:", value=5.5)
anion_so4 = st.sidebar.number_input("Anion [SO4]2-:", value=4.8)

# 4. TABS - NAVIGASI BAWAH
tab1, tab2 = st.tabs(["📊 Live Analytics Dashboard", "🗃️ Database Multi-Sampel"])

with tab1:
    st.markdown(f"📍 **Hasil Analisis Sampel Aktif:** `{nama_sampel}`")
    
    # Menampilkan indikator angka
    col1, col2, col3 = st.columns(3)
    col1.metric("pH Level", ph_value)
    col2.metric("BOD", f"{bod_value} mg/L")
    col3.metric("COD", f"{cod_value} mg/L")

    # Grafik Plotly untuk Keseimbangan Redoks/Ion
    st.subheader("Keseimbangan Anion-Kation")
    fig = go.Figure(data=[
        go.Bar(name='Kation (Ca2+)', x=['Ion Balance'], y=[kation_ca], marker_color='#00d4ff'),
        go.Bar(name='Anion (SO4 2-)', x=['Ion Balance'], y=[anion_so4], marker_color='#ff007f')
    ])
    fig.update_layout(barmode='group', template="plotly_dark", margin=dict(t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.write("Rekapitulasi Data Base Sampel (Simulasi Sementara)")
    # Tabel data interaktif
    data_mock = {
        "ID Sampel": [nama_sampel, "SAMPEL-000"],
        "pH": [ph_value, 6.8],
        "BOD (mg/L)": [bod_value, 12.0],
        "COD (mg/L)": [cod_value, 35.0]
    }
    df = pd.DataFrame(data_mock)
    st.dataframe(df, use_container_width=True)
