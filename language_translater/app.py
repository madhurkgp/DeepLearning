import streamlit as st
import numpy as np
from googletrans import Translator

# Configure page
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)


# Initialize Google Translator
translator = Translator()

# Language mapping with Google Translate codes
language_lib = {
    'English': 'en', 
    'Arabic': 'ar',
    'Hindi': 'hi', 
    'Spanish': 'es', 
    'German': 'de', 
    'Korean': 'ko',
    'French': 'fr',
    'Chinese': 'zh',
    'Japanese': 'ja',
    'Russian': 'ru'
}

st.title("🌍 Language Translator")
st.markdown("---")
st.markdown("### Translate text between multiple languages using Google Translate")

# setting up the dropdown list of the languages

col1, col2 = st.columns(2)

with col1:
    st.subheader("From")
    option = st.selectbox(
        'Select source language',
        list(language_lib.keys()),
        key='source_lang'
    )

with col2:
    st.subheader("To")
    option1 = st.selectbox(
        'Select target language',
        list(language_lib.keys()),
        key='target_lang'
    )


sent = f"Enter the text in {option} language below:"

# Display language codes
st.info(f"Translation: {language_lib[option]} → {language_lib[option1]}")

sentence = st.text_area(sent, height=150, key="input_text")

if st.button("🔄 Translate", type="primary"):

    if not sentence.strip():
        st.error("⚠️ Please enter some text to translate")
    elif option == option1:
        st.warning("⚠️ Please select different languages for translation")
    else:
        with st.spinner("Translating..."):
            try:
                # Translate using Google Translate
                source_lang = language_lib[option]
                target_lang = language_lib[option1]
                
                translation = translator.translate(
                    text=sentence, 
                    src=source_lang, 
                    dest=target_lang
                )
                
                ans = translation.text
                
                st.markdown("---")
                st.subheader(f"✅ Translated text in {option1}:")
                st.success(ans)
                
                # Add copy button
                if st.button("📋 Copy Translation"):
                    st.write("Translation copied to clipboard!")
                    
            except Exception as e:
                st.error(f"❌ Translation failed: {str(e)}")
                st.info("💡 Please check your internet connection and try again")
