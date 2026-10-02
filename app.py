"""Kişisel site — giriş noktası.

Ortak stil ve üst menü burada; sayfaların içeriği sayfalar/ klasöründe.
"""

import base64
import os
import sys
from pathlib import Path

import streamlit as st

KOK = Path(__file__).parent
sys.path.insert(0, str(KOK / "src"))

# Sunucuda .env dosyası yok; anahtar Streamlit Secrets'tan geliyor.
# Yerelde secrets.toml olmadığı için erişim hata veriyor, o durumda .env devreye giriyor.
try:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

st.set_page_config(
    page_title="Ahmed Çakıroğlu",
    page_icon=":material/memory:",
    layout="wide",
)

# Renkler
GECE = "#0B1B33"        # derin, mat lacivert
GECE_2 = "#132B52"      # gradyanın açık ucu
BUZ = "#8FB4F0"         # lacivert üstünde etiket rengi
MAVI = "#2453D6"        # beyaz üstünde aksiyon rengi
ZEMIN = "#EEF1F6"       # açık gri
CIZGI = "#D8DFEA"
IKINCIL = "#52627A"

# Çok hafif doku: SVG gürültü. Base64 kodlu, çünkü st.html stil bloğunda
# "<" karakteri görürse bloğun tamamını güvenlik gereği siliyor.
_GURULTU = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'>"
    "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/>"
    "<feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.05 0'/></filter>"
    "<rect width='100%' height='100%' filter='url(#n)'/></svg>"
)
DOKU = "url(data:image/svg+xml;base64," + base64.b64encode(_GURULTU.encode()).decode() + ")"

st.html(
    f"""
    <style>
      /* ---------- Sayfa iskeleti: ekranın tamamı ---------- */
      .block-container {{
        max-width: 100%;
        padding: 4.75rem 2rem 1.5rem;
      }}
      [data-testid="stToolbarActions"], [data-testid="stMainMenu"], [data-testid="stMainMenuButton"],
      [data-testid="stAppDeployButton"], [data-testid="stBaseButton-header"],
      [data-testid="stDecoration"], footer {{ display: none; }}

      [data-testid="stHeader"] {{
        background: rgba(238, 241, 246, 0.82);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid {CIZGI};
      }}

      /* ---------- Üst menü: hap şeklinde ---------- */
      [data-testid="stTopNavLink"] {{
        border-radius: 999px !important;
        padding: 0.4rem 1rem !important;
        transition: background 0.15s ease;
      }}
      [data-testid="stTopNavLink"] span {{ font-weight: 500; font-size: 0.9rem; }}
      [data-testid="stTopNavLink"][aria-current="page"] {{ background: {GECE} !important; }}
      [data-testid="stTopNavLink"][aria-current="page"] span {{ color: #FFFFFF !important; }}

      /* ---------- Sol panel ---------- */
      .st-key-profil {{
        min-height: calc(100vh - 6.75rem);
        background:
          {DOKU},
          radial-gradient(120% 80% at 0% 0%, rgba(143,180,240,0.16) 0%, rgba(143,180,240,0) 55%),
          linear-gradient(160deg, {GECE_2} 0%, {GECE} 60%);
        color: #FFFFFF;
        border-radius: 24px;
        padding: clamp(2rem, 3.6vw, 3.75rem);
        gap: 0;
        box-shadow: 0 24px 60px -28px rgba(11, 27, 51, 0.55);
      }}
      .st-key-profil p, .st-key-profil span, .st-key-profil div {{ color: #DCE5F4; }}

      .simge {{
        display: inline-block; width: 18px; height: 18px; flex: none;
        background-color: currentColor;
        -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat;
        -webkit-mask-size: contain; mask-size: contain;
        -webkit-mask-position: center; mask-position: center;
      }}

      .ad {{
        font-family: "Unbounded", "Poppins", sans-serif;
        font-size: clamp(2.6rem, 4.4vw, 4.6rem);
        font-weight: 600;
        line-height: 1.02;
        letter-spacing: -0.02em;
        color: #FFFFFF !important;
        margin: 0;
      }}
      .ad-cizgi {{
        width: 56px; height: 3px; border-radius: 3px;
        background: linear-gradient(90deg, {BUZ}, rgba(143,180,240,0));
        margin: 1.4rem 0 0.9rem;
      }}
      .unvan {{
        font-size: 1rem; font-weight: 500; letter-spacing: 0.01em;
        color: {BUZ} !important; margin: 0 0 1.6rem;
      }}
      .ozet {{
        font-size: 1.05rem; line-height: 1.75; max-width: 38em;
        margin: 0 0 2.4rem; color: #DCE5F4 !important;
      }}

      /* Cam kart */
      .cam {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 18px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.07), 0 10px 30px -18px rgba(0,0,0,0.6);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
      }}

      .kunye {{ padding: 0.4rem 1.5rem; margin: 0 0 2.2rem; }}
      .kunye-satir {{
        display: grid;
        grid-template-columns: minmax(10rem, 13rem) 1fr;
        gap: 1.25rem;
        padding: 1.05rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        align-items: start;
      }}
      .kunye-satir:last-child {{ border-bottom: none; }}
      .kunye-etiket {{
        display: flex; align-items: center; gap: 0.6rem;
        font-weight: 600; font-size: 0.95rem; color: {BUZ} !important;
      }}
      .kunye-etiket .simge {{ color: {BUZ}; }}
      .kunye-deger {{ font-size: 0.97rem; line-height: 1.55; color: #FFFFFF !important; }}
      .kunye-deger strong {{ color: #FFFFFF; font-weight: 600; }}
      .kunye-alt {{ display: block; color: #C3D1E8 !important; }}

      .etiketler {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.55rem; }}
      .etiket {{
        display: inline-flex; align-items: center; gap: 0.45rem;
        padding: 0.32rem 0.8rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        font-size: 0.86rem; font-weight: 500; color: #FFFFFF !important;
      }}
      .kunye-deger > .etiketler:first-child {{ margin-top: 0; }}
      .etiket .simge {{ width: 15px; height: 15px; color: #FFFFFF; }}

      .bolum {{
        display: flex; align-items: center; gap: 0.6rem;
        font-weight: 600; font-size: 1.05rem; color: #FFFFFF !important;
        margin: 0 0 1rem;
      }}
      .bolum .simge {{ color: {BUZ}; }}

      .projeler {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr)); gap: 0.9rem; margin: 0 0 2.2rem; }}
      .proje {{ padding: 1.2rem 1.25rem; display: flex; flex-direction: column; gap: 0.5rem; }}
      .proje-ust {{ display: flex; align-items: center; gap: 0.65rem; }}
      .proje-simge {{
        width: 34px; height: 34px; border-radius: 10px; flex: none;
        display: grid; place-items: center;
        background: rgba(143,180,240,0.14); color: {BUZ};
      }}
      .proje-ad {{ font-weight: 600; font-size: 0.98rem; color: #FFFFFF !important; line-height: 1.3; }}
      .proje-aciklama {{ font-size: 0.9rem; line-height: 1.6; color: #C3D1E8 !important; }}
      .proje-link {{
        display: inline-flex; align-items: center; gap: 0.3rem;
        margin-top: auto; padding-top: 0.25rem;
        font-size: 0.86rem; font-weight: 500;
        color: {BUZ} !important; text-decoration: none;
      }}
      .proje-link .simge {{ width: 15px; height: 15px; }}
      .proje-link:hover {{ color: #FFFFFF !important; }}

      .baglantilar {{ display: flex; gap: 0.75rem; flex-wrap: wrap; }}
      .baglantilar a {{
        display: inline-flex; align-items: center; gap: 0.55rem;
        padding: 0.65rem 1.25rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.18);
        color: #FFFFFF !important; text-decoration: none;
        font-size: 0.92rem; font-weight: 500;
        transition: background 0.15s ease, border-color 0.15s ease;
      }}
      .baglantilar a:hover {{ background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.4); }}
      .st-key-profil a:focus-visible {{ outline: 2px solid {BUZ}; outline-offset: 3px; border-radius: 999px; }}

      /* ---------- Sağ panel: süzülen sohbet kartı ---------- */
      [data-testid="stLayoutWrapper"]:has(> .st-key-sohbet) {{
        position: sticky;
        top: 4.75rem;
        height: calc(100vh - 6.75rem);
        flex-shrink: 0;
      }}
      .st-key-sohbet {{
        height: 100%;
        background:
          radial-gradient(90% 60% at 100% 0%, rgba(36,83,214,0.07) 0%, rgba(36,83,214,0) 60%),
          #FFFFFF;
        border: 1px solid rgba(216, 223, 234, 0.9);
        border-radius: 24px;
        padding: 2rem 2rem 1.4rem;
        box-shadow:
          0 1px 2px rgba(11, 27, 51, 0.05),
          0 30px 70px -30px rgba(11, 27, 51, 0.30);
        display: flex;
        flex-direction: column;
        flex-wrap: nowrap;
      }}

      .sohbet-ust {{ display: flex; align-items: center; gap: 0.9rem; }}
      .sohbet-ust img {{ width: 46px; height: 46px; flex: none; }}
      .sohbet-ad {{
        font-family: "Unbounded", "Poppins", sans-serif;
        font-size: 1.45rem; font-weight: 600; color: {GECE};
        margin: 0; line-height: 1.2;
      }}
      .sohbet-aciklama {{ color: {IKINCIL}; font-size: 0.95rem; line-height: 1.6; margin: 0.9rem 0 0; max-width: 42em; }}

      [data-testid="stLayoutWrapper"]:has(> .st-key-mesajlar) {{
        flex: 1 1 auto;
        min-height: 0;
      }}
      .st-key-mesajlar {{
        height: 100% !important;
        border: none;
        padding: 0.5rem 0.25rem;
      }}

      [data-testid="stChatMessage"] {{
        background: transparent;
        padding: 0.65rem 0.5rem;
        gap: 0.85rem;
      }}
      [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        background: {ZEMIN};
        border-radius: 16px;
      }}
      [data-testid="stChatMessageAvatarUser"] {{ background: {GECE}; color: #FFFFFF; border-radius: 12px; }}
      [data-testid="stChatMessageContent"] p {{ line-height: 1.65; font-size: 0.98rem; }}

      .kaynak {{ font-size: 0.85rem; color: {IKINCIL}; line-height: 1.5; margin: 0.15rem 0; }}

      /* Soru alanı: içe basılmış, geniş, yuvarlak */
      [data-testid="stChatInput"] {{
        border-radius: 22px !important;
        background: #F3F5F9 !important;
        border: 1px solid {CIZGI} !important;
        box-shadow: inset 2px 2px 6px rgba(11,27,51,0.06), inset -2px -2px 6px rgba(255,255,255,0.9);
        padding: 0.45rem 0.5rem 0.45rem 0.75rem;
      }}
      [data-testid="stChatInput"] > div {{
        background: transparent !important;
        border-color: transparent !important;
      }}
      [data-testid="stChatInput"]:focus-within {{
        border-color: {MAVI} !important;
        box-shadow: 0 0 0 4px rgba(36,83,214,0.12);
      }}
      [data-testid="stChatInputTextArea"] {{ font-size: 1rem !important; min-height: 2.6rem; }}
      [data-testid="stChatInputSubmitButton"] {{
        width: 2.6rem !important; height: 2.6rem !important;
        border-radius: 999px !important;
        background: {GECE} !important;
        color: #FFFFFF !important;
      }}
      [data-testid="stChatInputSubmitButton"]:disabled {{ background: #B8C3D6 !important; }}
      [data-testid="stChatInputSubmitButton"] svg {{ color: #FFFFFF !important; fill: #FFFFFF !important; }}

      /* ---------- Makale sayfası ---------- */
      .st-key-makale {{ max-width: 780px; margin: 0 auto; }}
      .st-key-makale p, .st-key-makale li {{ font-size: 1.02rem; line-height: 1.75; }}
      .st-key-makale h1 {{ font-size: clamp(2rem, 3.4vw, 2.8rem); font-weight: 600; line-height: 1.1; }}
      .st-key-makale h2 {{
        font-family: "Poppins", sans-serif; font-size: 1.4rem; font-weight: 600;
        margin-top: 2.6rem; padding-top: 1.6rem; border-top: 1px solid {CIZGI};
      }}
      .st-key-makale h3 {{ font-family: "Poppins", sans-serif; font-size: 1.1rem; font-weight: 600; margin-top: 1.6rem; }}
      .st-key-makale table {{ width: 100%; font-size: 0.95rem; }}
      .st-key-makale th {{ background: {GECE}; color: #FFFFFF; font-weight: 600; text-align: left; }}

      .akis {{ display: flex; flex-wrap: wrap; align-items: stretch; gap: 0.4rem; margin: 1.2rem 0 0.4rem; }}
      .akis-adim {{
        flex: 1 1 120px;
        background: #FFFFFF;
        border: 1px solid {CIZGI};
        border-radius: 14px;
        padding: 0.8rem 0.9rem;
        box-shadow: 0 8px 24px -16px rgba(11,27,51,0.25);
      }}
      .akis-adim strong {{ display: block; font-size: 0.93rem; color: {GECE}; font-weight: 600; }}
      .akis-adim span {{ display: block; font-size: 0.8rem; color: {IKINCIL}; line-height: 1.4; margin-top: 0.2rem; }}
      .akis-ok {{ align-self: center; color: #7A8CA8; font-size: 1.1rem; }}

      .grafik {{
        background: #FFFFFF; border: 1px solid {CIZGI}; border-radius: 18px;
        padding: 1.4rem 1.5rem 1.1rem; margin: 1.2rem 0;
        box-shadow: 0 12px 32px -20px rgba(11,27,51,0.25);
      }}
      .grafik-baslik {{ font-weight: 600; color: {GECE}; margin: 0 0 1rem; font-size: 1rem; }}
      .grafik-satir {{ display: grid; grid-template-columns: 11rem 1fr; gap: 0.8rem; align-items: center; margin: 0.6rem 0; }}
      .grafik-etiket {{ font-size: 0.86rem; color: {GECE}; line-height: 1.3; }}
      .grafik-iz {{ position: relative; height: 22px; }}
      .grafik-iz::before {{ content: ""; position: absolute; left: 0; right: 0; top: 10px; height: 1px; background: {CIZGI}; }}
      .grafik-bar {{ position: absolute; top: 4px; height: 14px; border-radius: 4px; }}
      .grafik-ortusme {{
        position: absolute; top: -4px; bottom: -4px;
        background: repeating-linear-gradient(135deg, rgba(11,27,51,0.16) 0 3px, transparent 3px 7px);
        border-left: 1px dashed {GECE}; border-right: 1px dashed {GECE};
      }}
      .grafik-eksen {{ display: grid; grid-template-columns: 11rem 1fr; gap: 0.8rem; margin-top: 0.4rem; }}
      .grafik-olcek {{ position: relative; height: 1.2rem; font-size: 0.76rem; color: {IKINCIL}; }}
      .grafik-olcek span {{ position: absolute; transform: translateX(-50%); }}
      .grafik-not {{ font-size: 0.85rem; color: {IKINCIL}; margin: 0.9rem 0 0; line-height: 1.55; }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ transition: none !important; }}
      }}

      @media (max-width: 900px) {{
        .block-container {{ padding: 4.5rem 1rem 1.5rem; }}
        .st-key-profil {{ min-height: auto; }}
        [data-testid="stLayoutWrapper"]:has(> .st-key-sohbet) {{ position: static; }}
        [data-testid="stLayoutWrapper"]:has(> .st-key-sohbet) {{ height: 80vh; }}
        .st-key-sohbet {{ padding: 1.4rem 1.1rem 1rem; }}
        .kunye {{ padding: 0.2rem 1rem; }}
        .kunye-satir {{ grid-template-columns: 1fr; gap: 0.45rem; }}
        .grafik-satir, .grafik-eksen {{ grid-template-columns: 1fr; }}
        .akis-ok {{ display: none; }}
      }}
    </style>
    """
)

sayfa = st.navigation(
    [
        st.Page("sayfalar/ana_sayfa.py", title="Ana sayfa", default=True),
        st.Page("sayfalar/nasil_yapildi.py", title="AhmedGPT nasıl yapıldı", url_path="nasil-yapildi"),
    ],
    position="top",
)
sayfa.run()
