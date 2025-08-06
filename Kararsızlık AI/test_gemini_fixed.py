import google.generativeai as genai
import os

# API anahtarını ayarla
os.environ['GEMINI_API_KEY'] = 'AIzaSyD4dZn3FL1-3f89fKr7r_XdjrFPZBnqNDg'

try:
    # Gemini'yi konfigüre et
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Kullanılabilir modelleri listele
    print("🔍 Kullanılabilir modeller:")
    models = genai.list_models()
    for model in models:
        print(f"  - {model.name}")
    
    # Test modeli oluştur (daha hafif model)
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    
    # Basit test
    response = model.generate_content("Merhaba, bu bir test mesajıdır.")
    
    print("\n✅ API Anahtarı Çalışıyor!")
    print("Yanıt:", response.text)
    
except Exception as e:
    print(f"❌ Hata: {str(e)}")
    print("\n🔧 Çözüm önerileri:")
    print("1. API anahtarını Google AI Studio'dan yeniden al")
    print("2. Model adını 'models/gemini-pro' olarak kullan")
    print("3. API anahtarının doğru kopyalandığından emin ol") 