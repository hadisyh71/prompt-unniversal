import streamlit as st
from groq import Groq

# --- KONFIGURASI ---
st.set_page_config(page_title="AI Prompt Master", page_icon="🎨", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #E2E8F0; }
    h1 { color: #10B981; }
    .stButton>button { background: #10B981; color: white; font-weight: bold; width: 100%; }
    .stTextArea textarea { background-color: #1E293B; color: white; }
    </style>
""", unsafe_allow_html=True)

# --- API KEY ---
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    with st.sidebar:
        api_key = st.text_input("Groq API Key:", type="password")

# --- MAIN APP ---
st.title("🎨 AI Prompt Master (Llama 4 Powered)")

col1, col2 = st.columns(2)
with col1:
    target = st.selectbox("Target AI:", ("Midjourney v6", "Flux.1", "Dall-E 3", "Stable Diffusion XL", "Runway Gen-2"))
    style = st.selectbox("Style Visual:", ("Cinematic Realistic", "3D Pixar/Disney", "Anime Studio Ghibli", "Cyberpunk/Neon", "Dark Fantasy"))
with col2:
    ratio = st.selectbox("Rasio:", ("--ar 16:9 (Landscape)", "--ar 9:16 (Vertical)", "--ar 1:1 (Square)", "--ar 21:9 (Ultrawide)"))
    lighting = st.selectbox("Lighting:", ("Natural Lighting", "Cinematic Lighting", "Neon Lights", "Golden Hour", "Dark/Moody"))

idea = st.text_area("Ide Konsep (Boleh Bahasa Indonesia):", placeholder="Contoh: Kucing raksasa tidur di atas Monas saat hujan deras...", height=150)

if st.button("🪄 GENERATE PROMPT"):
    if not api_key: st.error("API Key belum diisi!"); st.stop()
    if not idea: st.warning("Isi idenya dulu bos!"); st.stop()

    client = Groq(api_key=api_key)
    
    with st.spinner("Sedang meracik prompt..."):
        try:
            sys_prompt = f"""
            Act as an Expert Prompt Engineer for {target}.
            Style: {style}. Lighting: {lighting}. Ratio: {ratio}.
            User Idea: '{idea}'.
            
            Task: Write a HIGHLY DETAILED prompt in English. 
            Include camera angles, textures, and artistic details. 
            Result should be a single prompt block ready to copy.
            """

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": sys_prompt}],
                model="llama-3.3-70b-versatile", # Model Teks Paling Cerdas di Groq
            )
            
            st.subheader("Hasil Prompt:")
            st.code(chat_completion.choices[0].message.content, language="markdown")
            
        except Exception as e:
            st.error(f"Error: {e}")
