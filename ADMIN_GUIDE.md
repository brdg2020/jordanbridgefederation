# Jordan Bridge Federation (JBF) — Portal Yönetim & Güncelleme Rehberi

Bu rehber, **jordanbridgefederation.com** portalını sıfır teknik zorlukla nasıl güncelleyeceğinizi anlatır.

---

## 1. Yeni Turnuva Skoru veya Lig Sonucu Ekleme (30 Saniye)

Tüm canlı veriler `/public/data/` klasöründeki temiz JSON dosyalarından beslenir:
* **Jordan Cup / Lig Sıralaması:** `public/data/jordancup2026.json`
* **Vugraph / Festival Sonuçları:** `public/data/festival2026.json`
* **Yönetim Kurulu & Kadro:** `public/data/committee.json`

### Nasıl Güncellenir?
1. GitHub'da `brdg2020/jordanbridgefederation` deposuna gidin.
2. `public/data/jordancup2026.json` dosyasına tıklayın, sağ üstteki **Kalem (Düzenle)** ikonuna basın.
3. Takım puanlarını veya yeni sıralamayı yazıp **Commit changes** butonuna basın.
4. **Site 30 saniye içinde otomatik olarak güncellenir!**

---

## 2. Magic Contest HTML Dosyasından Otomatik Veri Çekme

Eğer turnuva direktörü (Waleed El Menyawi veya Raad Otoom) size Magic Contest HTML çıktısını verirse:
1. Dosyayı `public/archive/` altına atın.
2. Repository içindeki `python3 parse_festival_data.py` scriptini çalıştırın.
3. Script tüm takımları, rauntları, IMP ve VP skorlarını saniyeler içinde `festival2026.json`'a dönüştürür.

---

## 3. Yeni Fotoğraf veya Duyuru Ekleme

1. Fotoğrafı `public/gallery/` klasörüne atın.
2. `build_site.py` içindeki galeri listesine ekleyip çalıştırın.
3. Git commit & push yaptığınızda yeni fotoğraflar anında sitede belirir.
