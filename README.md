# 🏠 Yuva

### Özel olan, özel kalır.

## Güncel ilerleme — 18 Eylül 2026

**Faz 0 tasarım belgeleri tamamlandı; Faz 1 geliştirme hazırlığı başladı.** Henüz çalışan veya indirilebilir bir Yuva tarayıcısı yok. Aşağıdaki ürün anlatımı hedeflenen davranışları açıklar.

| Alan | Gerçek durum |
| --- | --- |
| Mimari | Chromium Stable + küçük Yuva deposu + ayrı bileşen/yama katmanı seçildi. |
| Kaynak kimliği | Yuva `0.1.0-dev`, Chromium `153.0.8010.53`, yama kümesi `1`; tam commit ve DEPS özeti [sabitlendi](config/versions.json). Henüz derlenmedi. |
| Geliştirici araçları | Ortam denetimi, kaynak kök kilidi, açık seçenekle güvenli kök getirme, upstream sürüm/yama denetimi ve Git indeks koruması eklendi. Varsayılan bootstrap indirmez. |
| Doğrulama | 55 araç testi yerelde ve [Windows/macOS/Linux CI'sının her birinde geçti](https://github.com/yigitbayol/yuva-browser/actions/runs/35280081007). Kök getirme testleri küçük yerel Git depolarını kullanır. Bunlar tarayıcı derleme veya Pardus uyumluluk testleri değildir. |
| Tarayıcı özellikleri | Kalkan, geçici depolama, banka/kamu koruması ve içerik koruması tasarlandı; tarayıcıya henüz uygulanmadı. |
| Platformlar | Windows, macOS, genel Linux ve Pardus hedefleniyor; hiçbirinin Yuva derlemesi henüz doğrulanmadı. Pardus için ayrı testler ve yerel `.deb` zorunlu. |

**Son geliştirme:** `bootstrap --fetch-roots` ve `check-lock` eklendi. Getirme ve hata durumları küçük yerel Git depolarıyla sınandı; gerçek Chromium henüz getirilmedi. Kilit şu anda yalnız iki kaynak kökünü kapsıyor; tam bağımlılık kilidi değil.

**Sıradaki adım:** Derleme ortamını nitelendirmek; sabit gclient üzerinden DEPS/CIPD/GCS bağımlılık grafiğini, hook incelemesini ve SDK/araç zinciri kilidini tamamlamak. Ardından ilk saf Chromium referans derlemesi gelecek. [Aşamalar ve doğrulama sınırları](docs/DEPENDENCY_LOCK.md).

Geliştirme araçlarını Chromium indirmeden denemek için:

```sh
./scripts/bootstrap --plan
./scripts/check-lock
./scripts/doctor
python3 -m unittest discover -s tests/tooling -v
```

`doctor` eksik disk/SDK gibi engellerde hata koduyla durur. `bootstrap` varsayılan olarak yalnız plan ve önkoşul denetimi yapar. `--fetch-roots` büyük indirmeyi açıkça ister; ancak ortam/güncellik kapıları geçerse çalışır. Bağımlılıkları veya hook'ları çalıştırmaz ve tarayıcı derlemez. Gereksinimler ve Windows komutları [derleme belgesinde](docs/BUILD.md).

[Mimari karar](docs/adr/0001-thin-chromium-layer.md) · [Sıralı işler ve durumları](IMPLEMENTATION_PLAN.md) · [Yol haritası](ROADMAP.md) · [Teknik belgeler](docs/README.md) · [Araç CI sonuçları](https://github.com/yigitbayol/yuva-browser/actions/workflows/development-tools.yml)

---

**Yuva**, Türkiye'de geliştirilen, açık kaynak ve gizlilik odaklı bir web tarayıcısıdır.

Yuva'nın amacı internete yeni özellikler eklemek değil; **internette gezinmeyi yeniden kullanıcıya ait hale getirmektir.**

Takip edilmek, profillenmek veya gezinme geçmişini bir teknoloji şirketiyle paylaşmak bir web tarayıcısının varsayılan davranışı olmamalı.

Yuva bu düşünceyle geliştiriliyor.

> **Yuva'nın gizli modu yoktur. Çünkü Yuva'nın kendisi gizlidir.**

---

## Neden Yuva?

Bugün kullandığımız tarayıcıların çoğunda gizlilik kullanıcının ayrıca seçmesi gereken bir özellik.

Çerezleri kapatmanız, gizli pencere açmanız, takip engelleyici kurmanız veya hangi verilerin toplandığını araştırmanız gerekiyor.

Yuva'da bunun tersini yapmak istiyoruz.

**Gizlilik varsayılandır.**

Bir web sitesi siz özellikle izin vermediğiniz sürece Yuva'da kalıcı bir yere sahip olmamalı.

Temel yaklaşımımız:

**Her şeyi hatırla → Kullanıcı temizlesin**

yerine:

**Hiçbir şeyi hatırlama → Kullanıcı istediğini hatırlatsın.**

---

# 🛡️ Yuva Kalkan

Yuva'nın gizlilik ve takip önleme katmanıdır.

Yuva Kalkan'ın amacı kullanıcıyı mümkün olduğunca:

* siteler arası takipten,
* üçüncü taraf takip çerezlerinden,
* reklam takipçilerinden,
* tracking URL parametrelerinden,
* fingerprinting girişimlerinden,
* WebRTC kaynaklı IP sızıntılarından,
* şüpheli yönlendirmelerden

korumaktır.

Bütün bunların mümkün olduğunca **web sitelerini bozmadan** yapılması hedeflenir.

Yuva'nın amacı internette görünmez olduğunuzu iddia etmek değildir.

Amacımız **takip edilmeyi mümkün olduğunca zorlaştırmak ve kontrolü kullanıcıya vermektir.**

Varsayılan Standart koruma takipçileri engellemeyi, takip yapmayan reklamları ise genel olarak engellememeyi hedefler. Sıkı koruma reklam engellemeyi de ekler. Siteye özgü filtre istisnaları TLS, oltalama ve zorunlu içerik korumasını kapatamaz.

> **Yuva reklamları değil, sizi takip eden sistemi engeller.**

Yuva internetin gelir modeline karar vermez. Kullanıcının takip edilip edilmeyeceğine kullanıcı karar verir. Kendi reklamımızı yerleştirmek veya ücret karşılığında reklam istisnası satmak ürün politikasının dışındadır.

---

# 🏡 Bu siteyi hatırla

Yuva'da site verilerinin mümkün olduğunca geçici olması hedeflenmektedir.

Ancak gerçek hayatta bazı sitelerin bizi hatırlamasını isteriz.

Bu nedenle Yuva'nın temel özelliklerinden biri:

### Bu siteyi hatırla

olacaktır.

Bir site için özellikle izin verdiğinizde Yuva gerekli oturum verilerinin kalıcı olmasına izin verebilir.

Böylece:

**İnternet sizi varsayılan olarak hatırlamaz.**

**Kimi hatırlayacağına siz karar verirsiniz.**

---

# 🇹🇷 Türkiye için tasarlandı

Yuva yalnızca Türkçeye çevrilmiş bir tarayıcı olmayacak.

Türkiye'deki internet kullanımını dikkate alarak tasarlanacak.

Özellikle:

* kamu hizmetleri,
* e-Devlet,
* bankacılık,
* ödeme sistemleri,
* e-imza,
* mobil imza,
* KamuSM,
* UYAP,
* üniversiteler,
* belge ve PDF işlemleri

gibi Türkiye'de yoğun kullanılan web deneyimlerinde güvenlik ve kullanım kolaylığı öncelikli olacaktır.

---

# ✓ Doğrulanmış Siteler

Phishing saldırılarında sahte bir adresi gerçek bir kamu kurumu veya banka gibi göstermek oldukça kolaydır.

Yuva bunun için ek bir güvenlik katmanı geliştirmeyi hedefliyor:

### Yuva Doğrulanmış Siteler

Örneğin gerçek bir kamu hizmetine bağlandığınızda Yuva:

> ✓ Doğrulanmış kamu sitesi

gösterebilir.

Benzer şekilde ileride:

> ✓ Doğrulanmış banka
> ✓ Doğrulanmış üniversite
> ✓ Doğrulanmış kamu kurumu

gibi doğrulamalar yapılabilir.

Bu sistem Chromium'un TLS ve sertifika güvenlik mekanizmalarının **yerine geçmez**.

Onların üzerinde çalışan ek bir phishing koruma katmanıdır.

Doğrulanmış alan adlarının açık, denetlenebilir, sürümlenmiş ve kriptografik olarak imzalanmış bir kayıt sistemi üzerinden dağıtılması hedeflenmektedir.

---

# 🎭 Sahte sitelere karşı koruma

Yuva, doğrulanmış alan adlarına benzeyen şüpheli adresleri tespit etmeye yönelik ek korumalar geliştirmeyi hedeflemektedir.

Örneğin:

```text
turkiye.gov.tr       ✓

turk1ye.gov.tr       ⚠
turkiye-gov.example  ⚠
```

IDN homograph, Unicode karakter benzerliği, typosquatting ve benzeri phishing tekniklerine karşı ek kontroller planlanmaktadır.

---

# 🔒 Yuva, nereye gittiğinizi bilmez

Bu, Yuva'nın temel tasarım prensiplerinden biridir.

Yuva'nın kendi altyapısına:

* gezinme geçmişi,
* ziyaret edilen URL'ler,
* arama geçmişi,
* reklam kimliği,
* kullanıcı profili

gönderilmemesi hedeflenmektedir.

Yuva bir reklam platformu değildir.

Kullanıcının internet davranışından bir profil oluşturmak Yuva'nın işi değildir.

> **Tarayıcınız internette nereye gittiğinizi bilmek zorunda değil.**

---

# 🔎 Arama sizin seçiminiz

Yuva bir arama motoru değildir.

Aramalarınızı Yuva sunucularından geçirmek gibi bir hedefimiz bulunmamaktadır.

Kullanıcı hangi arama sağlayıcısını kullanacağına kendisi karar verebilmelidir.

---

# 🧩 Sade

Bir tarayıcının her şeyi yapması gerektiğine inanmıyoruz.

Yuva'nın içinde varsayılan olarak:

* reklam,
* haber akışı,
* kripto para cüzdanı,
* ödül sistemi,
* alışveriş sistemi,
* zorunlu hesap,
* zorunlu bulut servisi,
* zorunlu yapay zekâ asistanı

bulunmasını istemiyoruz.

Yuva'nın görevi basit:

**Web'i açmak. Hızlı, güvenli ve özel şekilde.**

---

# 🤖 Yapay zekâ

Yapay zekânın faydalı olabileceğine inanıyoruz.

Ancak tarayıcı geçmişinin otomatik olarak bir yapay zekâ servisine aktarılmasının doğru olduğuna inanmıyoruz.

Yuva'ya ileride AI özellikleri eklenirse bunların:

* isteğe bağlı,
* varsayılan olarak kapalı,
* açıkça izin verilen,
* mümkün olduğunda yerel çalışabilen

bir yapıda olması hedeflenmektedir.

---

# 🌍 Açık kaynak

Yuva açık kaynak olarak geliştirilmektedir.

Çünkü gizlilik konusunda:

> **Bize güvenin.**

demek yeterli değildir.

Kod incelenebilmeli.

Ne gönderildiği görülebilmeli.

Güvenlik mekanizmaları tartışılabilmeli.

Hatalar bulunabilmeli.

Topluluk katkıda bulunabilmeli.

**Güven, denetlenebilir olmalıdır.**

---

# ⚙️ Teknoloji

Yuva'nın Chromium tabanlı geliştirilmesi planlanmaktadır.

Bunun temel nedenleri:

* modern web standartlarıyla uyumluluk,
* Chromium güvenlik mimarisi,
* sandbox ve site isolation,
* geniş web sitesi uyumluluğu,
* Chromium extension ekosistemi,
* düzenli güvenlik güncellemeleridir.

Yuva'nın amacı Chromium'u yeniden yazmak değildir.

Amacımız mümkün olduğunca upstream Chromium'a yakın kalırken Yuva'nın gizlilik ve güvenlik katmanlarını ayrı ve sürdürülebilir şekilde geliştirmektir.

---

# 🔄 Güvenlik güncellemeleri

Tarayıcı güvenliği yalnızca özelliklerle sağlanamaz.

Bir tarayıcının güvenli kalabilmesi için Chromium güvenlik güncellemelerini hızlı şekilde alabilmesi gerekir.

Bu nedenle Yuva'nın mimarisinde:

**upstream güncelleme hızı, özellik sayısından daha önemlidir.**

Bir özellik Chromium güvenlik güncellemelerini almamızı ciddi biçimde zorlaştırıyorsa o özellik yeniden değerlendirilmelidir.

---

# 🧭 İlkelerimiz

Yuva geliştirilirken karar sıralamamız:

```text
Güvenlik
    ↓
Upstream sürdürülebilirliği
    ↓
Gizlilik
    ↓
Web Uyumluluğu
    ↓
Sadelik
    ↓
Özellikler
```

Bir özellik kullanıcı gizliliğine zarar veriyorsa eklenmemelidir.

Bir özellik güvenliği zayıflatıyorsa eklenmemelidir.

Bir özellik Yuva'yı gereksiz yere karmaşıklaştırıyorsa gerçekten gerekli olup olmadığı sorgulanmalıdır.

---

# 🚧 Proje Durumu

Yuva geliştirme hazırlığı aşamasındadır. Güncel gerçekleşen işler sayfanın başındaki ilerleme tablosunda gösterilir. Aşağıdaki kutular çalışan tarayıcı özelliği ile tasarım çalışmasını birbirine karıştırmaz.

İlk hedef:

### Yuva 0.1 — Developer Preview

İlk hedef ve sonraki araştırmalar:

* [x] Chromium tabanının ve ince depo stratejisinin belirlenmesi
* [x] Faz 0 mimari, tehdit modeli ve tasarım belgeleri
* [x] Kaynak başlangıç sürümü ve commit kaydı (tam bağımlılık kilidi henüz değil)
* [x] İndirmesiz plan, ortam ve upstream denetim araçları
* [x] Kaynak kök kilidi ve açık seçenekle güvenli getirme aracı (yerel Git testleri)
* [ ] Tam bağımlılık kilidi, kaynak hazırlama ve ilk referans derlemesi
* [ ] Google bağımlılıklarının analizi
* [ ] Yuva marka ve temel arayüzü
* [ ] Türkçe birinci sınıf dil desteği
* [ ] Privacy-first varsayılanlar
* [ ] Yuva Kalkan altyapısı
* [ ] Tracker engelleme
* [ ] Tracking parameter temizleme
* [ ] HTTPS-first
* [ ] Güvenli DNS
* [ ] Fingerprinting korumalarının araştırılması
* [ ] Geçici site verisi mimarisi
* [ ] "Bu siteyi hatırla" — 0.1 sonrasında, depolama deneyleri başarılı olursa
* [ ] Yuva Doğrulanmış Siteler
* [ ] Yetkili kaynaklarla doğrulanmış Türk bankacılık kayıtları
* [ ] Türk kamu alan adları kayıt altyapısı
* [ ] Phishing/lookalike domain koruması
* [ ] Resmî dağıtımlarda imzalı yerel yetişkin içerik engeli
* [ ] Windows build
* [ ] macOS build
* [ ] Linux build
* [ ] Desteklenen Pardus sürümlerinde ayrı derleme/uyumluluk testleri ve yerel `.deb`
* [ ] Güvenli release pipeline
* [ ] GitHub Releases üzerinden dağıtım

---

# 🗺️ Yol Haritası

### 0.1 — Developer Preview

Güvenli Chromium temeli, Yuva markası ve temel mahremiyet korumaları. Resmî önizleme ikilisi banka/kamu oltalama koruması, yerel içerik engeli, güvenli yayın ve dört platform ailesinin test kapılarından sonra yayımlanabilir.

### 0.2 — Alpha

Yuva Kalkan, takip engelleme ve Doğrulanmış Siteler korumalarını olgunlaştırma; seçici hatırlama deneyleri.

### 0.3 — Beta

Günlük kullanıma uygunluk, performans, site uyumluluğu ve platform testleri.

### 1.0 — Stable

Günlük kullanım için güvenli ve kararlı Yuva sürümü.

---

# 🧑‍💻 Katkıda Bulunun

Yuva yalnızca bir şirketin ürünü olarak değil, açık kaynak bir Türkiye teknoloji projesi olarak büyüyebilir.

Katkılar yalnızca kod ile sınırlı değildir.

İhtiyacımız olacak:

* Chromium geliştiricileri
* güvenlik araştırmacıları
* privacy araştırmacıları
* frontend geliştiricileri
* UX tasarımcıları
* Türkçe dil katkıcıları
* Linux geliştiricileri
* Windows/macOS geliştiricileri
* penetration tester'lar
* kamu servisleri konusunda deneyimli geliştiriciler

Bug bulduysanız issue açabilirsiniz.

Güvenlik açığı bulduysanız lütfen `SECURITY.md` içerisindeki responsible disclosure sürecini kullanın.

---

# ❤️ Neden "Yuva"?

İnternet giderek hayatımızın daha büyük bir parçası haline geliyor.

Çalışıyoruz.

Öğreniyoruz.

Bankacılık işlemlerimizi yapıyoruz.

Devlet hizmetlerine erişiyoruz.

Konuşuyoruz.

Araştırıyoruz.

Ve bütün bunları çoğunlukla bir tarayıcının içinden yapıyoruz.

Böylesine kişisel bir alanın gerçekten kullanıcıya ait olması gerektiğine inanıyoruz.

Bu yüzden adı **Yuva**.

---

## Yuva

### Özel olan, özel kalır.

**Açık kaynak. Gizlilik odaklı. Türkiye'de geliştiriliyor.**

---

> ⚠️ **Not:** Yuva aktif geliştirme aşamasındadır ve henüz günlük kullanım veya kritik işlemler için kararlı bir sürüm değildir. İlk geliştirme sürümleri güvenlik araştırması ve test amacıyla yayınlanacaktır.
