# Derleme, yayın ve güncelleme güvenliği

Durum: Faz 0 önerisi, 18 Eylül 2026. Workflow, üretim anahtarı, ikili yayın veya ürün güncelleyicisi oluşturulmadı.

```text
Chromium güvenlik yayını → incelenmiş kaynak kilidi / yamalar
→ yalıtılmış platform derlemeleri → güvenlik / uyumluluk kapıları
→ değişmez artefakt özetleri / SBOM / üretim kanıtı
→ bağımsız yayın yetkilendirmesi → OS imzası / noter onayı
→ imzalı yayın üstverisi → GitHub Release → doğrulanmış kurulum
```

GitHub dağıtım/işbirliği hizmetidir, güven kökü değildir. Aynı ele geçirilmiş sayfadaki SHA-256 dosyası ikiliyi yetkilendirmez. Yeşil CI veya attestation kaynak kodun zararsızlığını kanıtlamaz.

## GitHub Actions ve görev ayrımı

Planlanan işler: `presubmit.yml`, `upstream-watch.yml`, `build-candidate.yml`, `verify-candidate.yml`, `authorize-release.yml`, `publish.yml`. Adlar tasarımdır, çalışan dosyalar değildir.

PR CI salt okunur yetkili ve sırsızdır. `pull_request_target`/`workflow_run` üzerinden güvenilmeyen PR kodu ayrıcalıklı çalıştırılmaz. İnsan onayı kodu temizlemez. Geçici koşucular kullanılır; açık PR kalıcı güvenilir self-hosted derleyiciye, Docker soketine, imzalayıcıya veya iç ağa erişemez.

Action'lar tam commit SHA'ya sabitlenir; yetki iş bazında asgari tutulur. Güvenilmeyen metin shell koduna eklenmez, veri/argüman olarak geçirilir. Workflow, güven kökü, yama sırası ve yayın politikası iki kişilik CODEOWNERS incelemesi gerektirir. [GitHub güvenli kullanım rehberi](https://docs.github.com/en/actions/reference/security/secure-use).

Yayın; kilitli imajdan yeni VM, korunmuş commit ve doğrulanmış bağımlılıkla üretilir. Getirme işi belgelenmiş upstream uçlarına erişebilir; derleme mümkün olduğunda sonrasında çevrimdışıdır. PR önbelleğiyle güvenilir derleme önbelleği ayrılır; içerik adresli/doğrulanmış girdiler kullanılır. PR nesnesi veya kirli çalışma alanı yeniden kullanılmaz.

İmzalayıcı ayrı kısıtlı hizmettir: onay/provenance ile tam manifest ve hash kabul eder; keyfi betik/yol çalıştırmaz. Derleyici anahtarı alamaz. Donanım/HSM/korumalı anahtar saklama ve kısa ömürlü dar kimlik kullanılır. Çevrimdışı köklerin ayrı sorumluları vardır. CI hesabı tek başına güven kökünü değiştiremez.

## Zorunlu masaüstü matrisi

Windows x86_64, macOS ARM64/x86_64, genel Linux x86_64 ve **Pardus 23.x/25.x x86_64** ayrı işlerdir. Pardus'ta kaynak derleme, yerel `.deb`, XFCE/GNOME ve gerçek Pardus çekirdeği üzerinde test zorunludur. Destek kolları her yayın öncesi resmî yaşam döngüsüyle yenilenir; ayrıntılar [Pardus desteği](docs/PARDUS_SUPPORT.md).

`desktop-ready` terfisi bütün zorunlu işlerin aynı kaynak/yama kümesi ve dağıtılacak artefaktlarla başarılı olmasını ister. Eksik/atlanan/iptal iş ve `continue-on-error` başarı sayılmaz. Genel Linux işi Pardus'un yerine geçemez. Başarılı tek hedefe açıkça sınırlı acil güvenlik paketi çıkabilir; tüm masaüstü hazır iddiası yapılamaz.

## Yayın kanıtları

Her platform/mimari için yayımlanır:

- Yuva/Chromium sürümü, kaynak commit'i, kilit ve yama sırası hash'i.
- Kaynağı yeniden kurma tarifi; lisansların gerektirdiği kaynak arşivi/erişimi.
- Gerçek Chromium DEPS, Rust ve ek çalışma/derleme bağımlılıklarını kapsayan SPDX/CycloneDX SBOM; lisans/hash ve tarama boşlukları.
- SLSA/in-toto biçiminde üretim kanıtı; beklenen builder/workflow, girdiler, boyut ve SHA-256.
- Test manifesti, güvenlik farkları, bilinen sınırlamalar ve destek durumu.
- Ayrılabilen imzasız içerik özeti, son imzalı paket özeti, yetkilendirilmiş yayın üstverisi ve okunabilir checksum.

GitHub attestation doğrulaması beklenen depo, workflow, korunmuş ref ve hash'i sınırlamalıdır; herhangi bir geçerli GitHub imzası yeterli değildir. Şartları karşılamadan SLSA seviyesi iddia edilmez. [Artefakt kanıtları](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations).

## Platform imzalama ve paketleme

| Platform | Koşul |
| --- | --- |
| Windows | Korumalı anahtarla Authenticode ve onaylı zaman damgası; zincir/yayıncı/hash doğrulaması; Mark of the Web ve istismar azaltımları korunur |
| macOS | İç içe kod/bundle Developer ID imzası, incelenmiş Chromium entitlements, uygun hardened runtime, noter onayı/stapling; çevrimdışı Gatekeeper testi |
| Genel Linux | İmzalı depo/paket üstverisi veya bağımsız doğrulanan arşiv; sandbox izinleri ve dağıtım kısıtları korunur |
| Pardus | Her destek kolunda yerel `.deb`; temiz kurulum/yükseltme/kaldırma, bağımlılık çözümü; GitHub'da imzalı yayın üstverisi, gelecekte kapsamlı anahtarla imzalı APT Release/InRelease |

OS imzası yayıncı bütünlüğünü gösterir; eski sürüme dönme izni değildir. İmzalama algoritmaları açık seçilir, sonuç doğrulanır. [SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool), [Apple noter onayı](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution).

Gatekeeper/SmartScreen/AppArmor/seccomp veya sandbox'ı kapatma talimatı verilmez. Güvensiz bayrakla açılan paket kapıdan geçmez. Pardus bakım betikleri ağdan kod indirmez, küresel güvenliği kapatmaz veya kaldırırken kullanıcı profilini silmez. `trusted=yes` yasaktır. Yerel imzasız geliştirici derlemesi herkese açık önizleme değildir.

Gerekli OS imzası, SDK, anahtarlık veya bildirim bütünleşmesi kullanılabilir; gereksiz Microsoft/Apple/Google özel hizmet bağımlılığı eklenmez. Her dış hizmetin amacı/veri akışı belgelenir. Pardus veya genel Linux kullanıcısına özel bulut hesabı zorunlu kılınamaz.

## Yeniden üretilebilirlik

0.1: kilitli kaynağın yeniden kurulması, belgelenmiş tekrar derleme ve referans ortamda iki temiz derlemenin yayımlanmış karşılaştırması. Açıklanamayan imzasız yürütülebilir farklar çözülür; zaman damgası/imza/paket farkları açık listelenir. Bütün OS kurucularında bit düzeyinde aynılık iddia edilmez.

0.3: tüm yayımlanan imzasız içeriklerde bağımsız derleyici ve diffoscope/eşdeğer rapor. 1.0: girdiler/çıktılar için tekrar doğrulama ve açık istisna politikası. Locale, saat dilimi, araçlar, üretim yolları, kaynak üretimi, arşiv sırası ve PGO profilleri sabitlenir. PGO için Yuva gezinme verisi toplanmaz.

Ham ve karşılaştırma özetleri tutulur. Ele geçirilmiş builder kötü ikiliyi de attest edebilir; ayrı yönetilen yeniden derleme farklı kanıt sağlar. İmzalı/noter onaylı sarmalayıcı deterministik içerikten ayrı doğrulanır.

## 0.1 kurulum ve güncellik

Nitelendirilmiş artefaktlar GitHub ön sürümü olarak yayımlanır. İndirilen shell betiği çalıştırma veya yalnız `releases/latest`e güvenme yoktur. Üstveri; kimlik, OS/mimari, kanal, kaynak sürümü, monoton yayın sırası, güvenlik dönemi/asgari sürüm, boyut ve hash'i bağlar. **Tarayıcı yayın kökü**, registry kökünden ayrıdır.

Küçük denetlenebilir doğrulayıcı ve bağımsız kök parmak izi/OS yayıncı kanalları sunulur. Aynı ele geçirilmiş yerden indirilen doğrulayıcı kendi güvenini kuramaz; ilk kurulum güven sınırı açık anlatılır. Kurulum öncesi OS kimliği, imzalı üstveri ve üretim kanıtı denetlenir.

0.1 elle kurulum kullanabilir; imzalı üstveriden güncelleme bildirimi ve sürüm yaşı görünür. Sessiz indirme/çalıştırma yapılmaz. Elle güncelleme yükü açıklanır; eski önizlemeye günlük bankacılık için güvenli denmez. İmzalama, doğrulama veya çalışan genel tehdit arka ucu eksikse herkese açık ikili verilmez.

## Otomatik güncelleyici hedefi

Windows/macOS kurulum mekaniği için Chromium Updater incelenir. Upstream tasarımı ping/telemetri ve sunucu protokolü içerir; yeniden adlandırmak yeterli değildir. Gereksiz raporlar kaldırılır, ağ davranışı kanıtlanır. Linux/Pardus'ta doğal imzalı paket yöneticisi tercih edilir; ayrı güncelleyici onunla yarışmaz. [Chromium Updater tasarımı](https://raw.githubusercontent.com/chromium/chromium/main/docs/updater/design_doc.md).

Bakımı yapılan TUF istemcisi ve ayrı tarayıcı kökü kullanılır: öneri 2/3 çevrimdışı kök, iki bağımsız hedef onayı, ayrı sınırlı tazelik rolleri. [Trusted Sites](TRUSTED_SITES_DESIGN.md) ilkeleri paylaşılabilir; anahtar/rol ad alanı paylaşılamaz.

Durum akışı: üstveriyi doğrula → uygun hedefi seç → özel alana indir → boyut/hash/imza/yayıncı doğrula → güvenli hazırlık → atomik kurulum/geçiş → yerel sağlık kontrolü → tamamla. Onaysız kaynak, yanlış kanal/mimari, arşiv yol aşımı, symlink/hardlink kaçışı, açma bombası ve keyfi kurulum komutu reddedilir.

Hazırlama sonrasında TOCTOU için tekrar doğrula. Güncellemeleri sırala; kullanıcı/sistem kurulumunu ayır; yalnız kurulum sınırında yükseltilmiş yetki kullan. Geri sürüm engeli ve güvenlik dönemi gezinme temizliğinden ayrı tutulur. Renderer URL'si/komutu kurucuya ulaşamaz.

Güç kesintisinde önceki ikiliye dönüş yalnız imzalı asgari güvenlik eşiğini karşılıyor ve açıkça yetkilendirilmişse mümkündür. Bilinen açık sürüme sessiz dönüş yoktur; aksi durumda veri korunur ve onarım durumu gösterilir. Bozuk yayın daha yüksek sıra ile düzeltilir; aynı sürümün baytları değiştirilmez.

Sabit üstveri uçlarına rastgele gecikmeli kontrol; kalıcı kurulum kimliği, referrer, çerez veya site bazlı parametre yok. Başlangıçta geliştirici/kararlı kanalları yeterlidir. GitHub/CDN IP/zaman/platform isteğini yine görebilir. Güncelleme telemetrisi ve URL içeren günlükler kapalıdır.

## Olay ve testler

GitHub hesabı/action değişimi, cache zehirleme, değiştirilmiş artefakt/kanıt, anahtar kaybı, tekrar/eski üstveri, süre dolması, kök döndürme, kesik indirme/kurulum ve disk dolması denenir. Çevrimiçi/çevrimdışı kurulum ve iki sorumlu gereklidir.

Ele geçirilmede terfiyi durdur, çevrimiçi yetkiyi iptal et, yetkilendirilmiş daha yüksek üstveri/anahtar döndürmesi yayımla, temiz ortamda yeniden üret, olay kanıtını koru ve doğrulanmış kanallardan duyur. Kök eşiğinin kaybı, HTTPS'ten gelen yeni anahtara güvenme gerekçesi değildir.

## Zorunlu ürün kapıları

`releaseSecurityGatesPassed`, çalışan genel tehdit/indirme kaynağına ek olarak banka/kamu kapsam manifestini, iki bağımsız kayıt incelemesini, registry imza/expiry/rollback ve benzerlik kalite testlerini; içerik kaynağı lisansını, imzalı yerel liste/bypass/yanlış pozitif/kayıt tutmama testlerini içerir. Bu koşullar resmî Developer Preview için de zorunludur; boş fixture üretim listesi yerine geçmez.

Kalkan Standart/Sıkı/Off ayrımı, Off altında zorunlu korumaların devamı, GPC/DNT ve geçici veri sınırları sınanır. Sistem/Açık/Koyu canlı tema ve erişilebilirlik bütün platform işlerinde yer alır. Vakitler gibi isteğe bağlı yardımcı, güvenlik paketinin veya platform güncellemesinin yayın bağımlılığı olamaz.
