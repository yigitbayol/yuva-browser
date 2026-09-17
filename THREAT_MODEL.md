# Tehdit modeli

Durum: Faz 0, 18 Eylül 2026. Kontroller tasarımdır; henüz tarayıcı üzerinde kanıtlanmadı. Güvenlik ve upstream güncelleme sürdürülebilirliği diğer ürün hedeflerinin önkoşuludur.

## Güvenlik çalışmasının öncelikleri

1. Bankacılık ve finansal oltalama.
2. Kamu hizmeti/kurum taklidi.
3. Kimlik bilgisi ve oturum çalınması.
4. Zararlı indirmeler.
5. Takip ve profilleme.
6. Yetişkin içerik engelleme.
7. Genel kötü amaçlı siteler.

Bu sıra kaynak ve olay önceliğidir; alttaki zorunlu korumayı kaldırmaz. Kritik aktif motor istismarı bütün özellik çalışmalarını durdurur. Resmî dağıtımda kapsamlı banka/kamu kaydı, benzer adres koruması, yerel içerik engeli ve mahremiyet varsayılanları zorunludur. Hiçbiri Chromium güvenlik mekanizmalarını zayıflatamaz.

## Varlıklar, saldırganlar, güven sınırları

Korunanlar: kimlik bilgisi, oturum, belge, gezinme verisi, izinler, indirilen dosya, güncelleme bütünlüğü, alan adı kimliği, yerel politika ve kullanıcının güvenlik durumunu doğru anlaması.

Saldırganlar: oltalamacı, kötü niyetli site/reklam ağı, eklenti ve yerel yardımcı; ağ/DNS saldırganı; ele geçirilmiş meşru kurum; bağımlılık, derleyici, bakımcı, imzalayıcı veya dağıtıcı. Başka OS hesabı ile yönetici/kernel yetkisi ayrılır. Yuva ele geçirilmiş kernel/yönetici, fiziksel RAM okuma, baskı, küresel trafik korelasyonu veya kullanıcının kendini siteye tanıtmasına karşı mutlak koruma vaat etmez.

Sınırlar: renderer ↔ browser; browser ↔ network/utility/storage; site ↔ partition; sayfa ↔ eklenti/native host; süreç ↔ OS; bileşen verisi ↔ doğrulayıcı; build ↔ signer; dağıtıcı ↔ updater. İmzalı girdi de sınırlı parser girdisidir. Registry üyeliği siteyi ayrıcalıklı bir güven alanına taşımaz.

## Tehdit, kontrol ve kanıt

| Tehdit | Tasarlanan kontrol | Kanıt ve kalan risk |
| --- | --- | --- |
| Banka taklidi / sahte giriş | BDDK kaynaklı envanter, tam origin kaydı, çok sinyalli yerel kesinti, sade Türkçe güvenli eylem | Kapsam mutabakatı, MFA/yönlendirme/IDN korpusu; bilinmeyen saldırı ve ele geçirilmiş banka kalır |
| Kamu kurumu / e-Devlet taklidi | Yetkili dizin ve iki inceleme, TLS + güncel kayıt rozeti, benzerlik analizi | Belediye/üniversite/UYAP alt alan kapsamı; `gov.tr` tek başına güven değildir |
| Oturum/kimlik hırsızlığı | Site isolation, izin sınırı, OTR varsayılanı, parola/WebAuthn origin denetimi | XSS, çalınmış gerçek oturum ve kullanıcının sahte forma yazması tamamen önlenemez |
| Zararlı dosya | Çalışan genel tehdit/indirme koruması, OS quarantine, sandbox içinde PDFium | Sentetik zararlı testleri; tanınmayan dosya geçebilir, otomatik çalıştırma yok |
| Siteler arası takip | Üçüncü taraf çerez engeli, partitioning, yerel takip filtreleri, dar parametre temizliği | Frame/worker/SSO testleri; IP, hesap ve birinci taraf takibi kalır |
| Parmak izi | Ölçülmüş düşük entropi kontrolleri; canvas/WebGL/audio/font için aşamalı araştırma | Korelasyon ve bozulma ölçümü; özgün Yuva davranışı yeni parmak izi olabilir |
| Bilinen yetişkin site / politika bypass | Ayrı imzalı yerel içerik indeksi, gezinme/ağ/cache kapıları | Worker/BFCache/eklenti/DoH testleri; yeni domain/proxy/karma siteler ve değiştirilmiş kaynak kapsam sınırı |
| Genel kötü amaçlı sayfa / motor açığı | Chromium yaması, sandbox, süreç/site isolation, istismar azaltımı | Her OS'de gerçek sandbox ve güncelleme tatbikatı; sıfır gün riski sürer |
| Kötü eklenti | Açık izin, host erişim sınırı, imzalı güncelleme, banka bağlamı incelemesi | MV3 worker/content script/debugger/split-spanning; izinli eklenti veri çıkarabilir |
| Yerel imza yardımcısı | Açık kurulum/başlatma, origin doğrulama, sınırlı köprü | Loopback CSRF/rebinding/protokol testleri; harici yazılım güvenliği Yuva kontrolünde değil |
| Güncelleme altyapısı/GitHub ele geçirilmesi | Sabit kök, bağımsız eşik yetkisi, TUF, OS imzası, artan sürüm | Tamper/replay/rotation/TOCTOU; saldırgan erişimi kesebilir |
| Registry imzacısı/kanıt kaynağı ele geçirilmesi | Ayrı roller, iki insan incelemesi, tam host, süre ve iptal | Kötü imzalı kayıt testi; hedef/root eşik ele geçirilirse sahte kayıt yetkilendirilebilir |
| İçerik/filtre kaynağı zehirleme | Köken/lisans, fark bütçesi, yanlış pozitif korpusu, sınırlı veri, ayrı imzalar | Sağlık/kamu/banka yanlış engeli; yetkili kötü liste kullanılabilirliği bozabilir |
| MITM / sertifika | Normal Chromium doğrulayıcı, CT/iptal/kök güncellemeleri, HTTPS-first | Hatalı zincir/ad/tarih; yerel güvenilir araya girme ve CA hatası kalır |
| DNS saldırısı | TLS doğrulama, incelenmiş DoH ve açık strict mod | Captive portal/proxy/IPv6/downgrade; resolver sorguları görebilir |
| Tedarik zinciri | Tam kimlik/hash kilidi, köken/lisans, SBOM, asgari bağımlılık | Değişen girdiyi reddetme; upstream veya kaynak sahibi ele geçirilebilir |
| Build ortamı ele geçirilmesi | Geçici VM, ayrı signer, provenance, bağımsız yeniden derleme | Kötü builder da attest edebilir; bağımsız sonuç kıyası gerekir |
| Çökme / depolama kalıntısı | Denetlenmiş geçici context, servis kapanışı, silme günlüğü, güvenli tekrar deneme | Disk/swap/OS dump adli iz garantisi yok; SSD silme güvenliği iddiası yok |
| Sahte güvenlik arayüzü | Tarayıcı chrome'unda metin+ikon, fullscreen origin affordance, TLS hatasına öncelik | Sayfa ekran resmi çizebilir; rozet kuruma kefalet değildir |
| İsteğe bağlı Vakitler üzerinden konum/inanç çıkarımı | Varsayılan kapalı, elle şehir, yerel hesap, profil/telemetri yok | Kullanıcının açık uzak sağlayıcı seçimi şehir/IP'yi o sağlayıcıya gösterebilir |

## Varsayılanlar ve değişmezler

TLS hatası, karışık içerik, sandbox ve origin isolation uyum adına atlanmaz. Trusted Sites genel tehdit kararını veya içerik sınıflandırmasını otomatik iptal etmez. Kalkan istisnası güvenlik/registry/içerik engelini kapatmaz. “Bu siteyi hatırla” izin, üçüncü taraf erişimi veya başka sitelerin verilerine yetki vermez.

Engellenen içerik denemesi kalıcı günlüğe veya Yuva sunucusuna yazılmaz. Yanlış pozitif bildiriminde domain paylaşımı açık ve ayrı onay ister. Liste güncellemesi sabit tüm paket üzerinden olur; ziyaret edilen domain için sorgu yapılamaz. İlk sürümlerde çökme yüklemesi ve Yuva telemetrisi yoktur.

## Arıza tablosu

| Arıza | Davranış |
| --- | --- |
| TLS hatası | Chromium güvenlik ekranı; pozitif kurum rozeti yok |
| Trusted Sites verisi eski/bozuk | Uygun eski veri varsa kullan; süre bitince rozet ve yeni sezgisel kesinti yok, güncellik kaybı görünür |
| İçerik listesi eski | Son doğrulanmış negatif listeyle bilinen engeller sürer; güncel olduğu iddia edilmez |
| Hiç doğrulanmış içerik verisi yok / yerel indeks bozuk | Dış gezinme onarım ekranında durur; imzalı onarım/güncelleme erişimi ayrı dar kapıda |
| Genel tehdit hizmeti kesintisi | Son uygun yerel veri, belirgin bozulmuş koruma durumu; yeni yayın kapısı başarısız; TLS gevşetilmez |
| Kalkan kural derleyicisi hatası | Aday reddedilir; son sağlam kurallar; etkinmiş gibi sahte sayaç yok |
| Güncelleme imza/rollback hatası | Kurulum reddedilir; mevcut doğrulanmış kurulum ve güncellik uyarısı |
| Geçici veri temizleme hatası | “Silindi” denmez; eski context yeniden bağlanmaz, güvenli onarım/tekrar deneme |
| Pardus kapısı başarısız | Masaüstüne hazır terfi yok; kapsam sessiz küçültülmez |

## Kanıtlama ve artık risk kabulü

Birim testleri yanında fuzzing, gerçek platform sandbox, çok origin/worker/depolama, TLS, yönlendirme, eklenti, çevrimdışı imza ve saldırgan CI testleri gerekir. Canlı kullanıcı/banka verisi kullanmadan sentetik korpus; kurum izinli kabul testi ayrı süreçtir. Bütün zorunlu platformlarda aynı kaynak/yama kümesi sınanır.

Her değişiklik tehdit→kontrol→test→sahip bağlantısını [güvenlik özellik kaydına](docs/SECURITY_FEATURE_REGISTER.md) ekler. Kritik artık risk iki sorumlu ve gerekçeli karar gerektirir; ürünün güvenlik değişmezine istisna verilemez. Anahtar/tedarik zinciri olayı [SECURITY.md](SECURITY.md) sürecine gider. Tasarım incelemesi uygulama veya bağımsız güvenlik denetimi yerine geçmez.
