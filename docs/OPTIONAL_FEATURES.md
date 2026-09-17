# İsteğe bağlı küçük yardımcılar: Vakitler

Durum: Faz 0 tasarımı, 18 Eylül 2026. Uygulama yoktur; 0.1 güvenlik/yayın işlerini geciktiremez. Yuva dinî ve siyasi açıdan tarafsızdır. Kullanıcının dini, inancı, dünya görüşü veya pratiği varsayılmaz. Dinî işlev tarayıcının kimliği değildir.

## Açık etkinleştirme ve kapsam

Türkçe ad **Vakitler**, gelecekteki İngilizce çeviri **Prayer Times**; dahili kimlik `prayer_times`. Varsayılan `enabled: false`. Yalnız **Ayarlar → İsteğe Bağlı Özellikler → Vakitler → Etkinleştir** eylemiyle açılır. Ülke, dil, IP, geçmiş, davranış veya Ramazan tarihi bu ayarı değiştiremez. Özellik kapalıyken UI, zamanlayıcı, veri indirmesi ve konum isteği yoktur.

En fazla sonraki vakit, bugünün altı vakti, kalan süre ve etkin özellik içinde Ramazan iftar/imsak bilgisi gösterilir. Dar araç alanında örneğin “Akşam 19:21”; tıklayınca “Bugün” altında İmsak/Güneş/Öğle/İkindi/Akşam/Yatsı listesi. Bu saat yalnız yerleşim örneğidir, hesap değeri değildir. Rutin OS bildirimi ve ses başlangıç kapsamı dışındadır; otomatik ezan/ses hiçbir zaman bu tasarımın parçası değildir.

Kur'an/ayet/hadis, yazı/haber/tavsiye/vaaz, dinî reklam veya profilleme yoktur. Yeni sekmeyi kaplamaz, marka/renkleri değiştirmez, dinî görsel veya istenmeyen içerik getirmez. Bir saat gibi küçük davranır. Güvenlik uyarıları her zaman bu yardımcıdan önce gelir.

## Kurulum ve konum

Kullanıcı ülke ve şehri elle seçer; coğrafi alan seçim olmadan doldurulmaz. Şehir merkezi/ilçe seçimi, lisanslı yerel şehir dizinindeki koordinat ve IANA saat dilimine eşlenir. Büyük şehirlerde merkez ile ilçe farkı açık gösterilir. Varsayılan GPS, IP konumlandırma ve uzak konum saklama yoktur. Kullanıcının seçtiği şehir yerel tercihtir; kimlikle ilişkilendirilmez ve telemetriye gitmez.

Sonradan otomatik konum sunulursa ayrı izin, amaç açıklaması ve mümkün olan kaba konum gerekir. Reddetmek elle seçimi engellemez. Otomatik şehir önerisi özelliği etkinleştirme izni değildir. Kapatınca zamanlayıcı/ağ işi iptal edilir; yardımcıya ait şehir, tercih ve önbellek varsayılan temizlenir. Kullanıcı verisini eşitleyen hizmet kurulmaz.

## Sağlayıcı ve hesaplama araştırması

| Aday | Bulgu | Karar |
| --- | --- | --- |
| Diyanet resmî vakit verisi | Kurumun [açıklaması](https://kurul.diyanet.gov.tr/tr/faaliyetler/2020-2025/ibadet-vakitleri-dini-gun-ve-gecelerin-tespiti/ileri-enlemlerde-namaz-vakitleri) ve [AwqatSalah API belgesi](https://awqatsalah.diyanet.gov.tr/scalar/) mevcut | Türkiye için yetkili kaynak adayı. Bu incelemede yeniden dağıtım, ticari/açık kaynak istemci kullanımı, önbellekleme ve API yetkilendirme koşulları kesinleşmedi. İzin/koşullar alınmadan scrape veya resmî veri dağıtımı yapılmaz. |
| Yerel Adhan hesaplaması | [Kaynak](https://github.com/batoulapps/adhan-js), [MIT lisansı](https://raw.githubusercontent.com/batoulapps/adhan-js/master/LICENSE), [yöntemler](https://raw.githubusercontent.com/batoulapps/adhan-js/master/METHODS.md) | Çevrimdışı aday. `Turkey` yöntemi Diyanet yaklaşımıdır, resmî takvimle özdeş değildir. Diğer bölge yöntemleri ve yüksek enlem davranışı seçilebilir. Sürüm kilidi ve referans test gerekir. |

Öneri: mahremiyet için yerel hesaplama arka ucu; resmî veri ancak uygun kullanım hakkı ve açık kullanıcı sağlayıcı seçimiyle alternatif. Yaklaşık yerel hesap “Diyanet'in resmî saati” diye sunulmaz. Yöntem, ikindi seçeneği, yüksek enlem kuralı ve düzeltme değerleri İngilizce enum/parametrelerle temsil edilir, Türkçe açıklanır. Kullanıcının elle seçtiği bölge için yöntem önerilebilir; din veya mezhep kullanıcı hakkında çıkarılamaz. Parametre seçimi yalnız hesap tercihidir.

Uzak sağlayıcı seçildiğinde şehir/dönem/IP'nin o sağlayıcıya görünebileceği etkinleştirmeden önce açıklanır. Yuva proxy'si veya telemetry servisi yoktur. Hesap/kişiye özgü anahtar zorunlu hizmet ilk sürüme alınmaz; paylaşılan gizli API anahtarı kaynak veya ikiliye gömülemez. Ağsız hesap da kullanıcının bilinçli seçimiyle kullanılabilir. Sağlayıcı sözleşmesi bunu karşılamıyorsa entegrasyon ertelenir.

## Bileşen sözleşmesi

Önerilen `PrayerTimeProvider` yalnız `getCapabilities()` ve `getTimes(request)` arayüzüne sahiptir. İstek: `city_id`, `country_code`, `local_date_range`, `time_zone`, `calculation_method`, `asr_method`, `high_latitude_rule`. Yerel sağlayıcı koordinatı yerel dizinden alır; uzak sağlayıcıya kesin GPS verilmez. Yanıt: `source_id`, `method_version`, `generated_at`, `valid_date_range`, `time_zone`, `daily_times`, `calendar_source`, `quality_status`. Bu bir tasarım sözleşmesidir, mevcut API değildir.

Sonuçlar düz veri olmalıdır; HTML/script çalıştırılmaz. Boyut/süre ve tarih sıralaması denetlenir. Anahtar şehir+yöntem+sürüm+saat dilimi+tarih aralığıyla yerel önbelleklenir. Tarihi geçen veri bugünün saati diye gösterilmez; “Vakit bilgisi güncellenemedi” görünür. Sağlayıcı değişimi örtülü yapılmaz; kullanıcı izinli yerel fallback varsa kaynağı görünürdür.

Yuva'nın dağıttığı şehir/metot/takvim paketleri bileşen güvenlik altyapısıyla imzalanır; lisans/köken ayrı tutulur. TLS dış sağlayıcının bağlantı güvenidir, astronomik doğruluk veya resmî onay garantisi değildir. Node çalışma zamanı tarayıcıya gömülmez; seçilen hesap kütüphanesi build-time sabitlenip sınırlı yardımcı ortamda çalıştırılır, CDN script yüklenmez.

## Tarih, Ramazan ve saat doğruluğu

UTC anları seçilen şehrin IANA saat dilimiyle gösterilir; cihazın saat dilimi varsayılmaz. Gece yarısı, sonraki gün imsak, yaz/kış saati, leap year, uyku/uyanma ve OS saat değişimi yeniden hesaplatır. Sayacı her saniye ekran okuyucuya duyurmak yoktur. Kutup bölgelerinde hesaplanamayan vakit uydurulmaz; seçilmiş yöntemin durumu açıklanır.

Ramazan yalnız özellik zaten etkin ve kullanıcının seçtiği takvim kaynağı tarih için geçerliyse iftarı, sonrasında ertesi gün imsak bilgisini öne çıkarır. Yerel takvim ve astronomik Hicrî tarih farklılaşabilir; kaynak/yöntem açık gösterilir, belirsizlikte Ramazan varsayılmaz. Ramazan başlangıcı özellik veya bildirim açmaz.

## Kabul testleri

Kapalı durumda sıfır yardımcı ağ/konum çağrısı; dil/IP/ülke/Ramazan değişiminde kapalı kalma; elle şehir değişimi ve kapatma temizliği; yöntem/saat dilimi/DST/gece yarısı/yüksek enlem/çevrimdışı sınırları; imzalı veri ve bozuk sağlayıcı yanıtı; farklı lisanslı referans vakitleriyle tolerans raporu gerekir. Kaynak doğruluğu kanıtlanmadan dinî uygulama için kesin saat iddiası yapılamaz.

Türkçe ekran okuyucu, klavye, Sistem/Açık/Koyu ve bütün masaüstü hedeflerinde küçük yerleşim test edilir. Yeni sekme ve marka aynı kalır. Güvenlik çekirdeğinden bağımsız, sonraki sürüm kararıyla ilerler; bu belge çalışan Vakitler özelliği vaat etmez.
