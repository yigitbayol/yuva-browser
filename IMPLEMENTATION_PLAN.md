# Sıralı uygulama planı

Durum: Faz 1 geliştirme hazırlığı, 18 Eylül 2026. **İnce depo kararı kabul edildi; ilk hazırlık araçları uygulandı. Çalışan tarayıcı henüz yok.** Her görev küçük PR veya sınırları belirtilmiş deneydir; büyük görev ölçüm/veri kapsamına göre aynı güvenlik kapısını koruyan alt PRlara ayrılır. Henüz oluşturulmamış dosya yolları öneridir. Kimlikler İngilizce; açıklamalar Türkçe.

01–41 resmî 0.1 yolunu; 42–46 Alpha/Beta işlerini; 47 bağımsız isteğe bağlı yardımcıyı; 48 Stable kapısını tanımlar. İleri özellik eksikliği temel zorunlu güvenliği erteleyemez. Aşağıdaki tablo dışında görevlerin tamamlandığı varsayılmaz.

## Gerçekleşen kapsam

| Görev | Durum ve kalan iş |
| --- | --- |
| 01 | İnce depo ve önkoşul ADR'leri kabul edildi. Ürün bileşenlerinin ayrı güvenlik/deney kararları bekliyor. |
| 02 | Yerel macOS ARM64 envanteri ve `doctor` hazır. Disk bütçesi ve tam Xcode engelleri var; diğer platformlarda derleme kapasitesi henüz nitelendirilmedi. |
| 03 | `config/versions.json` içinde Chromium sürüm/commit, DEPS SHA-256 ve depot_tools commit'i sabitlendi; uzak kaynak kimliği denetlendi. Tam DEPS/CIPD/SDK kilidi bekliyor. |
| 04 | `bootstrap --plan` ve önkoşul kapısı hazır. Kaynak indirme, hook incelemesi, bağımlılık hazırlama ve GN yapılandırması uygulanmadı. |
| 05 | Sıralı, hash denetimli yama manifestosu ve geçici Git indeksinde uyumluluk denetimi test edildi. Ürün yaması yok; gerçek kaynak hazırlama ve sonuç ağaç özeti hattı bekliyor. |
| 06 | Başlanmadı; Chromium indirilmedi veya derlenmedi. |
| 36 | Yalnız geliştirici araçları için Windows/macOS/Linux CI ve upstream izleyicisi tanımlandı. Tarayıcı/Pardus testleri, yayın, imzalama ve provenans hattı bekliyor. |

Araç testleri `tests/tooling/` içindedir. Sıradaki küçük işler sırasıyla: hedef derleme makinesinin kaynak/SDK nitelendirmesi; tam bağımlılık kilidi şeması ve doğrulayıcısı; açık indirme seçeneğiyle dış çalışma alanı hazırlama; ilk saf Chromium derlemesi. İndirme/büyük derleme bu hazırlık tesliminin parçası değildir. Her ilerleme README'ye yansıtılır.

## 01 — Mimari kararları incele

- **Amaç:** Temel, güvenlik değişmezleri ve genişleyen resmî 0.1 kapsamını kabul edilmiş ADR haline getir.
- **Dosyalar/bileşenler:** docs/adr/, DECISION_SUMMARY.md, ROADMAP.md
- **Bağımlılıklar:** Yok; Faz 0 çıktısı
- **Güvenlik:** İnceleme tamamlanmadan büyük Chromium değişikliği yok.
- **Testler:** Belgeler arası kapsam, zorunlu koruma ve dil/Pardus tutarlılığı.
- **Tamamlanma ölçütü:** Karar sahipleri, açık kapılar ve kabul gerekçesi kaydedilmiş.

## 02 — Ekip ve derleme kapasitesini nitelendir

- **Amaç:** Platform makineleri, yedek sorumlular ve maliyet/süre bütçesini belirle.
- **Dosyalar/bileşenler:** docs/BUILD.md, build/toolchains/, docs/PARDUS_SUPPORT.md
- **Bağımlılıklar:** 01
- **Güvenlik:** İmzalama sırları builder üzerinde bulunamaz; iki müdahale sorumlusu gerekir.
- **Testler:** Windows/macOS/Linux/Pardus kaynak/disk/SDK envanteri, soğuk derleme kapasite deneyi.
- **Tamamlanma ölçütü:** Yeterli kapasite ve erişim politikası kanıtlı; destek kolları resmî kaynakla sabitlenmiş.

## 03 — Upstream ve araç kilidini tanımla

- **Amaç:** Güncel güvenlik yamalı Stable commit ve bütün DEPS/araç/SDK girdilerini bağla.
- **Dosyalar/bileşenler:** config/versions.json, config/upstream.lock.json, build/config/
- **Bağımlılıklar:** 01, 02
- **Güvenlik:** Hareketli latest, doğrulanmamış hook veya rastgele ikili kullanılmaz.
- **Testler:** Hash/commit uyuşmazlığı ve değişen araç girdisinin reddi.
- **Tamamlanma ölçütü:** Temiz ortamda aynı kaynak ve araç kimlikleri çözülebiliyor.

## 04 — Kaynak hazırlama aracını oluştur

- **Amaç:** Chromium çalışma alanını depodan ayrı, doğrulanmış girdilerle kur.
- **Dosyalar/bileşenler:** scripts/yuva_dev/, docs/BUILD.md
- **Bağımlılıklar:** 03
- **Güvenlik:** İndirilmiş betik körlemesine yürütülmez; yollar/symlink ve mevcut kullanıcı verisi korunur.
- **Testler:** Boş çalışma alanı, kesinti, disk dolması, tekrar çalıştırma.
- **Tamamlanma ölçütü:** Gizli depo veya Yuva hesabı olmadan belgelenmiş kurulum yeniden yapılabiliyor.

## 05 — Kesin yama uygulama hattını oluştur

- **Amaç:** Sıralı sahipli yamaları temiz kaynağa uygula ve sonuç hash üret.
- **Dosyalar/bileşenler:** scripts/yuva_dev/, patches/series.json
- **Bağımlılıklar:** 03, 04
- **Güvenlik:** Fuzzy uygulama ve kısmi başarı yasak; her ithalde lisans/köken.
- **Testler:** Yanlış taban/sıra, eksik dosya, değiştirilmiş hash ve çakışma.
- **Tamamlanma ölçütü:** Hatalar kapalı sonuçlanıyor; yamalı ağaç deterministik ve gerekçeleri Türkçe.

## 06 — Saf Chromium referansını derle

- **Amaç:** Ürün farkı olmadan bütün masaüstü ailelerinde temel sonuç al.
- **Dosyalar/bileşenler:** build/config/, tests/browser/, docs/BUILD.md
- **Bağımlılıklar:** 02, 04
- **Güvenlik:** Sandbox kapatma ile derleme/çalışma başarısı alınmaz.
- **Testler:** Açılış/render/PDF ve platform smoke; Pardus 23.x/25.x ayrı kaynak derlemesi.
- **Tamamlanma ölçütü:** Her hedefin build süresi/artefaktı ve başarısızlıkları kaydedilmiş.

## 07 — Güvenlik temel testlerini kur

- **Amaç:** Korunacak upstream güvenlik davranışını ölçülebilir hale getir.
- **Dosyalar/bileşenler:** tests/security/, docs/SECURITY_FEATURE_REGISTER.md
- **Bağımlılıklar:** 06
- **Güvenlik:** TLS, site/süreç yalıtımı ve exploit mitigation değişmezi.
- **Testler:** Sertifika adı/süre/zincir, mixed content, renderer sandbox, cross-origin olumsuz testler.
- **Tamamlanma ölçütü:** Her zorunlu platformda yeşil temel ve sürüm bilgisi var.

## 08 — Ağ ve Google hizmet envanterini çıkar

- **Amaç:** Temiz profil ağ akışlarını ve kaldırılabilir gereksiz hizmetleri ayır.
- **Dosyalar/bileşenler:** docs/adr/, components/browser/policy/, patches/privacy/
- **Bağımlılıklar:** 05, 07
- **Güvenlik:** CT/kök/iptal/threat güncellemesi eşdeğersiz kaldırılmaz; sentetik veri kullan.
- **Testler:** Başlangıç/boşta/arama/çökme yakalaması ve endpoint negatif kontrolleri.
- **Tamamlanma ölçütü:** Her uç için amaç/veri/karar var; Yuva telemetrisi ve gizli URL yüklemesi yok.

## 09 — Genel tehdit kaynağını nitelendir

- **Amaç:** Oltalama, malware ve indirme için çalışan lisanslı güvenli veri yolu seç.
- **Dosyalar/bileşenler:** components/, docs/adr/, PRIVACY.md
- **Bağımlılıklar:** 08
- **Güvenlik:** GPC/Trusted Sites takip listesi bunun yerine geçmez; URL ve hash-prefix sızıntısı incelenir.
- **Testler:** Sentetik zararlı site/dosya, stale/offline, relay arızası, ağ gizliliği.
- **Tamamlanma ölçütü:** Koşullar ve kapsama kanıtı onaylı; yoksa resmî ikili kapısı kapalı.

## 10 — Marka ve Türkçe kaynakları ayır

- **Amaç:** Minimal Yuva kimliği ve GRIT yerelleştirme kaynaklarını ekle.
- **Dosyalar/bileşenler:** resources/, patches/chromium/branding/, docs/LANGUAGE_POLICY.md
- **Bağımlılıklar:** 05, 06
- **Güvenlik:** Kod/enum/parametre İngilizce; UI/yorum Türkçe; güvenlik metni zayıflatılmaz.
- **Testler:** Türkçe casing/bidi/kesilme, kaynak anahtarı, uygulama kimliği çakışması.
- **Tamamlanma ölçütü:** Yuva markasıyla açılıyor; ikinci render kabuğu veya ağır UI yok.

## 11 — Semantik token ve canlı tema hattını kur

- **Amaç:** System/Light/Dark çözümünü native renk sağlayıcı ve WebUI arasında birleştir.
- **Dosyalar/bileşenler:** components/browser/ui/, resources/, docs/DESIGN_SYSTEM.md
- **Bağımlılıklar:** 10
- **Güvenlik:** Kritik uyarı görünür; web sayfası chrome temasını değiştiremez.
- **Testler:** OS canlı değişim, elle seçim, kontrast, forced-colors, DPI ve klavye; Pardus ayrı.
- **Tamamlanma ölçütü:** Yeniden başlatmasız üç mod, varsayılan Sistem; token dışı ham renk yok.

## 12 — Geçici profil yazılarını denetle

- **Amaç:** OTR ve parent keyed service disk/ağ yan etkisini incele.
- **Dosyalar/bileşenler:** components/browser/storage/, tests/privacy/, docs/adr/
- **Bağımlılıklar:** 07, 08
- **Güvenlik:** OTR path paylaşımı ve eklenti yazıları görmezden gelinmez.
- **Testler:** SQLite/LevelDB/cache/service worker/dump dosya farkı, normal kapanış ve çökme.
- **Tamamlanma ölçütü:** Yazı envanteri ve kabul edilebilir istisnalar açık; çözümsüz site kalıcılığı yok.

## 13 — Bütün pencere oturum yaşam döngüsünü kur

- **Amaç:** Normal web açılışlarının tek geçici bağlama yönlendirilmesini uygula.
- **Dosyalar/bileşenler:** components/browser/storage/, patches/privacy/, tests/privacy/
- **Bağımlılıklar:** 12
- **Güvenlik:** Popup/harici protokol/extension/restore kalıcı profile kaçamaz.
- **Testler:** Son pencere, macOS boş süreç, background worker, çok sekme, çökme/yeniden açılış.
- **Tamamlanma ölçütü:** Web verisi oturum bitince yeniden kullanılamıyor; kullanıcıya adli silme sözü yok.

## 14 — Mahremiyet varsayılanlarını nitelendir

- **Amaç:** Üçüncü taraf engeli, partitioning, HTTPS-first, referrer, izin ve DNS/WebRTC politikasını kur.
- **Dosyalar/bileşenler:** components/browser/policy/, build/config/, tests/privacy/
- **Bağımlılıklar:** 07, 09, 13
- **Güvenlik:** DoH/VPN/WebRTC için sızıntısızlık iddiası kanıtsız değil; TLS fallback yok.
- **Testler:** İki site/aynı tracker, CHIPS/Storage Access, proxy/IPv6/TURN, captive portal, izin ömrü.
- **Tamamlanma ölçütü:** Sınırları belgeli varsayılanlar ve kritik uyum testi geçiyor.

## 15 — Yerel takip motorunu değerlendir

- **Amaç:** adblock-rust lisansı/FFI/performansını dar bir prototiple nitelendir.
- **Dosyalar/bileşenler:** third_party/, components/yuva_kalkan/, tests/fuzz/
- **Bağımlılıklar:** 05, 08
- **Güvenlik:** Panic/ömür/boyut sınırları; başlangıçta scriptlet/uzak kod yok.
- **Testler:** Parser fuzz, adversarial kural, worker/redirect kaynak bağlamı ve gecikme.
- **Tamamlanma ölçütü:** Motor seçimi ADR ile gerekçeli; MPL kaynak/bildirim yükümlülüğü karşılanıyor.

## 16 — Takip ve reklam veri kümelerini ayır

- **Amaç:** Standart takip alt kümesi ile Sıkı genel reklam kurallarını ayrı derle.
- **Dosyalar/bileşenler:** scripts/, components/yuva_kalkan/, tests/fixtures/
- **Bağımlılıklar:** 15
- **Güvenlik:** Ücretli allowlist, kendi reklamı veya kaynağı belirsiz kural yok.
- **Testler:** Bağlamsal reklama Standart izin, tracker engeli, Sıkı farkı, lisans ve yanlış pozitif.
- **Tamamlanma ölçütü:** Sürüm/hash/köken/lisans taşıyan deterministik iki politika kümesi var.

## 17 — Dar izleme parametresi temizliğini ekle

- **Amaç:** fbclid/gclid/utm ailesini kanıtlı üst gezinme bağlamında temizle.
- **Dosyalar/bileşenler:** components/yuva_kalkan/, tests/compatibility/
- **Bağımlılıklar:** 14, 16
- **Güvenlik:** İmzalı URL/ödeme/auth/POST/body/fragment keyfi değiştirilmez.
- **Testler:** Kodlama/duplicate parametre, redirect, signed URL ve banka giriş fixtureları.
- **Tamamlanma ölçütü:** Temizlenen parametre RAM sayacı doğru; istisnalar dar ve sürümlü.

## 18 — GPC ve DNT tercihlerini uygula

- **Amaç:** HTTP/DOM/worker sinyallerini açık mahremiyet ayarına bağla.
- **Dosyalar/bileşenler:** components/privacy_signals/, components/browser/ui/, tests/privacy/
- **Bağımlılıklar:** 10, 14
- **Güvenlik:** Sinyal yokluğu rıza değildir; DNT açıklaması ve kullanıcı seçimi koşulu korunur.
- **Testler:** Üst gezinmede GPC snapshot, worker/header tutarlılığı, kapatma/yenileme ve fingerprint farkı.
- **Tamamlanma ölçütü:** Varsayılanlar/sınırlar Türkçe açıklanıyor; kabul rızası üretilmiyor.

## 19 — Kalkan seviye ve küçük panel sözleşmesini uygula

- **Amaç:** Standart/Sıkı/siteye özel Kapalı ve doğru oturum sayacını sun.
- **Dosyalar/bileşenler:** components/browser/ui/, components/yuva_kalkan/, tests/browser/
- **Bağımlılıklar:** 11, 13, 16, 17, 18
- **Güvenlik:** Off zorunlu güvenlik/içerik/çerez/partition korumasını kapatamaz; site sayacı telemetri değil.
- **Testler:** Yetkisiz sayfa çağrısı, navigation/BFCache, alt küme sayacı, klavye/ekran okuyucu.
- **Tamamlanma ölçütü:** Yalnız uygulanan koruma gösteriliyor; Remember etkin düğme olarak sunulmuyor.

## 20 — Ortak imzalı veri doğrulayıcıyı kur

- **Amaç:** Bakımlı TUF istemcisini rol/expiry/rollback ve atomik durumla bütünleştir.
- **Dosyalar/bileşenler:** components/component_security/, tests/security/, tests/fuzz/
- **Bağımlılıklar:** 03, 07
- **Güvenlik:** Browser/registry/content/filter ayrı kök; HTTPS yetki değildir.
- **Testler:** Tamper/replay/rotation/equivocation/saat/çökme/boyut ve platform crypto vektörleri.
- **Tamamlanma ölçütü:** Bağımsız inceleme ve bütün negatif vektörler geçiyor.

## 21 — Trusted Sites şemasını ve derleyicisini oluştur

- **Amaç:** Kurum, exact origin, kanıt, kapsam ve süre alanlarını doğrula.
- **Dosyalar/bileşenler:** trusted-sites/schema/, trusted-sites/fixtures/, scripts/
- **Bağımlılıklar:** 20
- **Güvenlik:** Duplicate/çelişkili host, public suffix ve keyfi script/regex reddi.
- **Testler:** IDNA/PSL/port/category/size, JSON duplicate ve tutarsız login listesi.
- **Tamamlanma ölçütü:** Şema sürümlü; yalnız ayrılmış test domain fixtureları kullanılıyor.

## 22 — Banka kapsam envanterini hazırla

- **Amaç:** BDDK faaliyet kapsamındaki her kurumu kaynak snapshot ile mutabık hale getir.
- **Dosyalar/bileşenler:** yuva-trusted-sites taslak deposu, trusted-sites/governance/
- **Bağımlılıklar:** 21
- **Güvenlik:** Liste uydurulmaz; DNS/TLS tek kimlik kanıtı değil; müşteri verisi yok.
- **Testler:** Sayfalama/kategori/iptal farkı, iki kaynak incelemesi, primary/login/auth/corporate kapsamı.
- **Tamamlanma ölçütü:** Her kurumun durumu/kanıtı var; kritik çözülmemiş domain üretim kapısını engelliyor.

## 23 — Kamu hizmeti kapsamını hazırla

- **Amaç:** e-Devlet/kurum/belediye/YÖK/UYAP dizinlerinden kanıtlı hizmet envanteri üret.
- **Dosyalar/bileşenler:** yuva-trusted-sites taslak deposu, trusted-sites/governance/
- **Bağımlılıklar:** 21
- **Güvenlik:** gov.tr/edu.tr wildcard güveni ve özel kuruluşu kamu sayma yok.
- **Testler:** Bütün sayfa/harfler, shared host ve üçüncü taraf kimlik sağlayıcısı ayrımı.
- **Tamamlanma ölçütü:** Tanımlı kaynak kapsam manifesti, iki inceleme ve giriş akışı kanıtı tamam.

## 24 — Registry anahtar ve yayın işletimini kur

- **Amaç:** Kök töreni, ayrı yetkiler, süreli yeniden inceleme ve acil çıkarma sürecini işlet.
- **Dosyalar/bileşenler:** Ayrı registry yayın işleri, trusted-sites/governance/
- **Bağımlılıklar:** 20, 22, 23
- **Güvenlik:** Özel anahtar depoya/CI buildera giremez; iki insan payload digest onayı.
- **Testler:** Çevrimdışı istemci, root kaybı/rotasyon, kaynak iptali ve stale badge deneyi.
- **Tamamlanma ölçütü:** İlk üretim paketi ve kapsam raporu bağımsız onaylı; hizmet sorumluları hazır.

## 25 — Origin rozeti ve yerel eşleşmeyi bütünleştir

- **Amaç:** Normal TLS + güncel kayıt durumunu browser-owned UIya bağla.
- **Dosyalar/bileşenler:** components/trusted_sites/, components/browser/ui/
- **Bağımlılıklar:** 11, 20, 21, 24
- **Güvenlik:** Kurum güvenilirliği garantisi değil; TLS bypass veya stale olumlu rozet yok.
- **Testler:** Redirect/provisional commit/BFCache/fullscreen/TLS race ve tam host/port.
- **Tamamlanma ölçütü:** Bütün negatif durumlarda rozet kalkıyor, ayrıntı doğru ve erişilebilir.

## 26 — Benzer adres sınıflandırıcısını ve kesintiyi nitelendir

- **Amaç:** Unicode/mesafe/klavye/brand/PSL/redirect sinyallerini birleştir.
- **Dosyalar/bileşenler:** components/trusted_sites/, tests/security/, tests/fixtures/
- **Bağımlılıklar:** 22, 23, 25
- **Güvenlik:** Salt benzerlikle blok yok; resmî hedefe saldırgan parametre/POST aktarılmaz.
- **Testler:** Türkçe benign/sentetik saldırı korpusu, precision/FP/gecikme ve ağdan önce kesinti.
- **Tamamlanma ölçütü:** Önerilen kalite kapıları ölçülmüş; sade Türkçe güvenli eylem ve düzeltme yolu var.

## 27 — Banka güvenlik bağlamını araştır ve sınırla

- **Amaç:** Otomatik origin bağlamı/HTTPS/download/redirect temelini kur; derin extension/pano müdahalesini ADRye ayır.
- **Dosyalar/bileşenler:** components/bank_security/, docs/adr/, tests/compatibility/
- **Bağımlılıklar:** 09, 25, 26
- **Güvenlik:** MFA/3DS/WebAuthn sessiz değişmez; pano içeriği kaydı ve genel eklenti kapatma yok.
- **Testler:** Content script/worker/activeTab/debugger erişim haritası ve izinli bankacılık testleri.
- **Tamamlanma ölçütü:** Temel bağlam ölçülmüş; ileri kontrol uygulanmadıysa sınırı açık, iddia yok.

## 28 — İçerik kaynak lisansı ve kalitesini onayla

- **Amaç:** UT1/alternatif kaynakları veri hakları, kategori ve güncellikle karşılaştır.
- **Dosyalar/bileşenler:** content-protection/governance/, üçüncü taraf veri bildirimleri
- **Bağımlılıklar:** 01
- **Güvenlik:** CC BY-SA/Unlicense şartları ayrı; yeniden dağıtımı belirsiz veri alınmaz.
- **Testler:** Kaynak snapshot, license diff, sağlık/eğitim/kamu benign örnekleri.
- **Tamamlanma ölçütü:** Seçim ve atıf/türev koşulları yazılı; milyonları elle listeleme yok.

## 29 — İçerik içe alma hattını oluştur

- **Amaç:** Sınırlı arşivden normalize/dedup/kategori denetimli veri üret.
- **Dosyalar/bileşenler:** scripts/, content-protection/schema/, tests/fuzz/
- **Bağımlılıklar:** 20, 28
- **Güvenlik:** Path traversal/decompression bomb/shared suffix ve kaynak zehirleme sınırı.
- **Testler:** Domain/IDNA/public-private suffix, anormal fark, kurum listesi çelişkisi.
- **Tamamlanma ölçütü:** Deterministik payload ve kaynak/köken/düzeltme manifesti var.

## 30 — Kompakt içerik indeksini ölç

- **Amaç:** Tam küme referansı ile trie/hash/Bloom adayını karşılaştır.
- **Dosyalar/bileşenler:** components/content_protection/, tests/fixtures/
- **Bağımlılıklar:** 29
- **Güvenlik:** Bloom pozitif tek başına blok olamaz; parser/mmap sınırı.
- **Testler:** Milyonluk veri eşdeğerliği, adversarial indeks, p95/RSS/açılış bütçesi.
- **Tamamlanma ölçütü:** Exact eşleşme kanıtlı; seçimin bellek/gecikme raporu yayımlanabilir.

## 31 — İçerik yerel yaptırımını bütünleştir

- **Amaç:** Gezinme/ağ/worker/cache/restore kapılarında zorunlu politikayı uygula.
- **Dosyalar/bileşenler:** components/content_protection/, patches/chromium/security/, tests/browser/
- **Bağımlılıklar:** 13, 20, 30
- **Güvenlik:** Off/Remember/extension bypass yok; eski negatif liste ve verisiz onarım durumu açık.
- **Testler:** Redirect/popup/prefetch/DNS speculation/BFCache/service worker/offline/bozuk liste/çökme.
- **Tamamlanma ölçütü:** Bilinen hedef dış isteğe gitmeden engelli; deneme geçmişi/log/telemetri yok.

## 32 — Yanlış pozitif ve düzeltme sürecini kur

- **Amaç:** Kayıt/içerik/filtre hatası için açık ve mahremiyetli rapor yolu sağla.
- **Dosyalar/bileşenler:** components/browser/ui/, docs/, ayrı veri yayın işleri
- **Bağımlılıklar:** 19, 24, 26, 31
- **Güvenlik:** Domain yalnız açık onayla; path/query/history yok; kamuya görünür rapor açıklanır.
- **Testler:** Gönderim öncesi önizleme/iptal, imzalı daha-yüksek sürüm düzeltmesi, consent negatif testi.
- **Tamamlanma ölçütü:** Sorumlu ve yanıt hedefi var; düzeltme genel malware kararını kaldırmıyor.

## 33 — Pardus yerel paketini üret

- **Amaç:** Her destek koluna doğal Debian paketi ve masaüstü bütünleşmesi ekle.
- **Dosyalar/bileşenler:** build/packaging/pardus/debian/, docs/PARDUS_SUPPORT.md
- **Bağımlılıklar:** 06, 10, 13
- **Güvenlik:** Bakım betiğinde ağdan kod, sandbox kapatma veya kullanıcı profili silme yok.
- **Testler:** dpkg-shlibdeps, temiz kurulum/yükseltme/kaldırma, dependency ve imza hatası.
- **Tamamlanma ölçütü:** 23.x/25.x ayrı .deb build artefaktı ve kaynak/bağımlılık kaydı var.

## 34 — Pardus masaüstü yeterliliğini kanıtla

- **Amaç:** Gerçek desteklenen Pardus çekirdeğinde XFCE/GNOME akışlarını nitelendir.
- **Dosyalar/bileşenler:** tests/compatibility/, platform CI matrisi
- **Bağımlılıklar:** 07, 11, 14, 19, 26, 31, 33
- **Güvenlik:** Generic Linux veya container sonucu yerine geçmez; başarısız kol sessiz kaldırılamaz.
- **Testler:** Sandbox, tema değişimi, Orca/DPI, PDF/yazıcı, keychain, Türk hizmetleri ve güncelleme.
- **Tamamlanma ölçütü:** Her destek kolu için gereken oturum/test artefaktı yeşil.

## 35 — Bütün masaüstü uyumluluk matrisini tamamla

- **Amaç:** Windows/macOS/Linux ve Pardus kritik hizmet/MFA/eklentiyi karşılaştır.
- **Dosyalar/bileşenler:** tests/compatibility/, docs/TURKISH_WEB_COMPATIBILITY.md
- **Bağımlılıklar:** 27, 32, 34
- **Güvenlik:** Gerçek hesap/PIN kullanmadan fixture; canlı kabul yalnız kurum/testçi izniyle.
- **Testler:** e-imza/mobil imza/KamuSM/UYAP/QR/PDF/3DS; iki macOS mimarisi.
- **Tamamlanma ölçütü:** Her akışın tam sürümlü sonucu ve destek dışı middleware sınırı açık.

## 36 — Sırsız CI ve güvenilir build ayrımını kur

- **Amaç:** Tam SHA action, asgari yetki, geçici runner ve ayrı yayın işleri oluştur.
- **Dosyalar/bileşenler:** .github/workflows/, .github/CODEOWNERS, build/toolchains/
- **Bağımlılıklar:** 02, 03, 05
- **Güvenlik:** PR kodu ayrıcalıklı runner/signer/secret/Docker socket göremez.
- **Testler:** Fork PR, workflow injection, cache poisoning, artefakt değiştirme ve iptal işi.
- **Tamamlanma ölçütü:** Güven sınırları denetlenmiş; atlanan test desktop-ready üretemiyor.

## 37 — SBOM, lisans ve yeniden üretim kanıtını ekle

- **Amaç:** Gerçek bağımlılık grafiği ve unsigned içerik karşılaştırmasını üret.
- **Dosyalar/bileşenler:** scripts/licenses/, scripts/release/, build/
- **Bağımlılıklar:** 16, 24, 29, 35, 36
- **Güvenlik:** Tüm Chromium DEPS/araç/liste girdisi; SBOM eksikliği gizlenmez.
- **Testler:** İki temiz derleme, değişmiş bağımlılık, notice/source archive ve provenance özeti.
- **Tamamlanma ölçütü:** Açıklanamayan executable farkı yok; imza/zaman farkları ayrı rapor.

## 38 — İmzalama ve yetkili release hattını kur

- **Amaç:** OS imzası/noter, ayrı binary TUF kökü ve GitHub artefakt yayını tasarımını uygula.
- **Dosyalar/bileşenler:** scripts/release/, .github/workflows/, components/updater/
- **Bağımlılıklar:** 20, 36, 37
- **Güvenlik:** GitHub/checksum tek başına yetki değil; signer yalnız onaylı digest kabul eder.
- **Testler:** Authenticode/Gatekeeper/offline .deb doğrulama, wrong publisher/channel/arch, role/TOCTOU.
- **Tamamlanma ölçütü:** İmzalı paket/manifest/SBOM/provenance birbirine bağlı, özel anahtar açığa çıkmıyor.

## 39 — Güncellik bildirimi ve ilk kurulum doğrulamasını ekle

- **Amaç:** 0.1 elle güncelleme sınırını güvenilir meta veriyle görünür yap.
- **Dosyalar/bileşenler:** components/updater/, components/browser/ui/, docs/BUILD.md
- **Bağımlılıklar:** 38
- **Güvenlik:** İlk kurulum güveni aynı ele geçirilmiş indirme sayfasına indirgenemez.
- **Testler:** Stale metadata, clock, replay, yanlış platform, bağımsız kök/publisher doğrulama.
- **Tamamlanma ölçütü:** Kullanıcı sürüm yaşı ve doğrulanmış güncelleme yolunu görüyor; kör binary yürütme yok.

## 40 — Upstream ve olay tatbikatlarını çalıştır

- **Amaç:** Acil/rutin roll ve anahtar/runner kesintisini süreyle ölç.
- **Dosyalar/bileşenler:** scripts/release/, UPSTREAM_STRATEGY.md, SECURITY.md
- **Bağımlılıklar:** 35, 38, 39
- **Güvenlik:** SLA tutturmak için güvenlik testi kapatılamaz; iki müdahale sorumlusu.
- **Testler:** Üç roll, registry/content rotation, eksik platform, bozuk kurucu ve recovery.
- **Tamamlanma ölçütü:** Hedef süre/capacity kanıtlı veya yayın ertelenmiş; özel bildirim kanalı denenmiş.

## 41 — Resmî 0.1 yayın kapısını değerlendir

- **Amaç:** Sadece bütün temel güvenlik ve platform koşulları sağlanmış adayı terfi ettir.
- **Dosyalar/bileşenler:** Release manifest, ROADMAP.md, PRIVACY.md
- **Bağımlılıklar:** 09, 19, 24, 26, 27, 31, 32, 35, 37, 38, 39, 40
- **Güvenlik:** Eksik bank/kamu/content koruması olan ikili resmî önizleme olamaz.
- **Testler:** Dağıtılacak baytların dışarıdan doğrulanması, tüm matris ve ağ/veri envanteri.
- **Tamamlanma ölçütü:** Windows/macOS/Linux/Pardus kapıları yeşil; sınırlar açık; aksi halde kaynak-only.

## 42 — Hatırlama ADR ve prototipini hazırla

- **Amaç:** Ayrı context ile selective persistence maliyetini araştır.
- **Dosyalar/bileşenler:** components/browser/storage/, docs/adr/, tests/privacy/
- **Bağımlılıklar:** 13, 35
- **Güvenlik:** OTR in_memory bayrağıyla çözüm yok; site/origin ve üçüncü taraf kapsamı açık.
- **Testler:** SSO/POST/opener/postMessage/worker/çok context kaynak bütçesi.
- **Tamamlanma ölçütü:** Güvenli yönlendirme kanıtlı ya da özellik gerekçeyle ertelenmiş.

## 43 — Hatırlama ve Unut pilotunu nitelendir

- **Amaç:** Temiz yeniden açma ve iptal/quiesce/silme yaşam döngüsünü sınırlı pilotta kur.
- **Dosyalar/bileşenler:** components/browser/storage/, components/browser/ui/, tests/privacy/
- **Bağımlılıklar:** 42
- **Güvenlik:** Canlı veri nakli, sahte yalnız-login vaadi ve yarım silmede başarı yok.
- **Testler:** İptal, eşzamanlı sekme, crash journal, BFCache, disk dolması, eski context erişimi.
- **Tamamlanma ölçütü:** Kalıcılık açık kullanıcı eylemi; Unut arızası görünür ve güvenli tekrar denemeli.

## 44 — CMP ret ve Sıkı kozmetik filtre deneyini incele

- **Amaç:** Rıza uydurmadan düşük bakım yüküyle isteğe uygun ret/kozmetik desteğini değerlendir.
- **Dosyalar/bileşenler:** components/yuva_kalkan/, docs/adr/, tests/compatibility/
- **Bağımlılıklar:** 16, 18, 19, 32
- **Güvenlik:** Accept/TCF rızası üretme veya tercihsiz banner gizleme yok; hukuki inceleme gerekir.
- **Testler:** CMP sürüm değişimi, ret başarısızlığı, bozulmuş sayfa ve Standart/Sıkı farkı.
- **Tamamlanma ölçütü:** Yalnız test edilmiş dar davranış etkin, bilinmeyen CMP görünür.

## 45 — Otomatik kurulum uyarlayıcılarını nitelendir

- **Amaç:** Windows/macOS güvenli updater, Linux/Pardus tek sahip paket yöneticisi kur.
- **Dosyalar/bileşenler:** components/updater/, build/packaging/, tests/security/
- **Bağımlılıklar:** 38, 39, 40
- **Güvenlik:** Artan güvenlik eşiği; sessiz rollback/telemetri yok; installer IPC dar.
- **Testler:** TOCTOU/path traversal/symlink/güç kesintisi/disk dolması/yetki ve sağlık kurtarma.
- **Tamamlanma ölçütü:** Onaysız bayt çalışmıyor, veri korunuyor, geçmiş sürüme güvenli olmayan dönüş yok.

## 46 — Beta bağımsız denetimini ve fingerprint araştırmasını tamamla

- **Amaç:** Depolama/update/registry/content dış incelemesi ve ölçülü entropi azaltımı yap.
- **Dosyalar/bileşenler:** tests/, docs/adr/, güvenlik denetim raporları
- **Bağımlılıklar:** 43, 44, 45
- **Güvenlik:** Denetim logosu garanti değil; canvas/WebGL/audio/font farkı yeni fingerprint yaratabilir.
- **Testler:** Correlation/uyumluluk/performance, bütün OS accessibility ve bağımsız rebuild.
- **Tamamlanma ölçütü:** Önemli bulgular kapalı; yalnız kanıtlı mitigasyonlar yayın kapsamına alınmış.

## 47 — İsteğe bağlı Vakitler fizibilitesini nitelendir

- **Amaç:** Sağlayıcı hakları, yerel hesap ve manuel şehirle sonraki küçük yardımcıyı değerlendir.
- **Dosyalar/bileşenler:** components/optional/prayer_times/, docs/OPTIONAL_FEATURES.md
- **Bağımlılıklar:** 11, 36; güvenlik çekirdeği işleri öncelikli
- **Güvenlik:** Varsayılan off; din/IP çıkarımı, GPS sessiz erişim, telemetry, ses/portal yok.
- **Testler:** Kapalı ağ yok, timezone/DST/Ramazan/gece yarısı/high latitude, provider lisans/doğruluk.
- **Tamamlanma ölçütü:** Ayrı kapsam kararı ve ölçülmüş doğruluk varsa opt-in pilot; güvenlik yayınına engel değil.

## 48 — 1.0 işletim yeterliliğini doğrula

- **Amaç:** Sürdürülebilir güncelleme, veri inceleme ve destek sonu işletimini kanıtla.
- **Dosyalar/bileşenler:** ROADMAP.md, SECURITY.md, destek/yayın manifestleri
- **Bağımlılıklar:** 41, 45, 46
- **Güvenlik:** Kritik/yüksek bulgu ve bakımcı yedeksizliğiyle stable terfi yok.
- **Testler:** Sekiz haftalık roll kayıtları, incident/rotation, tüm platform/registry/content kapıları.
- **Tamamlanma ölçütü:** Açık destek politikası, çözülmüş önemli bulgular ve sürdürülebilir ekip; anonimlik iddiası yok.
