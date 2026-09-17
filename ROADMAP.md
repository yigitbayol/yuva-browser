# Yol haritası

Durum: 18 Eylül 2026 tarihli öneri. Tarihler ekip, ölçülmüş derleme kapasitesi ve güvenlik kapılarına bağlıdır; teslim tarihi vaadi yoktur. Geç eklenen zorunlu güvenlik kapsamı 0.1'i ilk basit markalama önizlemesinden daha büyük yapmıştır. Kapsamı gizlemek yerine ikili yayın bu kapılara bağlanır.

## Faz 0 — Mimari inceleme

Temel, depolama, güvenlik, kayıt, içerik, yayın ve tasarım belgeleri hazırlandı. İngilizce kod/parametre, Türkçe yorum/belge/UI ve birinci sınıf Pardus kuralları kaydedildi. [İnce depo](docs/adr/0001-thin-chromium-layer.md) ve [önkoşul denetimi](docs/adr/0002-development-preflight.md) kararları geliştirme hazırlığı için kabul edildi. İlgili güvenlik tasarımı incelenmeden büyük Chromium değişikliği yapılmaz.

## Güncel aşama — Faz 1 geliştirme hazırlığı

Sabit kaynak kimlikleri, boş yama manifestosu, salt okunur ortam kontrolü, kök kilidi ve açık seçenekle kök getirme, upstream sürüm/yama denetimi ve Git indeks koruması mevcut. Araçlar CI'da sınanıyor; gerçek Chromium kaynakları henüz getirilmedi veya derlenmedi. Sırada ortam nitelendirmesi, tam bağımlılık/hook/araç kilidi ve GN hazırlığı var. Ayrıntılı gerçekleşme durumu [uygulama planındadır](IMPLEMENTATION_PLAN.md).

## 0.1 — Developer Preview

Önce yerel mühendislik çıktısı: kilitli Chromium'dan açılan, modern web'i çizen, Yuva markalı, Türkçe, Sistem/Açık/Koyu destekli minimal tarayıcı. Gereksiz Google hizmetlerini dar ve ölçülmüş biçimde kaldır; sandbox, TLS, isolation ve güvenlik bileşeni güncellemelerini koru. Bütün normal pencereler denetlenmiş geçici oturumdur; Yuva telemetrisi yoktur.

Kalkan varsayılan Standart: takip/üçüncü taraf çerez engeli, partitioning, dar parametre temizliği, HTTPS-first ve incelenmiş DNS/WebRTC varsayılanları. GPC ve açıklanmış DNT tercihi; Sıkı reklam kuralları ve siteye özgü filtre istisnası. Kapsamlı fingerprint direnci ve çalışan “Bu siteyi hatırla” 0.1 vaadi değildir.

**Resmî önizleme ikilisinin ek zorunlu koşulları:**

- Yetkili envantere göre kapsamı kanıtlanmış banka/kamu registry'si; imzalı dağıtım, TLS'le sınırlı rozet ve yüksek güvenli benzer adres kesintisi.
- Ayrı, lisansı incelenmiş, imzalı yerel yetişkin içerik engeli; yanlış pozitif ve kayıt tutmama kanıtı.
- Genel kötü amaçlı site/indirme korumasının çalışan, lisans/veri akışı incelenmiş kaynağı; Trusted Sites bunun yerine geçmez.
- Windows x86_64, macOS ARM64/x86_64, genel Linux x86_64 ve desteklenen Pardus 23.x/25.x açık derleme/testleri; Pardus yerel `.deb`.
- Geçici depolama/disk/çökme, sandbox/TLS, kritik Türk hizmeti, MFA, görünüm/erişilebilirlik ve ağ envanteri kanıtı.
- OS imzası, bağımsız yetkilendirilmiş yayın meta verisi, SBOM/lisans/provenance, kaynak yeniden kurma ve referans çift derleme raporu.
- Elle doğrulanmış kurulum olabilir; imzalı güncellik bildirimi ve eski önizlemenin sınırları görünür. Üç upstream güncelleme tatbikatı, iki yayın sorumlusu ve özel güvenlik bildirim kanalı gerekir.

Bunlar tamamlanmazsa yalnız kaynak/tasarım ilerlemesi yayımlanır. Test fixture'ı üretim koruması diye sunulamaz. Dört platform ailesi geçmeden “masaüstüne hazır” denemez; acil tek-platform düzeltmesinin dar kapsamı açık yazılır.

## 0.2 — Alpha

0.1'de zorunlu olan korumaları olgunlaştır: banka/kamu kayıt operasyonu ve düzeltme süresi, çok sinyalli analizin precision/false-positive ölçümleri, içerik indeks performansı, Türkçe site uyumluluğu. Bank Security Mode eklenti/pano/indirme müdahaleleri yalnız ayrı tasarım ve MFA testlerinden sonra genişletilir.

Hatırlama için ayrı context prototipi, SSO/worker/POST/popup/Forget/çökme testleri; kanıt yoksa özellik ertelenir, geçici varsayılan değişmez. CMP ret desteği belgelenmiş API/akışlarla araştırılır; kabul rızası uydurulamaz. Sıkı kozmetik reklam filtreleri güvenli veri sınırında değerlendirilebilir. Eklentiler açık erişimle nitelendirilir; mağaza kurulmaz.

Çıkış: veri protokolleri, anahtar rotasyonu/replay/çevrimdışı tatbikatı, bütün masaüstü güncelleyici kurulum/hata akışları ve depolama ADR'si. Gerekirse güncelleme kurulum onayı kullanıcıda kalabilir; doğrulama gevşetilmez.

## 0.3 — Beta

Günlük akış, performans, kaynak kullanımı ve dört platform ailesinde güvenli otomatik güncelleme. Bağımsız depolama/güncelleme/registry/içerik incelemesi; imzasız içeriğin bağımsız yeniden üretim kıyası; erişilebilirlik ve uyumluluk raporu. Fingerprinting için canvas/WebGL/audio/font müdahaleleri ancak ölçülmüş etki/uyum/taşıma maliyetiyle eklenir.

[Vakitler](docs/OPTIONAL_FEATURES.md) için en erken bu aşamada ayrı kapsam kararı: varsayılan kapalı, elle şehir, yerel hesap/provider soyutlaması, lisans ve doğruluk kanıtı. Bu yardımcı beta veya güvenlik yayınının zorunlu çıkış koşulu değildir; güvenlik işini geciktiremez.

## 1.0 — Stable

Yayımlanan özelliklerde açık kritik/yüksek güvenlik veya veri kaybı/kalıcılık sınırı hatası kalmamalı. En az sekiz haftalık sürdürülebilir güvenlik güncelleme operasyonu, bütün zorunlu platform kapıları, anahtar/koşucu kesintisi tatbikatı ve önemli bulguları kapatılmış bağımsız inceleme gerekir.

Destek sonu politikası, gerçek ağ/veri envanteri, yeniden üretim kanıtı, kaynak lisansları, banka/kamu kapsam raporu, içerik düzeltme süreci ve eklenti sınırları yayımlanır. Tam anonimlik, bütün takibi önleme, kuruma kefalet veya içerik engelinin atlatılamazlığı iddia edilmez.

Android sonraki Chromium hattı; iOS ayrı motor/dağıtım fizibilitesidir. Hiçbiri masaüstü güvenlik güncellemesini bekletemez.
