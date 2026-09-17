# Geliştirme ve derleme iş akışı

Güncelleme: 18 Eylül 2026. Geliştirici araçları ve açık seçenekle kök kaynak getirme uygulandı. **Gerçek Chromium henüz indirilmedi/derlenmedi; çalışan Yuva ikilisi yok.** Bootstrap varsayılan olarak büyük indirme başlatmaz. Kök getirme küçük yerel Git depolarında sınandı; tam bağımlılık hazırlığı henüz yok.

## Şimdi çalıştırılabilen komutlar

Python **3.11+** ve Git gerekir; Python paket kurulumu gerekmez. macOS/Linux'ta depo kökünde:

```bash
./scripts/bootstrap --plan
./scripts/doctor
./scripts/check-upstream
./scripts/check-lock
./scripts/check-repository
python3 -m unittest discover -s tests/tooling -v
```

Windows'ta aynı araçlar `python scripts/bootstrap --plan`, `python scripts/doctor`, `python scripts/check-upstream` ve `python scripts/check-repository` biçiminde çağrılır. Komut/parametreler İngilizce, yardım ve açıklamalar Türkçedir.

Windows'ta dosyaya yönlendirilmiş Türkçe çıktılar için `python -X utf8 scripts/check-upstream --format json` kullanın. Araç CI'sı `PYTHONUTF8=1` ile çalışır.

| Komut | Gerçek davranışı |
| --- | --- |
| `bootstrap --plan` | Sabit sürüm, revizyon, Yuva/yama sürümü, dış hedef dizin ve disk bütçesini gösterir; ağ veya host aracı çalıştırmaz |
| `bootstrap` | Plan + host önkoşullarını denetler; açık getirme seçeneği verilmediği için sıfır olmayan sonuç verir |
| `bootstrap --fetch-roots` | Ortam ve güncellik denetiminden sonra sabit iki Git kökünü getirir/doğrular; alt bağımlılık/hook/yama çalıştırmaz |
| `doctor` | Disk, yol, mimari, Git/Python; Mac'te Xcode/SDK/APFS/RAM; kurulum/indirme yapmaz |
| `check-upstream` | Yerel sürüm şeması, yama manifesti/sırası/hash; ağsız çalışır |
| `check-upstream --network` | Küçük resmî meta verilerle Mac/Windows/Linux Stable sürümlerini, sabit etiketi/commit'i, DEPS hash'ini ve depot_tools commit'ini karşılaştırır |
| `check-repository` | Git indeksindeki gerçek dosya yollarını, nesne boyutlarını ve yasak kaynak/çıktı kalıplarını denetler |
| `check-lock` | Kaynak/yama özetleri, kök revizyonlar ve çözülmemiş aşamaların tutarlılığını denetler; ağ kullanmaz |

Bütün araçlarda `--help` ve `--format json` kullanılabilir. JSON alan/enum değerleri İngilizce; açıklayıcı mesajlar Türkçedir. Çıkış `0`: istenen denetim başarılı; `1`: doğrulama/ortam/eksik uygulama engeli; `2`: geçersiz komut; `check-upstream` için `3`: incelenmesi gereken yeni upstream sürümü. `bootstrap --plan` başarısı hazırlanmış kaynak veya derleme kanıtı değildir.

`check-upstream --network` sabit ChromiumDash/Gitiles uçlarına en fazla birkaç küçük meta veri isteği yapar; tek yanıt 4 MiB ile sınırlıdır. Yönlendirme, kanal/ad biçimi, tarih, commit ve özet hataları reddedilir. Kaynak arşivi indirmez, DEPS/hook çalıştırmaz, sürüm kaydını değiştirmez. HTTPS doğrulaması Yuva ikili yayın imzasının yerine geçmez.

## Sabit başlangıç ve sınırı

[config/versions.json](../config/versions.json) şu başlangıcı kaydeder:

| Alan | Değer |
| --- | --- |
| `yuva_version` | `0.1.0-dev` |
| `chromium_version` | `153.0.8010.53` |
| `chromium_revision` | `792bf6722e73a45aa9e47c163b9901bdc17f3230` |
| `patchset_version` | `1`; [yama listesi](../patches/series.json) şu anda boş |
| `scope` / `qualification` | `source_baseline` / `unbuilt` |

Başlangıç [resmî Stable duyurusu](https://chromereleases.googleblog.com/search/label/Stable%20updates) ve [ChromiumDash](https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Mac&num=1) ile incelendi; çalışma anında yeniden kontrol edilmelidir. Mac için seçilen kaynak, Windows/Linux/Pardus yeterliliği anlamına gelmez. Hareketli “latest” ile build yapılmaz. `config/upstream.lock.json` artık bu kaydı ve yama manifestosunu bağlar; kapsamı yalnız `source_roots` olarak işaretlidir. Çözümlenmiş DEPS/CIPD/GCS/Rust/SDK/derleyici/PGO girdilerini içeren tam kilit sonraki aşamadır. [Kilit sözleşmesi](DEPENDENCY_LOCK.md).

## Disk, donanım ve çalışma alanı

Chromium kaynak/bağımlılık/cache/çıktıları yapılandırmaya göre yaklaşık 100–200 GB veya daha fazla alan isteyebilir. Yuva'nın ilk büyük indirme önkoşulu **200 GiB boş alan** olarak ihtiyatlı seçildi; evrensel Chromium asgari gereksinimi değildir. Sembol içeren çoklu build ve yeniden üretim kıyası daha fazla alan ister. Başlangıçta ayrı builder için 32–64 GiB RAM planlanabilir; gerçek kapasite ölçülür. 8 GiB RAM düşük paralellik ve swap baskısı yaratabilir.

Varsayılan dış çalışma alanı, depo ile kardeş `yuva-chromium/` dizinidir; yol boşluk içermez. Hedefi değiştirmek için:

```bash
./scripts/bootstrap --plan --workspace /Volumes/Development/yuva-chromium
./scripts/doctor --workspace /Volumes/Development/yuva-chromium
```

Bunlar dizin oluşturmaz. Yuva deposu ile iç içe hedef ve dosya hedefi reddedilir; gerçek getirme yolunda hiçbir symlink bileşenine izin verilmez. macOS diski APFS olmalıdır. `--fetch-roots` öncesinde sürüm/revizyon, yaklaşık disk ihtiyacı ve tam hedef gösterilir; açık indirme seçeneği olmadan devam edilmez.

18 Eylül yerel denetiminde Mac ARM64, 8 GiB RAM, yaklaşık 78 GiB boş alan ve yalnız seçili Command Line Tools bulundu. APFS/SDK erişimi var; disk bütçesi ve tam Xcode eksik. Bu geçici ölçüm başka makinenin durumunu göstermez. Yeni ortamda `doctor` tekrar çalıştırılır; otomatik Xcode kurulumu veya global güvenlik ayarı değişikliği yoktur.

## Platform önkoşulları

| Hedef | Gereken ortam | Ek yayın kapısı |
| --- | --- | --- |
| macOS ARM64 / x86_64 | İlgili mimari, APFS, tam Xcode ve revizyona uygun SDK; native test ortamı | Her mimaride sandbox, imza/noter, gerçek UI/MFA testi |
| Windows x86_64 | Sabit sürümün istediği Windows SDK/Visual Studio araçları ve clang-cl | İmzalama, installer/update ve süreç güvenliği |
| Genel Linux x86_64 | Revizyonun istediği host bağımlılıkları, sysroot ve derleyici | Dağıtılan ortamda gerçek sandbox ve ABI testi |
| Pardus 23.x / 25.x x86_64 | Ayrı Pardus kaynak derlemesi, sürümlü imaj/paket tabanı | Yerel `.deb`, gerçek çekirdek, XFCE/GNOME ve desteklenen oturumlar |

Kesin araç sürümleri seçili kaynak revizyonundaki belgelerden çıkarılıp tam kilide bağlanacak. Upstream başvuru: [macOS](https://chromium.googlesource.com/chromium/src/+/main/docs/mac_build_instructions.md), [Windows](https://github.com/chromium/chromium/blob/main/docs/windows_build_instructions.md), [Linux](https://github.com/chromium/chromium/blob/main/docs/linux/build_instructions.md). Bugün tam SDK/bağımlılık reçetesi nitelendirilmedi; desteklenen build gibi sunulmaz. `doctor` diğer OS'lerde bu eksiği açık engel olarak verir.

## Yama uyumunu kaynak indirmeden sınamak

Önceden yerelde bulunan, ayrı ve origin'i resmî Chromium deposu olan bir kaynak ağacında:

```bash
./scripts/check-upstream --source-dir /Volumes/Development/yuva-chromium/src
```

Alternatif hedefte `--target-revision` ile **tam 40 karakter commit** verilir. Hedef yerelde yoksa araç durur; otomatik fetch yapmaz. Geçici Git indeksi ve geçici nesne deposunda yamaları sıralı uygular; gerçek checkout, indeks ve nesne deposuna yeni patch blob'u yazmaz. İlk çakışma, etkilenen bileşenler ve sonraki denenmemiş yamalar raporlanır. Kısmi/promisor clone örtük ağ riski nedeniyle reddedilir.

Bu test temiz bağlamda uygulama uyumudur, güvenlik/derleme/çalışma uyumu değildir. Boş yama kümesi başarıya eşit ürün özelliği sayılmaz. Kimlik, özet ve şema hatasında hiçbir yama atlanmaz.

## Sonraki tam bootstrap/build tasarımı

Hedef akış `./scripts/bootstrap` → `./scripts/build` → `./scripts/run`. **`build` ve `run` henüz mevcut değildir.** Aşağıdaki kök getirme uygulanmıştır; örnek komut büyük indirmeyi açıkça ister ve bu teslimde çalıştırılmamıştır:

```bash
./scripts/bootstrap --fetch-roots --workspace /Volumes/Development/yuva-chromium
```

Üst dizin önceden var olmalı, hedef yeni veya aynı kilitle tamamlanmış temiz Yuva alanı olmalıdır. Ortam kapısı geçmezse upstream isteği/fetch başlamaz. Yeni Stable saptanırsa önce kilit incelemesi gerekir. Hedef HEAD/origin, temiz Git ağacı, DEPS özeti ve VERSION doğrulanır. Sistem/global Git ayarları, haricî hook/filtreler ve alt modül getirme kullanılmaz; HTTPS doğrulaması korunur. Kaynaklar getirilse de `source_prepared` ve `build_ready` hâlâ `false` kalır; yalnız `source_roots_prepared` başarılı olabilir.

Kesinti/hata durumu dış alandaki `.yuva-bootstrap.json` dosyasında saklanır. Aynı anda ikinci hazırlama veya güç kesintisinden kalmış işlem kilidi reddedilir. Başarısız/yabancı/kirli alan üzerine yazılmaz ve otomatik silinmez. Tamamlanmış temiz alan yeniden doğrulanır; aynı kökler tekrar getirilmez. Bu ilk sürümde otomatik kısmi indirme onarımı yoktur. Mevcut dosyaları inceleyin veya ayrı bir yeni hedef seçin; kilit silerek başarı uydurmayın.

Tam hazırlığa devam akışı:

1. Planı göster, host/disk/yol ve incelenmiş kaynak/yama kimliklerini doğrula.
2. Uygulanan `--fetch-roots` ile ayrı dış alana sabit depot_tools ve Chromium commit'ini getir; beklenmedik HEAD/etiketi reddet.
3. DEPS'i doğrula; bağımlılık ve araç/hook envanterini incele. İlk getirmede hook'ları çalıştırma; keyfi indirilen kodu güvenilir sayma.
4. Platforma göre DEPS/CIPD/SDK/derleyici girdilerini çözümle ve tam kilit üret; yeniden çalıştırmada tutarsızlığı durdur. Bootstrap betiği `depot_tools`u sessiz güncelleyemez.
5. Yetkili ve nitelendirilmiş hook aşamasıyla araçları hazırla; indirilen girdilerin kimliğini doğrula. Yuva hesap/özel depo gerektirme.
6. Temiz kaynağa yamaları deterministik uygula, son ağaç/yama hash'lerini yaz; çakışmada kapalı dur.
7. İncelenmiş GN argümanlarından build dizini oluştur. İlk önce değişmemiş Chromium güvenlik temeli, sonra Yuva katmanı derlenir.
8. `build` bütün kayıtları doğrulayarak derler; `run` yalnız o çıktı ve ayrı geliştirici profiliyle açar. Sandbox/TLS kapatma bayrağı eklenmez. Çalışan ikilinin kaynak kimliği doğrulanabilir olur.

Kök işlem durumu ve temiz alanda tekrar doğrulama uygulanmıştır. Bağımlılık/hook/yama aşamalarının journal/onarımı sonraki iştir. Mevcut kullanıcı dizini üzerine kör silme yoktur. Ayrı araç veya build olmadan tam hazırlık başarı dosyası oluşturulamaz. Bu oturumda büyük indirme başlatılmadı.

## CI ve commit disiplini

[development-tools.yml](../.github/workflows/development-tools.yml) sırsız, tam SHA sabitli action'larla Python araç testlerini üç host ailesinde çalıştırır. Bu tarayıcı derlemesi, Pardus testi veya desktop-ready kapısı değildir. [upstream-watch.yml](../.github/workflows/upstream-watch.yml) iki saatte bir planlanan küçük meta veri denetimidir; yeni sürüm veya doğrulama hatası işi başarısız yapar, kaynak/yama silmez veya otomatik yayın yapmaz. GitHub schedule gecikebilir; işletim yedeği gerekir.

İlk araç tesliminin 18 Eylül 2026 doğrulaması: `2975528` kaynak commit'inde 36 test yerelde ve [üç CI hostunun her birinde](https://github.com/yigitbayol/yuva-browser/actions/runs/35278595752) geçti; atlanan test yok. [Uzak upstream denetimi](https://github.com/yigitbayol/yuva-browser/actions/runs/35278601704) de başarılı. İndekste 53 dosya/toplam 318.826 bayt denetlendi; Chromium kaynağı veya ikili çıktı eklenmedi. Bu tarihsel kayıt daha sonraki commit veya upstream sürümlerinin doğrulandığı anlamına gelmez. Kök hazırlama için eklenen testler gerçek Git'i küçük yerel fixture depolarında kullanır; tam Chromium getirme başarısı iddia etmez.

Kök hazırlama tesliminde `1f525b3` için 55 test yerelde ve [Windows/macOS/Linux CI'sının her birinde](https://github.com/yigitbayol/yuva-browser/actions/runs/35280081007) geçti; atlanan test yok. Yanlış commit/DEPS, değiştirilmiş kilit, disk/ağ hatası, kirli/yabancı dizin, aktif işlem kilidi, symlink ve ortam engelinde ağın hiç başlamaması sınandı. Yerel Mac hâlâ yaklaşık 77 GiB boş alan ve yalnız Command Line Tools nedeniyle gerçek getirme önkoşullarını karşılamıyor.

Bu oturumdaki ek ağ denemesinde resmî Chromium Git HTTP `info/refs` başlık isteği 15 saniyede zaman aşımına uğradı; yanıt vermeyen `git ls-remote` işlemi de sonlandırıldı. Bu, genel bir upstream kesintisi kanıtı değildir. Gitiles meta veri erişimi ile Git taşımasının çalışması ayrı kontrollerdir. Gerçek getirme öncesinde bu ortamın Git bağlantısı yeniden nitelendirilmeli; yerel fixture sonuçları uzak sunucudan getirme kanıtı olarak kullanılmamalıdır.

Her commit öncesi `git add` sonrasında `./scripts/check-repository` ve `git diff --cached --check` çalıştırılır. `.gitignore` tek başına yeterli değildir; zorla eklenen dosyalar da kontrol edilir. Tarayıcı ikilileri yalnız nitelendirilmiş GitHub Releases artefaktıdır, Git geçmişine girmez. Tam yayın matrisi [Pardus planı](PARDUS_SUPPORT.md) ve [yayın güvenliğinde](../BUILD_RELEASE_SECURITY.md).
