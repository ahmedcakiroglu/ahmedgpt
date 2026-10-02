"""AhmedGPT'nin nasıl çalıştığını ve ölçüm sonuçlarını anlatan sayfa."""

import streamlit as st

REPO = "https://github.com/ahmedcakiroglu/ahmedgpt"

# Eşik grafiği: 0 – 0.6 arası benzerlik ekseni
EKSEN_UST = 0.6


def konum(deger):
    return f"{deger / EKSEN_UST * 100:.2f}%"


def genislik(bas, son):
    return f"{(son - bas) / EKSEN_UST * 100:.2f}%"


DOGRU = (0.126, 0.500)
CEVAPSIZ = (0.184, 0.206)

with st.container(key="makale"):
    st.markdown("# AhmedGPT nasıl yapıldı")
    st.markdown(
        "AhmedGPT, ziyaretçilerin benim hakkımdaki sorularını cevaplayan bir "
        "RAG (Retrieval-Augmented Generation) sistemi. Dil modeline benim hakkımda "
        "bir şey öğretmedim; her soruda ilgili bilgiyi bulup modelin önüne koyuyorum "
        "ve yalnızca onu kullanmasını istiyorum. Bu sayfada sistemin nasıl "
        "çalıştığını ve ölçtüğüm sonuçları anlatıyorum."
    )

    st.markdown("## Bir soru nasıl cevaplanıyor")
    st.html(
        """
        <div class="akis" role="list" aria-label="Bir sorunun cevaplanma adımları">
          <div class="akis-adim" role="listitem"><strong>Soru</strong><span>Ziyaretçi yazıyor</span></div>
          <div class="akis-ok" aria-hidden="true">›</div>
          <div class="akis-adim" role="listitem"><strong>Vektöre çevirme</strong><span>384 boyutlu embedding</span></div>
          <div class="akis-ok" aria-hidden="true">›</div>
          <div class="akis-adim" role="listitem"><strong>Arama</strong><span>36 parça içinde kosinüs benzerliği</span></div>
          <div class="akis-ok" aria-hidden="true">›</div>
          <div class="akis-adim" role="listitem"><strong>Bağlam</strong><span>En yakın 3 parça</span></div>
          <div class="akis-ok" aria-hidden="true">›</div>
          <div class="akis-adim" role="listitem"><strong>Dil modeli</strong><span>Sadece bu bağlamla cevap</span></div>
        </div>
        """
    )
    st.markdown(
        "Soru ve bilgi tabanındaki her paragraf aynı embedding modeliyle vektöre "
        "çevriliyor. Anlamca yakın metinlerin vektörleri de birbirine yakın düştüğü "
        "için, sorunun vektörüne en yakın üç paragraf soruyla en ilgili bilgiyi "
        "taşıyor. Bu üç paragraf dil modeline \"bilgiler\" olarak veriliyor; modele "
        "bunların dışına çıkmaması, cevap yoksa bilmediğini söylemesi talimatı "
        "veriliyor. Cevabın altındaki *Kaynaklar* kısmı, hangi paragrafların "
        "kullanıldığını ve benzerlik skorlarını gösteriyor."
    )

    st.markdown("## Bilgi tabanı")
    st.markdown(
        "Kaynak, benim yazdığım beş Markdown dosyası: eğitim, projeler, teknik "
        "yetkinlikler, kariyer hedefleri ve kişisel bilgiler. Metin boş satırlardan "
        "paragraflara bölünüyor ve toplam 36 parça çıkıyor. Başlıklar ayrı parça "
        "olmuyor, altlarındaki paragrafın başına ekleniyor. Böylece \"Kasım 2005 "
        "doğumlu.\" gibi kısa bir paragraf bile hangi konuya ait olduğunu taşıyor."
    )
    st.markdown(
        "Yaş gibi hesap gerektiren bilgileri dil modeline bırakmadım. İlk denemede "
        "model doğum tarihinden yaşı yanlış hesapladı; şimdi yaş kodda bugünün "
        "tarihinden hesaplanıp modele hazır veriliyor."
    )

    st.markdown("## Bileşenler")
    st.markdown(
        """
| Bileşen | Seçim | Neden |
|---|---|---|
| Embedding | `paraphrase-multilingual-MiniLM-L12-v2` | Türkçe destekli, işlemcide hızlı |
| Arama | Kosinüs benzerliği, ilk 3 sonuç | 36 parça için vektör veritabanı gereksiz |
| Dil modeli | Gemini Flash-Lite | Cevaplar kısa ve hesap içermiyor, hız öncelikli |
| Arayüz | Streamlit | Python ile tek yerde, kolay yayınlanıyor |
        """
    )

    st.markdown("## Ölçüm")
    st.markdown(
        "Sistemi 26 soruluk bir test setiyle ölçtüm. 22 sorunun cevabı bilgi "
        "tabanında var ve her biri için doğru paragrafı işaretledim; 4 sorunun "
        "cevabı bilgi tabanında yok. Ölçtüğüm şey Recall@k: doğru paragrafın ilk "
        "k sonuç arasında gelme oranı."
    )
    st.markdown(
        """
| | İlk ölçüm | Düzeltmeden sonra |
|---|---|---|
| Recall@1 | %59,1 | %63,6 |
| Recall@3 | %81,8 | **%86,4** |
| Recall@5 | %86,4 | %90,9 |
        """
    )
    st.markdown(
        "Sistem ilk 3 sonucu kullandığı için asıl önemli satır Recall@3. Artış için "
        "model ya da kod değiştirmedim; yalnızca üç paragrafı yeniden yazdım. Terim "
        "listelerini düz cümlelere çevirdim, link yığınlarını ne işe yaradıklarını "
        "anlatan cümlelere dönüştürdüm ve eksik kalan alan terimlerini ekledim."
    )
    st.markdown(
        "Precision yerine Recall'a bakmamın sebebi şu: dil modeline giden alakasız "
        "bir paragraf zarar vermiyor, model onu görmezden geliyor. Ama doğru paragraf "
        "gelmezse model o bilgiye hiç ulaşamıyor."
    )

    st.markdown("## Ölçerken fark ettiklerim")

    st.markdown("### Ortak bir kelime bütün skorları şişiriyor")
    st.markdown(
        "İlk sürümde her paragraf \"Ahmed\" diye başlıyordu, soruların çoğunda da "
        "\"Ahmed\" geçiyordu. Sorudan bu kelimeyi çıkardığımda bütün skorlar yaklaşık "
        "0,30 düştü ve doğru paragraf 5. sıradan 1. sıraya çıktı. Ortak kelime bütün "
        "metinleri aynı yöne çekip aralarındaki farkı siliyordu. O yüzden bilgi "
        "tabanında hiçbir paragraf adımla başlamıyor."
    )

    st.markdown("### Bir eşik değeriyle \"bilmiyorum\" demek mümkün değil")
    st.markdown(
        "Benzerlik skoru belli bir değerin altındaysa cevap vermemeyi denemek "
        "istedim. Bunun için iki grubun skorlarını karşılaştırdım:"
    )
    st.html(
        f"""
        <figure class="grafik" aria-label="Benzerlik skoru aralıkları">
          <p class="grafik-baslik">Benzerlik skorlarının aralığı</p>

          <div class="grafik-satir">
            <span class="grafik-etiket">Cevabı olan sorular, doğru paragrafın skoru</span>
            <div class="grafik-iz">
              <div class="grafik-bar" style="left:{konum(DOGRU[0])}; width:{genislik(*DOGRU)}; background:#1D4ED8;"
                   title="Cevabı olan sorular: {DOGRU[0]:.3f} – {DOGRU[1]:.3f}"></div>
              <div class="grafik-ortusme" style="left:{konum(CEVAPSIZ[0])}; width:{genislik(*CEVAPSIZ)};"
                   title="Örtüşme: {CEVAPSIZ[0]:.3f} – {CEVAPSIZ[1]:.3f}"></div>
            </div>
          </div>

          <div class="grafik-satir">
            <span class="grafik-etiket">Cevabı olmayan sorular, en yüksek skor</span>
            <div class="grafik-iz">
              <div class="grafik-bar" style="left:{konum(CEVAPSIZ[0])}; width:{genislik(*CEVAPSIZ)}; background:#D97706;"
                   title="Cevabı olmayan sorular: {CEVAPSIZ[0]:.3f} – {CEVAPSIZ[1]:.3f}"></div>
            </div>
          </div>

          <div class="grafik-eksen">
            <span></span>
            <div class="grafik-olcek">
              <span style="left:0%">0</span>
              <span style="left:{konum(0.1)}">0,1</span>
              <span style="left:{konum(0.2)}">0,2</span>
              <span style="left:{konum(0.3)}">0,3</span>
              <span style="left:{konum(0.4)}">0,4</span>
              <span style="left:{konum(0.5)}">0,5</span>
              <span style="left:100%">0,6</span>
            </div>
          </div>

          <p class="grafik-not">
            Cevabı olan sorularda doğru paragrafın skoru 0,126 ile 0,500 arasında;
            cevabı olmayan sorularda en yüksek skor 0,184 ile 0,206 arasında. Taralı
            bölgede iki grup üst üste biniyor.
          </p>
        </figure>
        """
    )
    st.markdown(
        "Cevabı olmayan soruların skorları, cevabı olan soruların aralığının tam "
        "içinde kalıyor. Hangi eşiği seçersem seçeyim ya cevabı olan soruları "
        "kesiyorum ya da cevabı olmayanları geçiriyorum. Bu yüzden eşik kullanmadım; "
        "\"bilmiyorum\" kararını dil modeline bıraktım ve test setindeki 4 sorunun "
        "dördünde de doğru çalıştı."
    )

    st.markdown("### Bir paragrafı iyileştirmek başka bir soruyu bozabiliyor")
    st.markdown(
        "Paragrafları yeniden yazdıktan sonra daha önce doğru çalışan \"Hangi "
        "sertifikaları var?\" sorusu ilk üçün dışına düştü. Sorunun kendi skoru hiç "
        "değişmemişti; yeni yazdığım paragraflar daha yüksek skor alıp önüne "
        "geçmişti. Arama sonucu göreli bir sıralama olduğu için her değişiklikten "
        "sonra test setinin tamamını yeniden çalıştırıyorum."
    )

    st.markdown("## Bilinen kısıtlar")
    st.markdown(
        """
- **Önceki mesajları hatırlamıyor.** Her soru ayrı işleniyor; "O projede ne kullandı?" gibi bir devam sorusundaki "o"yu çözemiyor.
- **Kısa ve çok anlamlı sorularda kaçırıyor.** Kalan hataların hepsi bu tipte; örneğin "araç" hem yazılım aracı hem taşıt anlamına geliyor.
- **Test seti küçük.** 22 soruda tek bir soru sonucu yaklaşık 4,5 puan oynatıyor; sonuçlar yön gösteriyor, kesin değer değil.
- **İlk açılış yavaş olabiliyor.** Ücretsiz sunucu bir süre ziyaret almazsa uyuyor; uyanması yarım dakika ile bir dakika arası sürüyor.
        """
    )

    st.markdown("## Kaynak kod")
    st.markdown(
        f"Kodun tamamı, test seti ve ölçüm defterleri [GitHub'da]({REPO}) açık."
    )
