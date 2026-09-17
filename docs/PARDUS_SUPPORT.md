# Birinci sınıf Pardus desteği

Durum: zorunlu ürün/yayın gereksinimi; uygulama henüz yok. Araştırma tarihi: 18 Eylül 2026. Pardus genel Linux uyumluluğunun alt notu değildir; ayrı sorumlusu, derleme işleri, test görüntüleri ve yerel `.deb` paketi bulunacaktır.

## Güncel destek kapsamı

Resmî takvim Pardus 23 ailesi için 2027 üçüncü çeyrek, 25 ailesi için 2029 ikinci yarıyıl destek sonu gösteriyor; Pardus 21 desteği 1 Mayıs 2025'te bitmiş görünüyor. Başlangıç destek kolları **23.x ve 25.x** olarak belirlenir. [Resmî yaşam döngüsü](https://pardus.org.tr/pardus-surum-yonetimi/).

25.2 yayını 11 Eylül 2026'da duyurulmuş; yaşam döngüsü tablosu henüz bunu satır olarak göstermiyor. Takvimdeki planlanan ara sürümün gerçekten yayımlandığı varsayılmamalıdır. [25.2 duyurusu](https://pardus.org.tr/pardus-25-2-surumu-yayimlandi/). 23 kolunun doğrulanmış ISO/paket başlangıcı, uygulama sırasında [resmî görüntü dizininden](https://indir.pardus.org.tr/ISO/Pardus23/) seçilip güncel güvenlik depolarıyla nitelendirilir; bu tasarım 23.5'in yayımlandığı iddiasında bulunmaz.

İlk kilit dosyası her kol için `release`, `imageDigest`, `packageSnapshot`, `architecture`, `desktop`, `displayServer`, `supportUntil`, `verifiedAt` alanlarını İngilizce tutar. Yalnız hareketli `latest` etiketi kullanılmaz. Destek takvimi her yayın öncesi ve aylık denetlenir; yeni destek kolu matrise alınmadan genel masaüstü yeterliliği iddia edilmez. Süresi biten kolun kaldırılması açık destek kararı gerektirir; test başarısızlığı yüzünden sessizce kapsam daraltılmaz.

## Zorunlu CI matrisi

| İş kimliği | Ortam ve çıktı | Yayın koşulu |
| --- | --- | --- |
| `build-pardus-23-amd64` | Kilitli Pardus 23 kullanıcı alanında kaynak derleme, doğal `.deb` | Başarılı derleme ve bağımlılık çözümü |
| `build-pardus-25-amd64` | Kilitli Pardus 25 kullanıcı alanında kaynak derleme, doğal `.deb` | Başarılı derleme ve bağımlılık çözümü |
| `test-pardus-23-xfce` / `test-pardus-23-gnome` | Gerçek Pardus çekirdeği ve güncel paketlerle sanal/fiziksel masaüstü | Kurulum, render, mahremiyet ve sandbox |
| `test-pardus-25-xfce` / `test-pardus-25-gnome` | Gerçek Pardus çekirdeği ve güncel paketlerle sanal/fiziksel masaüstü | Aynı testler; desteklenen X11/Wayland oturumları |

Derleme kapları tekrarlanabilir kullanıcı alanı sağlayabilir; host çekirdeğini paylaştıkları için Pardus sandbox/masaüstü yeterliliğinin yerine geçmez. Her destek kolunda yerel paket üretilir. Tek artefakt ancak ABI/bağımlılık kanıtı ve tüm kol testleriyle ortaklaştırılabilir; iki ayrı derleme işi yine korunur.

Masaüstüne hazır olma koşulu:

```text
desktopReady = windowsBuildPassed
    && macosBuildsPassed
    && genericLinuxBuildPassed
    && allSupportedPardusBuildsPassed
    && allSupportedPardusCompatibilityTestsPassed
    && releaseSecurityGatesPassed
```

Eksik, iptal edilmiş veya atlanmış iş başarılı sayılmaz. Windows/macOS/genel Linux/Pardus ailelerinde `continue-on-error` yayın kapısını yumuşatamaz. Güvenlik düzeltmesi için yalnız geçen hedefe açıkça sınırlı acil artefakt çıkarılabilir; buna tam masaüstü yayını denemez ve başarısız platform saklanamaz.

## Yerel Debian paketi

`build/packaging/pardus/debian/` altında `control`, `rules`, `copyright`, `changelog`, kaynak biçimi ve gerekli bakım betikleri planlanır. İngilizce paket/alan adları ve Türkçe açıklama/notlar kullanılır. Gerçek bağımlılıklar `dpkg-shlibdeps` ve kol içi çözümlemeyle çıkarılır; masaüstü girişi, MIME/URL ilişkileri, simge ve kaldırma davranışı test edilir.

Bakım betiği ağdan keyfi betik indirmez; sandbox izinlerini bozmaz, sistem güvenliğini küresel kapatmaz, kullanıcı profilini kaldırma sırasında silmez. Debian paket yöneticisi kurulumun sahibidir; başka güncelleyici onunla yarışmaz. GitHub'daki `.deb` bağımsız imzalı yayın üstverisiyle doğrulanır. Gelecekte APT deposunda özel anahtarlıklı `Signed-By` kapsamı ve imzalı Release/InRelease kullanılır; `trusted=yes` ve imza denetimini kapatma yasaktır. HTTPS tek başına paket yetkilendirmesi değildir.

## Testler ve hizmet bağımsızlığı

Temiz kurulum, önceki Yuva sürümünden yükseltme, kaldırma/yeniden kurma, bağımlılık hatası, bozuk imza, disk dolması, Türkçe arayüz/fontlar, yazdırma/PDF, indirme, varsayılan tarayıcı, bildirim, anahtarlık, WebAuthn ve Türk hizmet akışları kapsanır. Sandbox, site yalıtımı, sertifika hatası ve geçici veri/çökme testleri zorunludur. Yerel imza yardımcısı desteği ölçülmeden ilan edilmez.

Pardus kullanıcısına Microsoft/Apple/Google hesabı veya özel bulut hizmeti şart koşulamaz. Zorunlu OS güvenlik/anahtarlık/bildirim bütünleşmesi açık ve platforma özgü olur. Henüz CI işi çalıştırılmadı, Pardus ikilisi veya `.deb` üretilmedi.
