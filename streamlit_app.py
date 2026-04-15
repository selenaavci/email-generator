import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="MailCraft Agent", layout="centered")


def get_client():
    api_key = st.secrets.get("LLM_API_KEY", "")
    base_url = st.secrets.get("LLM_BASE_URL", "")
    if not api_key:
        st.error(
            "LLM_API_KEY bulunamadı. Streamlit Cloud ayarlarından "
            "**Settings → Secrets** bölümüne ekleyin."
        )
        st.stop()
    return OpenAI(api_key=api_key, base_url=base_url)


def get_model():
    return st.secrets.get("LLM_MODEL", "")


DILLER = ["Türkçe", "İngilizce"]
TONLAR = ["Resmî", "Samimi", "Net", "İkna edici", "Nazik"]
UZUNLUKLAR = ["Kısa", "Orta", "Uzun"]
KATEGORILER = [
    "Belirtilmedi",
    "Teşekkür",
    "Toplantı talebi",
    "Toplantı erteleme",
    "Bilgilendirme",
    "Özür",
    "Teklif / Fiyat talebi",
    "Takip / Hatırlatma",
    "İş başvurusu",
    "Şikâyet",
]

SABLONLAR = {
    "Yok": "",
    "Toplantı ertelemesi talebi": "Planlanan toplantının uygun bir tarihe ertelenmesini nazikçe rica et.",
    "Teklif için teşekkür": "Gönderilen teklif için teşekkür et ve birkaç gün içinde geri dönüş yapılacağını belirt.",
    "Bilgi talebi": "Belirli bir konuda detaylı bilgi talep eden bir mail yaz.",
    "İzin talebi": "Belirtilen tarihler için izin talebinde bulun, gerekli devir bilgilerini de ekle.",
    "Hatırlatma": "Daha önce gönderilen mail ile ilgili kibarca hatırlatma yap.",
}

YENIDEN_URETIM_VARYANTLARI = [
    "Aynı istekle yeniden üret",
    "Daha kısa",
    "Daha resmî",
    "Daha nazik",
    "Daha net",
]

ALICI_HITAPLARI = ["Belirtilmedi", "Hanım", "Bey"]


def sistem_promptu(cikti_dili: str) -> str:
    return (
        "Sen MailCraft adında bir e-posta yazım asistanısın. "
        "Kullanıcının verdiği bağlama göre profesyonel, doğal akışlı e-postalar üretirsin. "
        f"Üretilen e-posta yalnızca **{cikti_dili}** dilinde olmalıdır. "
        "Çıktı yalnızca e-posta metni olmalıdır; açıklama, not veya markdown başlığı ekleme. "
        "İlk satır 'Konu: ...' şeklinde olmalı, sonrasında boş satır, ardından e-posta gövdesi gelmeli. "
        "Bilinmeyen bilgiler için uygun yer tutucu kullan (örn. [Adınız], [Alıcı Adı]). "
        "Emoji kullanma, aşırı resmî veya aşırı gündelik olma; tonu kullanıcı seçimine göre ayarla. "
        "Türkçe çıktılarda hitap kuralı: alıcının cinsiyeti/hitabı belirtilmişse "
        "'Merhaba [Ad] Hanım,' veya 'Merhaba [Ad] Bey,' biçiminde başla; samimi tonda "
        "'Merhaba [Ad],' kullanılabilir. Cinsiyet/hitap belirtilmemişse 'Sayın [Ad]' gibi "
        "cinsiyet belirten hitaplardan kaçın; bunun yerine 'Merhaba [Ad],' veya 'Sayın "
        "[Alıcı Adı]' (soyad biliniyorsa) ya da 'Merhaba,' kullan. Asla sadece isme "
        "'Sayın [Ad]' şeklinde hitap etme. İngilizce çıktılarda standart 'Dear [Ad]' / "
        "'Hello [Ad]' kullan."
    )


def kullanici_promptu(
    mod: str,
    cikti_dili: str,
    kullanici_talebi: str,
    yanitlanacak: str,
    gonderen: str,
    alici: str,
    alici_hitap: str,
    ton: str,
    uzunluk: str,
    kategori: str,
    imza: str,
    konu_onerisi: bool,
    varyant: str,
) -> str:
    parcalar = []
    parcalar.append(f"Mail türü: {mod}")
    parcalar.append(f"Çıktı dili: {cikti_dili}")
    parcalar.append(f"Ton: {ton}")
    parcalar.append(f"Uzunluk: {uzunluk}")
    if kategori and kategori != "Belirtilmedi":
        parcalar.append(f"Kategori: {kategori}")
    parcalar.append(f"Gönderen adı: {gonderen.strip() or '[Adınız]'}")
    parcalar.append(f"Alıcı adı: {alici.strip() or '[Alıcı Adı]'}")
    if alici_hitap and alici_hitap != "Belirtilmedi":
        parcalar.append(
            f"Alıcı hitabı: {alici_hitap}. Türkçe çıktıda 'Merhaba [Ad] {alici_hitap},' "
            f"biçiminde hitap et; 'Sayın [Ad]' kullanma."
        )
    else:
        parcalar.append(
            "Alıcı hitabı belirtilmedi. Cinsiyet belirten hitap ('Sayın [Ad]', "
            "'[Ad] Hanım/Bey') KULLANMA; bunun yerine 'Merhaba [Ad],' veya nötr bir "
            "hitap tercih et."
        )
    parcalar.append(
        "Konu başlığı önerisi: "
        + ("Evet, yaratıcı ve konuya uygun bir konu başlığı öner."
           if konu_onerisi else "Evet (standart).")
    )

    if mod == "Mail Yanıtı" and yanitlanacak.strip():
        parcalar.append("Yanıtlanacak mail içeriği:\n---\n" + yanitlanacak.strip() + "\n---")

    parcalar.append("Kullanıcının açıklaması / isteği:\n" + kullanici_talebi.strip())

    if imza.strip():
        parcalar.append("Mailin sonuna şu imzayı ekle (olduğu gibi):\n" + imza.strip())

    if varyant and varyant != "Aynı istekle yeniden üret":
        parcalar.append(f"Yeniden üretim talebi: {varyant}. Bunu dikkate alarak yeniden yaz.")

    return "\n\n".join(parcalar)


def mail_uret(payload: dict, varyant: str = "Aynı istekle yeniden üret") -> str:
    client = get_client()
    model = get_model()
    messages = [
        {"role": "system", "content": sistem_promptu(payload["cikti_dili"])},
        {"role": "user", "content": kullanici_promptu(**payload, varyant=varyant)},
    ]
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()


st.title("MailCraft Agent")
st.caption("Kısa bir açıklama yazın, sistem sizin için profesyonel e-posta taslağı üretsin.")

with st.sidebar:
    st.header("Ayarlar")
    ton = st.selectbox("Ton", TONLAR, index=0)
    uzunluk = st.selectbox("Mail uzunluğu", UZUNLUKLAR, index=1)
    kategori = st.selectbox("Kategori (opsiyonel)", KATEGORILER, index=0)
    konu_onerisi = st.checkbox("Yaratıcı konu başlığı önerisi", value=True)
    st.divider()
    st.subheader("Kurumsal imza (opsiyonel)")
    imza = st.text_area(
        "İmza şablonu",
        placeholder="Ad Soyad\nUnvan\nŞirket\nTelefon / E-posta",
        height=120,
    )

mod = st.radio("Mail Türü", ["Yeni Mail", "Mail Yanıtı"], horizontal=True)
cikti_dili = st.selectbox("Dil Seçimi (çıktı dili)", DILLER, index=0)

sablon = st.selectbox("Hazır Şablon (opsiyonel)", list(SABLONLAR.keys()), index=0)
varsayilan_talep = SABLONLAR.get(sablon, "")

kullanici_talebi = st.text_area(
    "Ne Demek İstiyorsunuz?",
    value=varsayilan_talep,
    height=130,
    placeholder="Örn. Toplantıyı gelecek haftaya ertelemek istediğimi nazikçe söyle.",
)

yanitlanacak = ""
if mod == "Mail Yanıtı":
    yanitlanacak = st.text_area(
        "Yanıtlanacak Mail",
        height=180,
        placeholder="Yanıtlamak istediğiniz e-postanın gövdesini buraya yapıştırın.",
    )

col1, col2 = st.columns(2)
with col1:
    gonderen = st.text_input("Adınız (Opsiyonel)")
with col2:
    alici = st.text_input("Alıcı Adı (Opsiyonel)")

alici_hitap = st.radio(
    "Alıcı Hitabı (Opsiyonel)",
    ALICI_HITAPLARI,
    index=0,
    horizontal=True,
)

olustur = st.button("Maili Oluştur", type="primary", use_container_width=True)


if "son_payload" not in st.session_state:
    st.session_state.son_payload = None
if "son_cikti" not in st.session_state:
    st.session_state.son_cikti = ""


if olustur:
    if not kullanici_talebi.strip():
        st.warning("Lütfen ne demek istediğinizi kısaca yazın.")
    elif mod == "Mail Yanıtı" and not yanitlanacak.strip():
        st.warning("Mail Yanıtı modunda yanıtlanacak maili yapıştırmanız gerekir.")
    else:
        payload = dict(
            mod=mod,
            cikti_dili=cikti_dili,
            kullanici_talebi=kullanici_talebi,
            yanitlanacak=yanitlanacak,
            gonderen=gonderen,
            alici=alici,
            alici_hitap=alici_hitap,
            ton=ton,
            uzunluk=uzunluk,
            kategori=kategori,
            imza=imza,
            konu_onerisi=konu_onerisi,
        )
        with st.spinner("Mail üretiliyor..."):
            try:
                st.session_state.son_cikti = mail_uret(payload)
                st.session_state.son_payload = payload
            except Exception as e:
                st.error(f"Üretim sırasında bir hata oluştu: {e}")


if st.session_state.son_cikti:
    st.divider()
    st.subheader("Üretilen E-posta")
    st.code(st.session_state.son_cikti, language="markdown")
    st.caption("Sağ üstteki simgeye basarak çıktıyı kopyalayabilirsiniz.")

    st.divider()
    st.subheader("Yeniden Üret")
    varyant = st.selectbox("Varyant", YENIDEN_URETIM_VARYANTLARI, index=0)
    if st.button("Yeniden Oluştur", use_container_width=True):
        with st.spinner("Yeniden üretiliyor..."):
            try:
                st.session_state.son_cikti = mail_uret(
                    st.session_state.son_payload, varyant=varyant
                )
                st.rerun()
            except Exception as e:
                st.error(f"Üretim sırasında bir hata oluştu: {e}")
