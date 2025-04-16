import streamlit as st 
import openai
import fitz  # PyMuPDF

st.set_page_config(page_title="Health Literacy Assistant", page_icon="🩺")
st.title("🧠 Global Health Literacy Assistant")

uploaded_file = st.file_uploader("📄 Upload a medical document (PDF)", type=["pdf"])
input_text = st.text_area("✏️ Or paste medical text here:")
language = st.selectbox("🌐 Output language", ["English", "Spanish", "Swahili", "Arabic"])
reading_level = st.selectbox("📚 Target reading level", ["6th grade", "Basic adult", "Teen", "College"])

if st.button("🔄 Simplify"):
    if uploaded_file:
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        input_text = "\n".join([page.get_text() for page in pdf_doc])

    if not input_text:
        st.warning("Please provide some input.")
    else:
        prompt = f"""
        You are a health literacy assistant.
        Rewrite the following medical content in {language} at a {reading_level} reading level.
        Use simple language, short sentences, and explain all medical terms clearly.

        Content:
        {input_text}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        output = response["choices"][0]["message"]["content"]
        st.markdown("### 🩺 Simplified Explanation")
        st.write(output)
