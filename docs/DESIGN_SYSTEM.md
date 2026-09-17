# Yuva tasarım sistemi

Durum: 18 Eylül 2026, ürün uygulanmadan hazırlanmış tasarım sözleşmesi. [Görsel bileşen envanteri](DESIGN_COMPONENTS.html) yerel, bağımsız bir inceleme belgesidir; Chromium arayüzü veya çalışan güvenlik ürünü değildir.

## Görsel ilke

Yuva sakin, yerel hissettiren ve dünyada tanıdık bir tarayıcıdır. Türkiye'de geliştirilmesi kırmızı/beyaz ulusal renk şeması veya dinî/siyasi görsel kimlik gerektirmez. Tarayıcı chrome'u çoğunlukla nötrdür. Tek marka vurgusu **Yuva mavisi `#2563EB`**; koyu zeminde aynı renk ailesinden erişilebilir varyant kullanılır. Kırmızı tehlike/silme, amber uyarı, yeşil doğrulanmış durum, mavi eylem/seçim içindir.

Aşırı gradient, glassmorphism, büyük kontroller, dekoratif dashboard, yoğun gölge, doygun yüzey, zorunlu animasyon ve görsel gürültü yoktur. Güvenlik uyarısı sadelik uğruna küçültülemez veya silikleştirilemez. Ürün ilk aşamada Chromium yerleşim ve davranışlarını korur; kapsamlı yeniden tasarım yapılmaz.

## Görünüm ve canlı sistem takibi

Ayar değerleri `system`, `light`, `dark`; Türkçe seçenekler **Sistem**, **Açık**, **Koyu**. Varsayılan `system`. Sistem tercihinde işletim sistemi değişimi canlı izlenir; yeniden başlatma gerekmez. Açık/Koyu seçimi OS değişiminde korunur. Tercih yereldir, web sitesi tarafından değiştirilemez.

Ürün uygulamasında Chromium NativeTheme/ColorProvider/ThemeService akışı ve platform bildirimleri incelenerek tek çözülmüş tema durumu kullanılır. Views kontrolleri ve WebUI token'ları aynı kaynaktan beslenir; iki ayrı palet evrilmez. Bağımsız HTML envanteri yalnız bu davranışı `prefers-color-scheme` ile örnekler, gerçek OS entegrasyon testi sayılmaz. Sayfa `prefers-color-scheme` davranışı ayrıca mahremiyet/uyumluluk incelemesi ister; browser chrome teması web içeriğinin zorla ters çevrilmesi değildir.

## Semantik renkler

Ham renkler yalnız token kaynağında bulunur; komponentler semantik token tüketir. Bir token hem metin hem arka plan için gelişi güzel kullanılmaz. Native tarafında karşılık gelen İngilizce renk kimlikleri tanımlanır.

| Token | Açık | Koyu | Amaç |
| --- | --- | --- | --- |
| `--yuva-background` | `#FFFFFF` | `#18181B` | Ana zemin; koyuda saf siyah yok |
| `--yuva-surface` | `#F6F7F9` | `#202023` | Sekme/ayar ikincil yüzeyi |
| `--yuva-surface-elevated` | `#FFFFFF` | `#27272A` | Menü/diyalog yüzeyi |
| `--yuva-text-primary` | `#18181B` | `#FAFAFA` | Temel metin |
| `--yuva-text-secondary` | `#52525B` | `#A1A1AA` | Açıklama; açıkta başlangıç `#71717A` yerine daha geniş kontrast payı |
| `--yuva-border` | `#E4E4E7` | `#3F3F46` | Dekoratif ayırıcı; kontrolün tek sınırı olamaz |
| `--yuva-control-border` | `#71717A` | `#A1A1AA` | Anlamlı kontrol sınırı |
| `--yuva-accent` | `#2563EB` | `#60A5FA` | Link/odak/seçim; koyuda erişilebilir mavi varyant |
| `--yuva-action-background` | `#2563EB` | `#2563EB` | Birincil düğme zemini |
| `--yuva-action-text` | `#FFFFFF` | `#FFFFFF` | Birincil düğme metni |
| `--yuva-success` / `--yuva-security-verified` | `#15803D` | `#22C55E` | İkon + metinle doğrulama |
| `--yuva-warning` / `--yuva-security-warning` | `#B45309` | `#F59E0B` | İkon + metinle dikkat |
| `--yuva-danger` / `--yuva-security-danger` | `#B91C1C` | `#F87171` | İkon + metinle tehlike |

Başlangıç yeşili `#16A34A` ve amber `#D97706` beyaz üstünde küçük metin için 4,5:1 sağlamıyor. Koyu `#3B82F6` ve `#EF4444`, yükseltilmiş `#27272A` üstünde küçük metinde yetersiz. Bu nedenle yukarıdaki varyantlar seçildi. Marka renginin tonunu yüzeylere yaymak yerine küçük eylemlerde kullanırız.

Hesaplanan örnekler (sRGB WCAG yöntemi, yuvarlanmış):

| Metin / zemin | Kontrast |
| --- | --- |
| Açık ikincil `#52525B` / `#F6F7F9` | 7,21:1 |
| Açık vurgu `#2563EB` / `#F6F7F9` | 4,82:1 |
| Açık doğrulama `#15803D` / `#F6F7F9` | 4,68:1 |
| Açık uyarı `#B45309` / `#F6F7F9` | 4,68:1 |
| Koyu ikincil `#A1A1AA` / `#27272A` | 5,81:1 |
| Koyu vurgu `#60A5FA` / `#27272A` | 5,86:1 |
| Koyu tehlike `#F87171` / `#27272A` | 5,38:1 |
| Beyaz / birincil düğme `#2563EB` | 5,17:1 |

Bu tablo bütün UI'nın AA sertifikası değildir. Hover, pressed, seçili, disabled, focus ve OS forced-colors birlikte denetlenir. Opacity uygulanarak metin/ikon kontrastı düşürülmez. Birincil düğmenin odak halkası kendi mavisinden ayrılan yüzey aralığıyla çizilir.

## Tipografi, aralık ve geometri

Sistem fontu kullanılır: Windows yerel UI fontu, macOS sistem fontu, Linux/Pardus sistem sans-serif ve Türkçe glif desteği. Uzak font indirilmez. Ürün kontrol metni yaklaşık 13–14 pt/DIP karşılığı OS ölçeğinde, açıklama 12–13, belge gövdesi 16 CSS px; bunlar OS erişilebilirlik metin ölçeğiyle büyür. Güvenlik uyarısında başlık/hiyerarşi belirgin, host okunur olmalıdır. Monospace yalnız teknik ayrıntı/host gerektiğinde; `İ/ı/Ş/Ğ` ve çift yönlü metin testleri zorunludur.

Aralık token'ları: 4, 8, 12, 16, 24, 32 birim. Kontrol yüksekliği başlangıç 36, kompakt native ikon hedefi en az 32; dokunma bağlamında 44 önerilir. Yarıçap: kontrol 6, panel 8, diyalog 10; hap biçimi her elemana uygulanmaz. 1 birim ayırıcı, OS ölçeğinde net çizgi. Gölge yalnız platformun popup ayrımına gerektiği kadar; belge örneğinde yoktur.

İkonlar aynı optik ağırlıkta Chromium/native vektör ailesinden 16/20/24 ölçeklerinde gelir. Emoji ürün güvenlik ikonu olarak kullanılmaz; platformlar arasında anlam/renk değişebilir. Metin etiketleri gerçek güvenlik durumunu taşır. Sadece ikon düğmesi erişilebilir ad ve klavye tooltip'i içerir.

## Güvenlik durumları ve öncelik

| Durum | Görünen metin / davranış |
| --- | --- |
| Kalkan etkin | Kalkan ikonu + “Koruma açık”; isteğe bağlı oturumluk “12 takip isteği engellendi” |
| Kalkan istisnası | “Bu sitede bazı korumalar kapalı”; hangi özellik olduğu açık |
| Banka/kamu doğrulanmış | Onay ikonu + “Doğrulanmış banka” / “Doğrulanmış kamu sitesi”; yeşil yardımcıdır |
| Kayıt bilinmiyor/eski | Nötr durum veya ayrıntıda “Doğrulama bilgisi güncel değil”; yeşil yok, kötü site iddiası yok |
| Yüksek güvenli benzer adres | “DİKKAT — Sahte site olabilir”, “Bu adres gerçek site olmayabilir.”; temiz resmî hedef/güvenli geri eylemi |
| Genel tehlikeli site | “Bu site tehlikeli olabilir.”; belirgin tarayıcı güvenlik ekranı |
| TLS hatası | Chromium güvenlik ekranı öncelikli; doğrulama rozeti gösterilmez |
| İçerik politikası engeli | “Bu içerik Yuva tarafından engellendi.”; kaynak/sürüm isteğe bağlı ayrıntı; ahlaki dil yok |

“Korunuyorsunuz” tüm tehlikelerin önlendiğini düşündürebileceğinden ilk arayüzde daha sınırlı “Koruma açık” tercih edilir. Sayaçlar kategori ilişkisini açıklar: reklam takipçileri toplam takip isteğinin alt kümesi olabilir; sayılar toplanarak şişirilmez. Sürekli hareketli sayaç ve ekran okuyucu anonsu yoktur.

Öncelik: TLS/zararlı site/oltalama ekranı → içerik engeli → koruma güncelliği/istisna → olumlu rozet → marka/isteğe bağlı yardımcı. Bilinen tehlike durumunda aynı yerde güven veren olumlu rozet sunulmaz. Kalkan panelinde “Site verileri: Yuva kapanınca sil” ve tasarlanmış “Bu siteyi hatırla” eylemi yer alabilir; uygulanmamış eylem üretimde etkin görünmez.

## Erişilebilirlik sözleşmesi

[WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) uygulanabilir bölümlerde hedeflenir: normal metin 4,5:1, büyük metin 3:1, anlamlı ikon/kontrol sınırı 3:1. AA minimum hedef 24×24 CSS px veya standardın aralık/diğer istisnalarıdır; Yuva'nın 32/36/44 önerisi ürün ergonomisidir. [Hedef boyutu](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [metin dışı kontrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

Görünür 3 birim odak halkası, en az 2 birim yüzey aralığı; fokus sticky öğe altında saklanamaz. Tab sırası mantıklıdır; native menü/sekme ok tuşlarını, dialog Escape ve odak geri dönüşünü korur. Tooltip tek açıklama kaynağı değildir. Uyarı metni ekran okuyucuda başlık/rol ile açıklanır; toast güvenlik kararının tek taşıyıcısı olamaz. [Gizlenmeyen odak](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).

Windows Narrator/NVDA, macOS VoiceOver, Linux/Pardus Orca; klavye, OS %100/%125/%150/%200 ölçek, yüksek DPI, metin büyütme ve dar pencere test edilir. Forced-colors sistem renkleri önceliklidir; marka rengi dayatılmaz. `prefers-reduced-motion` ile gereksiz geçiş yoktur; ilk kapsamda dekoratif animasyon zaten yoktur. Renk tek başına güvenlik/uyarı/hata anlamı taşıyamaz.

## Bileşen envanteri

| İngilizce bileşen kimliği | Türkçe kullanım / durumlar | Davranış |
| --- | --- | --- |
| `Button` | Birincil, ikincil, tehlike, devre dışı | Açık eylem; bekleme çift işlemi engeller |
| `Input` | Etiket, yardım, hata | Placeholder etiket yerine geçmez |
| `AddressBar` | URL/arama, güvenlik, odak | Chromium URL gösterim kuralları; hassas host elision yok |
| `Tab` | Seçili, arka plan, yükleme, kapatma | OS alışkanlığı ve klavye korunur |
| `Menu` | Seçili/normal/devre dışı | Native roller, ok tuşları, Escape |
| `Dialog` | Başlık, açıklama, güvenli birincil eylem | Odak kapatılınca başlatana döner |
| `Tooltip` | Kısa ikincil bilgi | Hover ve klavye odağı, Escape ile kapanır |
| `Toast` | Kısa tamamlanma bilgisi | Kritik güvenlik uyarısını saklayamaz |
| `SecurityBadge` | Genel güvenlik durumu | İkon + metin; yalnız renk değil |
| `YuvaKalkan` | Etkin/istisna/güncellik, oturum sayacı | Standart/Sıkı/siteye özel Kapalı; dar panel, gereksiz grafik yok |
| `TrustedSiteBadge` | Banka/kamu/üniversite | TLS + güncel kayıt; ayrıntı ve sınırlama |
| `Warning` | Benzer adres/TLS/genel tehlike/içerik | Güvenli eylem belirgin; devam tuzağı yok |
| `SettingsRow` | Etiket, açıklama, seçim | Klavye, açık bağlı kontrol, yerel tercih |

## Yeni sekme ve isteğe bağlı yardımcı

Yeni sekme: Yuva adı, “Ara veya adres yaz”, “Sık Kullanılanlar”, “+ Ekle”. Haber, reklam, hava durumu, borsa, alışveriş, sponsor bağlantı veya akış yoktur. Favoriler kullanıcının açık eklemesidir; geçici gezinmeden sessiz “en çok ziyaret edilen” çıkarılmaz. Sonraki widget'lar ayrı açık etkinleştirme ister.

[Vakitler](OPTIONAL_FEATURES.md) varsayılan kapalıdır; yalnız açıldıktan sonra küçük saat alanı olabilir. Yeni sekmeyi ele geçirmez, dinî görsel/renk getirmez ve ülke/dilden etkinleşmez. İlk envanterde ürün kontrolü olarak uygulanmaz.

## Platform farkları

- **Windows:** native pencere kontrolleri, Snap/başlık alanı, ölçek ve contrast theme; imza veya güvenlik ekranları marka için gizlenmez.
- **macOS:** standart pencere düğmeleri, başlık alanı, menü çubuğu, Retina, klavye kısayolları ve VoiceOver. Windows penceresini taklit etmez.
- **Linux:** GTK/desktop tema değişimi, portal, font, X11/Wayland ve pencere yöneticisi farkı. Tema bilgisi yoksa belirgin ve belgelenmiş nötr varsayılan; elle Açık/Koyu çalışır.
- **Pardus:** desteklenen her dalda XFCE/GNOME tema değişimi canlı denenir; native `.deb` içindeki font/simge ve masaüstü girişleri test edilir. Genel Linux sonucu Pardus yerine geçmez.

Bütün OS'leri piksel piksel eşitlemek amaç değildir. Ortak token/anlam ve yerel davranış birlikte korunur. Envanter doğrulaması gerçek platform erişilebilirlik testinin yerini tutmaz; bu testler ürün uygulanınca yayın kapısıdır.

Kalkan seviye metinleri: **Standart — Takipçileri engeller.** **Sıkı — Takipçileri ve reklamları engeller.** **Kapalı — Bu sitede takip ve reklam filtreleri kapalı.** Alt açıklama zorunlu güvenlik ve içerik korumasının sürdüğünü belirtir. Site Verileri ayrı kontroldür: Sadece gerekli olanlar / Site beni hatırlayabilir / Özel ayarlar. Hatırlama rıza veya takip izni değildir; çerez amacının otomatik kesin sınıflandırılamadığı açıklanır. [Asıl politika](../PRIVACY_ARCHITECTURE.md).
