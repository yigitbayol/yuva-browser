# Geliştirme ve derleme iş akışı

Güncelleme: 18 Eylül 2026. İlk geliştirici araçları uygulandı. **Chromium henüz indirilmedi/derlenmedi; çalışan Yuva ikilisi yok.** Mevcut bootstrap yalnız plan/önkoşul aşamasıdır. Büyük indirmeyi otomatik başlatmaz.

## Şimdi çalıştırılabilen komutlar

Python **3.11+** ve Git gerekir; Python paket kurulumu gerekmez. macOS/Linux'ta depo kökünde:

```bash
./scripts/bootstrap --plan
./scripts/doctor
./scripts/check-upstream
./scripts/check-repository
python3 -m unittest discover -s tests/tooling -v
```

Windows'ta aynı araçlar `python scripts/bootstrap --plan`, `python scripts/doctor`, `python scripts/check-upstream` ve `python scripts/check-repository` biçiminde çağrılır. Komut/parametreler İngilizce, yardım ve açıklamalar Türkçedir.

Windows'ta dosyaya yönlendirilmiş Türkçe çıktılar için `python -X utf8 scripts/check-upstream --format json` kullanın. Araç CI'sı `PYTHONUTF8=1` ile çalışır.

| Komut | Gerçek davranışı |
| --- | --- |
| `bootstrap --plan` | Sabit sürüm, revizyon, Yuva/yama sürümü, dış hedef dizin ve disk bütçesini gösterir; ağ veya host aracı çalıştırmaz |
| `bootstrap` | Plan + host önkoşullarını denetler; kaynak hazırlama henüz uygulanmadığı için sıfır olmayan sonuç verir |
| `doctor` | Disk, yol, mimari, Git/Python; Mac'te Xcode/SDK/APFS/RAM; kurulum/indirme yapmaz |
| `check-upstream` | Yerel sürüm şeması, yama manifesti/sırası/hash; ağsız çalışır |
| `check-upstream --network` | Küçük resmî meta verilerle Mac/Windows/Linux Stable sürümlerini, sabit etiketi/commit'i, DEPS hash'ini ve depot_tools commit'ini karşılaştırır |
| `check-repository` | Git indeksindeki gerçek dosya yollarını, nesne boyutlarını ve yasak kaynak/çıktı kalıplarını denetler |

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

Başlangıç [resmî Stable duyurusu](https://chromereleases.googleblog.com/search/label/Stable%20updates) ve [ChromiumDash](https://chromiumdash.appspot.com/fetch_releases?channel=Stable&platform=Mac&num=1) ile incelendi; çalışma anında yeniden kontrol edilmelidir. Mac için seçilen kaynak, Windows/Linux/Pardus yeterliliği anlamına gelmez. Hareketli “latest” ile build yapılmaz. Bu kayıt yalnız kaynak başlangıcıdır; çözümlenmiş DEPS/CIPD/Rust/SDK/derleyici/PGO girdilerini içeren tam `config/upstream.lock.json` sonraki aşamadır.

## Disk, donanım ve çalışma alanı

Chromium kaynak/bağımlılık/cache/çıktıları yapılandırmaya göre yaklaşık 100–200 GB veya daha fazla alan isteyebilir. Yuva'nın ilk büyük indirme önkoşulu **200 GiB boş alan** olarak ihtiyatlı seçildi; evrensel Chromium asgari gereksinimi değildir. Sembol içeren çoklu build ve yeniden üretim kıyası daha fazla alan ister. Başlangıçta ayrı builder için 32–64 GiB RAM planlanabilir; gerçek kapasite ölçülür. 8 GiB RAM düşük paralellik ve swap baskısı yaratabilir.

Varsayılan dış çalışma alanı, depo ile kardeş `yuva-chromium/` dizinidir; yol boşluk içermez. Hedefi değiştirmek için:

```bash
./scripts/bootstrap --plan --workspace /Volumes/Development/yuva-chromium
./scripts/doctor --workspace /Volumes/Development/yuva-chromium
```

Bunlar dizin oluşturmaz. Yuva deposu ile iç içe hedef, dosya hedefi ve kaçan symlink yolu reddedilir. macOS diski APFS olmalıdır. Büyük kaynak/araç indirme başlayacağı gelecekte sürüm/revizyon, yaklaşık disk ihtiyacı ve tam hedef önce gösterilecek; açık indirme eylemi olmadan devam edilmeyecek.

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

Hedef akış `./scripts/bootstrap` → `./scripts/build` → `./scripts/run`. **`build` ve `run` henüz mevcut değildir.** Tam bootstrap için sıradaki işler:

1. Planı göster, host/disk/yol ve incelenmiş kaynak/yama kimliklerini doğrula.
2. Açık indirme eylemiyle, ayrı dış alana sabit depot_tools ve Chromium commit'ini getir; beklenmedik HEAD/etiketi reddet.
3. DEPS'i doğrula; bağımlılık ve araç/hook envanterini incele. İlk getirmede hook'ları çalıştırma; keyfi indirilen kodu güvenilir sayma.
4. Platforma göre DEPS/CIPD/SDK/derleyici girdilerini çözümle ve tam kilit üret; yeniden çalıştırmada tutarsızlığı durdur. Bootstrap betiği `depot_tools`u sessiz güncelleyemez.
5. Yetkili ve nitelendirilmiş hook aşamasıyla araçları hazırla; indirilen girdilerin kimliğini doğrula. Yuva hesap/özel depo gerektirme.
6. Temiz kaynağa yamaları deterministik uygula, son ağaç/yama hash'lerini yaz; çakışmada kapalı dur.
7. İncelenmiş GN argümanlarından build dizini oluştur. İlk önce değişmemiş Chromium güvenlik temeli, sonra Yuva katmanı derlenir.
8. `build` bütün kayıtları doğrulayarak derler; `run` yalnız o çıktı ve ayrı geliştirici profiliyle açar. Sandbox/TLS kapatma bayrağı eklenmez. Çalışan ikilinin kaynak kimliği doğrulanabilir olur.

Kısmi işlem durumu/journal ve güvenli tekrar deneme tasarlanacak; mevcut kullanıcı dizini üzerine kör silme yoktur. Ayrı araç veya build olmadan başarı dosyası oluşturulamaz. Mimari analizi sırasında büyük indirme başlatılmadı.

## CI ve commit disiplini

[development-tools.yml](../.github/workflows/development-tools.yml) sırsız, tam SHA sabitli action'larla Python araç testlerini üç host ailesinde çalıştırır. Bu tarayıcı derlemesi, Pardus testi veya desktop-ready kapısı değildir. [upstream-watch.yml](../.github/workflows/upstream-watch.yml) iki saatte bir planlanan küçük meta veri denetimidir; yeni sürüm veya doğrulama hatası işi başarısız yapar, kaynak/yama silmez veya otomatik yayın yapmaz. GitHub schedule gecikebilir; işletim yedeği gerekir.

Her commit öncesi `git add` sonrasında `./scripts/check-repository` ve `git diff --cached --check` çalıştırılır. `.gitignore` tek başına yeterli değildir; zorla eklenen dosyalar da kontrol edilir. Tarayıcı ikilileri yalnız nitelendirilmiş GitHub Releases artefaktıdır, Git geçmişine girmez. Tam yayın matrisi [Pardus planı](PARDUS_SUPPORT.md) ve [yayın güvenliğinde](../BUILD_RELEASE_SECURITY.md).
