# Chromium temeli ve uygulanabilirlik analizi

Araştırma: 17–18 Eylül 2026. Durum: Faz 0 önerisi. Chromium indirilmedi/derlenmedi; çatalların geçmiş yayın gecikmeleri karşılaştırmalı olarak ölçülmedi. Aşağıdaki değerlendirmeler kaynak incelemesine dayalı mühendislik yargılarıdır.

## Öneri

**Doğrudan, güvenlik yamaları güncel Chromium Stable kaynak kodu** kullanılsın. Tam commit sabitlensin; Yuva bileşenleri ve küçük, sıralı yama kümesi ayrı tutulsun. Mahremiyet çatallarından yalnız tek tek incelenmiş çalışmalar alınsın. Bağımsız evrilen Blink/V8 çatalı küçük ekip için sürdürülebilir değildir.

CEF, Electron veya sistem WebView kullanmak; tarayıcı arayüzü, izinler, güvenlik akışları ve eklenti bütünleşmesini yeniden kurmayı gerektirir. Tam Chromium tarayıcı uygulamasını korumak daha uygundur.

## İncelenen ortam

| Bulgular | Sonuç |
| --- | --- |
| Git kökü `yuva-browser`; başlangıçta yalnız tek satır README ve temiz çalışma ağacı | Korunacak mevcut uygulama/bağımlılık yok |
| macOS 26.5.2, ARM64, sekiz mantıksal CPU, 8 GiB RAM | Tasarım/bileşen çalışması yapılabilir; tam derleme sınırlı |
| Başlangıçta yaklaşık 22 GiB, kullanıcı temizliği sonrasında yaklaşık 55 GiB boş alan | Chromium çalışma alanı için hâlâ yetersiz planlama kapasitesi |
| Command Line Tools seçili; tam Xcode seçili konumda yok | macOS önkoşulu eksik |
| Git, Python 3, Node, clang, codesign, gh ve Docker komutları mevcut | Sürümler, imzalama kimlikleri ve uzak derleme kapasitesi nitelendirilmedi |
| `gn`, `ninja`, `autoninja`, `gclient` PATH içinde yok | Chromium araçları yapılandırılmadı |

Proje kapsamlı bellek araması sonuç vermedi; kod grafiği araçları mevcut değildi. Kaynak envanteri doğrudan incelendi. Yuva için sır/anahtar, imzalama hesabı veya özel altyapı incelenmedi.

Chromium'un Linux/Windows belgeleri en az 100 GB disk ve 8 GB asgari RAM'den fazlasını önerir; macOS uygun tam Xcode/SDK ister. Gerçek önkoşullar seçilen revizyondan yeniden okunmalıdır. [Derleme girişi](https://www.chromium.org/developers/how-tos/get-the-code/), [Linux](https://github.com/chromium/chromium/blob/main/docs/linux/build_instructions.md), [Windows](https://github.com/chromium/chromium/blob/main/docs/windows_build_instructions.md), [macOS](https://chromium.googlesource.com/chromium/src/+/main/docs/mac_build_instructions.md).

Ölçülmemiş kapasite tahmini: ayrı 16–32 çekirdekli, 64 GiB RAM ve 500 GB–1 TB SSD derleme makineleri; yerel Windows/macOS ve açık Pardus derleme/test ortamları. Soğuk/artımlı derleme ile test süreleri ölçülmeden uzun vadeli kapasite satın alınmamalıdır. Ücretsiz CI koşucuları güvenilir yayın kapasitesi planı değildir.

## Temellerin karşılaştırılması

| Temel | Güvenlik hızı / bakım yükü | Mahremiyet / Google bağımlılığı | Uyumluluk ve platformlar | Karar |
| --- | --- | --- | --- | --- |
| Chromium | Düzeltmelere doğrudan erişim; derleme/test/dağıtım Yuva'ya ait | Hizmet envanteri ve varsayılan değişiklikleri gerekir; güçlü mevcut güvenlik/depolama altyapısı | Web/eklenti uyumluluğunun temel kaynağı; Windows/macOS/Linux | **Seçilen temel önerisi** |
| ungoogled-chromium | Toptan takip edilirse ek çatal ve platform yayın adımı | Safe Browsing dahil geniş kaldırmalar; genel alan adı ikameleri risk taşır | Chromium'a yakın arayüz; ayrı platform depoları; mağaza akışları farklı | Tek tek yama kaynağı |
| Brave / brave-core | Geniş ürün katmanını devralıp ayıklamak ciddi bakım yükü | Olgun mahremiyet araştırması; Yuva kapsamı dışında ürün hizmetleri | Masaüstü/mobil deneyim; ayrılan bileşenler yeniden bütünleştirilir | Bağımsız bileşenleri değerlendir |
| Cromite | Ek yama/yayın bağımlılığı; macOS çalışması gerekir | Yararlı sertleştirme araştırması; davranış/lisans tek tek incelenmeli | İncelenen README Android/Windows/Linux belirtir, macOS belirtmez | Araştırma kaynağı |
| Derin bağımsız Chromium çatalı | Çakışma ve doğrulama maliyeti birikir | Tam kontrol, aynı ölçüde sorumluluk | Her motor/platform farkı Yuva'ya kalır | Reddediliyor |

Hiçbir çatal için doğrulanmış Yuva güvenlik SLA'sı varsayılmıyor. ungoogled-chromium Safe Browsing kaldırmasını, platform depolarını ve topluluk ikililerinin doğrulanabilirlik sınırlarını açıklar; tüm yapılandırmasını devralmamak için somut gerekçelerdir. [Proje belgesi](https://github.com/ungoogled-software/ungoogled-chromium).

Brave'in ayrı Rust engelleme motoru, tüm ürünü devralmadan incelenebilir. [brave-core](https://github.com/brave/brave-core), [adblock-rust](https://github.com/brave/adblock-rust). Cromite platformlarını ve yama lisanslarını ayrıca belirtir. [Cromite README](https://raw.githubusercontent.com/uazo/cromite/master/README.md).

| Ölçüt | Değerlendirme |
| --- | --- |
| Güvenlik güncellemesi | Doğrudan Chromium, aradaki çatalın yayınını bekleme zorunluluğunu kaldırır; Yuva'nın hızı yine operasyon kapasitesine bağlıdır |
| Yeniden üretilebilirlik | Upstream deterministik derleme çalışması başlangıçtır; Yuva kurucuları, imzalama ve her ithal bileşen bağımsız kanıt ister |
| Otomatik güncelleme | Hiçbir kaynak seçimi işletilen Yuva güncelleyicisi sağlamaz; çatalın sunucu/anahtarları devralınamaz |
| Google bağımlılığı | Gereksiz hizmetler dar değişikliklerle kaldırılır; güvenlik verisi yenilemesi önce korunur veya eşdeğeri sağlanır |
| Sertleştirme | Mevcut mekanizma/varsayılan öncelikli; derin Blink parmak izi yamaları yüksek taşıma maliyetlidir |
| Sürdürülebilirlik | Küçük yama kümesi, sahiplik ve az yayın dalı; bütün masaüstü hedefleri için sürekli yeterlilik |

Chromium'un deterministik derleme hedefi Yuva'nın imzalı paketlerinin aynı baytlarla üretildiği anlamına gelmez. [Deterministik derleme belgesi](https://chromium.googlesource.com/chromium/src.git/+/HEAD/docs/deterministic_builds.md).

## Derleme ve güncelleme bakımının temel bazında karşılığı

| Temel | Tekrar derleme / platform işi | Yuva güncelleyicisine etkisi | Uzun vadeli yük |
| --- | --- | --- | --- |
| Chromium | Upstream kilit/toolchain üzerinden üç masaüstü OS; Pardus özel paket/testini Yuva ekler | Chromium Updater mekanikleri adaydır; Yuva sunucu/protokol/yetki/telemetri denetimi gerekir | Küçük yama katmanı ile en kısa güvenlik yolu; imza/CI maliyeti yine Yuva'da |
| ungoogled-chromium | Platform depoları/paketleme farklı; yayımlanan her ikilinin kaynakla tekrar üretildiği varsayılmaz | Çatalın dağıtımı Yuva için güvenli otomatik updater sağlamaz | Platform yamaları ve kaldırılan güvenlik servislerini yeniden değerlendirme yükü |
| Brave | Kendi bağımlılık/yama/ürün derleme grafiği; bileşeni ayırmak tüm tarayıcıyı yeniden üretmekten farklı | Brave anahtar/sunucu/hizmetleri devralınamaz; updater protokol/veri akışı yine ayrılmalı | Bileşen almak uygulanabilir; tam ürün budamak geniş sürekli çakışma alanı |
| Cromite | İlan edilen Windows/Linux/Android hatları; macOS ve açık Pardus yeterliliği ek iş | Mevcut çatal dağıtımı Yuva kimliği/kökü altında yeniden tasarlanır | GPL yama analizi ve ek upstream yayın aşaması; birincil temel seçilmiyor |
| Derin kendi çatalımız | Bütün motor/araç/platform farklarının tekrar üretimini ekip taşır | Güncelleme altyapısı ve güvenlik semantiğinin tamamı ekipte | Küçük takım için kabul edilmeyen sürdürülebilirlik riski |

Bunlar incelenen proje yapılarından mühendislik çıkarımlarıdır; ölçülmüş karşılaştırmalı performans veya yayın gecikmesi tablosu değildir. Uygulama öncesi son üç Chromium güvenlik yayını için her adayın kaynak/paket tarihini aynı yöntemle ölçmek yararlıdır, fakat başka çatalın hızını Yuva SLA'sı saymak doğru değildir.

## Bağımlılık incelemesinden sonra lisans seçimi

Özgün Yuva kodu ve belgeleri için **BSD-3-Clause** öneriliyor ve kök LICENSE buna göre hazırlanıyor. Gerekçe upstream katkı kolaylığı ve küçük, izin verici katman yaklaşımıdır. Bu seçim Chromium'u, kopyalanan yamayı veya filtre verisini yeniden lisanslamaz. MPL dosya düzeyinde karşılıklılık alternatifi; geniş copyleft ise bilinçli dağıtım kararıdır.

| İncelenen materyal | Lisans bulgusu | Alma/dağıtma koşulu |
| --- | --- | --- |
| Chromium kök lisansı | Üç koşullu BSD türü | Bildirimler korunur; üçüncü taraflar ayrıca çıkarılır |
| ungoogled-chromium | Kök BSD-3-Clause | Ödünç alınan yamanın kökeni/başlığı da incelenir |
| brave-core / adblock-rust | MPL-2.0 | Kapsanan dosya/değişiklik lisansı ve kaynak sağlama yükümlülüğü korunur |
| Cromite/Bromite | Depo GPLv3; README Bromite için GPLv3-only, Cromite özgün yamaları için GPL-2+ belirtir | Her yama ve birleşik eser değerlendirilir; yalnız BSD etiketine dönüştürülmez |
| Filtre listeleri | Ayrı lisanslı veri; EasyList GPLv3-or-later veya CC BY-SA 3.0 sunar | Seçilen koşullar, atıf ve türev yükümlülükleri kaydedilir |

Kaynaklar: [Chromium](https://chromium.googlesource.com/chromium/src/+/main/LICENSE), [ungoogled](https://raw.githubusercontent.com/ungoogled-software/ungoogled-chromium/master/LICENSE), [Brave](https://raw.githubusercontent.com/brave/brave-core/master/LICENSE), [adblock-rust](https://raw.githubusercontent.com/brave/adblock-rust/master/LICENSE), [Cromite](https://raw.githubusercontent.com/uazo/cromite/master/LICENSE), [MPL açıklaması](https://www.mozilla.org/en-US/MPL/2.0/FAQ/), [EasyList lisansı](https://easylist.to/pages/licence.html), [BSD metni](https://opensource.org/license/bsd-3-clause).

Şu anda dış uygulama/liste içe alınmadı. İkili dağıtım, gerçek kilitli bağımlılık grafiğinin bildirimlerini ve kaynak sağlama yükümlülüklerini gerektirir. Chromium; Chrome markasını, başka tarayıcının API anahtarını, Widevine dağıtımını veya medya patent haklarını otomatik vermez. [API anahtarları](https://www.chromium.org/developers/how-tos/api-keys/).

## Ekip ve yayın kararı

Planlama varsayımı: Chromium/güvenlik, platform/yayın ve mahremiyet/depolama alanlarını kapsayan en az üç deneyimli çekirdek mühendis; iki eğitimli yayın sorumlusu ve bağımsız güvenlik incelemesi. Bu, üç kişinin büyük tarayıcı ekiplerinin tüm kabiliyetini sağlayabileceği iddiası değildir. Yedeksiz tek bakımcı çok platformlu güvenli kararlı sürüm sözü veremez.

Derleme, imzalama, dağıtım, test cihazı ve olay müdahalesi bütçelenir. Hesap maliyeti ölçülen derleme saati × aylık sıklık × platform fiyatıyla çıkarılır. Kapsam büyütmeden üç zamanında upstream güncelleme tatbikatı gerekir.

Pardus birinci sınıf hedeftir; mevcut destek kolları ve ayrı `.deb`/CI koşulları [Pardus planında](docs/PARDUS_SUPPORT.md) tanımlanır. Windows, macOS, genel Linux ve Pardus kapıları birlikte geçmeden “masaüstüne hazır” denemez.

0.1 sınırlı önizleme olarak mümkündür. Kapasite eksikse eski ikililer dağıtmak yerine kaynak/tasarım projesi olarak kalınır. Parmak izi ve seçici kalıcılık çalışmaları Chromium güvenlik düzeltmesini bekletemez. Gereksiz özel Microsoft/Apple/Google hizmet bağımlılığı eklenmez; zorunlu OS güvenlik entegrasyonları gerekçelendirilir.

Sonraki zorunlu gereksinimler fizibilite kapsamını büyüttü: kapsamlı banka/kamu envanteri, yüksek güvenli oltalama kesintisi ve resmî içerik engeli için sürekli veri inceleme/yanlış pozitif/anahtar işletimi gerekir. Üç mühendis varsayımı bu işlerin tamamının personel tahmini değildir; ayrı veri/güvenlik operasyonu kapasitesi ölçülmelidir. [İçerik lisans incelemesi](CONTENT_PROTECTION.md) UT1 CC BY-SA 4.0 ve Blocklist Project Unlicense adaylarını ayrıca ele alır; henüz veri ithal edilmedi. İleri isteğe bağlı Vakitler güvenlik kaynaklarını tüketerek yayını geciktiremez.
