# Karar özeti

Durum: mimari inceleme için öneriler, 18 Eylül 2026. Bu belgeler mimari incelenmeden ürün uygulamasına başlama izni değildir.

| Karar | Öneri | Gerekçe / kapı |
| --- | --- | --- |
| Tarayıcı temeli | Güvenlik yamaları güncel Chromium Stable, tam kaynak commit'i | Aradaki çatalı beklemeden upstream; tam tarayıcı güvenlik mimarisi |
| Depo | Küçük `yuva-browser` katmanı, dış Chromium çalışma alanı; üretimde ayrı registry/içerik veri depoları | Denetlenebilir ürün farkı ve ayrı yayın yetkisi |
| Yamalar | Sıralı, hash'li, sahipli; yapılandırma/kanca/ayrı bileşen önceliği | Bulanık uygulama, büyük gölge dosya ve bağımsız Blink/V8 evrimi yok |
| Mahremiyet motoru | Tarayıcı yetkisinde Yuva Kalkan; yerel karar, upstream yaptırım | Sayfa/renderer politika yetkisi veya Yuva URL sorgu servisi yok |
| Takip ve reklam | Standart takip karşıtı; Sıkı reklam engeli; Off yalnız site filtreleri | Takip yapmayan reklam genel engellenmez. Kendi reklamımız/ücretli allowlist yok |
| Eşleştirici | MPL-2.0 adblock-rust aday; lisanslı takip alt kümesi, ayrı Sıkı kuralları | Yeni parser dili yazma; ağ kuralları önce, scriptlet ertelenir |
| Tercih sinyalleri | GPC açık; DNT açıklanmış mahremiyet tercihi; CMP yalnız gerçek ret | Sinyal teknik engel veya evrensel hukuki garanti değil; sahte kabul yok |
| Geçici depolama | 0.1 mevcut OTR altyapısı, tüm normal pencereler, yazı/hizmet denetimi | Sadece çıkışta temizleme çökmede yeterli değil |
| Hatırlama | 0.1 uygulama yok; ayrı BrowserContext deneyleri | OTR kalıcı partition alamaz; yeniden açma/SSO/Unut kanıt ister |
| Trusted Sites / Banking Registry | Yetkili envanter, exact HTTPS host/port, TUF ve ayrı kök/eşik | Yerel/offline; TLS yerine geçmez, kapsam/provenance yayın koşulu |
| Benzer adresler | Chromium/ICU + çok sinyal + ölçülmüş Türkçe kesinti | Salt edit distance yetmez; yanlış pozitif ve MFA testleri zorunlu |
| Bank Security Mode | Otomatik doğrulanmış origin bağlamı; derin müdahaleler tasarım/test kapılı | Eklenti/pano kısıtı auth akışını sessiz bozamaz |
| Content Protection | Resmî dağıtımda zorunlu, ayrı imzalı yerel domain indeksi | Deneme URL/log/profil yok; lisans, düzeltme ve offline kanıtı |
| Upstream | Doğrudan roll; acil 24 saat/rutin 48 saat önerilen hedef | Henüz SLA değil; kapasite/tatbikatla kanıtlanmalı |
| Yayın | OS imzalı GitHub ön sürümü, TUF meta verisi, SBOM/provenance/yeniden üretim | GitHub veya checksum tek başına güven kökü değil |
| Otomatik güncelleme | Windows/macOS Chromium Updater uyarlayıcısı değerlendirmesi; Linux/Pardus imzalı paket yöneticisi | Ayrı yetkilendirme; sessiz rollback/telemetri yok |
| Platformlar | Windows x86_64, macOS ARM64/x86_64, genel Linux x86_64, birinci sınıf Pardus x86_64 | Desteklenen Pardus 23.x/25.x kaynak derleme/test + `.deb`; dört aile geçmeden desktop-ready yok |
| Tasarım | Native/minimal, nötr yüzey, tek mavi aile; Sistem/Açık/Koyu canlı | WCAG2.2AA uygulanabilir hedefler; güvenlik metin+ikon+renk |
| Dil | Kod/anahtar/enum/parametre İngilizce; yorum/not/belge/UI Türkçe | GRIT ve yerelleştirme; upstream/lisans metinleri korunur |
| Eklenti | Mümkün MV3 uyumu, açık host izni, Faz 1 mağaza yok | OTR ve hassas sayfa erişimi gizlilik riski |
| Arama | Kullanıcı seçimi, doğrudan sağlayıcı, öneri kapalı | Yuva proxy'si veya Google hesabı zorunluluğu yok |
| Telemetri | Başlangıçta Yuva telemetrisi ve crash upload yok | Geçmiş/URL/arama/reklam kimliği/profil toplanamaz |
| Lisans | Özgün materyal BSD-3-Clause; inherited kod ve veri lisansları ayrı | Kök lisanslar incelendi; gerçek ithal bağımlılık ayrıca denetlenir |
| Vakitler | Ayrı ve sonraki isteğe bağlı yardımcı; kapalı, elle şehir, yerel hesap önceliği | Din tahmini/kimlik değişimi/ezan/portal yok; sağlayıcı lisansı ve doğruluk kapısı |

## Yayını engelleyen açık konular

Derleme kapasitesi/tam SDK ve korumalı imzalama henüz kurulmadı. Genel tehdit kaynağı, banka/kamu kapsam envanteri, üretim anahtarları, içerik lisans/kalite onayı ve özel açık bildirim kanalı tamamlanmadı. Geçici profil yazıları, seçici kalıcılık, Türk hizmetleri, gerçek platform tema/erişilebilirlik ve yeniden üretim henüz tarayıcıda ölçülmedi.

Yeni zorunlu güvenlik kapsamıyla 0.1 resmî ikili için daha fazla mühendislik/işletim gerekir. Küçük ekiple sürdürülebilirlik yalnız yama sayısı değil kayıt doğrulama/düzeltme ve nöbet kapasitesidir. Kapılar geçmezse kaynak/tasarım projesi olarak kalmak gerekir; eksik güvenlikle yayın yapılmaz. [Temel analizi](FOUNDATION_ANALYSIS.md), [sıralı işler](IMPLEMENTATION_PLAN.md).
