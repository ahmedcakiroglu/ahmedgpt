# AhmedGPT

**Canlı demo: [ahmedcakiroglugpt.streamlit.app](https://ahmedcakiroglugpt.streamlit.app/)**

Kişisel portfolyo sitesi için RAG (Retrieval-Augmented Generation) tabanlı soru-cevap asistanı. Ziyaretçiler Ahmed Çakıroğlu hakkında soru soruyor; sistem elindeki bilgi tabanından ilgili bölümleri bulup dil modeline bağlam olarak veriyor ve modelin sadece bu bilgilere dayanarak cevap vermesini sağlıyor.

Projenin odağı "çalışan bir chatbot" değil, **retrieval kalitesinin ölçülmesi ve iyileştirilmesi**. Aşağıdaki sonuçlar, model veya kod değiştirilmeden yalnızca bilgi tabanı metinleri yeniden yazılarak elde edildi.

---

## Mimari

```
Soru
  │
  ├─► embedding modeli ──► soru vektörü (384 boyut)
  │
  ├─► kosinüs benzerliği ──► 36 parça arasında sıralama
  │
  ├─► top-k seçimi (k=3)
  │
  ├─► bağlam + sistem promptu ──► LLM
  │
  └─► cevap + kullanılan kaynaklar
```

| Bileşen | Seçim | Gerekçe |
|---|---|---|
| Embedding | `paraphrase-multilingual-MiniLM-L12-v2` (384-d) | Türkçe destekli, CPU'da hızlı, bu ölçek için yeterli |
| Retrieval | Kosinüs benzerliği, top-k | 36 parça için vektör veritabanı gereksiz karmaşıklık |
| LLM | `gemini-3.5-flash-lite` | Cevaplar matematik/kod içermiyor; hız ve maliyet öncelikli |
| Arayüz | Streamlit | Tek dosyada çalışan, deploy'u kolay UI |

**Parçalama (chunking):** Bilgi tabanı 5 Markdown dosyasından oluşuyor. Paragraflar boş satırdan bölünüyor; başlıklar ayrı parça olmuyor, altlarındaki paragrafın başına bağlam olarak ekleniyor (`Kariyer Hedefleri — Hedeflenen sektör\n\n<paragraf>`). Bu sayede kısa paragraflar da hangi konuya ait olduğunu taşıyor.

---

## Ölçüm sonuçları

26 soruluk bir test seti hazırlandı: 22 cevaplanabilir soru (her biri için beklenen doğru parça etiketli) + 4 bilgi tabanında karşılığı olmayan soru.

### Retrieval başarımı

| Metrik | İyileştirme öncesi | İyileştirme sonrası |
|---|---|---|
| Recall@1 | 59.1% | **63.6%** |
| Recall@3 | 81.8% | **86.4%** |
| Recall@5 | 86.4% | **90.9%** |

İyileştirme, **3 parçanın yeniden yazılmasından** ibaret:
- Terim listeleri düz metne çevrildi (listeler embedding'de seyreliyor, anlam dağılıyor)
- URL yığınları, niyet taşıyan cümlelere dönüştürüldü ("iletişim kurmak isteyenler için...")
- Eksik alan terimleri eklendi ("tıbbi görüntü işleme")

Model, kod ve parametreler aynı kaldı.

### Neden Recall, Precision değil?

Bir RAG sisteminde getirilen alakasız parça zarar vermiyor — dil modeli onu görmezden geliyor. Ama **getirilmeyen doğru parça telafi edilemez**; model o bilgiye hiç erişemiyor. Bu yüzden optimize edilen metrik Recall.

### Benzerlik eşiği denemesi (negatif sonuç)

"Skor şu değerin altındaysa cevaplama" şeklinde bir eşik konulabilir mi diye ölçüldü:

```
doğru cevapların skor aralığı:   0.126 ──────────────── 0.500
cevaplanamaz soruların aralığı:          0.184 ─ 0.206
                                          └── örtüşme ──┘
```

İki dağılım örtüştüğü için ayırıcı bir eşik değeri **yok**. Eşik koymak, düşük skorlu ama doğru cevapları da eler. Savunma katmanı olarak sistem promptundaki "bilgilerde yoksa *Bu konuda bilgim yok* de" talimatı kullanıldı; 4 cevaplanamaz soruda da doğru çalıştı.

### Anizotropi kaynaklı bir hata ve çözümü

İlk sürümde bilgi tabanındaki her paragraf "Ahmed" kelimesiyle başlıyordu, sorular da "Ahmed" içeriyordu. Sonuç: tüm parçalar birbirine yaklaştı ve ayırt edicilik kayboldu.

Ölçüm: sorudan "Ahmed" kelimesi çıkarıldığında **tüm skorlar ~0.30 düştü** ve doğru parça 5. sıradan **1. sıraya** çıktı. Ortak metin, embedding uzayında yapay bir ortak yön oluşturuyor ve skorlara sabit bir katkı ekliyor.

Benimsenen kural: bilgi tabanındaki hiçbir paragraf kişi adıyla başlamıyor.

### Retrieval zero-sum'dur

İyileştirmeden sonra daha önce doğru çalışan bir soru ("Hangi sertifikaları var?") top-3 dışına düştü. Kendi skoru **değişmedi** (0.264) — yeni yazılan parçalar ondan yüksek skor alıp sıralamada önüne geçti. Sıralama mutlak değil görecelidir; her değişiklikten sonra test setinin tamamı yeniden koşulmalı.

---

## Bilinen kısıtlar

- **Konuşma hafızası yok.** Her soru bağımsız işleniyor. "Peki o projede ne kullandı?" gibi bir takip sorusundaki "o" referansı çözülemiyor.
- **Kısa ve çok anlamlı sorular kaçıyor.** Kalan 3 hatanın tamamı bu tip: "Bölümü ne?", "Hangi araçları kullanıyor?" ("araç" hem *tool* hem *vehicle*). Bilinen çözümler (query expansion, BM25 ile hibrit arama) bu ölçek için gereksiz karmaşıklık olduğundan uygulanmadı.
- **Test seti küçük.** 22 soruluk sette tek bir soru ±4.5 puan oynatıyor. Sonuçlar yön gösterir, kesin başarım değeri değildir.
- **Yaş hesabı kodda yapılıyor.** Dil modeli `thinking_level: minimal` ile basit tarih aritmetiğinde hata yaptı. Deterministik hesap kodda, dil işi modelde — prompta hazır sonuç veriliyor.
- **Ücretsiz barındırma uykuya geçiyor.** Streamlit Community Cloud'da uygulama bir süre ziyaretçi almazsa duruyor; sonraki ilk açılış ~30-60 saniye sürüyor. Yavaş olan parçaları vektörlemek değil (~2 sn), embedding modelinin belleğe yüklenmesi.

---

## Kurulum

```bash
conda create -n ahmedgpt python=3.11
conda activate ahmedgpt
pip install -r requirements.txt
```

Proje kökünde bir `.env` dosyası oluştur:

```
GOOGLE_API_KEY=buraya_kendi_anahtarin
```

Çalıştır:

```bash
streamlit run app.py
```

---

## Dosya yapısı

```
ahmedgpt/
├── app.py                 Giriş noktası: ortak stil ve üst menü
├── sayfalar/
│   ├── ana_sayfa.py       Tanıtım ve sohbet
│   └── nasil_yapildi.py   Sistemin anlatımı ve ölçüm sonuçları
├── arayuz/                Simgeler ve bot görseli
├── src/rag.py             RAG motoru (parçalama, arama, cevap üretimi)
├── data/                  Bilgi tabanı (5 Markdown dosyası, 36 parça)
├── notebooks/             Keşif ve ölçüm defterleri
│   ├── 01_embedding_deneme.ipynb
│   └── 02_chunking.ipynb   parçalama, arama, test seti ve değerlendirme
├── .streamlit/config.toml Tema
└── requirements.txt
```

`.env` dosyası `.gitignore` içindedir ve repoya dahil değildir.
