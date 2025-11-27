import streamlit as st
import random
import math

st.set_page_config(page_title="Retro Arcade Karekok Oyunu", layout="wide")

# --- RENKLER (CSS ile) ---
st.markdown("""
    <style>
    .stButton>button {background-color:#FF00C0; color:white; height:60px; width:200px; border-radius:15px; font-size:20px;}
    .stMarkdown {color:#00FFAA; font-family:Courier; }
    </style>
""", unsafe_allow_html=True)

# --- OYUN VERİLERİ ---
ZORLUKLAR = {
    "KOLAY": {"puan":5, "sayilar":[8,12,18,20,24,27,32,48]},
    "ORTA": {"puan":7, "sayilar":[54,63,72,75,98,108,125]},
    "ZOR": {"puan":10, "sayilar":[162,180,192,242,288,338,450]}
}

def karekok_sadelestir(sayi):
    sonuclar = []
    for a in range(1,int(math.sqrt(sayi))+1):
        b = sayi // (a*a)
        if a*a*b == sayi:
            sonuclar.append((a,b))
    return sonuclar[-1]

def soru_olustur(zorluk):
    sayi = random.choice(ZORLUKLAR[zorluk]["sayilar"])
    en_sade = karekok_sadelestir(sayi)
    a, b = en_sade
    yanlis = [(a+1,b),(a,b+1),(a+1,b+1)]
    secenekler = [en_sade]+yanlis
    random.shuffle(secenekler)
    return sayi, secenekler, en_sade

# --- SESSION STATE ---
if 'durum' not in st.session_state:
    st.session_state.durum = "MENU"
if 'puan' not in st.session_state:
    st.session_state.puan = 0
if 'soru_say' not in st.session_state:
    st.session_state.soru_say = 0
if 'secilen_zorluk' not in st.session_state:
    st.session_state.secilen_zorluk = None
if 'mevcut' not in st.session_state:
    st.session_state.mevcut = None
if 'geri' not in st.session_state:
    st.session_state.geri = ""

# --- FONKSİYONLAR ---
def yeni_soru():
    sayi, secenekler, dogru = soru_olustur(st.session_state.secilen_zorluk)
    st.session_state.mevcut = (sayi, secenekler, dogru)
    st.session_state.geri = ""

def secenek_sec(cevap):
    dogru = st.session_state.mevcut[2]
    if cevap == dogru:
        st.session_state.puan += ZORLUKLAR[st.session_state.secilen_zorluk]["puan"]
        st.session_state.geri = "DOĞRU!"
    else:
        st.session_state.geri = f"YANLIŞ! Doğru: {dogru[0]}√{dogru[1]}"
    st.session_state.soru_say += 1
    if st.session_state.soru_say < 10:
        yeni_soru()
    else:
        st.session_state.durum = "SONUC"

# --- ANA MENÜ ---
if st.session_state.durum == "MENU":
    st.markdown("<h1 style='color:#FF00C0'>RETRO ARCADE KAREKÖK OYUNU</h1>", unsafe_allow_html=True)
    if st.button("BAŞLA"):
        st.session_state.durum = "ZORLUK"

# --- ZORLUK SEÇİMİ ---
elif st.session_state.durum == "ZORLUK":
    st.markdown("<h2 style='color:#00FFAA'>Zorluk Seçin:</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    if col1.button("KOLAY"):
        st.session_state.secilen_zorluk = "KOLAY"
        st.session_state.durum = "OYUN"
        yeni_soru()
    if col2.button("ORTA"):
        st.session_state.secilen_zorluk = "ORTA"
        st.session_state.durum = "OYUN"
        yeni_soru()
    if col3.button("ZOR"):
        st.session_state.secilen_zorluk = "ZOR"
        st.session_state.durum = "OYUN"
        yeni_soru()

# --- OYUN ---
elif st.session_state.durum == "OYUN":
    sayi, secenekler, dogru = st.session_state.mevcut
    st.markdown(f"<h2 style='color:#FFFF00'>Soru {st.session_state.soru_say+1}/10</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:#00FFFF'>√{sayi} = ?</h1>", unsafe_allow_html=True)
    cols = st.columns(2)
    for i, sec in enumerate(secenekler):
        text = f"{sec[0]}√{sec[1]}" if sec[0]>1 else f"√{sec[1]}"
        if cols[i%2].button(text):
            secenek_sec(sec)
    st.markdown(f"<h3 style='color:#FF00FF'>{st.session_state.geri}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:#00FF00'>Puan: {st.session_state.puan}</h3>", unsafe_allow_html=True)

# --- SONUÇ ---
elif st.session_state.durum == "SONUC":
    st.markdown("<h1 style='color:#FF00C0'>OYUN BİTTİ!</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:#00FFAA'>Toplam Puan: {st.session_state.puan}</h2>", unsafe_allow_html=True)
    if st.button("YENİDEN OYNA"):
        st.session_state.durum = "MENU"
        st.session_state.puan = 0
        st.session_state.soru_say = 0
