# Projeler

## TEKNOFEST 2025 — Robotaksi Otonom Araç Yarışması

HÜMA Rover takımıyla Robotaksi kategorisinde finalist oldu. Takımdaki rolü SLAM (eşzamanlı konumlandırma ve haritalama) algoritmaları ve ROS2 tarafıydı. Otonom araç yazılımı, sensör verisi işleme ve robotik yazılım altyapısı konularında saha deneyimi kazandı.

## AhmedGPT — RAG tabanlı kişisel chatbot

Kendi hakkındaki bilgileri kaynak alan, ziyaretçilerin sorularını cevaplayan bir RAG chatbot'u. Sistem; metinleri anlamlı parçalara bölüp embedding modeliyle vektöre çeviriyor, gelen soruya kosinüs benzerliği ile en yakın parçaları buluyor ve bunları bağlam olarak bir dil modeline veriyor. Python, sentence-transformers ve vektör arama üzerine kurulu.

## Yapay zeka destekli X (Twitter) haber botu

GNews API, Claude API, Tweepy ve GitHub Actions kullanarak günde beş kez otomatik paylaşım yapan bir haber botu geliştirdi. Bot, haberleri çekip yapay zeka ile özetliyor ve otomatik olarak paylaşıyor. Geliştirme sürecinde OAuth kimlik doğrulama ve API limitleriyle ilgili çeşitli sorunları çözdü. GitHub Actions ile zamanlanmış görev (cron) kurulumu bu projede öğrendiği konulardan biri.

## Göğüs röntgeni sınıflandırma (CNN)

Tıbbi görüntü işleme alanında bir çalışma: NIH Chest X-ray veri seti üzerinde PyTorch ile sıfırdan bir evrişimli sinir ağı (CNN) eğitti. Sağlık verisiyle görüntü sınıflandırma problemini ele alan bu projede asıl odağı model performansı değil, doğru makine öğrenmesi mühendisliği pratiğiydi: hasta bazlı veri sızıntısının tespiti ve GroupShuffleSplit ile önlenmesi, MLflow ile deney takibi, ve accuracy yerine confusion matrix, precision/recall ve ROC-AUC ile değerlendirme.

Proje sonunda model AUC 0.48 ile rastgele tahmin seviyesinde kaldı. Bu sonuç, sınırlı veriyle sıfırdan CNN eğitmenin neden işe yaramadığını ve gerçek uygulamalarda neden transfer learning kullanıldığını somut olarak gösterdi.

## EEE212 — DC güç kaynağı tasarımı

LM2596 tabanlı anahtarlamalı regülatör kullanarak bir DC güç kaynağı tasarladı. Devre LTSpice ile simüle edildi, bileşenler Ankara'dan temin edilerek fiziksel olarak kuruldu. Analog devre tasarımı, simülasyon ve bileşen seçimi konularında pratik deneyim sağladı.

## Kişisel portfolyo web sitesi

Koyu ve teknik bir estetiğe sahip kişisel portfolyo sitesi geliştirdi. Sitede glitch animasyonları, parçacık alanları ve radar tarayıcı gibi bilim kurgu temalı arayüz öğeleri kullanıldı. HTML, CSS ve JavaScript ile sıfırdan kodlandı.
