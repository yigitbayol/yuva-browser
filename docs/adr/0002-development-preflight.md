# ADR 0002 — İndirme öncesi açık plan ve güvenli durma

Tarih: 18 Eylül 2026. Durum: kabul edildi — ilk geliştirici araçları.

`./scripts/bootstrap --plan` kaynak sürümü/revizyonu, dış hedef dizin ve disk bütçesini gösterir. `./scripts/bootstrap` buna salt okunur ortam denetimini ekler; bu ilk sürüm henüz kaynak getirmez veya derleme yapılandırmaz. Eksik aşamayı başarılı bootstrap diye göstermez; sıfır olmayan kod döndürür.

100–200 GB veya daha fazla gerçek çalışma alanı gerekebilir; yapılandırma, semboller ve önbellek miktarı değişir. İlk otomatik büyük indirmeyi başlatma için 200 GiB boş alan ihtiyatlı Yuva politikasıdır, upstream'in resmî evrensel minimumu değildir. Sonraki gerçek ölçümler bu politikayı gerekçeyle değiştirebilir. RAM 8 GiB altında engel, 32 GiB altında kapasite uyarısıdır; bu sayılar başarılı build garantisi değildir.

macOS için tam Xcode, erişilebilir SDK ve hedef aygıtta APFS kontrol edilir. Command Line Tools tek başına tam Xcode sayılmaz. Pardus OS kimliği ayrı tanınır; diğer Linux ile eşitlenmez. Windows/Linux/Pardus araç zinciri yeterliliği bu ilk sürümde tamamlanmadığından hazır sonucu verilmez.

İlk kaynak adayı resmî kanal verisi, Gitiles tag→commit eşleşmesi, DEPS SHA-256 ve depot_tools commit'iyle çapraz denetlenir. Bu geliştirici girdisi doğrulamasıdır; HTTPS'i ikili yayın için imza yetkisi saymaz. Kaynak/hook çalıştırılmaz. Tam alt bağımlılık grafiği incelenmeden büyük otomatik bootstrap aşaması açılmaz.

Git indeksi `.gitignore`dan bağımsız denetlenir: bilinen kaynak/çıktı/önbellek/sır yolları, tek dosyada 5 MiB ve toplam 100 MiB ince depo bütçesi. Bu bir genel sır tarayıcısı veya geçmiş temizleyici değildir. İncelenmiş büyük test verisi gerekirse sonraki ayrı politika kararı gerekir; genel bypass eklenmez.

Kullanıcıya veya CIya sunulan durumlar İngilizce makine değerleri, Türkçe açıklamalar taşır. Hatalı imza/hash, beklenmeyen sürüm, eksik bağımlılık, yama çakışması ve okunamayan veri sessizce başarıya dönüşemez.
