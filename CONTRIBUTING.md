# Katkıda bulunma

Yuva Faz 1 geliştirme hazırlığındadır. [İnce depo kararı](docs/adr/0001-thin-chromium-layer.md) kabul edildi; kaynak ve ortam denetim araçları geliştiriliyor. Önce [karar özetini](DECISION_SUMMARY.md) ve bağlantılı tasarımları inceleyin. Büyük Chromium değişiklikleri ilgili mimari incelemesinden sonra başlar. Sıralı işler ve gerçekleşen kapsam [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) içindedir.

[Zorunlu dil politikası](docs/LANGUAGE_POLICY.md): kod, tanımlayıcılar ve parametreler İngilizce; kod yorumları, geliştirici notları, teknik belgeler ve katkı açıklamaları Türkçe; kullanıcı arayüzü Türkçe. Bu kural bir tercih değil, kabul koşuludur.

Değişiklikleri küçük tutun; çözülen somut sorunu ve güvenlik/bakım etkisini açıklayın. Mevcut upstream mekanizmalarını tercih edin. Mahremiyet özellikleri uyumluluk sınırlarını ve veri akışını belgelemelidir; anonimlik veya takip edilemezlik iddiasında bulunmayın.

Her anlamlı geliştirmede README'nin ilerleme bölümünü ve ilgili görev durumunu güncelleyin. Tasarım, prototip, araç testi ve gerçek platformda doğrulanmış tarayıcı özelliğini ayrı belirtin; hedeflenen davranışı tamamlandı saymayın.

Python 3.11+ ile `python3 -m unittest discover -s tests/tooling -v`, `python3 scripts/check-upstream` ve `python3 scripts/check-lock` çalıştırın. Kaynak/yama kaydı değişirse kök kilidini aynı incelemede güncelleyin; testler kırıldı diye özetleri körlemesine yenilemeyin. Commit öncesi dosyaları açıkça seçerek indekse alın; `python3 scripts/check-repository` ve `git diff --cached --check` ile staged içeriği denetleyin. Chromium, depot_tools, bağımlılık indirmeleri, önbellekler ve ikili çıktılar depoya alınamaz. [Derleme belgesi](docs/BUILD.md) araçların sınırlarını açıklar.

Kod katkılarında bileşen/yama sahibi, upstream revizyonu, bağımlılıklar, lisans kökeni, testler ve tamamlanma ölçütü belirtilir. Yetki sınırı değişiklikleri iki kişi tarafından incelenir. Gerektiğinde tehdit modeli ve güvenlik özellik kaydı güncellenir. Chromium korumalarını kapatarak gerileme gizlenmez.

Sentetik hesap ve belgeler kullanın. Gerçek profiller, gezinme URL'leri, sırlar, imzalama anahtarları, kimlik numaraları veya özel hizmet parolaları depoya konulmaz. Hassas açık bildirimleri için [SECURITY.md](SECURITY.md) izlenir.

Özgün katkılar, dosyada aksi yazmıyorsa depo lisansına tabidir. İçe alınan bildirim ve lisanslar korunur; GPL/MPL yamaları incelemeden yalnız BSD etiketli dosyalara taşınmaz. Henüz CLA veya DCO zorunluluğu yapılandırılmamıştır; böyle bir şart getirilmeden önce belgelenmelidir.

Yeni varsayılanlar, izinler, ağ uçları ve kalıcı veriler açıklanmalıdır. Sade tarayıcı kapsamı dışındaki özellikler için yeni mimari karar gerekir.

Tasarım değişiklikleri [tasarım sistemi](docs/DESIGN_SYSTEM.md), güvenlik değişiklikleri [tehdit modeli](THREAT_MODEL.md) ve özellik kaydıyla değerlendirilir. Pardus ayrı yayın hedefidir. Banka/kamu koruması ve içerik politikası resmî dağıtımın zorunlu koşuludur. Standart takip karşıtıdır; kendi reklamımız veya ücretli allowlist yoktur. Vakitler gibi yardımcılar açık kullanıcı etkinleştirmesi dışında çalışamaz. Mimari incelemesi tamamlanmadan büyük Chromium uygulamasına başlanmaz.
