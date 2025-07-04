import streamlit as st
import PyPDF2
import openai

st.set_page_config(page_title="AI Resume Enhancer", layout="centered")
st.title("🧠 AI Resume Enhancer (OpenAI GPT-3.5)")
st.write("Upload your resume (PDF or text), and get AI-powered enhancement suggestions instantly.")

client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def enhance_resume(text):
    prompt = f"Improve the following resume content by rewriting weak sections and suggesting stronger wording:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content

def main():
    uploaded_file = st.file_uploader("📄 Upload your resume (.pdf or .txt)", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = uploaded_file.read().decode("utf-8")

        if st.button("✨ Enhance Resume"):
            with st.spinner("Improving your resume..."):
                improved = enhance_resume(resume_text)
            st.subheader("✅ Enhanced Resume Suggestions")
            st.text_area("Result", improved, height=400)

if __name__ == "__main__":
    main()
