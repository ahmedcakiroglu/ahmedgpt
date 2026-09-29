"""AhmedGPT — Streamlit arayüzü."""

import os
import sys
from pathlib import Path

import streamlit as st

KOK = Path(__file__).parent
sys.path.insert(0, str(KOK / "src"))

from rag import AhmedGPT  # noqa: E402

# Sunucuda .env dosyası yok; anahtar Streamlit Secrets'tan geliyor.
# Yerelde secrets.toml olmadığı için erişim hata veriyor, o durumda .env devreye giriyor.
try:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

st.set_page_config(
    page_title="AhmedGPT",
    page_icon="💬",
    layout="centered",
)

st.markdown(
    """
    <style>
      .stApp { background: #F5FAFF; }

      .baslik {
        font-size: 2rem;
        font-weight: 600;
        color: #1E3A5F;
        margin-bottom: 0.2rem;
      }
      .altbaslik {
        color: #5B7C99;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
      }

      [data-testid="stChatMessage"] {
        background: #FFFFFF;
        border: 1px solid #DCEBFA;
        border-radius: 12px;
        padding: 0.4rem 0.9rem;
        margin-bottom: 0.5rem;
      }

      .stButton > button {
        background: #FFFFFF;
        border: 1px solid #BBD9F5;
        color: #1E3A5F;
        border-radius: 999px;
        font-size: 0.85rem;
        padding: 0.3rem 0.9rem;
      }
      .stButton > button:hover {
        background: #E8F2FE;
        border-color: #7FB3E8;
        color: #1E3A5F;
      }

      footer, #MainMenu { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Bilgi tabanı yükleniyor...")
def motoru_yukle():
    return AhmedGPT(data_dir=KOK / "data", env_dosyasi=KOK / ".env")


st.markdown('<div class="baslik">AhmedGPT</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="altbaslik">Ahmed Çakıroğlu hakkında merak ettiklerinizi sorun.</div>',
    unsafe_allow_html=True,
)

try:
    motor = motoru_yukle()
except Exception as hata:
    st.error(f"Sistem başlatılamadı: {hata}")
    st.stop()

if "gecmis" not in st.session_state:
    st.session_state.gecmis = []

ORNEK_SORULAR = [
    "Hangi bölümde okuyor?",
    "Hangi projeleri yaptı?",
    "Nerede çalışmak istiyor?",
    "Hangi teknolojileri biliyor?",
]

if not st.session_state.gecmis:
    st.caption("Örnek sorular")
    kolonlar = st.columns(2)
    for i, ornek in enumerate(ORNEK_SORULAR):
        if kolonlar[i % 2].button(ornek, key=f"ornek_{i}", use_container_width=True):
            st.session_state.bekleyen_soru = ornek
            st.rerun()

for rol, metin in st.session_state.gecmis:
    with st.chat_message(rol, avatar="🙂" if rol == "user" else "💬"):
        st.write(metin)

soru = st.chat_input("Bir soru yazın...")

if "bekleyen_soru" in st.session_state:
    soru = st.session_state.pop("bekleyen_soru")

if soru:
    st.session_state.gecmis.append(("user", soru))
    with st.chat_message("user", avatar="🙂"):
        st.write(soru)

    with st.chat_message("assistant", avatar="💬"):
        with st.spinner("Düşünüyor..."):
            try:
                cevap, kaynaklar = motor.cevapla(soru)
            except Exception as hata:
                cevap, kaynaklar = f"Bir hata oluştu: {hata}", []

        st.write(cevap)

        if kaynaklar:
            with st.expander("Kullanılan kaynaklar"):
                for k in kaynaklar:
                    st.caption(
                        f"**{k['bolum']}** · {k['kaynak']} · benzerlik {k['skor']:.2f}"
                    )

    st.session_state.gecmis.append(("assistant", cevap))
