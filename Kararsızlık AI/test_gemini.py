import google.generativeai as genai
import os

# API anahtarını ayarla
os.environ['GEMINI_API_KEY'] = 'AIzaSyDmGDIr1QHyIfmOQm0w-PUvmoDjzfL9J_8'

try:
    # Gemini'yi konfigüre et
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Test modeli oluştur
    model = genai.GenerativeModel("gemini-pro")
    
    # Basit test
    response = model.generate_content("Merhaba, bu bir test mesajıdır.")
    
    print("✅ API Anahtarı Çalışıyor!")
    print("Yanıt:", response.text)
    
except Exception as e:
    print(f"❌ Hata: {str(e)}")
    print("\n🔧 Çözüm önerileri:")
    print("1. API anahtarını Google AI Studio'dan yeniden al")
    print("2. Google Cloud Console'da Generative Language API'yi etkinleştir")
    print("3. API anahtarının doğru kopyalandığından emin ol") 