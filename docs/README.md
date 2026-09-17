# Faz 0 belge dizini

Bu depo henüz çalışan Yuva tarayıcısı içermez. Kararlar incelenmeden büyük Chromium değişikliği yapılmaz. Ana README ürün manifestosudur; teknik kapsam ve yayın kapıları aşağıdadır.

- [Karar özeti](../DECISION_SUMMARY.md), [temel analizi](../FOUNDATION_ANALYSIS.md), [asıl mimari](../ARCHITECTURE.md).
- [Tehdit modeli](../THREAT_MODEL.md), [güvenlik politikası](../SECURITY.md), [özellik fark kaydı](SECURITY_FEATURE_REGISTER.md).
- [Mahremiyet mimarisi](../PRIVACY_ARCHITECTURE.md), [mahremiyet politikası](../PRIVACY.md).
- [Doğrulanmış siteler ve bankacılık](../TRUSTED_SITES_DESIGN.md), [içerik koruması](../CONTENT_PROTECTION.md).
- [Upstream stratejisi](../UPSTREAM_STRATEGY.md), [derleme/yayın güvenliği](../BUILD_RELEASE_SECURITY.md), [derleme planı](BUILD.md).
- [Birinci sınıf Pardus](PARDUS_SUPPORT.md), [Türkiye hizmet uyumluluğu](TURKISH_WEB_COMPATIBILITY.md).
- [Tasarım sistemi](DESIGN_SYSTEM.md), [yerel görsel envanter](DESIGN_COMPONENTS.html), [dil politikası](LANGUAGE_POLICY.md).
- [İsteğe bağlı Vakitler](OPTIONAL_FEATURES.md), [yol haritası](../ROADMAP.md), [48 sıralı görev](../IMPLEMENTATION_PLAN.md), [depo yapısı](../REPOSITORY_STRUCTURE.md).

[Bu aşamanın doğrulama kaydı](PHASE_0_VALIDATION.md) yapılan kontrolleri ve henüz denenmeyen platform davranışlarını ayırır.

Görsel envanter dış bağımlılık istemeyen tek HTML dosyasıdır; yerel tarayıcıda açılabilir. GitHub dosya görünümü HTMLyi uygulama olarak çalıştırmaz. Örneğin depo kökünde `python3 -m http.server 8765 --bind 127.0.0.1` çalıştırıp `http://127.0.0.1:8765/docs/DESIGN_COMPONENTS.html` adresini açın. Bu bir ürün arayüzü uygulaması değildir.
