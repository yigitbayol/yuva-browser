# Güvenlik politikası

Yuva şu anda yalnızca tasarım aşamasındadır. **Desteklenen tarayıcı ikilisi veya uygulanmış güvenlik garantisi yoktur.** Önerilen önlemler [THREAT_MODEL.md](THREAT_MODEL.md) ve [BUILD_RELEASE_SECURITY.md](BUILD_RELEASE_SECURITY.md) içindedir.

## Bildirim

Bu çalışmada özel güvenlik bildirimi veya izlenen güvenlik iletişim adresi yapılandırılmadı/doğrulanmadı. Parola, kişisel gezinme verisi, özel belge veya istismar edilebilir açık ayrıntılarını herkese açık issue içine koymayın.

İlk tarayıcı yayını öncesinde GitHub özel açık bildirimi etkinleştirilip denenmeli; izlenen alternatif iletişim adresi, gerekirse şifreleme anahtarı ve iki müdahale sorumlusu belirlenmelidir. Etkinleştirildiğinde deponun **Security → Advisories → Report a vulnerability** akışı kullanılmalıdır. Bu seçenek yoksa teknik ayrıntı içermeyen bir issue üzerinden özel iletişim kanalı istenebilir. Onay gelmeden bildirimin alındığını varsaymayın.

Bildirim; Yuva/Chromium/işletim sistemi sürümlerini, sentetik ve küçültülmüş yeniden üretimi, beklenen/gerçek davranışı ve etkiyi içermelidir. Gerçek oturum belirteci veya tam profil göndermeyin. Chromium kaynaklı açıklar gerektiğinde upstream güvenlik sürecine de iletilir; Yuva etkisi özel kanalda koordine edilir.

## Önerilen destek ve müdahale düzeni

Yalnız açıkça desteklenen kanal/platformun güncel sürümü düzeltme alır. Önizleme yayını kararlı sürüm güvenlik taahhüdü değildir. Her artefakt destek durumunu açıklamalı; eski sürümler güncelmiş gibi sunulmamalıdır.

Özel bildirimi iki iş günü içinde karşılama, acil bildirimi alındığında hemen önceliklendirme ve düzeltmeyi koordineli duyurma operasyonel hedeflerdir; henüz doğrulanmış hizmet taahhüdü veya ödül programı yoktur.

Uyumluluk için sandbox, süreç/site yalıtımı, TLS, karışık içerik veya güncelleme doğrulaması zayıflatılmaz. [Güvenlik özellik kaydı](docs/SECURITY_FEATURE_REGISTER.md) tutulur. Kalkan ya da Trusted Sites istisnası bu kuralları aşamaz.

İmzalama/derleme/kayıt altyapısının ele geçirilmesi güvenlik olayıdır. Yayın terfisi durdurulur, kanıt korunur, etkilenen yetki iptal edilir ve kimliği doğrulanmış kanaldan kurtarma yapılır. Kullanıcıdan imzasız acil ikiliye güvenmesi istenmez. Güncelleme gecikmesi ve tatbikatlar [UPSTREAM_STRATEGY.md](UPSTREAM_STRATEGY.md) içindedir.

## Zorunlu ürün güvenliği

Olay/çalışma önceliği: banka ve finansal oltalama → kamu kurumu taklidi → kimlik bilgisi hırsızlığı → zararlı indirmeler → takip/profilleme → yetişkin içerik engelleme → genel kötü amaçlı siteler. Bu sıralama alttaki zorunlu korumayı isteğe bağlı yapmaz; aktif Chromium istismarına acil müdahale her zaman gerekir.

Resmî Developer Preview dahil bütün dağıtımlar [banka/kamu kaydı ve benzer adres korumasını](TRUSTED_SITES_DESIGN.md), [yerel içerik engelini](CONTENT_PROTECTION.md) ve mahremiyet varsayılanlarını sağlamalıdır. Yetkili kurum envanteri/kanıt, imza/rollback, yanlış pozitif ve platform testleri yayın kapısıdır. Üretim listesi veya çalışan koruma henüz yoktur.

Bank Security Mode tasarım/test gerektirir; MFA, eklenti ve pano akışları sessizce değiştirilemez. İçerik engeli oltalamadan ayrıdır; denemeler loglanmaz, domain rapora yalnız açık onayla eklenir. Açık kaynak değiştirilerek sınırlamalar kaldırılabilir; atlatılamazlık veya tam anonimlik iddiası yoktur.
