"""AhmedGPT — RAG motoru.

Bilgi tabanını okur, parçalara böler, vektörler ve gelen sorulara
bu parçaları kaynak göstererek cevap üretir.
"""

import os
from datetime import date
from pathlib import Path

import torch
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer

EMBEDDING_MODELI = "paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODELI = "gemini-3.5-flash-lite"

DOGUM_YILI = 2005
DOGUM_AYI = 11

MIN_PARCA_UZUNLUGU = 10

SISTEM_PROMPT = """Sen Ahmed Çakıroğlu'nun kişisel sitesindeki asistansın.
Ziyaretçiler Ahmed hakkında soru soruyor, sen sadece aşağıda verilen bilgilere
dayanarak cevap veriyorsun.

Kurallar:
- Sadece BİLGİLER bölümündeki içeriği kullan. Kendi genel bilgini kullanma.
- Bilgilerde cevap yoksa "Bu konuda bilgim yok" de. Tahmin yürütme, uydurma.
- Kısa ve net cevap ver, 2-3 cümleyi geçme.
- Türkçe cevap ver, samimi ama profesyonel bir dille.
- Sana verilen tarih ve yaş bilgisini gerektiğinde kullanabilirsin."""


def yas_hesapla():
    """Doğum tarihinden bugünkü yaşı hesaplar."""
    bugun = date.today()
    yas = bugun.year - DOGUM_YILI
    if bugun.month < DOGUM_AYI:
        yas -= 1
    return yas


def parcalari_yukle(klasor):
    """Klasördeki .md dosyalarını okuyup parçalara böler.

    Paragraflar boş satırdan ayrılır. Başlıklar ayrı parça olmaz,
    altlarındaki paragrafın başına bağlam olarak eklenir.
    """
    parcalar = []

    for dosya in sorted(Path(klasor).glob("*.md")):
        icerik = dosya.read_text(encoding="utf-8")
        ana_baslik = ""
        bolum_baslik = ""

        for blok in icerik.split("\n\n"):
            blok = blok.strip()

            if not blok:
                continue

            if blok.startswith("## "):
                bolum_baslik = blok.lstrip("# ")
                continue

            if blok.startswith("# "):
                ana_baslik = blok.lstrip("# ")
                bolum_baslik = ""
                continue

            if len(blok) < MIN_PARCA_UZUNLUGU:
                continue

            parcalar.append({
                "metin": f"{ana_baslik} — {bolum_baslik}\n\n{blok}",
                "kaynak": dosya.name,
                "bolum": bolum_baslik,
            })

    return parcalar


class AhmedGPT:
    """Bilgi tabanını yükler ve sorulara cevap üretir."""

    def __init__(self, data_dir="data", env_dosyasi=".env"):
        load_dotenv(env_dosyasi)

        anahtar = os.getenv("GOOGLE_API_KEY")
        if not anahtar:
            raise RuntimeError(
                "GOOGLE_API_KEY bulunamadı. .env dosyasını kontrol et."
            )

        self.parcalar = parcalari_yukle(data_dir)
        if not self.parcalar:
            raise RuntimeError(f"{data_dir} klasöründe parça bulunamadı.")

        self.model = SentenceTransformer(EMBEDDING_MODELI)
        self.vektorler = self.model.encode(
            [p["metin"] for p in self.parcalar]
        )
        self.client = genai.Client(api_key=anahtar)

    def ara(self, soru, k=3):
        """Soruya en yakın k parçayı skorlarıyla döndürür."""
        soru_vektoru = self.model.encode([soru])
        skorlar = self.model.similarity(soru_vektoru, self.vektorler)[0]
        degerler, siralar = torch.topk(skorlar, k=min(k, len(self.parcalar)))

        return [
            {**self.parcalar[i], "skor": float(s)}
            for s, i in zip(degerler, siralar)
        ]

    def cevapla(self, soru, k=3):
        """Soruyu cevaplar. (cevap, kullanılan parçalar) döndürür."""
        bulunanlar = self.ara(soru, k=k)
        baglam = "\n\n---\n\n".join(p["metin"] for p in bulunanlar)

        mesaj = f"BİLGİLER:\n\n{baglam}\n\nSORU: {soru}"
        sistem = (
            f"{SISTEM_PROMPT}\n\n"
            f"Bugünün tarihi: {date.today().strftime('%d.%m.%Y')}. "
            f"Ahmed şu an {yas_hesapla()} yaşında."
        )

        yanit = self.client.interactions.create(
            model=LLM_MODELI,
            system_instruction=sistem,
            input=mesaj,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 500,
                "thinking_level": "minimal",
            },
        )

        return yanit.output_text, bulunanlar
