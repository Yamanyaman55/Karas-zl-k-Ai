import streamlit as st

st.title("🧪 Streamlit Test Uygulaması")
st.write("Bu bir test uygulamasıdır.")

# Basit form
with st.form("test_form"):
    name = st.text_input("Adınız:")
    age = st.slider("Yaşınız:", 0, 100, 25)
    submitted = st.form_submit_button("Gönder")

if submitted:
    st.success(f"Merhaba {name}! Yaşınız: {age}")
    st.balloons() 