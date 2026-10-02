"""Ana sayfa: solda tanıtım, sağda AhmedGPT."""

import base64
from pathlib import Path

import streamlit as st

from arayuz.simgeler import SIMGE
from rag import AhmedGPT

KOK = Path(__file__).parent.parent
BOT_SVG = KOK / "arayuz" / "bot.svg"
BOT_URI = "data:image/svg+xml;base64," + base64.b64encode(BOT_SVG.read_bytes()).decode()

GITHUB = "https://github.com/ahmedcakiroglu"
LINKEDIN = "https://www.linkedin.com/in/ahmed-%C3%A7ak%C4%B1ro%C4%9Flu"
HABER_BOTU = "https://github.com/ahmedcakiroglu/news-bot"

KARSILAMA = (
    "Hoş geldiniz! Ben AhmedGPT. Ahmed'in teknik yetkinlikleri, projeleri ve "
    "kariyeri hakkında detaylı bilgi verebilirim. Ne hakkında konuşmak istersiniz?"
)


@st.cache_resource(show_spinner="AhmedGPT hazırlanıyor...")
def motoru_yukle():
    return AhmedGPT(data_dir=KOK / "data", env_dosyasi=KOK / ".env")


def avatar(rol):
    return str(BOT_SVG) if rol == "assistant" else None


def kaynaklari_goster(kaynaklar):
    with st.expander(f"Kaynaklar ({len(kaynaklar)})"):
        for k in kaynaklar:
            st.html(
                f'<p class="kaynak"><strong>{k["bolum"]}</strong> — '
                f'{k["kaynak"]}, benzerlik {k["skor"]:.2f}</p>'
            )


def etiket(metin, simge=None):
    ic = SIMGE[simge] if simge else ""
    return f'<span class="etiket">{ic}{metin}</span>'


def kunye_satiri(simge, baslik, deger):
    return f"""
      <div class="kunye-satir">
        <span class="kunye-etiket">{SIMGE[simge]}{baslik}</span>
        <div class="kunye-deger">{deger}</div>
      </div>"""


def proje(simge, ad, aciklama, link_html=""):
    return f"""
      <div class="proje cam">
        <div class="proje-ust">
          <span class="proje-simge">{SIMGE[simge]}</span>
          <span class="proje-ad">{ad}</span>
        </div>
        <div class="proje-aciklama">{aciklama}</div>
        {link_html}
      </div>"""


KUNYE = "".join(
    [
        kunye_satiri(
            "egitim",
            "Eğitim",
            '<strong>Gazi Üniversitesi</strong>'
            '<span class="kunye-alt">Elektrik-Elektronik Mühendisliği</span>'
            '<div class="etiketler">'
            + etiket("3. sınıf")
            + etiket("Mezuniyet 2028")
            + "</div>",
        ),
        kunye_satiri(
            "konular",
            "Çalıştığım konular",
            '<div class="etiketler">'
            + etiket("Makine öğrenmesi")
            + etiket("Bilgisayarlı görü")
            + etiket("Dil modelleri")
            + etiket("Edge AI")
            + "</div>",
        ),
        kunye_satiri(
            "araclar",
            "Araçlar",
            '<div class="etiketler">'
            + etiket("Python", "python")
            + etiket("PyTorch", "pytorch")
            + etiket("scikit-learn", "scikitlearn")
            + etiket("MLflow", "mlflow")
            + etiket("Git", "git")
            + "</div>",
        ),
        kunye_satiri("dil", "Dil", "Türkçe, İngilizce (B2)"),
        kunye_satiri("konum", "Konum", "Ankara"),
    ]
)

PROJELER = "".join(
    [
        proje(
            "ahmedgpt",
            "AhmedGPT",
            "Bu sayfadaki asistan. Hakkımda yazdığım metinlerden soruyla ilgili "
            "kısımları bulup bir dil modeline veriyor. Doğru bilgiyi ilk üç sonuç "
            "içinde bulma oranı %86.",
            f'<a class="proje-link" href="nasil-yapildi" target="_self">'
            f'Nasıl yapıldı {SIMGE["ok"]}</a>',
        ),
        proje(
            "haber",
            "Yapay zeka destekli haber botu",
            "GitHub Actions üzerinde günde beş kez çalışıyor; haberleri Claude ile "
            "özetleyip görselle birlikte X'te paylaşıyor.",
            f'<a class="proje-link" href="{HABER_BOTU}" target="_blank" rel="noopener">'
            f'Kaynak kod {SIMGE["ok"]}</a>',
        ),
        proje(
            "robotaksi",
            "TEKNOFEST 2025 Robotaksi, finalist",
            "HÜMA Rover takımında SLAM ve ROS2 tarafında çalıştım.",
        ),
    ]
)


sol, sag = st.columns([9, 11], gap="large")

with sol:
    with st.container(key="profil"):
        st.html(
            f"""
            <h1 class="ad">Ahmed<br>Çakıroğlu</h1>
            <div class="ad-cizgi"></div>
            <p class="unvan">Yapay zeka ve elektronik</p>
            <p class="ozet">
              Gazi Üniversitesi'nde Elektrik-Elektronik Mühendisliği okuyorum.
              Yapay zeka ile elektroniğin kesiştiği yerde çalışıyorum: veriden
              model kurmayı, kurduğum modeli doğru ölçmeyi ve onu gerçek
              donanıma taşımayı öğreniyorum.
            </p>

            <div class="kunye cam">{KUNYE}</div>

            <p class="bolum">{SIMGE["projeler"]}Projeler</p>
            <div class="projeler">{PROJELER}</div>

            <div class="baglantilar">
              <a href="{GITHUB}" target="_blank" rel="noopener">{SIMGE["github"]}GitHub</a>
              <a href="{LINKEDIN}" target="_blank" rel="noopener">{SIMGE["linkedin"]}LinkedIn</a>
            </div>
            """
        )

with sag:
    with st.container(key="sohbet"):
        st.html(
            f"""
            <div class="sohbet-ust">
              <img src="{BOT_URI}" alt="">
              <p class="sohbet-ad">AhmedGPT</p>
            </div>
            <p class="sohbet-aciklama">
              Ahmed'in uzmanlık alanları ve projeleri hakkında merak ettiklerinizi sorabilirsiniz.
            </p>
            """
        )

        if "gecmis" not in st.session_state:
            st.session_state.gecmis = []

        mesajlar = st.container(height=480, key="mesajlar", autoscroll=True)

        with mesajlar:
            with st.chat_message("assistant", avatar=avatar("assistant")):
                st.write(KARSILAMA)
            for mesaj in st.session_state.gecmis:
                with st.chat_message(mesaj["rol"], avatar=avatar(mesaj["rol"])):
                    st.write(mesaj["metin"])
                    if mesaj.get("kaynaklar"):
                        kaynaklari_goster(mesaj["kaynaklar"])

        soru = st.chat_input("Bir soru yazın", key="soru")

        if soru:
            st.session_state.gecmis.append({"rol": "user", "metin": soru})
            with mesajlar:
                with st.chat_message("user"):
                    st.write(soru)
                with st.chat_message("assistant", avatar=avatar("assistant")):
                    kaynaklar = []
                    try:
                        motor = motoru_yukle()
                        with st.spinner("Cevap hazırlanıyor..."):
                            cevap, kaynaklar = motor.cevapla(soru)
                    except Exception as hata:
                        print(f"AhmedGPT hatası: {hata!r}")
                        cevap = "Şu an cevap üretemiyorum. Birazdan tekrar deneyin."
                    st.write(cevap)
                    if kaynaklar:
                        kaynaklari_goster(kaynaklar)
            st.session_state.gecmis.append(
                {"rol": "assistant", "metin": cevap, "kaynaklar": kaynaklar}
            )

        # Sayfa tamamen çizildikten sonra modeli yükle: ziyaretçi soldaki
        # tanıtımı okurken model hazırlanıyor, ilk soru beklemiyor.
        try:
            motoru_yukle()
        except Exception as hata:
            print(f"AhmedGPT yüklenemedi: {hata!r}")
