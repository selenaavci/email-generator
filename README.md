# MailCraft Agent

## Projenin Amacı

MailCraft Agent, kullanıcıların yeni bir e-posta oluşturmasını veya mevcut bir e-postaya hızlı ve doğru şekilde yanıt vermesini kolaylaştırmak için tasarlanmış, LLM destekli bir e-posta üretim aracıdır. Projenin temel amacı, teknik olmayan kullanıcıların da rahatlıkla kullanabileceği sade bir arayüz üzerinden, yalnızca metin girdisi vererek profesyonel e-postalar oluşturabilmesini sağlamaktır.

Bu ürün özellikle zaman kazandırmak, yazım kalitesini artırmak, dil bariyerini azaltmak ve kullanıcıların farklı senaryolarda daha rahat iletişim kurabilmesini desteklemek için tasarlanmıştır. Kullanıcı ister yeni bir e-posta yazmak istesin, ister kendisine gelen bir e-postaya yanıt hazırlamak istesin, sistem girilen bağlam ve istenen dile göre uygun bir e-posta taslağı üretir.

---

## Ürün Kapsamı

MailCraft Agent iki ana kullanım senaryosu sunar:

1. **Yeni Mail Oluşturma**  
   Kullanıcı yalnızca ne demek istediğini metin olarak yazar. Sistem bu isteği uygun e-posta formatında üretir.

2. **Mail Yanıtı Oluşturma**  
   Kullanıcı, yanıtlamak istediği e-postanın içeriğini metin olarak yapıştırır ve ayrıca vermek istediği cevabı kısa bir açıklama halinde belirtir. Sistem, bu bağlama uygun bir yanıt e-postası üretir.

Bu yapı sayesinde kullanıcı dosya yüklemek zorunda kalmadan, yalnızca metin ile çalışabilir. Özellikle güvenlik, sadelik ve kullanım kolaylığı açısından bu yaklaşım bilinçli olarak tercih edilmiştir.

---

## Temel Özellikler

- Türkçe arayüz
- Yeni mail oluşturma desteği
- Gelen maile yanıt oluşturma desteği
- Dil seçeneği üzerinden çıktı dilini belirleme
- Kullanıcı prompt’una göre bağlama uygun e-posta üretimi
- İsteğe bağlı isim alanları
- Kopyalanabilir çıktı
- Aynı içerik için yeniden üretim (regenerate) desteği
- Teknik olmayan kullanıcılar için sade ve anlaşılır kullanım akışı

---

## Arayüz Tasarımı

Uygulama **Streamlit** ile geliştirilecektir ve arayüz tamamen Türkçe olacaktır. Kullanıcı deneyiminin olabildiğince yalın, hızlı ve sezgisel olması hedeflenmektedir.

### Ana Form Bileşenleri

#### 1. Mail Türü
Kullanıcı ilk olarak aşağıdaki iki seçenekten birini seçer:

- **Yeni Mail**
- **Mail Yanıtı**

Bu seçim, ekranda açılacak form alanlarını dinamik olarak belirler.

#### 2. Dil Seçeneği
Kullanıcı, üretilecek e-postanın dilini seçer.

Önemli tasarım kararı:
- Arayüz tamamen Türkçe kalır.
- Kullanıcı İngilizce seçse bile yalnızca **üretilen e-posta çıktısı** İngilizce olur.
- Yani sistem dili değil, yalnızca çıktı dili değişir.

Örnek seçenekler:
- Türkçe
- İngilizce

#### 3. Kullanıcı Talebi
Her iki modda da kullanıcıdan, e-postada ne demek istediğini açıklayan bir metin alınır.

Örnek:
- “Toplantıyı gelecek haftaya ertelemek istediğimi nazikçe söyle.”
- “Teklif için teşekkür edip birkaç gün içinde geri döneceğimi belirt.”

#### 4. Yanıtlanacak Mail Alanı
Yalnızca **Mail Yanıtı** seçildiğinde görünür.

Bu alanda kullanıcı, yanıtlamak istediği e-postanın gövdesini düz metin olarak yapıştırır.

#### 5. İsteğe Bağlı Bilgiler
Kullanıcı isterse aşağıdaki alanları doldurabilir:
- **Adınız**
- **Gönderilecek Kişinin Adı**

Bu alanlar boş bırakılırsa sistem çıktı içerisinde gerekiyorsa yer tutucu ifadeler kullanabilir:
- `[Adınız]`
- `[Alıcı Adı]`

---

## Önerilen Kullanım Akışı

### Senaryo 1: Yeni Mail
1. Kullanıcı “Yeni Mail” seçer.
2. Üretilecek mailin dilini seçer.
3. Ne demek istediğini prompt alanına yazar.
4. İsterse kendi adını ve alıcı adını girer.
5. “Maili Oluştur” butonuna basar.
6. Sistem, uygun formatta e-postayı üretir.

### Senaryo 2: Mail Yanıtı
1. Kullanıcı “Mail Yanıtı” seçer.
2. Üretilecek mailin dilini seçer.
3. Yanıtlamak istediği maili metin alanına yapıştırır.
4. Vermek istediği cevabı prompt alanına yazar.
5. İsterse isim alanlarını doldurur.
6. “Maili Oluştur” butonuna basar.
7. Sistem, mevcut bağlama uygun bir yanıt e-postası üretir.

---

## Üretim Mantığı

Sistem, kullanıcıdan alınan yapılandırılmış girdileri bir LLM’e ileterek çıktı üretir. Üretim sırasında şu bilgiler modele gönderilir:

- Mail türü
- Çıktı dili
- Kullanıcının açıklaması / isteği
- Yanıtlanacak mail içeriği (varsa)
- Gönderen adı (varsa)
- Alıcı adı (varsa)

Bu sayede model yalnızca genel bir metin üretmez; seçilen senaryoya ve verilen bağlama göre daha isabetli, daha kullanışlı bir e-posta metni oluşturur.

---

## Neden Dosya Yükleme Yok?

Bu ürünün ilk versiyonunda kullanıcıların dosya yükleyememesi bilinçli bir tasarım tercihidir.

Bunun başlıca nedenleri:
- Kullanım akışını sade tutmak
- Teknik karmaşıklığı azaltmak
- Güvenlik ve veri kontrolünü kolaylaştırmak
- Kullanıcıyı yalnızca gerekli metin girdisine odaklamak

Bu nedenle sistem yalnızca **düz metin yapıştırma** mantığı ile çalışır.

---

## Hedef Kullanıcı Kitlesi

MailCraft Agent özellikle aşağıdaki kullanıcı grupları için uygundur:

- Teknik olmayan kurumsal kullanıcılar
- Hızlı e-posta desteğine ihtiyaç duyan ekipler
- İngilizce e-posta yazmakta zorlanan kullanıcılar
- Resmî veya yarı resmî mail dilinde desteğe ihtiyaç duyan çalışanlar
- Gelen maili hızlıca cevaplamak isteyen operasyon ekipleri

---

## Teknik Yaklaşım

- **Arayüz:** Streamlit
- **Girdi tipi:** Düz metin
- **Çıktı tipi:** Kopyalanabilir e-posta metni
- **Model:** LLM tabanlı metin üretimi
- **Dil desteği:** Türkçe ve İngilizce çıktı
- **Arayüz dili:** Tamamen Türkçe

---

## Örnek Arayüz Alanları

- Mail Türü
- Dil Seçimi
- Yanıtlanacak Mail
- Ne Demek İstiyorsunuz?
- Adınız (Opsiyonel)
- Alıcı Adı (Opsiyonel)
- Maili Oluştur
- Yeniden Oluştur
- Kopyala

---

## Beklenen Fayda

Bu ürünün sağlayacağı temel faydalar şunlardır:

- E-posta hazırlama süresini kısaltmak
- Yazım kalitesini artırmak
- Kullanıcıların daha profesyonel iletişim kurmasını desteklemek
- Özellikle İngilizce mail hazırlarken bariyeri azaltmak
- Günlük operasyonel işlerde hız ve tutarlılık sağlamak

---

## Gelecekte Eklenebilecek Geliştirmeler

İlk versiyon dışında ilerleyen aşamalarda şu geliştirmeler değerlendirilebilir:

- Ton seçimi (resmî, samimi, net, ikna edici vb.)
- Mail uzunluğu seçimi
- Daha kısa / daha resmî / daha nazik yeniden üretim seçenekleri
- Konu başlığı önerisi üretme
- Çok dilli destek
- Kurumsal imza şablonu ekleme
- Sık kullanılan mail şablonları
- Kategori bazlı mail üretimi (teşekkür, toplantı talebi, erteleme, bilgilendirme vb.)

---

## Sonuç

MailCraft Agent, kullanıcıların yalnızca kısa metin açıklamalarıyla etkili e-postalar oluşturmasını sağlayan sade ama yüksek fayda üreten bir araçtır. Türkçe arayüzü, metin bazlı kullanım modeli ve yeni mail / yanıt mail ayrımı sayesinde hem anlaşılır hem de pratik bir deneyim sunar. Özellikle kurumsal ortamlarda hızlı, tutarlı ve profesyonel e-posta üretimi için güçlü bir yardımcı araç olarak konumlanmaktadır.
