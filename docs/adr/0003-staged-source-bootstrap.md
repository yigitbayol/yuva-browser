# ADR 0003 — Kaynak kökleri ve tam bağımlılık hazırlığını ayırma

Tarih: 18 Eylül 2026. Durum: kabul edildi — geliştirici kaynak hazırlama kapsamı. Dayanak: sonraki geliştirmeye devam talimatı; kaynak ve bağımlılıkların aynı şey olmadığına ilişkin sabit upstream incelemesi.

## Karar

`config/upstream.lock.json` ilk aşamada açıkça `source_roots` kapsamındadır. Şema sürümü 1, kaynak/yama özetlerini ve iki Git kökünü bağlar; bütün çözülmemiş aşamaları taşır. Eksik verilerle tamamlanmış bağımlılık grafiği uydurulmaz. Şema doğrulaması derleme yeterliliği değildir.

`bootstrap --fetch-roots`, yeterli host üzerinde açıkça istendiğinde yalnız sabit Chromium/depot_tools köklerini getirir. Varsayılan ve `--plan` indirmez. Git dışında indirilen araç/hook çalıştırılmaz; alt bağımlılıklar otomatik getirilmez. Asıl Chromium deposu Yuva Git geçmişine girmez.

ADR 0002'nin büyük otomatik bootstrap kapısı tam bağımlılık/hook yürütmesi için sürer. Bu karar, çözümleyicinin inceleyebileceği sabit kökleri elde etmeyi ayrı ve dar bir işlem olarak tanımlar. Disk/SDK kapısını atlatan seçenek eklenmez. Gerçek indirme bu geliştirme oturumunda başlatılmaz.

## Sonuçlar ve sınırlar

İlk getirme, kesinti ve yeniden çağrı sentetik yerel Git depolarında sınanabilir; Chromium indirmeden güvenlik hataları yakalanır. Başarısız dizinler otomatik silinmez. Tamamlanmış, temiz ve aynı kilide ait kaynaklar yeniden doğrulanır; farklı/kirli veri korunarak işlem reddedilir.

Tam grafiği çözmek için ayrı upstream gclient uyarlayıcısı gerekecek. `flatten --pin-all-deps` tek başına bütün platform/SDK/hook girdilerini sabitlemez. Kendi DEPS yorumlayıcımızı yazmak upstream bakımını zorlaştıracağı için tercih edilmedi. Ayrıntılı sözleşme ve sonraki kanıtlar [bağımlılık kilidi belgesindedir](../DEPENDENCY_LOCK.md).
