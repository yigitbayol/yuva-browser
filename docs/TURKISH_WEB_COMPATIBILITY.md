# Türkiye web hizmetleri uyumluluk planı

Araştırma: 17–18 Eylül 2026. Bu belge test planıdır; Yuva uyumluluğu henüz doğrulanmadı. Gerçek hesap, kimlik numarası, banka parolası, özel belge veya imza işlemi kullanılmadı.

## Güncel kaynak bulguları

e-Devlet e-imza girişi ayrı masaüstü uygulamasına işlem kodu girilmesini anlatır. Mobil imza telefon/operatör akışıdır. Bu bulgular tarayıcıya imza middleware'i gömmeyi gerektirmez. [E-imza](https://giris.turkiye.gov.tr/Giris/Elektronik-Imza), [mobil imza](https://giris.turkiye.gov.tr/Giris/Mobil-Imza).

UYAP'ın 11 Haziran 2026 duyurusu eski UYAP e-İmza/ArkSigner girişinin 1 Haziran'da bittiğini ve e-Devlet veya Adalet e-İmza kullanılacağını belirtir. Adalet e-İmza'nın kullanıma sunulma duyurusu 13 Mayıs tarihini verir. Eski Java/eklenti kılavuzu güncel mimari kabul edilemez; sağlayıcının tarayıcı desteği iddiası Yuva testi değildir. [Geçiş duyurusu](https://www.uyap.gov.tr/uyap-dokuman-editoru-guncellendi), [Adalet e-İmza](https://www.uyap.gov.tr/Adalet%20E-%C4%B0mza%20Uygulamas%C4%B1%20Kullan%C4%B1ma%20Sunuldu).

UYAP Windows, macOS mimarileri ve Pardus/Debian dahil editör paketleri yayımlar. UDF düzenleme/imzalama harici iş akışıdır; PDF görüntülemek UDF desteği sayılmaz. [UYAP Editör](https://uyap.gov.tr/UYAP-Editor).

KamuSM işletim sistemi, kart ve okuyucuya göre sürücü/AKİS kurulumu yönlendirir. MA3/özel middleware dağıtım hakları ayrıca incelenir, izin olmadan paketlenmez. [Kurulum rehberi](https://kamusm.bilgem.tubitak.gov.tr/islemler/sertifikami_aldim_ne_yapmaliyim/), [sık sorulanlar](https://kamusm.bilgem.tubitak.gov.tr/SSS/).

BTK elektronik sertifika hizmet sağlayıcısı olmak, Yuva'ya TLS kökü eklemek için gerekçe değildir. Belge imzası, istemci sertifikası ve HTTPS sunucu güveni farklı amaçlardır. [BTK dizini](https://www.btk.gov.tr/elektronik-sertifika-hizmet-saglayicilari), [Chromium kök politikası](https://www.chromium.org/Home/chromium-security/root-ca-policy/).

## Kabul matrisi

Önce sentetik fixture, sonra kurum izinli hesap/donanım ve testçi açık rızası. Her sonuç tarayıcı/OS/middleware sürümü, tarih, akış ve sınırlamayı içerir. Bütün satırlar şu anda **Yuva'da denenmedi** durumundadır.

| Akış | Denenecek bağımlılık/durum | Güvenlik sınırı |
| --- | --- | --- |
| e-Devlet parola ve devredilmiş giriş | SameSite, yönlendirme, CSP, süre sonu, geri/ileri, üçüncü taraf engeli | `gov.tr` genel kalıcılık/izin istisnası yok |
| e-Devlet e-imza | Uygulamaya geçiş, işlem kodu, iptal/zaman aşımı | PIN/özel anahtar tarayıcıda toplanmaz, indirme otomatik çalışmaz |
| Mobil imza | Operatör, popup, long polling, kesinti/dönüş | OTP veya telefon kimliği kaydı yok |
| Adalet e-İmza / UYAP | Güncel yardımcı protokolü, popup, loopback | Eski eklentinin hâlâ gerekli olduğu varsayılmaz |
| KamuSM akıllı kart | OS sürücüsü, kart, istemci sertifikası seçimi | Anahtar işlemi destekli middleware'de; eski plugin geri getirilmez |
| Banka / ödeme | Passkey/WebAuthn, OTP, mobil onay, 3-D Secure, iframe, yönlendirme | Banka modu form/MFA'yı sessiz değiştiremez, TLS hatasını aşamaz |
| PDF | PDFium sandbox, form, yazdırma/kayıt, Türkçe glif | Görüntüleme gömülü imzanın doğrulandığı anlamına gelmez |
| QR / belge doğrulama | Hedef adres gösterimi, normal güvenlik denetimi | QR de oltalama olabilir; belge/QR Yuva'ya gönderilmez |
| UDF | İndirme ve açık harici editör başlatma | PDF diye sunulmaz veya otomatik yürütülmez |

Windows, iki macOS mimarisi, genel Linux ve **Pardus 23.x/25.x** ayrı sonuç ister. Pardus XFCE/GNOME, anahtarlık, kart sürücüsü, PDF/yazıcı ve yardımcı uygulama nitelendirilir. Web sayfasının açılması kart sürücüsünün o platformda çalıştığını kanıtlamaz.

## Yerel uygulama sınırı

Belgelenmiş harici uygulama ve Chromium Native Messaging tercih edilir. Native host manifest'i origin/eklenti kapsamı taşır; Yuva'nın uygulama kimliği sağlayıcı kaydını gerektirebilir. Chrome kayıtlarının hepsi sessizce devralınmaz. [Native Messaging](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging).

Gelecekte köprü: exact origin/extension ID, imzalı bağımsız kurulum, kimliği doğrulanmış mesaj, replay dirençli challenge, boyut sınırı ve kullanıcının onayladığı işlem. Loopback için Origin, CSRF, DNS rebinding, CORS, port probing, mixed content ve yerel ağ izinleri incelenir. Localhost'ta çalışmak güvenilir imzacı olmak değildir. Hatalı yerel sertifika için küresel bypass veya web security kapatma yoktur.

Harici protokol ekranı uygulama ve başlatan origin'i gösterir. Kamu/banka rozeti uygulama başlatmayı otomatik onaylayamaz. TLS, sandbox veya origin isolation bozulmadan çözülemeyen eski akış desteklenmiyor diye belgelenir.

Kalkan istisnası exact-site/özellik/süre ve gerekçeyle sınırlıdır; telemetriyle öğrenilmez. İçerik engeli ve genel tehdit kararı Kalkan istisnasından etkilenmez. Banka/Kamu kayıt kapsamı ve yanlış pozitif akış testi [Trusted Sites tasarımına](../TRUSTED_SITES_DESIGN.md) bağlanır. Yeni middleware sürümünde ilgili test yeniden çalışır.
