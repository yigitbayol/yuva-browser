# Mahremiyet mimarisi ve Yuva Kalkan

Durum: Faz 0 tasarımı, 18 Eylül 2026. Aşağıdaki davranışlar uygulanmış güvence değil, doğrulanması gereken hedeflerdir.

## Ürün sözleşmesi

Bütün normal pencerelerde mahremiyet varsayılandır; ayrı kullanıcı “gizli modu” yoktur. Geçicilik, tarayıcının yönettiği web durumunun oturumlar arasında bilerek saklanmamasıdır. Anonimlik, güvenli fiziksel silme, RAM/swap izi bırakmama veya siteye gönderilen veriyi geri alma değildir. İndirme, yer imi, açıkça kaydedilen parola ve ayar farklı yaşam döngüsündedir.

0.1'de oturum boyunca ortak geçici bağlam önerilir. Sekme kapatmak oturumu bitirmez. Son gezinme penceresinin kapanması ve worker'lar dahil bağlamın sonlandırılması oturumu bitirir. Arka plan uygulamaları sessizce ömrü uzatamaz. macOS'ta boş uygulama süreci kalabilir; web bağlamı yine yok edilmelidir. Yeni pencere yeni bağlam açar. Çökme sonrasında kalıcı profile geri yükleme olmaz.

## Takip karşıtı ürün politikası

**Yuva reklamları değil, sizi takip eden sistemi engeller.**

**Yuva internetin gelir modeline karar vermez. Kullanıcının takip edilip edilmeyeceğine kullanıcı karar verir.**

Varsayılan: **Takip kapalı. Takip yapmayan reklam izinli. Takip eden reklam engelli.** Bu bir ürün politikasıdır; bütün takip yöntemlerinin teknik olarak durdurulduğu iddiası değildir. Yuva kendi reklamını yerleştirmez, ücretli reklam allowlist'i/“kabul edilebilir reklam” anlaşması yapmaz, kullanıcı profili satmaz. Teknik uyum istisnası para karşılığı verilemez; açık gerekçe ve süre taşır.

| Davranış | Standart varsayılanı | Uygulama sınırı |
| --- | --- | --- |
| Üçüncü taraf takip çerezi / siteler arası takip / takip script'i | Engelle | Upstream çerez/partition sınırı ve yerel takip listesi |
| Parmak izi | Engelle veya azalt | Bilinen takip script'lerini engelle; motor yüzeylerinde ölçülmüş azaltım, kapsamlı başarı iddiası yok |
| `fbclid`, `gclid`, `utm_*` | Bilinen gezinme bağlamında temizle | İmzalı URL, auth/ödeme, POST ve anlamlı uygulama parametrelerinde dar istisna |
| Popup / pop-under reklam, otomatik reklam yönlendirmesi | Engelle | Chromium kullanıcı etkinliği/popup/abusive-navigation mekanizması; meşru kullanıcı eylemiyle pencereyi topluca yasaklama yok |
| Zararlı/oltalama reklamı | Engelle | Genel tehdit ve hassas alan adı koruması; Kalkan Off bunu kapatmaz |
| Sahte indirme düğmesi | Bilinen aldatıcı kaynak/akışları engelle | Bütün DOM düğmelerinin niyetini kusursuz anlama iddiası yok; yerel liste ve download güvenliği |
| Kripto madenciliği script'i | Engelle | İncelenmiş yerel kaynak/kurallar; bütün WebAssembly'yi kapatma yok |
| Birinci taraf çerez | İşlev için oturumluk izin verilebilir | Otomatik “gerekli” sınıflandırması yok; kalıcılık ayrı açık seçim |
| Takip yapmayan normal/bağlamsal reklam | Genel reklam kuralıyla engelleme | Üçüncü taraf çerez yasağı reklama istisna açmaz; içerik ve genel güvenlik politikası yine geçerli |

### Kalkan seviyeleri

Makine değerleri `standard`, `strict`, `off`; UI **Standart**, **Sıkı**, **Kapalı**.

- **Standart:** “Takipçileri engeller.” Varsayılan; genel reklam/kozmetik gizleme listesi yüklenmez.
- **Sıkı:** “Takipçileri ve reklamları engeller.” Kullanıcı seçimiyle genel reklam ağ kuralları ve sonradan incelenmiş kozmetik filtre eklenebilir; her reklamı yakalama garantisi yoktur.
- **Kapalı:** “Bu sitede takip ve reklam filtreleri kapalı.” Siteye özgü, varsayılan oturumluk uyum seçimi; geçici depolamayı, üçüncü taraf çerez varsayılanını, partitioning'i, GPC/DNT tercihini, TLS/sandbox'ı, banka/kamu/zararlı site ve Content Protection engelini kapatmaz. Çerez istisnası varsa ayrı açık kontroldür.

“Bu site için koruma uygulanmaz” gibi bütün güvenliğin kapandığını düşündüren metin kullanılmaz. Etkin seviye ile global varsayılan ayrı gösterilir. Bir banka sayfasında Kalkan kapatılsa bile oltalama/indirme/TLS denetimi sürer. İstisnalar yerelde, dar kapsam ve sıfırlama eylemiyle yönetilir.

### GPC, DNT ve rıza

GPC varsayılan açık: HTTP `Sec-GPC: 1` ile `navigator.globalPrivacyControl`/WorkerNavigator tutarlı olmalıdır. Güncel taslakta tercih üst gezinme başında sabitlenir; ayar değişince yeniden yükleme önerilir. Kapalı durumda başlık gönderilmez. GPC satış/paylaşım ve bağlamlar arası hedefleme tercihi sinyalidir; bütün veri işlemeyi, reklamı veya çerezi otomatik durdurmaz. Türkiye'de her siteye aynı hukuki yükümlülüğü getirdiği iddia edilmez. [GPC teknik belirtimi](https://w3c.github.io/gpc/).

DNT için hedef `DNT: 1` ve uyumlu `navigator.doNotTrack` değeridir. DNT belgesi kullanıcı tercihini gerektirir; özel mahremiyet tarayıcısını bilinçli seçme istisnasını da tanımlar. Yuva'nın dağıtım/ilk açılış açıklaması bu tercihi açıkça bildirmeli, kullanıcı kapatabilmelidir; genel amaçlı tarayıcıda gizlice kullanıcı tercihi uydurulamaz. Kurulumda açık bilgilendirme sağlanamayan yönetilen senaryoda önce kullanıcı seçimi alınır. DNT teknik engel değildir; sitelerin uyduğu veya evrensel hukuki zorunluluk olduğu iddia edilmez. Kapanınca `DNT: 0` ile izlemeye rıza üretmek yerine başlık kaldırılır. [DNT tercih kuralları](https://www.w3.org/TR/tracking-dnt/#determining).

GPC/DNT evrensel tercih sinyalleridir, domain bazlı rıza defteri veya reklam anlaşması değildir. Ek sinyallerin parmak izi maliyeti test edilir; sinyal yokluğu siteye olumlu rıza anlamına gelmez.

Site verisi paneli: **Sadece gerekli olanlar** / **Site beni hatırlayabilir** / **Özel ayarlar**. İlk etiket “Üçüncü taraf takibi engellenir; oturum verisi geçicidir. Her çerezin amacını tarayıcı belirleyemez.” açıklamasını taşır. Hatırlama takibe veya pazarlama rızasına izin değildir; sadece depolama ömrünü değiştirir.

CMP bütünleşmesi başlangıçta araştırma işidir. Belgelenmiş ret tercihi/API'si ve test edilmiş görünür “gerekli olmayanları reddet” eylemi kullanılabilir. Kullanıcı adına kabul işaretleme, sahte TCF/consent string üretme, çerez banner'ını tercihi kaydetmeden gizleme veya ret başarılıymış gibi gösterme yoktur. Bilinmeyen CMP görünür kalır. Geri alınabilir yerel ret tercihi, sağlayıcı sürüm testleri ve uygulama öncesi güncel hukuki inceleme gerekir; bütün ülkelerde rızanın aynı olduğu varsayılmaz. Genel scriptlet motoru sırf banner gizlemek için çekirdeğe alınmaz.

## Chromium bulguları

`StoragePartitionConfig`, bellek/disk bölümünü ayırır ve off-the-record bağlamında belleği zorunlu kılar. Bu yüzden OTR içinde `in_memory=false` seçmek “Bu siteyi hatırla” uygulaması değildir. [Kaynak](https://raw.githubusercontent.com/chromium/chromium/main/content/public/browser/storage_partition_config.h).

`BrowserContext` bölümü SiteInstance/yapılandırma üzerinden seçer; URL temelli erişim eskimiştir ve yaşam döngüsüne uygun kapatma gerekir. [BrowserContext](https://raw.githubusercontent.com/chromium/chromium/main/content/public/browser/browser_context.h). `GetStoragePartitionConfigForSite` kancası vardır; bunun doğrudan üst-seviye-site konteyneri API'si olduğu varsayılamaz. [ContentBrowserClient](https://raw.githubusercontent.com/chromium/chromium/main/content/public/browser/content_browser_client.h).

OTR profil incognito tercih hizmeti kullanırken ana profil yolunu döndürebilir. Ayrı ve tamamen boş dosya sistemi ad alanı değildir; keyed service ve yazmalar tek tek incelenir. [OffTheRecordProfileImpl](https://raw.githubusercontent.com/chromium/chromium/main/chrome/browser/profiles/off_the_record_profile_impl.cc).

Üç kavram ayrılır: `BrowserContext/Profile` hizmet/izin sahibi; `StoragePartition` çerez/ağ/depolama grubu ve bellek seçimi; `StorageKey`/ağ yalıtım anahtarları ise origin ve bağlama göre web verisini böler. Site isolation da bunlardan ayrı süreç güvenliği mekanizmasıdır. Chromium'un üçüncü taraf depolama bölümlendirmesi veriyi kendiliğinden geçici yapmaz. [Depolama bölümlendirmesi](https://privacysandbox.google.com/cookies/storage-partitioning).

## 0.1 geçici oturum

Başlatıcıya yalnız Incognito bayrağı eklemek yerine, mevcut OTR mekanizmasını dar profil/açılış bütünleşmesiyle kullan. Tüm giriş yollarını denetle. Kalıcı ana profil yalnız izinli kontrol durumunu tutar; normal içerik açmaz. OTR kalıcılık değişmezini hatırlama için kaldırma.

| Veri | Hedef ömür | Sınır / doğrulama |
| --- | --- | --- |
| Çerezler, sunucunun uzun ömürlü çerezleri dahil | Bellek/oturum; üçüncü taraf çerez engelli | Sunucu son kullanımı disk kalıcılığı yaratamaz |
| localStorage, IndexedDB, sessionStorage | Oturum | Worker, iframe, opak origin, kota hatası |
| Cache Storage ve service worker kayıtları | Bağlam ömrü | Sonlandırmadan sonra arka plan işi yok; erken silmede worker tekrar yazabilir |
| HTTP/kod önbelleği, ağ kimlik doğrulama durumu | Bellek veya desteklenen kalıcılık kapatma | Her arka uç ayrı doğrulanır |
| OPFS/File System, storage buckets, varsa Shared Storage | Bağlam dışına kalıcılık yok | Desteklenmeyen API normal başarısız olur; yeni upstream API'ler denetlenir |
| Geçmiş, son sekmeler, favicon, küçük resim, çökme geri yükleme | Kalıcı gezinme kaydı yok | Ana profil, oturum dosyası ve OS entegrasyonu |
| İzinler | Varsayılan oturumluk | Hatırlama mikrofon/konum izni vermez |
| HSTS/taşıma güvenliği | Upstream güvenlik anlamı korunur | Statik HSTS/CT/kök verisi önbellek sanılarak silinmez; dinamik durum ayrıca incelenir |
| İndirilen/dışa aktarılan dosya | Kullanıcının seçtiği yerde kalıcı | Geçici indirme listesi dosyayı veya OS karantina bilgisini silmez |
| Yer imi/ayar/ileride isteğe bağlı parola | Açıkça kalıcı | Örtük parola kaydı yok; OS güvenli deposu gerekir |
| Eklenti/yerel yardımcı, OS cache/swap/çökme dökümü | Basit StoragePartition güvencesi dışında | Eklentiler kısıtlı; otomatik çökme yüklemesi yok; sınırlar açıklanır |

`StoragePartition::ClearData` ve gezinme verisi kaldırma API'leri yararlıdır; asenkron silme, diske hiç yazmamanın yerine geçmez. [StoragePartition](https://chromium.googlesource.com/chromium/src/+/main/content/public/browser/storage_partition.h).

Varsayılan güvence düzenli kapanışa veya “sonraki açılışta sil”e dayanamaz. Her OS/Pardus'ta gezinme ve zorla öldürme sırasında dosya yazmaları ölçülür. Kalıcı oturum geri yükleme ve URL içeren OS son öğeleri mümkün olduğunda kapatılır. İndirmenin kaynak/karantina verisi OS zararlı yazılım koruması için korunabilir; bu istisna açıklanır, güvenlik zayıflatılmaz. Tam disk şifrelemesi Yuva'nın silme mekanizması değildir.

## “Bu siteyi hatırla” araştırma kapısı

0.1'de çalışan Hatırla düğmesi yoktur; desteklenmeyen kalıcılık sözü gösterilmez. 0.2 pilotu ancak depolama ADR'si ve sınır testlerinden sonra açılır.

| Yaklaşım | Değerlendirme |
| --- | --- |
| Kalıcı profil + oturumluk çerez + silme izin listesi | Kolay; çerez dışı yazma/çökme izi bırakır. Varsayılan geçicilik için reddedilir |
| Özel non-OTR profil; varsayılan bellek ve izinli disk bölümleri | Arayüz sade olabilir; SiteInstance/OOPIF/hizmet yönlendirmesi yüksek riskli |
| Hatırlanan konteyner için ayrı BrowserContext | Mevcut ayrım üzerinden daha anlaşılır; kaynak tüketimi/popup/SSO zor. İlk araştırma prototipi tercihi |

Ölçmeden ileri modeli yayın taahhüdüne dönüştürme. Sınırsız yerleşik bağlam oluşturma; çok sayıda hatırlanan site için kaynak bütçesi koy. Mevcut bağlam ayrımı, kanıtlanmamış çerez taşıma katmanına tercih edilir.

Önerilen kapsam Chromium PSL'sinden özel kayıtlar dahil türetilen **schemeful site** olur. Aynı site alt alanlarının çerez paylaşabileceği kullanıcıya açıklanır. Bu tam-origin veya yalnız oturum belirteci kasası değildir. Registry'nin doğrulanmış host kapsamıyla aynı değildir. `*.gov.tr`, `*.com.tr` veya kurumun tüm siteleri otomatik kalıcılık izni alamaz.

```text
temporary
  açık Remember eylemi → pendingReopen
  ilgili bağlamları kapat, temiz yeniden aç → remembered
remembered
  açık Forget eylemi → revoking
  belge/worker durdur, yeniden açmayı engelle, veriyi sil → temporary
  silme hatası → cleanupRequired
```

İngilizce makine değerleri arayüzde Türkçe gösterilir. Hatırlama temiz yeniden açılışta etkinleşir; yeniden giriş gerekebileceği bildirilir. Canlı çerez, IndexedDB tutamacı, worker veya cache geçiciden kalıcıya nakledilmez. Yeniden açma iptal edilirse geçici kalır. Çökme/kısmi işlem günlüğü bilinen duruma döndürür.

Pilot site çerezleri ve origin depolamasını kaba birim olarak, kaçınılmazsa o konteynere bağlı bölümlenmiş gömülü durumla birlikte saklayabilir. Gerçek sınır arayüzde açıklanır. “Yalnız giriş bilgisi” sözü verilmez; giriş çoklu alan, IndexedDB ve worker gerektirebilir. İnce çerez seçimi tutarsız oturum yaratabileceği için ertelenir.

Hatırlanan bağlamdan başka siteye üst-seviye gezinme varsayılan geçici bağlama döner. Kimlik sağlayıcı dönüşü, POST, opener/postMessage, blob ve ödeme popup'ı bunu zorlaştırır. Sentetik çoklu site deneyleri gerekir; POST gövdesi başka bağlamda kendiliğinden tekrar oynatılmaz. Güvenlik değişmezleri korunamıyorsa pilot kısıtlanır veya ertelenir. Kimlik sağlayıcı, bağlı site hatırlandı diye hatırlanmaz. Gelecek site grupları ayrı açık ve incelenebilir kullanıcı izni ister.

Unut önce kalıcılığı iptal eder; tüm ilgili belge/worker'ları durdurur; BFCache/prerender/tutamakları geçersiz kılar; kapsamlı arka uçları siler ve eski bağlamı yeniden kullandırmaz. Asenkron sonuç görünür; yarım silme sonraki erişimden önce tekrar denenir. SSD'de adli silme iddiası yoktur. Eşzamanlı sekme, profil, çökme ve şema geçişi test edilir.

## Kalkan sözleşmeleri

`EvaluateRequest(RequestContext, PolicySnapshot, RuleSnapshot) → Decision`: eylem, sabit kural/kategori kimliği ve nesil döndürür; URL günlüğü tutmaz. Başlatıcı/frame, üst-seviye schemeful site, kaynak türü ve yönlendirme durumu tarayıcı tarafından doğrulanır; renderer girdisine kör güvenilmez.

`GetPageSummary(WebContents, navigationId)`: sayaç ve koruma/kalıcılık durumu. Ana belge geçişinde sayaç sıfırlanır; BFCache belge durumunu geri getirir. Yeniden denenen yönlendirme aynı istek gibi sayılmaz. Reklam takipçisi toplam takip engelinin alt kümesidir; ikinci kez eklenmez. “12 takip isteği engellendi” 12 şirket veya takip edilemezlik kanıtı değildir.

`SetSiteException(scope, protection, lifetime)` yalnız tarayıcı arayüzünden çağrılır. Varsayılan oturum; kalıcı istisna ayrı açık seçim, süre ve sıfırlama kontrolü ister. İstisna takip engeli/parametre temizliğini gevşetebilir; TLS, sandbox, origin yalıtımı, imza doğrulaması, oltalama/zararlı indirme ve zorunlu içerik korumasını gevşetemez. Trusted Sites üyeliği istisna değildir.

## Koruma planı

| Koruma | Öneri | Uyumluluk / sınır |
| --- | --- | --- |
| Üçüncü taraf çerez | 0.1 varsayılan engel | Storage Access izni açık/dar/oturumluk; genel SSO listesi yok |
| Bölümlendirme | Upstream depolama/ağ anahtarları korunur | CHIPS/Storage Access etkileşimi kilitli sürümde denenir |
| Takip/reklam takip isteği | Yerel motor; adblock-rust değerlendirmesi | EasyPrivacy ve incelenmiş reklam-takip alt kümesi; tüm reklamları engelleme iddiası yok |
| URL parametre temizliği | 0.1 bilinen dar kurallar, üst-seviye GET | İmzalı URL/auth/ödeme belirteci, fragment ve POST hariç; genel `id`/`token` silme yok |
| Referrer | Origin dışına en fazla origin; HTTPS→HTTP yok; sitenin daha sıkı kuralı korunur | Gevşek site politikasını sınırlar; gerekçeli dar istisna |
| HTTPS-first | Upstream mekanizması ve görünür HTTP kararı | Sertifika hatası otomatik HTTP denemesi doğurmaz |
| DNS | Desteklenende otomatik şifreli yükseltme, görünür fallback, açık katı DoH seçeneği | Zorunlu üçüncü taraf/Yuva resolver yok; sağlayıcı sorguyu görür; captive portal ayrı |
| WebRTC | Yerel adres azaltımı korunur; dış arayüz/proxy politikası değerlendirilir | mDNS genel IP'yi gizlemez; UDP kısıtı görüşmeyi bozabilir; VPN/proxy/IPv6 testi |
| İzinler | Kullanıcı eylemi, origin kapsamı, oturum ömrü | Hatırlama izin veya kurumsal güven değildir |
| Bounce tracking | Önce upstream önlemlerini değerlendir | Aktif ödeme/kimlik akışını kanıtsız otomatik temizleme yok |
| Canvas/WebGL/audio | 0.1 upstream; ileri direnç ertelenir | Rastgele gürültü veya toplu engel yok; tutarsız sonuç yeni parmak izi olabilir |
| Font ve diğer yüzeyler | Yerel font erişim sınırlamaları korunur; gereksiz entropi azaltılır | CSS/font ölçümleri yine tanımlar; Türkçe font/erişilebilirlik çalışmalı |

Parmak izi araştırması site/oturum kapsamlı tutarlı bozmayı standartlaştırılmış yüzeylerle karşılaştırır; Brave/Cromite çalışmaları adaydır. Yuva'ya özgü davranış tanınabilirliği artırabilir. Çapraz site ilişkilendirme, görsel/ses doğruluğu, performans ve taşıma maliyeti ölçülmeden varsayılan değişmez. Kapsamlı koruma iddiası 0.1'de yoktur.

## Motor ve veri dağıtımı

Yeni genel filtre dili yerine bakımı yapılan motor tercih edilir. MPL-2.0 adblock-rust dar Rust/C++ sınırı, panic kontrolü ve güvenli ömürlerle değerlendirilir. Başlangıçta yalnız ağ kuralları; Standart için takip/mahremiyet alt kümesi, Sıkı için ayrıca lisanslı genel reklam kuralları kullanılır. EasyList gibi genel reklam kümesi Standart içine sessizce karıştırılmaz. Kozmetik kurallar yalnız Sıkı için sonraki incelemeye; yönlendirme kaynakları ve scriptlet ertelenir. Kural dosya sistemi veya keyfi kod yetkisi alamaz. [Motor belgesi](https://raw.githubusercontent.com/brave/adblock-rust/master/README.md).

Listeler imzalı, sürümlü, sabit kaynak revizyonlu, atıflı ve sınırlı sözdizimlidir. Türkçe liste eklenmeden köken/lisans/yanlış pozitif/bakım incelenir. Desteklenmeyen tür çalıştırılmaz. İmza yetkili yayını gösterir, iyi içerik garantisi vermez. Canary testleri, fuzz ve süreli kural düzeltmesi gerekir. Bozuk güncellemede son geçerli uyumlu liste tutulur, yaşı gösterilir. Liste yoksa engelleme kullanılamıyor denir; genel tarayıcı güvenliği açık kalır.

## Gerekli kanıt

Aynı üçüncü tarafı gömen iki site; aynı origin/çok sekme; bölümlü çerez; worker fetch; popup SSO; BFCache/prerender; WebSocket/WebTransport; yönlendirme; izin iptali; kota; kapanış/Unut sırasında çökme; dosya farkı; yeni oturum; özel profil kaçışı; eklenti/yerel mesajlaşma sınanır. Yayımlanan tüm OS'ler ve desteklenen Pardus kollarında tekrarlanır.

Sentetik ağ yakalaması Yuva'ya geçmiş, sorgu veya sayaç gönderilmediğini göstermelidir. Uyumluluk ayarlamak için gerçek kullanıcının URL kümesi toplanmaz. Yalnız ölçülmüş koruma duyurulur; kalan sınırlar Türkçe ve açık anlatılır.

## Zorunlu güvenlikten ayrım ve ölçüm

[Content Protection](CONTENT_PROTECTION.md) ayrı imzalı negatif politika bileşenidir; Kalkan seviye seçimi tarafından kapatılamaz. [Trusted Sites](TRUSTED_SITES_DESIGN.md) ve genel tehdit koruması da bağımsızdır. İçerik engel denemesi sayacı/geçmişi tutulmaz. Standart/Sıkı karşılaştırmalı korpus; takip yapmayan bağlamsal reklamın Standart'ta kaldığını, takip reklamının engellendiğini, Off'un zorunlu güvenliği etkilemediğini kanıtlamalıdır. GPC başlık/DOM/worker, DNT seçimi, CMP ret ve imzalı parametre istisnaları ayrıca test edilir.

Birinci taraf olmak takip yapmama kanıtı değildir. CNAME cloaking ve birinci taraf üzerinden taşınan takip endpoint'leri ayrıca araştırılır; normal uygulama çerezi veya bütün ilk taraf script'leri gelişigüzel engellenmez. Context içi oturum verisiyle siteler arası profil amacı aynı şey sayılmaz.
