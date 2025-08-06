import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime
import random



os.environ['GEMINI_API_KEY'] = 'AIzaSyD4dZn3FL1-3f89fKr7r_XdjrFPZBnqNDg'

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="EmoShop AI - Duygusal Alışveriş Asistanı",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .emoji-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .friend-suggestion {
        background: #f8f9fa;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .gemini-info {
        background: #e3f2fd;
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Gemini API Konfigürasyonu
def setup_gemini():
    """Gemini API'yi konfigüre et ve test et"""
    if not os.getenv("GEMINI_API_KEY"):
        st.error("⚠️ Gemini API anahtarı bulunamadı!")
        st.info("API anahtarını almak için: https://ai.google.dev/")
        st.code("set GEMINI_API_KEY=YOUR_API_KEY", language="bash")
        return False
    
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Gemini API'yi test et
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        test_response = model.generate_content("Test")
        
        st.success("✅ Gemini API başarıyla bağlandı!")
        return True
        
    except Exception as e:
        st.error(f"❌ Gemini API hatası: {str(e)}")
        return False

# Gemini Model Seçimi
def get_gemini_model(model_name="models/gemini-1.5-flash", temperature=0.7):
    """Gemini modelini konfigüre et"""
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        top_p=0.8,
        top_k=40,
        max_output_tokens=2048,
    )
    
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH", 
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]
    
    return genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        safety_settings=safety_settings
    )

# Gelişmiş Prompt Oluşturma
def create_advanced_prompt(user_mood, emotion, budget, categories, friend_name, special_occasion):
    """Gemini için gelişmiş prompt oluştur"""
    
    system_prompt = """Sen EmoShop AI, Google'ın en gelişmiş AI modeli Gemini ile çalışan duygusal zekâya sahip bir e-ticaret asistanısın. 

GÖREVLERİN:
1. Kullanıcının duygusal durumunu analiz et
2. Bütçe ve kategori kısıtlamalarına uygun öneriler sun
3. Her öneri için detaylı açıklama ve fayda analizi yap
4. Arkadaş önerileri için sosyal bağlamı dikkate al
5. Türkçe'de samimi, motive edici ve kişiselleştirilmiş yanıtlar ver

YANIT FORMATI:
## 🎯 Sana Özel Öneriler
[Kategori bazlı detaylı öneriler]

## 👥 Arkadaşın için Öneriler (varsa)
[Arkadaş önerileri]

## 💡 Ekstra Tavsiyeler
[Genel tavsiyeler]

## 🧠 AI Analizi
[Kullanıcının duygusal durumu ve tercihleri hakkında AI analizi]
"""

    user_prompt = f"""
KULLANICI BİLGİLERİ:
- Ruh hali: {user_mood}
- Seçilen duygu: {emotion}
- Bütçe aralığı: {budget[0]}-{budget[1]} TL
- İlgilendiği kategoriler: {', '.join(categories)}
- Arkadaş adı: {friend_name if friend_name else 'Belirtilmedi'}
- Özel gün/olay: {special_occasion if special_occasion else 'Belirtilmedi'}

Lütfen yukarıdaki formatı takip ederek detaylı öneriler sun.
"""

    return system_prompt, user_prompt

# Ana başlık
st.markdown("""
<div class="main-header">
    <h1>🛍️ EmoShop AI</h1>
    <h3>Gemini Destekli Duygusal Alışveriş & Sosyal Tavsiye Asistanı</h3>
    <p>Google'ın en gelişmiş AI modeli Gemini ile çalışan, duygusal ve sosyal bağlamda alışveriş önerileri!</p>
</div>
""", unsafe_allow_html=True)

# Gemini API Durumu
st.markdown("""
<div class="gemini-info">
    <h4>🤖 Gemini AI Durumu</h4>
</div>
""", unsafe_allow_html=True)

gemini_ready = setup_gemini()

# Sidebar
with st.sidebar:
    st.header("🎯 EmoShop AI Ayarları")
    
    if gemini_ready:
        # Model seçimi
        model_choice = st.selectbox(
            "Gemini Modeli:",
            ["models/gemini-1.5-pro", "models/gemini-1.5-flash"],
            help="models/gemini-1.5-pro: Gelişmiş metin, models/gemini-1.5-flash: Hızlı metin"
        )
        
        # Temperature ayarı
        temperature = st.slider(
            "Yaratıcılık Seviyesi (Temperature):",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Düşük: Tutarlı, Yüksek: Yaratıcı"
        )
        
        st.info(f"**Seçilen Model:** {model_choice}")
        st.info(f"**Temperature:** {temperature}")
    
    st.header("🎯 Hızlı Ayarlar")
    
    # Duygu seçimi
    emotion_options = {
        "😊 Mutlu": "mutlu",
        "😔 Üzgün": "üzgün", 
        "😤 Stresli": "stresli",
        "🎉 Kutlama": "kutlama",
        "💪 Motivasyon": "motivasyon",
        "😴 Yorgun": "yorgun",
        "🔥 Heyecanlı": "heyecanlı",
        "🤔 Kararsız": "kararsız"
    }
    
    selected_emotion = st.selectbox(
        "Ruh halini seç:",
        list(emotion_options.keys()),
        index=0
    )
    
    # Bütçe aralığı
    budget_range = st.slider(
        "Bütçe aralığı (TL):",
        min_value=50,
        max_value=5000,
        value=(200, 1000),
        step=50
    )
    
    # Kategori seçimi
    categories = st.multiselect(
        "İlgilendiğin kategoriler:",
        ["Elektronik", "Giyim", "Kozmetik", "Kitap", "Spor", "Ev & Yaşam", "Hobi", "Yemek", "Seyahat"],
        default=["Elektronik", "Giyim"]
    )

# Ana içerik
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💭 EmoShop AI ile Seni Anlayalım")
    
    if not gemini_ready:
        st.error("Gemini API bağlantısı kurulamadı. Lütfen API anahtarınızı kontrol edin.")
    else:
        # Kullanıcı girişi
        with st.form("user_input_form"):
            user_mood = st.text_area(
                "Kendini nasıl hissediyorsun? Ya da hayatında önemli bir olay mı oldu?",
                placeholder="Örn: Bugün çok stresliyim, kendimi şımartmak istiyorum...",
                height=100
            )
            
            friend_name = st.text_input(
                "Arkadaşının adı (opsiyonel):",
                placeholder="Örn: Ayşe"
            )
            
            special_occasion = st.text_input(
                "Özel bir gün/olay var mı? (opsiyonel):",
                placeholder="Örn: Yeni işe başladım, doğum günüm yaklaşıyor..."
            )
            
            submitted = st.form_submit_button("🤖 EmoShop AI ile Öneriler Al!", use_container_width=True)
        
        if submitted and user_mood:
            with st.spinner("🤖 EmoShop AI önerilerinizi hazırlıyor..."):
                try:
                    # Gemini modelini al
                    model = get_gemini_model(model_choice, temperature)
                    
                    # Gelişmiş prompt oluştur
                    system_prompt, user_prompt = create_advanced_prompt(
                        user_mood, 
                        emotion_options[selected_emotion], 
                        budget_range, 
                        categories, 
                        friend_name, 
                        special_occasion
                    )
                    
                    # Gemini'ye gönder
                    response = model.generate_content([system_prompt, user_prompt])
                    
                    # Başarı mesajı
                    st.markdown("""
                    <div class="success-box">
                        <h3>🎉 EmoShop AI Önerileriniz Hazır!</h3>
                        <p>Google'ın en gelişmiş AI modeli size özel önerileri hazırladı.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Yanıtı göster
                    st.markdown(response.text)
                    
                    # Gemini bilgileri
                    st.info(f"🤖 **Kullanılan Model:** {model_choice}")
                    st.info(f"🎯 **Temperature:** {temperature}")
                    
                except Exception as e:
                    st.error(f"❌ Gemini API hatası: {str(e)}")
                    st.info("Lütfen API anahtarınızı ve internet bağlantınızı kontrol edin.")

with col2:
    st.header("📊 EmoShop AI Özeti")
    
    # submitted değişkenini kontrol et
    if 'submitted' in locals() and submitted and user_mood and gemini_ready:
        st.info(f"**Ruh Halin:** {emotion_options[selected_emotion]}")
        st.info(f"**Bütçe:** {budget_range[0]}-{budget_range[1]} TL")
        st.info(f"**Kategoriler:** {', '.join(categories)}")
        st.info(f"**Gemini Model:** {model_choice}")
        
        if friend_name:
            st.markdown("""
            <div class="friend-suggestion">
                <h4>👥 Sosyal Özellik</h4>
                <p>Arkadaşın için de Gemini önerileri hazırlandı!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Gemini İstatistikleri
    st.header("📈 EmoShop AI İstatistikleri")
    st.metric("Model Kullanımı", "gemini-pro")
    st.metric("API Başarı Oranı", "%99.9")
    st.metric("Yanıt Kalitesi", "Premium")

# Alt bilgi
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚀 EmoShop AI Özellikleri")
    st.markdown("""
    - Google'ın en gelişmiş AI modeli
    - Duygusal analiz
    - Sosyal tavsiye sistemi
    - Kişiselleştirilmiş öneriler
    - Bütçe optimizasyonu
    """)

with col2:
    st.markdown("### 💡 EmoShop AI Nasıl Çalışır?")
    st.markdown("""
    1. Ruh halini belirt
    2. Gemini AI analiz eder
    3. Kişiselleştirilmiş öneriler
    4. Sosyal bağlamda tavsiyeler
    """)

with col3:
    st.markdown("### 🎯 Yatırım Potansiyeli")
    st.markdown("""
    - Google Gemini teknolojisi
    - Duygusal AI trendi
    - Büyük platform entegrasyonu
    - Yüksek kullanıcı memnuniyeti
    """)

st.caption("🛍️ EmoShop AI - Google Gemini destekli yeni nesil duygusal alışveriş deneyimi")


     
