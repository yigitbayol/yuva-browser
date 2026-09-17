# Derleme planı

Durum: Faz 0. Henüz Yuva derleme betiği veya Chromium kilit dosyası yoktur. Bu belge çalıştırılabilir bir Yuva derleme tarifi değildir.

## Ortamın hazırlığı

İncelenen Mac ARM64, 8 GiB RAM ve tam Xcode yerine seçili Command Line Tools içeriyor. İlk incelemede yaklaşık 22 GiB boş alan vardı; istenen Docker/önbellek temizliği sonrasında yaklaşık 55 GiB oldu. Bu alan planlanan Chromium çalışma alanı için yeterlilik kanıtı değildir. Yuva için paket/araç zinciri kurulmadı, Chromium indirilmedi ve tarayıcı derlenmedi.

Gereksinimler seçilen tam revizyondaki Chromium belgelerinden okunmalıdır: [Windows](https://github.com/chromium/chromium/blob/main/docs/windows_build_instructions.md), [macOS](https://chromium.googlesource.com/chromium/src/+/main/docs/mac_build_instructions.md), [Linux](https://github.com/chromium/chromium/blob/main/docs/linux/build_instructions.md).

| Hedef | Yerel derleme planı | Yeterlilik |
| --- | --- | --- |
| Pardus 23.x / 25.x x86_64 | Ayrı kilitli Pardus derlemeleri ve yerel `.deb` | Her destek kolunda XFCE/GNOME ve gerçek çekirdek testleri |
| Linux x86_64 | Desteklenen Linux imajı, sabit sysroot/derleyici, GN/Ninja | Referans; dağıtılan paket/OS üzerinde sandbox doğrulaması |
| Windows x86_64 | Desteklenen Windows, revizyonun gerektirdiği Visual Studio SDK ve clang-cl | İmzalama, kurulum/güncelleme ve süreç izinleri |
| macOS ARM64 | Apple Silicon, sabit tam Xcode/SDK | İmzalama/noter onayı, entitlements ve yerel yardımcı testleri |
| macOS x86_64 | Nitelendirilmiş hedef araç zinciri; gerçek Intel test ortamı | Ayrı mimari kanıtı; birleşik paket daha sonra değerlendirilebilir |

Başlangıç kapasite tahmini: derleyici başına 64 GiB RAM ve 500 GB–1 TB SSD; ölçümle güncellenmelidir. Bir komutun bulunması araç zincirinin yeterli olduğunu göstermez. Eski Chromium belgelerine dayanarak eski OS desteği sözü verilmez.

## Planlanan geliştirici akışı

1. Küresel güvenlik ayarlarını değiştirmeden önkoşulları ve kapasiteyi kontrol et.
2. İncelenmiş kilit dosyasından tam Chromium/depot_tools/DEPS/CIPD girdilerini getir ve doğrula.
3. Kaynağı depo dışında oluştur; sıralı yamaları kesin bağlam denetimiyle uygula ve ağaç özetini doğrula.
4. İncelenmiş dosyalardan GN yapılandırması üret; geliştirici ve yayın derlemelerini ayır.
5. Sabit yerel araç zinciriyle derle; ilgili tarayıcı/güvenlik/mahremiyet testlerini çalıştır.
6. Yerel paket oluştur; herkese açık dağıtımda ayrıca imzalama, üretim kanıtı ve bağımsız yayın yetkilendirmesi uygula.

Başlatma betiği indirme boyutunu açıklamalı; yetersiz disk, eksik SDK, kirli yama durumu veya desteklenmeyen yapılandırmada durmalıdır. “latest” bağımlılığı, doğrulanmamış betik çalıştırma, gizli altyapı gereksinimi ve sandbox kapatma yoktur. Upstream hook çalıştırmaları ve indirilen ikili araçlar açıkça belgelenir.

0.1 öncesinde her OS için gerçek komutlar/sürümler, süreler, kaynak erişilebilirliği ve iki temiz derleme karşılaştırması kaydedilir. Hedef Yuva hesabı gerektirmeyen kaynak derlemesidir; Chromium'un küçük veya hızlı derleneceği sözü değildir. Komut ve parametreler İngilizce, açıklamalar Türkçe olmalıdır.

## Pardus yayın kapısı

[Pardus desteği](PARDUS_SUPPORT.md) birinci sınıf zorunluluktur. Windows, macOS, genel Linux ve bütün desteklenen Pardus kolları geçmeden masaüstüne hazır yayın yoktur. Yerel `.deb` zorunludur; genel Linux başarısı Pardus başarısı sayılmaz.
