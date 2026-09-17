# Depo yapısı

Durum: öneri. Faz 0 yalnız belgeler, lisans ve bağımsız görsel tasarım envanteri içerir. Aşağıdaki kaynak ağaç henüz oluşturulmuş ürün uygulaması değildir. Dosya/dizin/anahtar adları İngilizce, açıklamalar Türkçedir.

```text
yuva-browser/
  README.md  LICENSE  CONTRIBUTING.md  SECURITY.md  PRIVACY.md
  FOUNDATION_ANALYSIS.md  ARCHITECTURE.md  THREAT_MODEL.md
  ROADMAP.md  REPOSITORY_STRUCTURE.md  UPSTREAM_STRATEGY.md
  PRIVACY_ARCHITECTURE.md  TRUSTED_SITES_DESIGN.md  CONTENT_PROTECTION.md
  BUILD_RELEASE_SECURITY.md  DECISION_SUMMARY.md  IMPLEMENTATION_PLAN.md
  docs/
    README.md  ARCHITECTURE.md  BUILD.md
    DESIGN_SYSTEM.md  DESIGN_COMPONENTS.html
    LANGUAGE_POLICY.md  PARDUS_SUPPORT.md  OPTIONAL_FEATURES.md
    SECURITY_FEATURE_REGISTER.md  TURKISH_WEB_COMPATIBILITY.md
    adr/                              # İncelenmiş kararlar; sonra oluşturulur
  chromium/
    upstream.lock.json                # Kaynak, araç, bağımlılık kimlikleri
    patches/series.json
    patches/{branding,integration,privacy,security}/
  yuva/
    app/                              # Marka ve GRIT kaynakları
    browser/{policy,storage,search,ui}/
    components/{kalkan,trusted_sites,bank_security,content_protection}/
    components/{component_security,privacy_signals}/
    optional/prayer_times/             # Sonraki isteğe bağlı yardımcı
    updater/
  build/{config,toolchains,packaging}/
  build/packaging/pardus/debian/       # Yerel .deb tanımları
  tools/{bootstrap,patches,licenses,release}/
  tests/{browser,privacy,security,compatibility,fixtures,fuzz}/
  trusted-sites/{schema,fixtures,governance}/
  content-protection/{schema,fixtures,governance}/
  third_party/                        # Yalnız incelenmiş ek bileşen/bildirimler
  .github/{workflows,CODEOWNERS,ISSUE_TEMPLATE}/
```

Chromium ayrı ve Git dışında bırakılan çalışma alanına alınır. İndirilen kaynak/build çıktısı, profil, gerçek gezinme yakalaması, test hesabı, anahtar ve sırlar depoya girmez. Uygulanmış yama çıktı ağacı elle düzenlenip asıl yama sanılamaz. Kilit ve yayın manifest'i Yuva commit'i, Chromium commit'i, sıra/hash ve bütün girdileri bağlar; gizli depo/hesap olmadan kaynak yeniden kurulabilmelidir.

Üretimde `yuva-trusted-sites` kurum kayıt/kanıt/kapsamı; `yuva-content-data` içerik kaynak/lisans/düzeltme paketini ayrı yetkiyle yayımlar. Takip filtrelerinin de bağımsız rolü bulunur. Doğrulayıcı paylaşılabilir; yürütülebilir, kimlik kaydı ve engel listesi imza yetkisi paylaşılamaz. Operasyon sınırı oluşmadan gereksiz yeni depolar açılmaz.

Sorumlular: Chromium/yama; mahremiyet/depolama; güvenlik/güven kökü; platform/yayın; ayrı Pardus sorumlusu; kurum kaydı inceleyicileri; içerik lisans/yanlış pozitif; Türkçe/erişilebilirlik. Kritik değişiklikte iki kişi, üretim kaydında iki bağımsız kanıt incelemesi gerekir. Tek kişiye bağlı üretim anahtarı veya nöbet sürdürülebilir değildir.

Kök ARCHITECTURE asıl kaynaktır; docs içindeki aynı adlı dosya bağlantıdır. Diğer belgeler protokol parametresini kopyalamak yerine asıl tasarıma bağlanır. Kabul edilmiş karar değişince önceki gerekçe ADR arşivinde kalır. Görsel HTML yalnız tasarım referansıdır, ürün WebUI kaynağı olarak taşınmaz.
