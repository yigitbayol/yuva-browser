# Chromium güncellemelerini alma stratejisi

Durum: Faz 0 önerisi, 18 Eylül 2026. Güvenlik güncellemeleri yeni özelliklerden önce gelir.

## Kaynak ve dallar

Tam commit'i sabitlenmiş, güvenlik yamaları güncel Chromium Stable sürümünden derlenir. Hareketli dal, rastgele snapshot veya Chrome-for-Testing ikilisi dağıtım temeli değildir. Resmî duyuru izlenir ve platform sürümü kaynak commit'ine eşlenir. Bu tasarımda “en güncel” sürüm numarası uydurulmaz; uygulama başlarken yeniden seçilir. Chromium sık güvenlik yayını yapar ve acil düzeltmeler takvim dışında gelebilir. [Güvenlik yayın düzeni](https://security.googleblog.com/2023/08/an-update-on-chrome-security-updates.html), [resmî duyurular](https://chromereleases.googleblog.com/search/label/Stable%20updates).

`yuva-browser` küçük kalır: bileşen, kaynak, yama, araç ve kilit dosyası. Chromium ayrı, Git'in dışladığı çalışma alanına alınır. Salt okunur ayna erişilebilirliği artırabilir; asıl kaynak/commit doğrulamasının yerine geçmez. Tam vendor ağacı veya hareketli dev submodule günlük incelemeye taşınmaz.

Önerilen kilit: Chromium sürüm/commit, DEPS ve alt bağımlılık kimlikleri, depot_tools, GN/Ninja/derleyici/SDK, Rust bağımlılıkları, GN argümanları, yama sırası özeti, liste/kayıt sürümleri, derleyici imaj özeti ve Yuva commit'i. CIPD ve indirilen araç/hook girdileri dahil edilir. npm/pip/action/container için hareketli referans kullanılmaz.

`main` sonraki incelenmiş katmanı; `integration/chromium-<version>` geçici güncelleme dalını; `release/<milestone>` desteklenen yayın hattını tutar. Az yayın hattı tercih edilir. Bağımsız Blink/V8 evrimi yeni mimari karar olmadan yasaktır.

## Yama disiplini

Tercih: desteklenen yapılandırma → mevcut embedder kancası → ayrı bileşen → küçük bütünleştirme yaması → ancak incelemeyle geniş değişiklik. Yapılandırma değişikliği sırf kod farkı küçük diye güvenli sayılmaz.

Her yamanın sabit İngilizce kimliği, sıralı bağımlılığı, upstream tabanı, köken commit'i/lisansı, Türkçe gerekçesi, sahibi/yedeği, testleri, güvenlik farkı, kaldırılma koşulu ve varsa upstream katkı bağlantısı bulunur. Markalama depolama/güvenlikten ayrılır. Büyük upstream dosyayı gölgeleyen kopya, genel metin ikamesi ve bulanık yama uygulaması kabul edilmez.

Temiz kaynağa kesin bağlam kontrolüyle uygulanır, sonuç ağacı hash'i kaydedilir. Bilinmeyen dosya, kısmi uygulama veya reddedilen parça derlemeyi durdurur. Çakışma eski dosyanın tamamını geri alarak değil sembol bazında çözülür.

0.1 için inceleme bütçesi: 30'dan az yama ve 100'den az upstream dosyasını hedefle. Bu bir uyarı eşiğidir; bağımsız işleri tek yamaya sıkıştırma gerekçesi değildir. Alt sistem, satır, çakışma ve mühendis-saat izlenir. Küçük de olsa Blink/V8 veya güvenlik değişmezi yaması özel gerekçe ister.

## Sürekli güvenlik güncellemesi

1. Resmî Stable güvenlik yayınlarını en az iki saatte bir kontrol et; otomasyon arızasına insan yedeği koy.
2. Tam kilidi, notları ve ilgili güvenlik verisini güncelleyen PR aç; başka mahremiyet çatalını bekleme.
3. Temiz geçici ortamda girdileri doğrula, yamaları uygula; çakışma/lisans/hizmet farkını çıkar.
4. Windows, macOS, genel Linux ve desteklenen Pardus kollarını açık matris işleriyle derle/test et. Sandbox, TLS, geçici veri, güncelleyici ve kritik uyumluluk kapılarını çalıştır.
5. İki sorumlu kaynak farkını ve tam artefakt özetini incelesin; [yayın güvenliği](BUILD_RELEASE_SECURITY.md) ile imzala/yayımla.
6. Dışarıdan indirilen baytları ve kurulumu doğrula; upstream/Yuva sürümü, tarih, veri güncelliği ve destek durumu yerelde görülsün.

Önerilen hedefler: upstream güvenlik kaynağı erişilebilir olduktan sonra dört saatte değerlendirme, aktif istismar edilen acil düzeltmede 24 saatte, rutin güvenlikte 48 saatte yayın. Bunlar başarılmış SLA değildir; kapasite ölçülüp tatbikatla kanıtlanmalıdır. Kaçırılan hedef olay olarak yükseltilir.

İkincil mahremiyet yaması çakışırsa etkisi belgelenerek kaldırılabilir/ertelenebilir; asgari geçici gezinme ve telemetrisizlik sözleşmesi bozulamaz. Sandbox/TLS testi kapatılarak hedef tutturulmaz. Temel sözleşme bozuksa o artefakt yayımlanmaz. Banka/kamu oltalama koruması, zorunlu içerik engeli ve çalışan genel tehdit koruması da bu sözleşmededir; “ikincil yama” sayılıp kaldırılarak resmî güvenlik yayını yapılamaz.

**Masaüstüne hazır yayın**, Windows/macOS/genel Linux derlemeleri ve desteklenen tüm Pardus testleri dahil bütün zorunlu işleri gerektirir. Tek hedefe acil güvenlik artefaktı çıkarılması bu etiketi kazandırmaz. Başarısız platform gizlenmez, destek/güncellik uyarısı gösterilir; Pardus matrisi test başarısızlığı nedeniyle daraltılamaz.

Tam upstream sürüm güncellemesi, bağımlılıkları bilinmeyen tekil CVE cherry-pick'ine tercih edilir. Acil cherry-pick iki inceleme, bağımlılık analizi, regresyon testi ve tam sürüme dönüş tarihi ister. Henüz kamuya açılmamış ambargolu düzeltmelerin kapsandığı iddia edilmez.

## Sürdürülebilir doğrulama

Yuva hatasını upstream'den ayırmak için saf Chromium derleme hattı tut. Sonraki kilometre taşını ayrı ileri uyumluluk hattında dene; Stable'a karıştırma. Her yamada ilgili testler, zamanlanmış geniş testler kullan; acil yayını ilgisiz sınırsız test genişletmesiyle geciktirme.

İstemci telemetrisi olmadan platform bazında ortanca/p95 yayın gecikmesi, yamasız yaş, güncelleme başarısızlığı, soğuk derleme, imzalama erişimi ve taşıma saati ölçülür. 0.1 için üç başarılı tatbikat; 1.0 için en az sekiz haftalık sürdürülebilir operasyon ve anahtar/koşucu kesintisi denemesi gerekir.

Genel düzeltmeler upstream'e önerilir, eski yamalar kaldırılır, her yama üç ayda bir gözden geçirilir. İki eğitimli yayın sorumlusu kalmazsa kararlı terfi durur; destek kaybı ve veri dışa aktarma/geçiş rehberi yayımlanır. Güncel tutulamayan tarayıcı kabul edilebilir sonuç değildir.
