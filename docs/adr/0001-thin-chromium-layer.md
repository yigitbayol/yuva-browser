# ADR 0001 — İnce Yuva katmanı ve sabit Chromium girdisi

Tarih: 18 Eylül 2026. Durum: **kabul edildi — geliştirme hazırlığı**. Dayanak: Faz 0 tasarımından sonra kullanıcının sıradaki geliştirmeye devam talimatı ve açık kaynak/depo stratejisi. Bu karar ürün güvenlik denetimi veya ikili yayın onayı değildir.

## Karar

Yuva doğrudan Chromium Stable kaynak revizyonunu tüketir. Yuva deposu, Chromium'un tam kopyası olmaz. Kaynak ve araçlar dış çalışma alanında; özgün bileşenler, marka, kaynaklar, yapılandırma, sıralı yamalar ve betikler bu depoda bulunur. Gereksiz vendor ağacı veya Chromium submodule'ü eklenmez.

Tam çatal seçeneği daha kolay ilk düzenleme sunabilir, ancak çok büyük Git geçmişi ve güvenlik farkı/birleştirme yükü getirir. İnce katman ayrı bileşen ve az sayıda bütünleştirme noktasıyla upstream alımını kolaylaştırır. Bu nedenle B seçeneği tercih edilir. Kaynak tekrar kurma sorumluluğu ortadan kalkmaz.

Öncelik: desteklenen yapılandırma/politika → Yuva bileşeni → yalıtılmış kanca → küçük yama → yalnız gerekçeli zorunlulukta invaziv değişiklik. TLS/sandbox/origin isolation rahatlık için değiştirilmez. Chromium güvenlik güncellemesi gecikiyorsa özellik yeniden değerlendirilir.

## İlk uygulanan sınır

`config/versions.json` dört açık kimliği (`chromium_version`, `chromium_revision`, `yuva_version`, `patchset_version`), DEPS özetini ve depot_tools revizyonunu tutar. `scope: source_baseline` ve `qualification: unbuilt` tam bağımlılık kilidi veya derleme başarısı iddiasını engeller. İlk teslimde tam kilit yoktu; [ADR 0003](0003-staged-source-bootstrap.md) sonrasında `config/upstream.lock.json` yalnız kök kaynakları bağlar. Çözümlenmiş DEPS/CIPD/GCS/SDK/derleyici/PGO/platform girdileri sonraki iştir.

`patches/series.json` şu anda boştur. Uygulanmış Yuva güvenlik özelliği sayılmaz. Her yama amaç, güvenlik/mahremiyet etkisi, çakışma riski, ilgili özellik/bileşen, test, bağımlılık ve hash taşır. Başarısız yama atılamaz.

## Bilinen zor alanlar

Seçici kalıcılık OTR içinde bir bayrakla çözülemez. BrowserContext/SiteInstance yönlendirmesi ince katmanı aşabilecek bir deneydir; güvenli çözüm kanıtlanmazsa ertelenir. Canvas/WebGL/audio/font ve bankada eklenti sınırları Blink/extension çekirdeğine temas edebilir; ayrı ADR, test ve upstream taşıma maliyeti gerekir. Bu zorluklar bağımsız motor çatalına sessiz geçiş gerekçesi değildir.

## Sonuç

Depo küçük ve Yuva odaklı kalır; kaynak yeniden kurma ve gizli indirme riski açık araçlarla yönetilir. Tam kaynak indirme/derleme bu kararla kendiliğinden başlamaz. [İş akışı](../BUILD.md), [upstream stratejisi](../../UPSTREAM_STRATEGY.md), [depo yapısı](../../REPOSITORY_STRUCTURE.md).
