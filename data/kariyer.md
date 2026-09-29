# Kariyer Hedefleri

## Genel yön: uçtan uca yapay zeka mühendisliği

Hedefi, yapay zekanın tek bir dar alanında kalmak yerine uçtan uca çalışabilen bir mühendis olmak: klasik makine öğrenmesinden derin öğrenmeye, büyük dil modeli tabanlı sistemlerden bu modellerin kaynak kısıtlı donanımlarda çalıştırılmasına kadar. Bu iki uç (LLM tarafı ve gömülü/donanım tarafı) birbirini besliyor, ikisini birden bilen mühendis sayısı az.

## Büyük dil modelleri ve ajan sistemleri

LLM tarafında odaklandığı konular RAG (Retrieval-Augmented Generation) mimarileri, prompt mühendisliği, çok ajanlı (multi-agent) sistem tasarımı ve araç kullanımı (tool use / function calling). Bir dil modelini sadece soru-cevap için kullanmak ile, kendi başına çok adımlı görevleri çözebilen bir sistem kurmak arasındaki farkı önemsiyor.

Bu alandaki yaklaşımı "API'ye prompt atmak" seviyesinde kalmamak üzerine kurulu. Bir RAG sisteminde asıl mühendislik işinin dil modelinde değil; metnin nasıl parçalandığında, hangi embedding modelinin seçildiğinde, kaç parça getirildiğinde ve retrieval kalitesinin nasıl ölçüldüğünde olduğunu düşünüyor. Aynı dil modeliyle iyi kurulmuş bir RAG ile kötü kurulmuş bir RAG arasında uçurum olduğunu projelerinde gördü.

## Edge AI ve gömülü yapay zeka

İkinci odak alanı, modelleri sunucularda değil; mikrodenetleyiciler, gömülü kartlar ve kaynak kısıtlı cihazlar üzerinde çalıştırmak. Bu alan Edge AI ve TinyML olarak biliniyor. Quantization (nicemleme), model boyutu küçültme ve gerçek zamanlı çıkarım (inference) optimizasyonu öğrenmek istediği konular arasında.

Bu tercihin arkasındaki mantık şu: sadece Python'da model eğiten çok sayıda kişi var, ancak eğitilen modeli gerçek bir donanıma, sensöre veya gömülü sisteme entegre edebilen mühendis sayısı çok daha az. Elektrik-Elektronik Mühendisliği altyapısı, devre bilgisi ve sinyal işleme temeli bu kesişimde ona avantaj sağlıyor.

## İki alanın kesişimi

Uzun vadede ilgisini çeken problemler, bu iki alanın buluştuğu yerde: cihaz üzerinde çalışan küçük dil modelleri, sensör verisini yorumlayan yapay zeka sistemleri ve otonom platformlarda karar veren ajan mimarileri. Sinyal işleme ile makine öğrenmesinin kesiştiği problemler de aynı şekilde.

## Hedeflenen sektör

Kariyerini Türk savunma sanayiinde sürdürmeyi hedefliyor. ASELSAN, ROKETSAN ve TUSAŞ öncelikli hedefleri arasında. Bu şirketlerin otonom sistemler, görüntü işleme, sinyal işleme ve gömülü yazılım alanlarındaki çalışmaları kendi ilgi alanlarıyla doğrudan örtüşüyor.

## Yüksek lisans planı

Lisans eğitiminden sonra yüksek lisans yapmayı planlıyor ve Almanya'yı değerlendiriyor. Alman üniversitelerinin mühendislik programlarını, başvuru şartlarını ve not dönüşüm sistemini araştırdı. Henüz kesinleşmiş bir üniversite veya program tercihi yok.

## Staj hedefi

Savunma sanayii veya yapay zeka alanında staj yapmayı hedefliyor.

## Çalışma yaklaşımı

Öğrenme yaklaşımında kod yazma bağımsızlığına önem veriyor. Hazır kod kopyalamak yerine her satırın ne yaptığını anlayarak ilerlemeyi, teorik temeli öğrenmeden uygulamaya geçmemeyi tercih ediyor. Örneğin RAG sistemleriyle çalışmaya başlamadan önce embedding geometrisi ve attention mekanizmasının matematiğini çalıştı.

Projelerinde "çalışan demo" seviyesinde kalmak yerine, mühendislik açısından doğru kurulmuş sistemler üretmeyi amaçlıyor: doğru veri bölme, deney takibi, anlamlı değerlendirme metrikleri ve sonuçların dürüstçe raporlanması.

## İlgi duyduğu teknik alanlar

Bilgisayarlı görü (computer vision), doğal dil işleme (NLP), LLM tabanlı ajan sistemleri, RAG mimarileri, TinyML, sensör füzyonu, PCB tasarımı ve ROS/C++ tabanlı robotik.
