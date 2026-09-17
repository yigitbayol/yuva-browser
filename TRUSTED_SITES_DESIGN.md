# Yuva Doğrulanmış Siteler ve Bankacılık Kaydı

Durum: 18 Eylül 2026 tarihli tasarım. Üretim anahtarı, doğrulanmış üretim kaydı veya çalışan tarayıcı koruması henüz yoktur. Aşağıdaki örnekler ayrılmış test alan adlarıdır.

## Amaç ve değişmez sınırlar

Yuva Trusted Sites, ek bir yerel alan adı kimliği ve oltalama korumasıdır. Sertifika otoritesi değildir. Chromium TLS doğrulaması, kök politikası, sandbox, site isolation, genel kötü amaçlı site/indirme koruması ve izin sınırları değişmez. Kayıt üyeliği hiçbir güvenlik denetimini atlatmaz; Kalkan istisnası veya kalıcı depolama izni vermez.

“✓ Doğrulanmış banka”, “✓ Doğrulanmış kamu sitesi” veya “✓ Doğrulanmış üniversite” yalnızca mevcut üst belge origin'inin güncel, imzalı kayıtla eşleştiğini ve normal TLS denetiminden geçtiğini ifade eder. Kurumun davranışı, içeriği veya ele geçirilmemiş olduğu garanti edilmez. Rozet bulunmaması sitenin kötü olduğu anlamına gelmez. Ayrıntı metni: “Alan adı doğrulanmış kayıtla eşleşiyor. Bağlantı tarayıcının normal TLS denetiminden geçti. Bu, kurum veya içerik için güvenilirlik garantisi değildir.”

Banka ve kamu kapsamı, benzer adres koruması ve sade Türkçe uyarılar resmî dağıtımın temel yayın koşullarıdır. Sonraki sürüme bırakılan isteğe bağlı eklentiler değildir. Aşamalı geliştirme yapılabilir; eksik korumayla resmî önizleme ikilisi yayımlanamaz.

## Kayıt yönetimi ve yetkili kaynaklar

Şema ve test verisi başlangıçta `trusted-sites/` altında planlanır. Üretim verisi, kanıt kayıtları ve yayın işi ayrı, açık `yuva-trusted-sites` deposunda; tarayıcıda yalnızca doğrulayıcı ve açık güven kökleri bulunur. C++ içine kurum listesi yazılmaz. “Yuva Trusted Banking Registry”, aynı protokolün ayrı banka veri kümesi ve inceleme sorumluluğudur; bir sertifika deposu değildir.

| Kapsam | Başlangıç kaynağı | Doğrulama kuralı |
| --- | --- | --- |
| Türkiye'de faaliyet izni bulunan bankalar | [BDDK banka listesi](https://www.bddk.org.tr/Kurulus/Liste/90), [kuruluş kategorileri](https://www.bddk.org.tr/Kurulus), [duyurular](https://www.bddk.org.tr/Duyuru/Liste) | Mevduat, katılım, kalkınma/yatırım ve ilgili diğer banka sınıfları kaynak kimliğiyle ayrılır; faaliyet durumu kontrol edilir. Temsilcilik, ödeme şirketi veya değerleme şirketi banka diye işaretlenmez. |
| Bakanlıklar, kamu kurumları, ulusal dijital hizmetler | [e-Devlet kurumlar dizini](https://www.turkiye.gov.tr/kurumlar) ve kurumun resmî yayınları | Dizinin bütün harf/sayfaları işlenir; dizindeki özel kuruluşlar kamu diye sınıflandırılmaz. e-Devlet ve UYAP giriş/yönlendirme origin'leri ayrıca incelenir. |
| Belediyeler ve üniversiteler | e-Devlet belediye/üniversite dizinleri, [YÖK üniversite dizini](https://www.yok.gov.tr/universiteler/universitelerimiz) | Alt kuruluşlar ve kurum türü ayrılır; `edu.tr` veya `gov.tr` son eki tek başına yeterli değildir. |

BDDK kimlik ve faaliyet kapsamının ana kaynağıdır; birlik ve kurum yayınları alan adı çapraz doğrulamasında ek kanıt olabilir. Kaynaktaki HTTP bağlantı otomatik olarak HTTPS kimlik onayı oluşturmaz. DNS kontrolü, geçerli sertifika, arama motoru sonucu veya banka logosu tek başına kurum sahipliği kanıtı değildir.

Her kayıt için iki bağımsız insan incelemesi gerekir: yetkili kaynaktan kurum kimliği, resmî kurumsal kanaldan tam alan adının işlevi ve sahipliği. Gerekirse önceden doğrulanmış iletişim kanalından kurumla teyit alınır. Ana site, bireysel/kurumsal internet bankacılığı, kimlik doğrulama ve yönlendirme alan adları ayrı envanterlenir. Üçüncü taraf MFA/ödeme origin'i bankaya aitmiş gibi rozet alamaz; sınırlı akış ilişkisi ayrıca kanıtlanır. Gerçek müşteri hesabı, parola veya müşteri trafiği toplanmaz.

### Kapsamın eksiksizliğini kanıtlama

Her yayın `coverage_manifest` taşır: kaynak URL'si, alınma zamanı, ham kaynağın SHA-256 özeti, ayrıştırıcı sürümü, bulunan kurum kimlikleri, incelenen kayıtlar, gerekçeli kapsam dışılar, çözülmemişler ve önceki yayına fark. Kurum sayıları kaynak anlık görüntüsünden hesaplanır, elle uydurulmaz. Her yetkili kurum için `verified`, `pending` veya `no_public_service` inceleme durumu ve kanıt bulunur; sonuncusu bağımsız teyit gerektirir. Tarayıcıya yalnızca onaylı origin'ler gider.

Resmî yayın kapısı: banka kaynağındaki faaliyet gösteren bütün kurumlar mutabık olmalı; kamu/üniversite/belediye dizinlerinin bütün sayfaları işlenmeli; bulunan hizmet alan adlarının incelemesi tamamlanmalı; kritik giriş akışlarında açıklanmamış eksik olmamalı. Eksik kayıtlar sessizce paydadan çıkarılamaz. Bu, tanımlı kaynak envanterine göre kapsamdır; internetteki bütün alan adlarının veya bütün saldırıların keşfedildiği iddia edilmez.

Kaynak farkları günlük, banka/giriş kayıtları en geç 30 günde, diğer kurumlar en geç 90 günde yeniden incelenir; faaliyet iptali, alan adı değişimi ve ele geçirilme bildirimi acil kuyruğa girer. Bunlar önerilen işletim hedefleridir; ekip bu hizmeti sürdüremiyorsa resmî yayın yapılamaz. Ücretli listeleme yoktur. Kanıt deposunda kişisel iletişim verisi veya sır tutulmaz. Düzeltme ve çıkarma gerekçeleri açık denetim kaydında yayımlanır.

## Önerilen veri şeması

Makine anahtarları, enum ve parametreler İngilizcedir; açıklamalar ve kullanıcı metni Türkçedir. Bu JSON bir şema örneğidir, üretim kaydı değildir:

```json
{
  "schema_version": 1,
  "registry_id": "yuva-trusted-sites-tr",
  "registry_version": 42,
  "issued_at": "2026-09-18T00:00:00Z",
  "expires_at": "2026-10-02T00:00:00Z",
  "minimum_reader_version": 1,
  "coverage_manifest_digest": "sha256:EXAMPLE_ONLY",
  "institutions": [{
    "institution_id": "tr-example-bank",
    "name_tr": "Örnek Banka",
    "category": "bank",
    "country": "TR",
    "regulator_reference": "example-authority-record",
    "status": "active",
    "official_domains": ["bank.example"],
    "login_domains": ["login.bank.example"],
    "origins": [
      {"host": "bank.example", "scheme": "https", "port": 443, "match": "exact", "role": "primary"},
      {"host": "login.bank.example", "scheme": "https", "port": 443, "match": "exact", "role": "authentication"}
    ],
    "verified_sources": ["evidence/example-001", "evidence/example-002"],
    "verified_at": "2026-09-18T00:00:00Z",
    "review_due_at": "2026-10-18T00:00:00Z",
    "review_ids": ["review/example-a", "review/example-b"],
    "similarity": {"protected_labels": ["examplebank"], "enabled": true}
  }],
  "revoked_institution_ids": []
}
```

`official_domains` ve `login_domains` kaynak envanteridir; çalışma zamanında ayrı yetki vermez. Derleyici bunların `origins` ile tutarlı olduğunu doğrular. `verified: true` gibi katkıcı tarafından yazılan bayrak güven üretmez. Durum, kategori ve rol kapalı enum'dur. Kayıt sürümü artan tam sayıdır. Domain başına çelişkili kurum sahipliği reddedilir. `revoked_institution_ids` bütün kurumu; origin bazındaki çıkarmalar yeni tam anlık görüntüyü etkiler.

V1 yalnızca tam HTTPS host + port eşleştirir. `www` ve giriş alt alan adları açıkça sıralanır; joker karakter ve otomatik alt alan adı mirası yoktur. GURL/Chromium IDNA davranışıyla uyumlu küçük harf ASCII A-label normalizasyonu, etiket sınırları ve PSL kontrolü gerekir. IP, tek etiket, public suffix, userinfo, yol, kontrol karakteri, bozuk IDNA roundtrip reddedilir. Görünen kurum adı güvenlik anahtarı değildir.

Başlangıç ayrıştırma bütçesi önerisi: sıkıştırılmamış 16 MiB, 100.000 origin, kurum başına 128 origin, metin alanı 256 bayt; gerçek kapsam ölçülerek sürümlenir. Sınırlara takılan büyük kurum sessizce kesilmez; yayın başarısız olur. Yinelenen JSON anahtarları, desteklenmeyen kritik alanlar/sürüm, hatalı tarih, aşırı sıkıştırma ve bellek tüketimi reddedilir. Kanıt dosyaları gezinme sırasında indirilmez.

## İmzalama, güncelleme ve anahtarlar

Yeni kripto protokolü yazmak yerine bakımı süren bir TUF istemcisi seçilir; Chromium entegrasyonu ve lisansı ayrıca incelenir. Tarayıcıda sabitlenmiş kök meta verisi, rol anahtarları ve eşik bulunur. İmzalı target meta verisi payload uzunluğunu/özetini bağlar. HTTPS başarısı yetkilendirme değildir. [TUF belirtimi](https://theupdateframework.github.io/specification/latest/).

Yuva için önerilen politika:

| Rol | Yetki / saklama | Süre hedefi |
| --- | --- | --- |
| Root | Ayrı kişilerde, çevrimdışı donanımla korunan 3 anahtardan 2 imza | 1 yıl; süreden önce rotasyon tatbikatı |
| Targets | Bağımsız 3 anahtardan 2 imza; ikisi de aynı payload özetini onaylar | 30 gün |
| Snapshot | Kısıtlı çevrimiçi imzalayıcı | 7 gün |
| Timestamp | Ayrı kısıtlı çevrimiçi imzalayıcı | 48 saat; günlük yenileme |
| Payload | Artan sürüm, kayıt inceleme son tarihleri | 14 gün |

Algoritma tercihi Ed25519; seçilen kütüphane ve bütün platformlarda vektör testleri geçmeden kesinleştirilmez. Root algoritma politikasını belirler; sunucu düşüremez. Tarayıcı ikilisi, doğrulanmış siteler, içerik listeleri ve takip filtreleri ayrı kök/yetkilere sahiptir. Bir veri imzacısı çalıştırılabilir dosya veya TLS istisnası yayımlayamaz. Çevrimdışı anahtarlar GitHub secrets içinde tutulmaz.

Bütün kullanıcılar ziyaretlerinden bağımsız, zamanlanmış ve rastgele sapmalı aynı tam Türkiye paketini alır. Alan adına göre sorgu, çerez, referrer, kurulum kimliği veya gezinme parametresi yoktur. Dağıtıcı IP ve sabit kaynak indirme zamanını görebilir. Paketin değişmez hash adlı URL'si, imzalı kök/baseline ve minimum sürümler derleme girdisidir.

### Doğrulama ve etkinleştirme

1. Sabitlenmiş kökü, son kabul edilen rol sürümlerini, payload sürümünü ve zaman tabanını yükle. Gezinme verisini temizlemek bu durumu sıfırlamaz. Bozuk durumu eski sürüme sessizce döndürme.
2. Ara kökleri sırayla, eski ve yeni eşikleri doğrulayarak döndür; sayı/boyut bütçesi uygula. Çevrimdışı istemciler için ara kökleri sakla.
3. TUF ile rol, süre, snapshot ilişkileri, target yetkisi, hash ve uzunluğu doğrula. Aynı sürümde farklı içerik, rollback ve mix-and-match reddedilir.
4. Şema, registry kimliği, minimum okuyucu, kayıt son tarihi ve iptalleri doğrula. Bir imza kötü içeriği güvenli parser girdisi yapmaz.
5. Yeni paket ve güven durumunu çökme güvenli atomik işlemle yaz; çalışma zamanında değişmez anlık görüntüye geç. Önceki kopya yalnızca hâlâ uygunluk süresi içindeyse kullanılabilir.
6. Commit, yönlendirme, TLS durumu, paket değişimi, süre dolumu, BFCache ve sekme geri yüklemesinde rozeti yeniden hesapla. Önceki sayfanın rozeti provisional navigation boyunca taşınmaz.

Root eşik kaybından kurtarma bağımsız doğrulanmış tarayıcı güncellemesi veya doğrulanmış elle kurulumla olur; HTTPS'den gelen yeni anahtara kendiliğinden güvenilmez. OS korumalı uygulama durumu tercih edilir; yönetici/kernel ele geçirmesine karşı mutlak koruma yoktur. İlk kurulum geçmişte görülmemiş sürümleri bilemez; gömülü minimum sürüm ve süre replay riskini sınırlar, tamamen yok etmez.

## Çevrimdışı kullanım ve arıza davranışı

Pozitif doğrulama kiralaması, ilgili meta veri/payload/kayıt inceleme sürelerinin en erken bitişidir. Güncel önbellek çevrimdışı bu tarihe kadar geçerlidir. Bozuk veya imzasız yeni aday reddedilir; uygun eski anlık görüntü korunur. Süre dolunca pozitif rozet ve yeni benzerlik kesintileri durur; koruma güncelliği Türkçe açıklanır, normal Chromium TLS ve genel tehdit koruması devam eder. Eski veri sonsuza kadar yeşil rozet üretemez. [TUF güvenlik modeli](https://theupdateframework.io/docs/security/).

Geri alınan saat için kalıcı, azalmayan zaman tabanı ve açılış içi monoton süre kullanılır. Güvenilir süre belirlenemiyorsa rozet gösterilmez; ileri saat hatası da kullanıcıya açıklanır. HTTP Date güvenilir saat kaynağı sayılmaz. Güncellemeyi engelleyen saldırgan hizmeti aksatabilir. Uzun çevrimdışı kalma veya eşik imzacıların ele geçirilmesi kriptografik olarak yok edilemez; sınırlar açık gösterilir. İçerik engellemenin eski liste davranışı [ayrı tasarımda](CONTENT_PROTECTION.md) tanımlıdır.

## TLS, gezinme ve gösterim

Tarayıcı sürecinin mevcut ana çerçeve URL'si kullanılır; sayfa JavaScript'i veya görünen metin kullanılmaz. HTTPS, tam port, güncel kayıt, aktif durum, kabul edilebilir Chromium sayfa güvenlik durumu şarttır. Sertifika hatası/bypass, tehlikeli karma içerik, hata sayfası, `data:`, `file:`, `blob:` ve eklenti/iç sayfalarda pozitif rozet yoktur. Kurumsal yerel köklerle TLS araya girilmediği garantisi verilmez.

Ayrıntılarda tam ASCII host, kurum/kategori, kayıt sürümü ve doğrulama tarihi görülür. Rozet tarayıcıya ait arayüzdedir; fullscreen origin göstergeleri korunur. Saldırgan sayfanın sahte tarayıcı resmi çizebilmesi devam eden bir risktir.

## Benzer adres analizi ve kesinti

Chromium URL ayrıştırması ve IDN gösterim/spoof denetimleri temel alınır. Tam host/registrable domain/alt etiketler ayrılır; `endsWith` veya çıplak substring güven kararı vermez. [Chromium URL gösterimi](https://chromium.googlesource.com/chromium/src/+/main/docs/security/url_display_guidelines/url_display_guidelines.md).

Unicode/ICU sürümü derlemeye sabitlenir. UTS #39 skeleton, karışık yazı sistemleri ve IDNA roundtrip yalnızca sinyaldir; `xn--` veya Türkçe karakter tek başına tehlike demek değildir. [Unicode benzeşen karakterler](https://unicode.org/reports/tr39/).

Yerel aday seçimi ve deterministik sınıflandırıcı şu bağımsız sinyalleri birleştirir:

- Yeterince ayırt edici marka/alan adında confusable skeleton eşitliği; ekleme/silme/değiştirme/transpozisyon mesafesi.
- Türkçe Q/F ve yaygın klavye komşuluğu; rakam-harf ikamesi; kısa marka için yüksek yanlış pozitif riski.
- PSL sınırlarını aşan marka gömme, `bank.example.secure-login.example` benzeri alt alan adı aldatması; login/secure ekleri ve yanıltıcı tireler.
- Gerçek alan adından şüpheli TLD değişimi; tek başına yabancı TLD'yi tehlikeli saymama.
- Gezinme başlatıcısı ve yönlendirme zincirinde doğrulanmış banka → benzer bilinmeyen host geçişi; kanıtlanmış üçüncü taraf kimlik akışıyla ayrım.

Zincir yalnızca sınırlı oturum belleğinde tutulur; URL yolu/sorgusu analitik olarak kaydedilmez. Her HTTP, meta refresh, JavaScript ve form hedefi uygun gezinme kancasında yeniden değerlendirilir; mümkün olan durumda ilk istek ve POST gövdesi gönderilmeden kesilir. Seçilen Chromium sürümünde kapsanmayan kanca varsa yayın engeli olarak kaydedilir. Bilinen kötü site listesi ve indirme denetimi ayrı çalışır; tam doğrulanmış alan adı bu denetimleri geçersiz kılamaz.

Yüksek güven için yalnız mesafe yetmez: örneğin ayırt edici skeleton eşleşmesi + farklı kayıt edilebilir alan adı + aldatıcı giriş/alt alan yapısı. Düşük güven sessiz yerel ayrıntı olabilir, sürekli modal uyarı olamaz. Model uzaktan çalışmaz; registry çalıştırılabilir regex/script taşımaz. İlgisiz adları benzeten kısa etiketler kesinti kapsamına alınmaz.

### Teknik bilgi gerektirmeyen Türkçe arayüz

Yüksek güvenli kesinti: **“DİKKAT — Sahte site olabilir”**, ardından **“Bu adres gerçek site olmayabilir.”** ve “Bu site, doğrulanmış bir banka adresine çok benziyor.” Kamu için kategori metni değişir. Gerçek ve ziyaret edilmeye çalışılan adres ayrı etiketlenir; uzunsa güvenlik açısından anlamlı host gizlenmez.

Tek ve güncel resmî hedef kesin olarak bulunmuşsa “Gitmek istediğiniz resmî site bu mu?” ve açık adres gösterilir. Birincil eylem **“Resmî siteye git”**, diğer güvenli eylem **“Geri dön”** olur. Resmî hedefe sadece kullanıcı eylemiyle temiz HTTPS GET yapılır; saldırgan yol/sorgu/POST/referrer aktarılmaz. Birden fazla belirsiz aday varsa resmî hedef tahmin edilmez, birincil eylem “Geri dön” olur.

“Gelişmiş seçenekler” kanıt, tam host ve hata bildirme sunar. Doğrulanmış kötü site kararı için devam düğmesi yoktur. Sezgisel yüksek güven uyarısında kalıcı tek tık bypass yoktur; yanlış pozitif düzeltme süreci tercih edilir. Deneylerde oturumluk override gerekirse ayrıca güvenlik/UX incelemesi gerekir, resmî ilk sürümün varsayılanı değildir. Uyarı kullanıcılara düşünmeden devam etme alışkanlığı kazandıramaz.

### Ölçüm

Sürüm kontrollü Türkçe/IDN meşru domain kümesi, kurumlardan izinli giriş akışları ve sentetik saldırı korpusu kullanılır. Tespit oranı, yanlış pozitif oranı, precision, kategori/sinyal bazlı dağılım ve gecikme yayımlanır. İlk önerilen kapı: adlandırılmış kritik akışlarda sıfır yanlış kesinti, en az 10.000 incelenmiş meşru host üzerinde %0,1 altında kesinti; güven aralığı ve örnekleme yanlılığı raporlanır. Sonuçlar henüz ölçülmedi. Her veri/Unicode/algoritma değişiminde tekrar test gerekir; düşük oran bile bankacılık akışı testinin yerini tutmaz.

## Bank Security Mode

İç bileşen adı `BankSecurityMode` olur. Güncel kayıttaki banka origin'i için gezinme başında aday bağlam; TLS başarıyla commit olunca etkin bağlam oluşur. Rozet gibi her yönlendirmede yeniden hesaplanır. Banka origin'inden ayrılınca rozet kalkar; sadece kısa ömürlü yönlendirme risk bağlamı kalır. Normal bir sitenin görünümünden banka modu çıkarılmaz.

| Koruma | Tasarım kararı | Uyum/kanıt koşulu |
| --- | --- | --- |
| HTTPS ve karma içerik | Banka hedefinde HTTP fallback yok; sertifika ve aktif karma içerik bypass yok | HTTP giriş adresi güvenli yükseltme; HSTS, form ve alt kaynak testleri |
| Eklenti erişimi | Hassas origin'lerde host erişimi/content script/istek gözlemi için tarayıcı düzeyi ek kapı araştırılır | `activeTab`, MV3 worker, debugger, webRequest/DNR, mevcut script ve iframe yolları birlikte incelenir; yalnız geç enjeksiyonu engellemek yeterli değildir |
| Parola yöneticisi ve erişilebilirlik | Toplu eklenti kapatma veya sessiz izin değişimi yok; gerekli bütünleşmeler açık kapsamlı ve kullanıcıya anlaşılır | Yerleşik parola yöneticisi, onaylı yardımcılar ve MFA ile izinli test; eksik engel için tam yalıtım iddiası yok |
| Pano | Chromium kullanıcı etkinliği/izin kuralları korunur; odaksız yazma kötüye kullanımına yönelik kısıt araştırılır | Pano içeriğini okumaz, loglamaz veya MFA kodlarını sınıflandırmaz |
| İndirme | Genel zararlı dosya koruması + bankadan başlayan beklenmeyen çalıştırılabilir dosyada açık uyarı | PDF/ekstre normal akışı korunur; banka kaydı dosya güvenlik kontrolünü atlatmaz |
| Yönlendirme | Benzer host kesintisi; dış kimlik sağlayıcı için ayrı kanıtlı akış ilişkisi | SSO, 3-D Secure, mobil onay, passkey ve açılır pencere testleri; form gövdesi değişmez |

Bankacılık alan adı/oltalama koruması zorunludur. Henüz kanıtlanmamış derin eklenti/pano müdahaleleri bu zorunluluğun uygulanmış olduğu şeklinde sunulmaz; tasarım ve test kapısı sonrasında eklenir. Kayıt süresi dolduğunda görünür güncellik kaybı vardır; otomatik olarak bütün siteye banka yetkileri verilmez. Hiçbir uyum istisnası TLS, sandbox veya origin isolation'ı gevşetemez.

## Zorunlu testler

İmza/rol/eşik hatası, imzasız HTTPS, bozuk/kesik/aşırı büyük veri, duplicate key, replay, aynı sürümde farklı içerik, süre dolumu, kök zinciri/anahtar iptali, saat sapması, çevrimdışı başlangıç, atomik güncellemede çökme ve eşzamanlı okuma testleri gerekir. IDNA/PSL/port, farklı alt alan, userinfo, IPv6, yönlendirme/BFCache/TLS yarışları fuzz edilir. MFA ve erişilebilirlik testleri Windows, macOS, Linux ve desteklenen Pardus dallarında çalışır. Kaynak kapsam mutabakatı ve iki bağımsız inceleme yayın kanıtının parçasıdır.
