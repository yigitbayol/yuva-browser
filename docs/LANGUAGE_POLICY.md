# Zorunlu dil politikası

Durum: kullanıcının 18 Eylül 2026 tarihli talimatıyla belirlenmiş, projenin vazgeçilmez kuralı. Bu politika tüm Yuva katkılarının kabul ölçütüdür.

| Alan | Zorunlu dil |
| --- | --- |
| Değişken, fonksiyon, sınıf, tür, modül ve ad alanı adları | İngilizce |
| Parametre adları, makineye yönelik seçenek ve enum değerleri | İngilizce |
| API alanları, JSON anahtarları, yapılandırma anahtarları ve ortam değişkenleri | İngilizce |
| Test adları, komutlar, kaynak dosya/dizin adları ve teknik kimlikler | İngilizce |
| Kod yorumları, docstring açıklamaları, TODO/FIXME açıklamaları | Türkçe |
| Geliştirici notları, mimari kararlar, teknik belgeler ve katkı açıklamaları | Türkçe |
| Kullanıcıya görünen menüler, düğmeler, uyarılar, hata açıklamaları ve yardım | Türkçe |

Örneğin kodda `storageMode`, `rememberSite`, `temporary`, `remembered`, `expiresAt` kullanılır; kullanıcıya “Geçici”, “Bu siteyi hatırla” ve “Saklama izni sona erdi” gösterilir. Makine değeri yerelleştirilmez; Türkçe metin yerelleştirme kaynağından alınır. Teknik günlük olay kimliği İngilizce olabilir; geliştiriciye açıklama ve kullanıcıya görünen mesaj Türkçedir.

Türkçe adları İngilizce harflerle yazmak bu kurala uymaz: `siteyiHatirla` yerine `rememberSite` kullanılır. Standart API/protokol adları ve kaynağa referans verilen semboller aynen korunur. URL/alan adı karşılaştırmalarında Türkçe büyük-küçük harf dönüşümü kullanılmaz.

Yuva'nın yazdığı veya değiştirdiği açıklamalar Türkçedir. İçe alınan üçüncü taraf kaynakların özgün telif/lisans bildirimleri ve dokunulmayan Chromium yorumları sırf çeviri amacıyla değiştirilmez; böylece hukuki metinler ve upstream ile küçük fark ilkesi korunur. Standart lisansın özgün metni esas kalır, açıklaması Türkçe belgelenir.

Arayüz Türkçe olarak tamamlanmadan özellik bitmiş sayılmaz. GRIT/GRD kaynakları ve İngilizce mesaj kimlikleri kullanılır; ileride başka dil eklenmesi Türkçe desteğinin kalitesini veya varsayılanını düşüremez. Güvenlik ve mahremiyet açıklamaları da bu kapsamdadır.

İnceleme kontrolü: tanımlayıcılar/parametreler İngilizce mi, yorum ve notlar Türkçe mi, arayüzde geliştirici jargonu veya çevrilmemiş metin var mı? Gelecekte otomatik denetimler yardımcı olabilir; dil algılaması tek başına kabul kararı vermez.
