# Yuva İçerik Koruması

Durum: 18 Eylül 2026, uygulanmamış tasarım. `Yuva Content Protection`, resmî Yuva dağıtımlarında bilinen yetişkin/pornografik siteleri engelleyen zorunlu yerel politika bileşenidir. Oltalama kararı, kuruluş doğrulaması ve takip engellemeden ayrı veri/yetki kullanır.

## Ürün ve gizlilik sınırı

Resmî ikililerde politika varsayılan olarak etkindir ve olağan Kalkan istisnası, “Bu siteyi hatırla”, tema veya eklenti tarafından kapatılamaz. Bu, çocuk güvenliği için eksiksiz ebeveyn denetimi veya bütün internet içeriğinin sınıflandırıldığı iddiası değildir. Alan adı listesi karma içerikli meşru hizmetlerde sayfa bazındaki her içeriği saptayamaz. Genel VPN/OS erişimini denetleyen bir sistem tasarlanmamaktadır.

Yuva açık kaynak olduğundan kaynak değiştirilebilir, farklı ikili derlenebilir veya ürün sınırlaması kaldırılabilir. “Atlatılamaz” iddiası yoktur; politika resmî dağıtımlara aittir. Veri lisansı kullanıcıların listeyi inceleme, değiştirme ve lisansına göre yeniden dağıtma haklarını engellemez.

Ziyaret/deneme URL'leri Yuva sunucusuna gönderilmez. Otomatik URL sınıflandırma servisi, gezinme profili ve ziyaret günlüğü yoktur. Engellenen gezinme geçmişe, oturum geri yüklemeye, önerilere veya kalıcı güvenlik sayacına eklenmez; interstitial'ın RAM'deki mevcut hedef bilgisi kapanınca bırakılır. Crash dump/diagnostics varsayılan kapalıdır; ileride eklense de hedef verileri dışarı çıkarılamaz. OS/ağ yöneticisinin bağımsız kayıtları üzerinde mutlak kontrol iddiası yoktur.

## Kaynak değerlendirmesi

18 Eylül 2026 incelemesinde uygun adaylar:

| Kaynak | Lisans / nitelik | Karar |
| --- | --- | --- |
| Université Toulouse Capitole UT1 kategorileri | [Kaynak](https://dsi.ut-capitole.fr/blacklists/index_en.php), yayımlanan [CC BY-SA 4.0 lisansı](https://dsi.ut-capitole.fr/blacklists/download/LICENSE.pdf) | İlk değerlendirme için `adult` kategorisi. Atıf, değişiklik bildirimi ve uyarlanmış veri paylaşım şartları korunur. Cinsel sağlık/eğitim ve karma kategoriler otomatik eklenmez. |
| Blocklist Project | [Depo](https://github.com/blocklistproject/Lists), [Unlicense](https://raw.githubusercontent.com/blocklistproject/Lists/master/LICENSE) | İkincil karşılaştırma adayı. Repo lisansı her alt kaynağın kökenini tek başına kanıtlamaz; kaynak zinciri, güncellik ve Türkçe yanlış pozitif incelemesi şarttır. |
| Ticari sınıflandırma kaynakları | Yeniden dağıtım ve çevrimdışı kullanım hakkı ayrıca gerekir | Belirsiz veya kapalı yeniden dağıtım lisansıyla resmî açık paket üretilemez. |

Liste dosyaları bu çalışma sırasında alınmadı; kaynaklar üretim için onaylanmış sayılmaz. Kaynak release tarihi sınıflandırma değişim tarihiyle aynı değildir. Lisans anlık görüntüsü, kategori kökeni, veri hakları ve bildirim metni her kaynak sürümüne bağlanır. Türetilmiş liste ayrı veri eseri olarak lisanslanır; Yuva'nın BSD-3-Clause kod lisansı verinin lisansını değiştirmez. Nihai yeniden dağıtım incelemesi yayın kapısıdır.

## İçe alma ve imzalı yayın

```text
kaynak anlık görüntüleri
  → lisans/köken doğrulaması
  → sınırlı ayrıştırma ve normalizasyon
  → tekrarları kaldırma / domain doğrulama
  → kategori ve yanlış pozitif incelemesi
  → deterministik yerel indeks
  → bağımsız inceleme / eşik imzası
  → doğrulanmış bileşen güncellemesi
  → tarayıcıda yerel eşleşme
```

İndirme işçisi ayrı, sır içermeyen ortamda çalışır. Arşiv path traversal, symlink, decompression bomb ve boyut sınırı test edilir. Dış kaynağın HTTPS üzerinden gelmesi Yuva güven onayı değildir. İçe alınan ham veri hash'i ve elde edilme tarihi saklanır; URL içeren kaynakta yol/sorgu alanları tarayıcı paketine taşınmaz. URL'nin host'a indirgenmesi kapsamı büyütecekse otomatik dönüşüm reddedilir.

Chromium'la uyumlu IDNA ASCII host normalizasyonu yapılır; IP/localhost/özel ağ/tek etiket/public suffix ve hatalı domain reddedilir. Domain exact veya açık `include_subdomains` kapsamı taşır. Etiket sınırı olmadan suffix eşleşmesi yoktur. Paylaşımlı barındırma, CDN, dinamik müşteri alt alanları ve genel bulut kökleri topluca engellenmez. Milyonlarca kaydı elle yönetmek yerine kaynak farkları, dağılım değişimleri ve örneklenmiş kalite denetimi kullanılır.

Her yayın: `schema_version`, `dataset_id`, `sequence`, `issued_at`, `review_due_at`, `minimum_reader_version`, `source_snapshots`, `license_notices`, `entry_count`, `index_hash`, `index_length`, `normalization_version`, `correction_revision` taşır. Çalışma zamanı indeksinde host/kapsam ve kaynak/reason kimlikleri bulunur; ziyaret bilgisi bulunmaz. Üretilen indeksin bayt düzeni sürümlenir, platformdan bağımsızdır. İmzalar sıkıştırılmamış içeriğin de hash ve sınırını bağlar.

Kaynak farkında banka/kamu/eğitim/sağlık alanına yeni blok, çok geniş suffix, anormal artış/azalış veya kategori taşması yayın işlemini durdurur. İki inceleyen gerekçeli karar verir. Trusted Sites ile çelişki otomatik olarak “her zaman izin ver” sonucuna dönüşmez: meşru kurum da ele geçirilmiş olabilir. İçerik sınıflandırma düzeltmesi genel kötü amaçlı site engelini asla kaldırmaz.

## Veri yapısı kararı

| Seçenek | Değerlendirme |
| --- | --- |
| Sıralı, sıkıştırılmış tam domain kümesi | Basit deterministik başlangıç; binary search ve etiket başına sorgu; referans uygulama |
| Ters etiketli radix/trie | Alt alan kapsamı ve ortak son eklerde alan tasarrufu; mmap indeks için tercih edilen ölçüm adayı |
| Tam hash tablosu | Hızlı; bellek ve çakışma/temsil incelemesi gerekir; hash eşitliği tek başına domain doğrulaması yerine kullanılmaz |
| Bloom filter | Yalnız hızlı negatif ön filtre; pozitif sonuç kesin küme/etiket eşleştirmesiyle doğrulanmadan site engellenmez |

Öneri: doğruluk için basit tam küme referansı, üretim için karşılaştırmalı ölçüm sonucu kompakt ters etiket indeksi. Ham milyonluk JSON tarayıcı açılışında parse edilmez. İmzalı indeks dosyası salt okunur map edilir; kaynağın ömrü immutable snapshot ile yönetilir. İş parçacığına bağlı mutable global sayaç yoktur. Hedef bütçeler ölçülecek: sıcak sorgu p95 <1 ms, referans 4–8 GiB Pardus cihazda artan çalışma kümesi <64 MiB, açılışta <100 ms ek maliyet. Bunlar ölçülmüş performans değildir; gerçek veriyle kapı kesinleştirilir.

## Yerel uygulama ve kapsam

Tarayıcı süreci gezinme kapısı ve Network Service isteği politikası birlikte çalışır. Üst gezinme ilk istekten önce, her yönlendirme, iframe, popup, prefetch/prerender, worker/subresource, WebSocket ve eklenti kaynaklı ağ erişimi uygun upstream kancalarda değerlendirilir. Tam URL sınıflandırmaya gönderilmez; yerel canonical host ve kaynak türü yeterlidir. Engelli hedefe preconnect/DNS speculation yapılmaması da test kapsamındadır.

Servis worker/offline cache, BFCache/prerender aktivasyonu, geri/ileri, session restore ve zaten açık sekme yeni policy snapshot altında tekrar değerlendirilir. Ağ isteği yapmayan cache yanıtı bir bypass olamaz. Yeni engellenen etkin origin için belge işleyişi durdurulur, engel sayfası gösterilir; depolama silme ayrı güvenli yaşam döngüsüyle yapılır. Güncelleme boyunca eski doğrulanmış indeks atomik geçişe kadar yürürlükte kalır.

DNS-only engel yeterli değildir; DoH, proxy, farklı DNS veya sistem hosts değişimiyle browser host kontrolü kaybolmaz. Bununla birlikte yeni alan adı, reverse proxy veya karma platformdaki içerik liste dışında kalabilir. IP literal ve `data:` gibi yollar için genel güvenlik politikası korunur; bunları sınırsız içerik tanıma olarak sunmayız. Kancaların gerçek kapsamı kod denetimi ve entegrasyon testleriyle kanıtlanmadan “tam” koruma iddiası yapılmaz.

## Güven kökü, güncellik ve çevrimdışı durum

[Trusted Sites protokolündeki](TRUSTED_SITES_DESIGN.md) TUF doğrulama, atomik durum, artan sürüm, kök rotasyonu ve parser sınırları yeniden kullanılır; içerik için ayrı kök ve targets eşik anahtarları gerekir. İmzalı veri komut/script içeremez. Tarayıcı ikilisi başlangıç için doğrulanmış içerik paketi taşır. Her kullanıcı aynı paket/delta programını kullanır; domaine göre parça istemek gezinmeyi ifşa edeceğinden yoktur. Delta ancak eski/yeni tam hash'leri doğrulanıp atomik geçiş yapıldığında kullanılabilir.

- Yeni paket imzasız/bozuk/eskiyse reddedilir; son doğrulanmış indeksle bilinen engeller sürer.
- Meta veri veya veri inceleme süresi dolarsa yeni yükleme kabulünde süre kontrolü gevşetilmez. Daha önce doğrulanmış yerel **negatif engel** verisi çalışmaya devam eder; “Koruma listesi güncel değil” gösterilir. Bu veri güncel diye sunulmaz ve pozitif kimlik rozeti üretmez.
- Hiçbir doğrulanmış veri yoksa veya indeks bütünlüğü bozulmuşsa dış web gezinmesi güvenli onarım ekranında durdurulur. Ayarlar, güncelleme ve doğrulanmış çevrimdışı paket içe alma çalışabilir; onarım ağı yalnız tarayıcıya ait dar bileşen istemcisinden sabit meta veri uçlarına erişir, sayfa/eklentiye genel bypass veya proxy API'si vermez; kullanıcıya koruma çalışıyormuş gibi gezinme açılmaz. Başlangıç paketi eski duruma sessiz rollback yapamaz.
- Düzeltilmiş bir yanlış pozitif yeni ve daha yüksek sürümlü imzalı düzeltmeyle kaldırılır; eski listeyi seçme arayüzü yoktur. Uzun çevrimdışı kalma düzeltmeyi geciktirebilir, bu sınır açıkça belirtilir.

## Engel sayfası, raporlama ve düzeltme

Birincil metin: **“Bu içerik Yuva tarafından engellendi.”** Güvenli eylem: “Geri dön”. Reklam, ahlaki değerlendirme, korkutucu yetişkin görseli veya takip bağlantısı yoktur. Ayrıntı açıldığında “Yetişkin içerik listesi”, kaynak kimliği, liste sürümü, son güncelleme ve “Yanlış sınıflandırma bildir” görünür. Bu, “zararlı yazılım” veya “sahte banka” kararıyla karıştırılmaz.

Bildirim kendiliğinden gitmez. Yerel önizleme, dahil edilecek **yalnız domain**, liste/sınıflandırma sürümü ve kullanıcının yazdığı açıklamayı gösterir. Domain ekleme açık onay gerektirir; yol, sorgu, geçmiş, referrer ve hesap bilgisi eklenmez. Onaysız form boş kalır. Kullanıcı adına otomatik GitHub issue açılmaz; domainin herkese açık issue'da görünme sonucu gönderim öncesi açıklanır. Özel bildirim kanalı kurulmadan özel olduğu iddia edilmez.

İnceleme ekibi kaynağa ve Yuva düzeltme deposuna ayrı gerekçeli kayıt açar; sağlık, eğitim ve bankacılık yanlış pozitifleri öncelikli ele alınır. Sınırlı exact-host düzeltmesi, kaynak ve kategoriyle bağlanır, süresi/iki incelemesi bulunur. Kullanıcının yerel geçiş düğmesi yerine hızlı imzalı düzeltme yolu sağlanır. Hedef: kritik yanlış pozitif triyajı 24 saat; hizmet henüz işletilmiyor.

## Test ve yayın koşulları

Kaynak lisansı/köken, normalizasyon, domain sınırları, private suffix, duplicate, kategori kaçağı, arşiv saldırısı, indeks eşdeğerliği ve fuzz testleri; milyonluk veri bellek/gecikme ölçümü; bilerek çakıştırılan Bloom sonuçlarının engel yaratmaması gerekir. İmza/rollback/expiry/rotation/offline/çökme testleri diğer bileşenlerle ortaktır.

Sağlık, cinsel eğitim, haber, bankacılık, kamu ve üniversite meşru korpusunda yanlış engeller incelenir; kaynak başına precision ve yanlış pozitif oranı yayımlanır. Ağ kayıtlarıyla Yuva'ya sınıflandırma URL'si çıkmadığı, engel geçmişi/logu oluşmadığı ve raporun onaysız gönderilmediği kanıtlanır. Tüm gezinme/cache/worker/eklenti bypass testleri Windows, macOS, Linux ve Pardus kapılarıdır. Zorunlu koruma tamamlanmadan resmî Developer Preview dahil ikili yayımlanmaz.
