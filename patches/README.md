# Yuva yama katmanı

`series.json` şu anda boş bir yama kümesidir. Chromium ürün davranışına henüz müdahale edilmedi. İleride bütünleşme yamaları `chromium/`, mahremiyet yamaları `privacy/` altında tutulacak; uygulanma sırası dosya adından değil manifestodan alınır.

Manifestonun kök alanları `schema_version`, `patchset_version`, `patches` olur. Sürüm `config/versions.json` ile aynı olmalıdır. Her yama aşağıdaki alanları taşır; anahtarlar/kimlikler İngilizce, açıklama metinleri Türkçedir:

| Alan | Anlamı |
| --- | --- |
| `id`, `file`, `sha256` | Benzersiz kimlik, depo içindeki göreli `.patch` yolu ve dosyanın SHA-256 özeti. |
| `purpose`, `feature` | Değişikliğin gerekçesi ve ilgili Yuva özellik kimliği. |
| `security_impact`, `privacy_impact` | Güvenlik ve mahremiyet etkileri; etkisizse gerekçesi. |
| `upstream_conflict_risk` | `low`, `medium` veya `high`; bakım maliyeti incelemesinin sonucu. |
| `tests`, `components` | Gerekli test kimlikleri ve etkilenen Yuva bileşenleri. Boş olamaz. Testler bu kayıt nedeniyle otomatik çalışmış sayılmaz. |
| `depends_on` | Önce uygulanması gereken, manifestoda daha önce bulunan yama kimlikleri. |
| `owner`, `backup_owner` | İnceleme ve upstream uyarlama sorumlularının depo kullanıcı/ekip kimlikleri. |
| `upstream_revision` | Yamanın incelendiği tam Chromium commit kimliği. |
| `license`, `source` | Lisans ifadesi ve köken kaydı; üçüncü taraf bildirimleri korunur. `source` belge niteliğindedir, araç bunu çalıştırmaz veya indirmez. |
| `removal_condition` | Yamanın ne zaman kaldırılabileceği; örneğin upstream çözümün alınması. |

Dosya özeti veya zorunlu alanı hatalı kayıt reddedilir. Yinelenen kimlik, bağımlılık sırası hatası, sembolik bağlantı ve depo dışına kaçan yol kabul edilmez. `.gitattributes` yama dosyalarında LF satır sonunu korur.

`scripts/check-upstream --source-dir <external-source> --target-revision <full-commit>` yalnız yerelde mevcut hedefi sınar. Geçici Git indeksi ve nesne deposunda sıralı uygulama yapılır; ilk çakışmada durulur ve sonraki yamalar denenmemiş olarak raporlanır. Gerçek çalışma ağacı, indeks ve nesne deposu değiştirilmez. Otomatik fetch, fuzzy kurtarma, başarısız yama atlama yoktur.

Bu komut yalnız Git düzeyinde uygulanabilirliği ölçer. Sonucun derlenmesi, güvenlik davranışı ve Chromium alt bağımlılıklarına yapılacak değişiklikler ayrı doğrulama gerektirir. Sahiplik/lisans metninin doğruluğu insan incelemesi ister; JSON doğrulayıcı bu incelemenin yerine geçmez. [Upstream stratejisi](../UPSTREAM_STRATEGY.md) ve [derleme akışı](../docs/BUILD.md).
