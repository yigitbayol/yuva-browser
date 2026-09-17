# Bağımlılık kilidi ve kaynak hazırlama sınırları

Durum: 18 Eylül 2026. **Kök kaynak kilidi ve kök getirme uygulandı. Tam bağımlılık/derleme kilidi henüz çözülmedi.** Bu ayrım makine çıktısında da korunur: `scope: source_roots`, `source_prepared: false`, `build_ready: false`.

## Neden iki aşama var?

Chromium bağımlılıkları Git, CIPD ve GCS türlerini içerir. `DEPS` yalnız bir paket listesi değildir: koşullar, alt DEPS dosyaları, platform değişkenleri ve hook'lar vardır. Kök DEPS dosyasının özeti bütün bu girdilerin çözüldüğünü kanıtlamaz. [Upstream bağımlılık belgesi](https://chromium.googlesource.com/chromium/src/+/main/docs/dependencies.md).

İncelenen sabit depot_tools sürümünde `gclient flatten --pin-all-deps`, henüz checkout yapılmamış bütün platform bağımlılıklarını kilitleme garantisi vermez. `revinfo --actual --output-json` ve `flatten --output-deps-files` sonraki çözümleyici için kanıt kaynaklarıdır; kendi başlarına SDK/hook indirmeleri dahil tam kilit değildir. Yuva DEPS için ikinci bir Python yorumlayıcısı yazmayacak. İncelenmiş upstream çözümleyici dar bir uyarlayıcı üzerinden kullanılacak. [Sabit gclient kaynağı](https://chromium.googlesource.com/chromium/tools/depot_tools/+/1a91c4bb802179b50776aabcc7d8aa53901a8e80/gclient.py).

## Uygulanan şema 1

[config/upstream.lock.json](../config/upstream.lock.json) şu alanları içerir:

| Alan | Sözleşme |
| --- | --- |
| `schema_version` | Tam sayı `1`; bilinmeyen şema/alan reddedilir. |
| `scope` | Yalnız `source_roots`. Elle `full_build` yazılması kabul edilmez. |
| `source_baseline_sha256` | `config/versions.json` dosyasının tam bayt özeti. |
| `patch_manifest_sha256` | `patches/series.json` dosyasının tam bayt özeti; yama dosyaları ayrıca doğrulanır. |
| `roots` | Sabit sırada depot_tools ve Chromium; beklenen kimlik, dış alandaki dizin, resmî HTTPS URL ve tam commit. |
| `targets` | Windows, iki macOS mimarisi, genel Linux, Pardus 23 ve Pardus 25 ayrı kimliklerdir. Liste destek/test başarısı değildir. |
| `pending_stages` | DEPS grafiği, CIPD, GCS, hook incelemesi, araç zinciri, yama uygulaması, build yapılandırması ve platform derlemeleri çözülmemiştir. |

Doğrulayıcı [lockfile.py](../scripts/yuva_dev/lockfile.py) içindedir. `./scripts/check-lock` ağsızdır. Başarılı çıkış kodu yalnız yukarıdaki sözleşmenin tutarlı olduğunu söyler; kapıları silmek veya hedef listesinden Pardus'u çıkarmak geçerli kilit üretmez. LF satır sonları `.gitattributes` ile korunur.

Sürüm/yama değişikliğinde ilgili kaynaklar önce incelenir, özetler yeniden hesaplanır ve kilit aynı PR'da güncellenir. Hata görünce kilidi otomatik yeniden yazma yoktur. Bu dosya Git incelemesine tabi geliştirme girdisidir; ürün yayın imzası veya TUF yetkilendirmesi değildir.

## Kök getirme sözleşmesi

`bootstrap --fetch-roots` önce sürüm, hedef ve disk ihtiyacını bildirir. Ortam kapısı ve çevrimiçi güncellik/kimlik denetimi geçmeden getirme başlamaz. Yalnız sabit iki commit için shallow Git fetch ve detached checkout yapılır. Kaynak beklenen origin/HEAD, temiz ağaç, DEPS SHA-256 ve `chrome/VERSION` ile yeniden doğrulanır.

Sistem/global Git yapılandırması ve miras alınan `GIT_*` değişkenleri kullanılmaz. HTTPS dışı taşıma, yönlendirme, alt modül tekrarı, haricî template ve hook çalıştırma kapalıdır; TLS doğrulaması açık kalır. İndirilen depot_tools PATH'e eklenmez, `gclient` veya DEPS çalıştırılmaz. Git nesne denetimi açıktır. Git'in kendisi mevcut güvenilir host aracıdır; ele geçirilmiş işletim sistemine karşı koruma iddiası yoktur.

Yeni çalışma alanı ayrı dizindir; symlink yol, mevcut yabancı dizin veya farklı kilit üzerine yazılmaz. `.yuva-bootstrap.lock` eşzamanlı işlemi engeller; `.yuva-bootstrap.json` durum dosyası atomik yenilenir. Normal hata/kesinti `failed` olur. Güç kesintisinden kalan kilit otomatik silinmez. Dosyalar korunur; bu ilk sürüm başarısız işlemde otomatik temizleme/onarım yapmaz. İnsan incelemesi veya yeni bir dış dizin gerekir.

`roots_ready` durumundaki temiz alan tekrar doğrulanabilir; kaynak yeniden getirilmez. Değişmiş dosya, izlenmeyen/ignored içerik, farklı HEAD veya beklenmeyen yerel Git yapılandırması varsa durulur. Uzun işlem sırasında Yuva kilidi değişirse başarı yazılmaz. Bu kontrol, aynı makinede yetkili ve kötü niyetli bir süreçle yarışa karşı güven sınırı değildir.

## Tam kilide geçiş — sonraki uygulama

Şema 2 ve çözümleyici aşağıdaki kanıtları üretmeden tam kilit veya build-ready sonucu verilmeyecek:

1. Her hedef için host/target mimarisi, Pardus sürümü, GN argümanları ve çözümlemede kullanılan koşulların özeti.
2. Kök ve `recursedeps` kapanışındaki bütün DEPS dosyaları: depo, commit, dosya yolu, SHA-256, ebeveyn kenarı. Eksik/çevrimli kapsam açık hata.
3. Git bağımlılıklarında tam URL/revizyon/yol; CIPD'de somut platform paketi ve değişmez instance kimliği; GCS'de nesne/generation/boyut ve içerik özeti. Hareketli ref ve çözülmemiş yer tutucu reddi.
4. Hook envanteri: kaynak betik özeti, amaç, hedef, komut argümanları, ağ uçları, indirilecek girdiler ve inceleme kararı. `--nohooks` yanında pre-DEPS hook'ları da kapalı tutulur; aşamalar ayrı açılır.
5. depot_tools/vpython/CIPD istemcisi/GN/Ninja/Clang/Rust/SDK/sysroot/PGO girdileri ve yerel lisans gereksinimleri. Otomatik depot_tools güncellemesi ve geliştirici araç metriği kapatılıp ağ davranışı sınanır.
6. Çözülmüş envanter ile gerçek checkout/kurulu paketlerin birebir karşılaştırması; sonra kaynak/hook/yama sonucu özetleri. Şema geçerliliği bu karşılaştırmanın yerine geçmez.
7. Temiz ikinci ortamda aynı kimliklerle yeniden hazırlama ve platform referans derlemesi. Üretim yayınında bunun üzerine imza, SBOM ve provenans kapıları gelir.

Mevcut kaynak getirme başarısını tam bağımlılık çözümü gibi göstermemek için şema 1 bilinçli olarak bu alanların çözüldüğü iddiasını kabul etmez. Bu teslimde gerçek Chromium kaynakları getirilmedi; küçük yerel Git depoları ile işlem sınırları sınandı. [Derleme rehberi](BUILD.md), [yayın güvenliği](../BUILD_RELEASE_SECURITY.md).
