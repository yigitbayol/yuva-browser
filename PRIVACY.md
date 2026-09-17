# Mahremiyet politikası ve tasarım taahhütleri

Durum: Faz 0. Henüz Yuva tarayıcısı yayımlanmadı. Bu belge mevcut bir ürünün ölçülmüş davranışını değil, hedeflenen davranışı açıklar. GitHub'ın bu depoya yapılan ziyaretleri işlemesi GitHub'ın politikalarına tabidir.

**Yuva, nereye gittiğini bilmez.** Gezinme geçmişi, ziyaret edilen URL'ler, arama sorguları, site bazlı koruma sayaçları ve hatırlanan site seçimleri Yuva altyapısına gönderilemez. Reklam kimliği, davranış profilleme, gizli analiz, zorunlu hesap veya bulut hizmeti bulunmaz. İlk sürümlerde Yuva telemetrisi ve otomatik çökme raporu yükleme yoktur.

Gezinme oturumları varsayılan olarak geçici tasarlanır; sınırlar [PRIVACY_ARCHITECTURE.md](PRIVACY_ARCHITECTURE.md) içindedir. Tek sekmenin kapanması oturumu bitirmez. İndirilen/dışa aktarılan dosyalar, açıkça kaydedilen yer imleri/ayarlar ve ileride izin verilen site verileri kalabilir. Geçici gezinme RAM, swap, işletim sistemi çökme kaydı, yedek veya diskte adli iz bırakmama garantisi değildir.

## Beklenen ağ akışları

| Alıcı | Amaç ve görülebilen veri |
| --- | --- |
| Siteler ve üçüncü tarafları | İstenen sayfa, IP ve kullanıcı girdileri; engelleme tüm gözlemi durdurmaz |
| Seçilen arama sağlayıcısı | Gönderilen sorgu; Yuva aracısı yoktur; öneriler başlangıçta kapalıdır |
| DNS/DoH sağlayıcısı ve ağ işletmecisi | Yapılandırmaya göre DNS sorgusu veya bağlantı üstverisi; DoH anonimlik sağlamaz |
| GitHub/CDN/bileşen dağıtıcısı | Sabit güncelleme/kayıt/liste yolları, IP, zaman ve platform/sürüm isteği; gezinmeye göre sorgu veya kurulum kimliği yoktur |
| Değerlendirilen tehdit istihbaratı sağlayıcısı | Yalnız onaylanmış ve belgelenmiş protokol verisi; hash öneki/OHTTP sınırlamaları vardır; seçim yayın önkoşuludur |
| Eklenti/yerel yardımcı işletmecisi | Verilen izinlere ve yazılım davranışına göre veri; Yuva koruma sınırının dışına çıkabilir |
| İşletim sistemi güven/imza hizmetleri | İşletim sistemi politikasına göre doğrulama ve güvenlik kontrolleri |

Trusted Sites eşleştirmesi yereldir; geçerli önbellek çevrimdışı da kullanılabilir. “Bu site güvenilir mi?” diye Yuva'ya alan adı gönderilmez. Süresi dolan kayıt olumlu etiketi kaldırır.

Bağlantı üstverileri kimliklendirme ve ilişkilendirmeye elverişlidir. Tam anonimlik, işverene/ISS'ye görünmezlik veya takip edilemezlik sözü verilmez. Hesapla giriş yapmak kullanıcıyı o hizmete tanıtır. Doğrulanmış alan adı etiketi kurumun davranışına veya içeriğine kefalet değildir.

Gelecekte tanılama için ayrı açık rıza, açık uygulama, izin verilen alanlarla sınırlı şema ve gönderilecek içeriğin incelenmesi gerekir. URL içeren çökme dökümleri sansürlemenin kusursuz olduğu varsayımıyla yüklenemez. Varsayılan kapalıdır; geçmiş gönderilmez, veri asgari tutulur.

Yayın öncesinde ölçülmüş uç/veri envanteri, saklama davranışı ve gerçek sağlayıcı seçimleri açıklanır. Önemli upstream/hizmet değişikliklerinde tekrar doğrulanır. Uyumluluk bildirimleri sentetik veya bilinçli temizlenmiş örnekler kullanır; otomatik gezinme kaydı toplanmaz.

Resmî dağıtımlardaki yetişkin içerik engeli yerel, imzalı liste kullanır. Engellenen denemeler kalıcı geçmiş/sayaç/günlük oluşturmaz ve Yuva'ya gönderilmez. Yanlış pozitif bildirimine yalnız önizlenmiş domain, açık onayla eklenebilir; yol/sorgu/kimlik bilgisi eklenmez. [İçerik koruması](CONTENT_PROTECTION.md).

Vakitler varsayılan kapalı isteğe bağlı yardımcıdır. Din/inanç tahmini yapılmaz. Etkinleştirildiğinde elle seçilen şehir yerelde tutulur; GPS sessizce alınmaz. Uzak sağlayıcı ancak veri akışı açıklanarak kullanıcı seçimiyle kullanılır; yerel hesaplama önceliklidir. [İsteğe bağlı özellikler](docs/OPTIONAL_FEATURES.md).

Yuva reklam karşıtı değil, takip karşıtıdır: **Yuva internetin gelir modeline karar vermez. Kullanıcının takip edilip edilmeyeceğine kullanıcı karar verir.** Standart takipçileri engeller, takip yapmayan reklama genel engel koymaz; Sıkı ayrıca reklamları engellemeyi hedefler. Siteye özgü Kapalı yalnız takip/reklam filtrelerini etkiler. Zorunlu güvenlik ve içerik koruması ayrı kalır. Yuva kendi reklamını göstermez ve ücretli reklam istisnası satmaz.

GPC varsayılan açık tercih sinyalidir; DNT de açıklanmış kullanıcı mahremiyet tercihine göre tasarlanır. Sinyaller tek başına teknik engel veya her ülkede bağlayıcı hukuki garanti değildir. Çerez tercihi hiçbir zaman sahte “kabul” rızasına dönüştürülmez. Hatırlama pazarlama izni vermez.
