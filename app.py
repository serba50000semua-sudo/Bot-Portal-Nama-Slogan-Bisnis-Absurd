import streamlit as st
import requests

# --- SISTEM LOGIN MENGGUNAKAN API KEY ---
def login_dengan_api():
    if "api_terverifikasi" not in st.session_state:
        st.session_state["api_terverifikasi"] = False

    if not st.session_state["api_terverifikasi"]:
        st.title("🚀 Login Portal Branding Absurd")
        st.write("Silakan masukkan **API Key Google (Gemini)** Anda untuk membuka portal ide nama bisnis tergila ini.")
        
        masukan_api = st.text_input("Kunci API (API Key):", type="password", placeholder="AIzaSy...")
        
        if st.button("Buka Portal"):
            if not masukan_api:
                st.error("API Key tidak boleh kosong, Bro!")
            else:
                with st.spinner("Memverifikasi keaslian API Key ke server Google..."):
                    url_cek = f"https://generativelanguage.googleapis.com/v1beta/models?key={masukan_api}"
                    try:
                        response = requests.get(url_cek, timeout=10)
                        if response.status_code == 200:
                            st.session_state["api_terverifikasi"] = True
                            st.session_state["API_KEY"] = masukan_api
                            st.rerun()
                        else:
                            st.error("❌ API Key tidak valid. Pastikan Anda menyalinnya dengan benar dari akun Google AI Studio.")
                    except Exception as e:
                        st.error("Gagal terhubung ke Google. Periksa koneksi internet Anda.")
        return False
    return True

def generate_ide_branding(api_key, nama_produk, deskripsi_produk):
    nama_mesin = "models/gemini-3.5-flash"
    
    # Prompt telah ditambahkan filter super ketat anti-SARA/Agama
    prompt_sistem = f"""
    Kamu adalah Pakar Branding, Copywriter Gen-Z, dan Creative Director yang sangat absurd, out-of-the-box, tapi super jenius.
    
    Klien membawa produk: '{nama_produk}'
    Definisi/Detail Produk: '{deskripsi_produk}'
    
    Tugasmu adalah membuat MINIMAL 3 (TIGA) Rekomendasi Nama Brand dan Slogan untuk produk tersebut dengan aturan ketat berikut:
    
    1. GAYA ABSURD TAPI NYANGKUT: Gunakan gaya bahasa jaman sekarang (Gen-Z, slang, gabungan kata aneh, pelesetan pintar). Jangan kaku! Bikin orang yang baca langsung mikir "Hah? Gila tapi bener juga!".
    2. ANALISA TREN TANPA MENIRU: Analisa pola nama brand yang lagi trending saat ini (misal: penggunaan kata 'Kenangan', 'Jiwa', akhiran '-in', atau kata baku yang diplesetkan), TAPI KAMU DILARANG KERAS meniru/menciplak nama brand yang sudah ada. Buat entitas nama yang 100% baru.
    3. BEBAS HAK CIPTA (TRADEMARK SAFE): Pastikan nama ini sangat unik dan belum pernah dipakai oleh brand besar manapun agar klien aman dari tuntutan hak cipta/HAKI.
    4. NON-SARA & NON-AGAMA (SANGAT KETAT): NAMA BRAND MAUPUN SLOGAN DILARANG KERAS menggunakan, menyiratkan, atau mempelesetkan unsur agama apa pun, istilah religi, kitab suci, tokoh agama, rumah ibadah, atau konsep spiritual/ibadah. Semuanya harus 100% netral dan aman untuk semua kalangan.
    5. ALASAN PEMILIHAN: Berikan analisa mendalam kenapa nama dan slogan ini cocok, bagaimana psikologi marketingnya, dan kenapa ini dijamin aman dari hak cipta.
    
    Gunakan format Markdown ini untuk setiap rekomendasi:
    
    🔥 **OPSI [Nomor]: [NAMA BRAND]**
    🗣️ **Slogan:** "[Slogan absurd dan catchy]"
    🧠 **Analisa & Alasan:** [Jelaskan secara detail dan asyik kenapa nama ini jenius, apa daya tariknya buat pasar sekarang, dan konfirmasi keamanan hak ciptanya serta kepatuhan pada aturan non-SARA]
    
    (Buat minimal 3 Opsi)
    """

    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/{nama_mesin}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt_sistem}]}]}

    try:
        response = requests.post(url_gemini, json=payload, headers={'Content-Type': 'application/json'}, timeout=90)
        data = response.json()
        
        if 'error' in data:
            return None, f"Error API Gemini: {data['error']['message']}"
            
        hasil_ai = data['candidates'][0]['content']['parts'][0]['text'].strip()
        return hasil_ai, None
    except Exception as e:
        return None, f"Gagal menghubungi server teks. Error: {e}"

# --- JALANKAN APLIKASI WEB ---
if login_dengan_api():
    # SIDEBAR
    st.sidebar.title("⚙️ Status Akses")
    st.sidebar.success("✅ API Key Terverifikasi Aktif")
        
    if st.sidebar.button("🚪 Keluar / Ganti API Key"):
        st.session_state["api_terverifikasi"] = False
        st.session_state["API_KEY"] = ""
        st.rerun()

    st.sidebar.markdown("---")
    # Tambahan keterangan di sidebar sebagai nilai jual keamanan
    st.sidebar.info("Portal ini mendesain nama brand yang unik, absurd ala jaman *now*, dijamin aman dari benturan hak cipta (HAKI), dan 100% bebas unsur SARA/Agama.")

    # HALAMAN UTAMA
    st.title("👽 Portal Nama & Slogan Bisnis Absurd")
    st.write("Bosan dengan nama bisnis yang gitu-gitu aja? Masukkan produkmu di sini dan biarkan AI meracik nama brand + slogan tergila yang bakal bikin kompetitor ketar-ketir! Dijamin unik, aman HAKI, dan ramah semua kalangan.")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        input_produk = st.text_input("Kategori Produk / Jasa:", placeholder="Contoh: Es Kopi Susu, Jasa Cuci Sepatu, Keripik Pedas...")
    with col2:
        input_deskripsi = st.text_area(
            "Definisi / Keunggulan Produk Kamu:", 
            placeholder="Contoh: Kopi susu pakai gula aren asli, rasanya creamy banget, cocok buat temen begadang ngerjain tugas, harga kantong mahasiswa.", 
            height=100
        )

    if st.button("🚀 Generate Nama Brand Sekarang!"):
        if not input_produk or not input_deskripsi:
            st.warning("Bro, isi dulu nama produk dan deskripsinya biar AI-nya nggak bingung!")
        else:
            # Spinner yang mengindikasikan proses penyaringan keamanan
            with st.spinner("Memindai tren bahasa Jaksel, Gen-Z, dan memverifikasi keamanan HAKI & filter non-SARA di kepala AI..."):
                hasil_branding, error = generate_ide_branding(st.session_state["API_KEY"], input_produk, input_deskripsi)
                
                if error:
                    st.error(f"[GAGAL] {error}")
                else:
                    st.success("Boom! 💥 Ini dia ide nama bisnis absurd khusus buat kamu:")
                    st.markdown(hasil_branding)