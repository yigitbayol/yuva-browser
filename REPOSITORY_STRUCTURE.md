# İnce Yuva deposu

Güncelleme: 18 Eylül 2026. **Yuva, Yuva'ya sahip olur; Chromium'un tam kaynak ve geçmişini bu depoda taşımaz.** [ADR 0001](docs/adr/0001-thin-chromium-layer.md) bu kararı kabul eder.

## Gerçekte mevcut olan yapı

```text
yuva-browser/
  README.md  LICENSE  CONTRIBUTING.md  SECURITY.md  PRIVACY.md
  ARCHITECTURE.md ve diğer tasarım belgeleri
  config/
    versions.json                    # Açık kaynak kimliği; tam build kilidi değil
    upstream.lock.json               # Kaynak/yama bağları; yalnız source_roots kapsamı
  patches/
    series.json                      # Sürüm 1; henüz yama yok
  scripts/
    bootstrap                        # Plan/önkoşul; açık seçenekle kök getirme
    check-lock                       # Kaynak kök kilidi denetimi
    doctor                           # Salt okunur ortam denetimi
    check-upstream                   # Sürüm/hash/yama uyumu
    check-repository                 # Git indeksi ve boyut bütçesi
    yuva_dev/                        # Python uygulaması; dış paket gerektirmez
  tests/tooling/                     # Sentetik olumsuz ve bütünleştirme testleri
  docs/
    BUILD.md  DESIGN_SYSTEM.md  DESIGN_COMPONENTS.html
    PARDUS_SUPPORT.md  LANGUAGE_POLICY.md ve diğer tasarımlar
    adr/
  .github/workflows/
    development-tools.yml
    upstream-watch.yml
  .gitignore
```

## Gerektiğinde eklenecek Yuva kaynakları

```text
patches/{chromium,privacy}/
components/{yuva_kalkan,trusted_sites,content_protection,component_security}/
components/{bank_security,privacy_signals,updater}/
components/browser/{policy,storage,search,ui}/
components/optional/prayer_times/
branding/
resources/
build/{config,toolchains,packaging}/
build/packaging/pardus/debian/
tests/{browser,privacy,security,compatibility,fixtures,fuzz}/
trusted-sites/{schema,fixtures,governance}/
content-protection/{schema,fixtures,governance}/
third_party/                         # Yalnız incelenmiş küçük ek bileşen/bildirim
```

Boş dizin veya uygulanmamış sahte bileşen eklemek ilerleme sayılmaz. Kod/dizin/parametre adları İngilizce; açıklamalar ve yorumlar Türkçedir. Tasarım HTMLsi ürün WebUI kodu değildir.

## Dış kaynak alanı

Depoyla kardeş, Git'e eklenmeyen çalışma alanı:

```text
Projects/
  yuva-browser/                      # Küçük, yayımlanabilir Yuva deposu
  yuva-chromium/                     # Sonraki açık bootstrap eylemiyle hazırlanacak
    depot_tools/
    src/                             # Sabit upstream + uygulanmış Yuva katmanı
      out/
    manifests/
```

Araçlar iç içe repo/çalışma alanını reddeder. İndirilen Chromium, depot_tools, bağımlılık, cache, profil ve çıktı depoya girmez. Kaynak arşivi/ikili dağıtım gerektiğinde GitHub Release veya tanımlı artefakt depolaması kullanılır; kaynak sağlama lisans yükümlülükleri sürer.

`upstream.lock.json` sonraki sürümde çözülmüş bağımlılık/araç girdileriyle genişleyecek. Mevcut `source_roots` kapsamı tam kilit değildir. Dış alandaki `.yuva-bootstrap.*` işlem durumu ve `.yuva-empty-hooks/` dizini yerel hazırlığa aittir; Git'e eklenmez.

`.gitignore` yaygın yolları dışlar. `scripts/check-repository` ayrıca **Git indeksindeki gerçek blob'ları** inceler: bilinen Chromium/çıktı/cache yolları, symlink/submodule, 5 MiB tek dosya, 100 MiB toplam ve 20.000 dosya sınırı. Bunlar ilk ince depo bütçesidir; her türlü gizlenmiş bağımlılığı/sırrı saptama garantisi değildir. Bir istisna gelecekte ayrı incelenmiş politika kararı ister.

## Sahiplik ve veri depoları

Üretimde `yuva-trusted-sites` kurum kanıt/kapsamını; `yuva-content-data` içerik köken/lisans/düzeltmesini ayrı yayın yetkisiyle tutar. Tarayıcı bu verileri imzayla doğrular; kurum alan adları C++ sabit listesi olmaz. Doğrulayıcı kod paylaşılabilir, binary/registry/content/filter imza yetkisi paylaşılmaz. Operasyon kurulmadan bu depolar açılmış sayılmaz.

Sorumluluklar: Chromium/yama, güvenlik/depolama, platform/yayın, ayrı Pardus, kurum doğrulama, içerik yanlış pozitif/lisans, Türkçe/erişilebilirlik. Kritik yetki sınırları ve üretim kayıtlarında iki bağımsız inceleme hedefi korunur. İlk geliştirici araçları bu operasyonun tamamlandığı anlamına gelmez.

Her anlamlı geliştirme PRı README durumunu günceller; plan/uygulama/derleme/platform testi ayrılır. Asıl mimari köktedir, docs/ARCHITECTURE bağlantı verir; eski ADR gerekçeleri arşivlenir.
