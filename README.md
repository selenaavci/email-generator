# 📧 MailCraft Agent

## Project Overview
MailCraft Agent, kullanıcıların **yeni e-posta oluşturmasını veya mevcut bir maile yanıt vermesini** kısa bir doğal dil açıklamasıyla otomatikleştiren, LLM destekli bir e-posta üretim modülüdür.

Teknik olmayan kullanıcılar bile **birkaç metin alanı doldurarak** profesyonel, ton-uyumlu, dile uygun ve formatlı e-posta taslağı üretebilir. Sistem; ton, uzunluk, kategori, dil, alıcı hitabı ve kurumsal imza gibi parametreleri prompt'a katarak LLM'e zenginleştirilmiş bağlam sunar ve tek tıkla "yeniden üret" varyantları (daha kısa / daha resmî / daha nazik / daha net) sağlar.

> ⚠️ **LLM gerektirir.** Bu agent kurum içi (vLLM, on-prem) veya OpenAI uyumlu bir LLM endpoint'i ile çalışır. **Cloud versiyonu** (`streamlit_app.py`) `st.secrets` üzerinden, **Windows versiyonu** (`mailcraft.py` / `email-generator/email_generator.py`) ise dosya başındaki sabitlerden credential okur. LLM yapılandırılmadan başlatıldığında uygulama erken durur ve kullanıcıyı bilgilendirir.

---

## 🎯 Project Purpose
Yazma süresini kısaltmak, dil/biçim hatalarını azaltmak ve farklı senaryolarda **tutarlı kurumsal ses tonu** sağlamak. Özellikle çok dilli iletişim (Türkçe / İngilizce) gereken durumlarda dil bariyerini düşürür ve yeni mail / mail yanıtı için tek bir arayüzde standardizasyon sunar.

Sadece "metin üreten" basit bir LLM wrapper'ı olmaktan farkı: **prompt mühendisliği** üzerinden hitap, yer tutucu, format, emoji yasağı, dil zorlaması ve ton kalibrasyonu doğrudan sistem prompt'unda enforce edilir.

---

## 👥 Target Use Cases

### 1. Kurumsal İletişim
- Toplantı talebi / erteleme / iptali
- Teklif / fiyat / bilgi talebi yanıtları
- Resmî bilgilendirme veya teşekkür mesajları

### 2. Müşteri / Operasyon Yanıtları
- Şikâyet ve geri bildirim yanıtları
- Takip ve hatırlatma e-postaları
- İzin / başvuru / iş ilişkili formlar

### 3. Multilingual Communication
- Türkçe ↔ İngilizce çıktı seçeneği
- Cinsiyet-belirtmeyen Türkçe hitap kuralları (Sayın [Ad] yerine Merhaba [Ad])
- Kurum içi standart imza şablonu desteği

---

## ⚙️ End-to-End Workflow

1. **Mod Seçimi** — Kullanıcı **Yeni Mail** veya **Mail Yanıtı** modunu seçer.
2. **Dil Seçimi** — Çıktı dili: Türkçe veya İngilizce.
3. **Ayarlar (sidebar)**
   - Ton (Resmî / Samimi / Net / İkna edici / Nazik)
   - Mail uzunluğu (Kısa / Orta / Uzun)
   - Kategori (Teşekkür / Toplantı / Bilgilendirme / Özür / Teklif vb.)
   - Yaratıcı konu başlığı önerisi (toggle)
   - Kurumsal imza şablonu (opsiyonel text area)
4. **Hazır Şablon (opsiyonel)** — Toplantı erteleme, teklif teşekkürü, izin talebi, hatırlatma gibi yaygın senaryolar için pre-fill metni.
5. **Talep Girişi** — Kullanıcı "ne demek istediğini" 1–3 cümleyle açıklar. Mail yanıtı modunda ek olarak yanıtlanacak orijinal mailin gövdesi yapıştırılır.
6. **Alıcı Bilgileri (opsiyonel)** — Gönderen / alıcı adı + alıcı hitabı (Belirtilmedi / Hanım / Bey).
7. **Prompt İnşası** — `kullanici_promptu()` parametreleri yapılandırılmış bir bağlama dönüştürür; sistem prompt'u ton, dil, hitap kuralları ve format dahil ihtiyaç duyulan davranışı LLM'e dikte eder.
8. **LLM Çağrısı** — OpenAI uyumlu chat completions endpoint'ine `temperature=0.7` ile gönderim. Yanıt: tek bir e-posta metni (Konu satırı + boş satır + gövde).
9. **Çıktı Görüntüleme** — `st.code(...)` widget'ında metin formatlı (kopyalama ikonu Streamlit'in native UI'sından).
10. **Yeniden Üretim** — Aynı bağlamla ya da varyantlarla (daha kısa / daha resmî / daha nazik / daha net) yeniden üretim.

---

## 🧩 Architecture Overview

**Core Layers:**

- **Configuration Layer**
  Cloud (`streamlit_app.py`): `st.secrets` üzerinden `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL` okur.
  Windows (`mailcraft.py` / `email-generator/email_generator.py`): dosya başındaki sabitlerden okur (`LLM_API_KEY = " "` formatında).

- **Prompt Engineering Layer**
  - `sistem_promptu(cikti_dili)` — Türkçe hitap kuralları, dil zorlaması, format şablonu, emoji yasağı
  - `kullanici_promptu(...)` — Kullanıcı parametrelerini yapılandırılmış paragraflara dönüştürür

- **LLM Client Layer**
  OpenAI Python SDK (`openai>=1.40`) — `base_url` özelleştirilebilir (vLLM, Azure OpenAI, on-prem endpoint). Yapılandırma eksikse `st.error` + `st.stop` ile erken sonlanır.

- **UI Layer (Streamlit)**
  Tek sayfa, sidebar'da ayarlar, ana alanda mod / dil / talep / yanıt-girişi / kişi bilgisi / üret butonu. Sonuç `st.code` ile gösterilir (Windows-RDP uyumlu, custom JavaScript yok).

- **Generation State Layer**
  `st.session_state.son_payload` — son istek; `st.session_state.son_cikti` — son üretilen mail. Yeniden üretim varyantları için aynı payload kullanılıp sadece varyant talimatı eklenir.

---

## 🤖 Model & Technology Stack

### LLM Integration
- OpenAI uyumlu chat completions API
- vLLM, Azure OpenAI, on-prem LLM (`base_url` özelleştirilebilir)
- `temperature=0.7` (yaratıcı ama kontrollü)
- Sistem prompt'u: ton/dil/hitap/format enforce

### Backend & UI
- Python
- Streamlit (UI, native `st.code` ile kopyalama — custom JS yok)
- openai (Python SDK ≥1.40)

### Platform Variants
- **Cloud** (`mailcraft-agent/streamlit_app.py`): `st.secrets`, Streamlit Cloud / Streamlit ≥1.32 ortam
- **Windows** (`mailcraft-agent/mailcraft.py` ve `email-generator/email_generator.py`): hardcoded LLM sabitleri, internete kapalı RDP ortamı, Streamlit `==1.26.0` pin

---

## 🧠 Prompt Engineering Strategy

LLM doğrudan ham metin üretmiyor; **prompt katmanında çok sayıda kural enforce edilir**:

- **Dil zorlaması** — Sistem prompt'u "Üretilen e-posta yalnızca **{dil}** dilinde olmalıdır" ile çıktı dilini sıkı tutar
- **Format zorlaması** — İlk satır `Konu: ...`, ardından boş satır, sonra gövde
- **Türkçe hitap kuralı** — Cinsiyet bilinmediğinde "Sayın [Ad]" yasak; "Merhaba [Ad]" tercih edilir; bilinen cinsiyette "Merhaba [Ad] Hanım/Bey,"
- **Yer tutucu kullanımı** — Bilinmeyen alanlarda `[Adınız]`, `[Alıcı Adı]` gibi placeholder'lar
- **Emoji yasağı** — Sistem prompt'unda açıkça yasaklanır
- **Ton kalibrasyonu** — Ton ile ne aşırı resmî ne de aşırı gündelik; kullanıcının seçtiği parametreye göre ayarlanır
- **Yeniden üretim varyantları** — Aynı bağlamla "daha kısa / daha resmî / daha nazik / daha net" tek tık iyileştirme

LLM'e ham veri değil, **yapılandırılmış parametreler** (mod, dil, ton, uzunluk, kategori, hitap, imza, varyant) verilir; bu sayede kontrol ve açıklanabilirlik artar.

---

## 📊 Example Output

### Sistem girdileri
- Mod: Yeni Mail
- Dil: Türkçe
- Ton: Nazik
- Uzunluk: Orta
- Kategori: Toplantı erteleme
- Alıcı: Ahmet, Hitap: Bey
- Talep: "Yarınki toplantıyı önümüzdeki haftaya ertelemek istiyorum"

### Üretilen çıktı (örnek)
```
Konu: Yarınki Toplantımızın Ertelenmesi Hakkında

Merhaba Ahmet Bey,

Yarın için planlanan toplantımızı, beklenmedik bir gelişme nedeniyle önümüzdeki
haftaya ertelemek durumundayım. Anlayışınız için şimdiden teşekkür ederim.

Sizin için uygun olan tarih ve saati paylaşırsanız, takvimi buna göre yeniden
düzenleyebiliriz.

İyi çalışmalar dilerim.
[Adınız]
```

### Yeniden Üretim Varyantları
| Varyant | Etki |
|---------|------|
| Aynı istekle yeniden üret | Yeni bir varyasyon (aynı parametre) |
| Daha kısa | Cümle ve paragraf sayısı azaltılır |
| Daha resmî | Resmî dil kalıpları, daha uzun hitap |
| Daha nazik | Yumuşatıcı ifadeler, teşekkür dozu artırılır |
| Daha net | Süslemesiz, doğrudan açıklama |

---

## 🔐 Banking & Compliance Considerations

- **LLM trafik kontrolü** — Cloud'da `st.secrets` ile credential dosya dışında; Windows'ta dosya başında sabit (kurum içi RDP'de güvenli kabul edilen yer)
- **Dış servis bağımlılığı opsiyonel** — `base_url` ile on-prem / vLLM / Azure OpenAI'a yönlendirilebilir; OpenAI API zorunluluğu yoktur
- **Yer tutucu yaklaşımı** — Üretilen mail'de `[Adınız]`, `[Alıcı Adı]` placeholder'ları vardır; LLM gerçek müşteri verisi üretmez
- **Custom JavaScript yok** — Windows RDP ortamında "you must run JavaScript" tarzı iframe güvenlik uyarıları yaşanmaz; tüm UI native Streamlit bileşenleriyle çalışır
- **Kullanıcı verisi LLM'e gider** — Talep + yanıtlanacak mail içeriği prompt'a dahil edildiği için, LLM endpoint'inin loglama ve gizlilik politikası kurum standartlarına uygun olmalıdır
- **Auditability** — Streamlit oturum log'ları üzerinden hangi parametrelerle ne üretildiği izlenebilir

---

## 🚀 Business Impact

- E-posta yazım süresini **dakika seviyesinden saniyeye** indirir
- Çok dilli iletişimde dil bariyerini düşürür
- Standart kurumsal imza ve hitap kalıplarıyla **marka dili tutarlılığı** sağlar
- Teknik olmayan kullanıcıların doğal dilden profesyonel mail üretmesini sağlar
- Mail yanıtlarında okuyup-yorumlayıp-yanıtlama süresini kısaltır
- Yeniden üretim varyantları sayesinde tek tık ile alternatif tonlar denenebilir
- Windows RDP, Streamlit Cloud ve hibrit ortamlarda aynı kullanıcı deneyimini sunar

---

## 🔮 Future Enhancements

- E-posta geçmişi: oturumlar arası tutulan üretim arşivi
- Kullanıcıya özel imza profilleri ve şablon kütüphanesi
- Çoklu LLM provider seçimi (OpenAI / Azure / vLLM / Anthropic) UI üzerinden seçilebilir
- E-posta gönderim entegrasyonu (Outlook, Gmail API)
- Konu önerisi A/B testi (3 alternatif başlık öneren mod)
- Dil otomatik tespiti (yanıt modunda yanıtlanacak mail'in dilini otomatik kullan)
- Marka tone-of-voice fine-tune (kurumsal stil rehberi LLM context'ine yedirilir)
- Spell-check ve gramer doğrulama post-processing katmanı
