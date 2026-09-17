# Chromium güvenlik özellikleri ve Yuva fark kaydı

Durum: önerilen kayıt, uygulanmış değişiklik yok. Her yama kimliği, sahibi/yedeği, upstream revizyonu, Türkçe gerekçesi, güvenlik etkisi, testleri, geri alma/kaldırma koşulu ve inceleme bağlantısı ile bu tabloyu genişletmelidir. Yapılandırma değişikliği de güvenlik değişikliğidir.

| Özellik | Planlanan tutum | Zorunlu kanıt |
| --- | --- | --- |
| Sandbox / süreç yalıtımı / site isolation | Koru; güvensiz geliştirme bayrağı dağıtılamaz | Windows/macOS/Linux/Pardus gerçek ortam doğrulaması |
| TLS / kök güven / CT / iptal / HSTS | Koru ve güncelle; kurum kaydı sertifika yetkisi vermez | Hatalı zincir/isim/süre, yerel kök ve bileşen yenileme |
| CORS / CSP / COOP / COEP / mixed content | Koru; e-imza uyumu için küresel istisna yok | Negatif origin/loopback/karma içerik testleri |
| İstismar azaltımları | Chromium'un platforma uygun azaltımlarını koru | GN/derleyici/OS imza ve entitlement farkı |
| Safe Browsing / genel indirme koruması | Eşdeğer çalışan veri akışı olmadan kaldırma | Lisans, güncellik, zararlı URL/dosya kapsamı, ağ gizliliği |
| Çerez ve storage partitioning | Üçüncü taraf engeli + upstream partitioning | SSO, iframe/worker, CHIPS ve Storage Access API |
| Normal profil kalıcılığı | Geçici context'e yönlendirme; kaynak yazıları denetlenir | Çökme, disk/SQLite/LevelDB, background servis ve dış bağlantılar |
| WebRTC / DNS / HTTPS | Mahremiyet varsayılanını artır, ağ uyumunu ölç | IPv6/STUN/TURN/VPN, portal, strict DNS ve HTTP fallback |
| Eklenti sistemi | MV3 izin/güncelleme sınırlarını koru; banka bağlamını araştır | Host erişimi, split/spanning, native messaging, debugger |
| Trusted Sites / Bank Security Mode | Ek origin kimliği ve oltalama kesintisi | İmza, kapsam, TLS/redirect yarışı, MFA, yanlış pozitif |
| Content Protection | Ayrı zorunlu negatif domain politikası | İmza, kaynak lisansı, yerel indeks, bypass ve kayıt tutmama |
| Güncelleyici | Ayrı kök, artan sürüm, OS imzası | Replay/rotation/TOCTOU/çökme ve yetki yükseltme |
| Güvenlik arayüzü | Metin + ikon + semantik renk | İki tema, forced colors, ekran okuyucu, klavye |

Hiçbir satır “uygulandı” anlamına gelmez. Yeniden tabanlama bu kaydı ilgili Chromium farkıyla tekrar değerlendirir. Herkese açık yayın, belge üzerinde işaretleme ile değil bağlantılı test artefaktlarıyla geçer.
