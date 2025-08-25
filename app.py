import streamlit as st
from utils.loaders import load_file, load_url
from utils.chunker import chunk_docspip 
from utils.rag import build_vector_store, get_rag_chain

st.set_page_config(page_title="AI Study Guide", page_icon="📚", layout="wide")

st.title("📚 AI-Powered Study Guide (RAG)")
st.markdown("Upload your notes or paste a link, then ask questions with AI.")

# --- Input section
st.sidebar.header("📂 Data Source")

upload_file = st.sidebar.file_uploader("Upload file", type=["pdf", "docx", "txt"])
url_input = st.sidebar.text_input("...or paste a website / ChatGPT link")

if upload_file or url_input:
    st.success("✅ Data source ready!")

    # --- Load docs
    if upload_file:
        with open(upload_file.name, "wb") as f:
            f.write(upload_file.getbuffer())
        docs = load_file(upload_file.name)

    elif url_input:
        docs = load_url(url_input)

    # --- Chunking
    st.sidebar.write("🔄 Processing chunks...")
    chunks = chunk_docs(docs)

    # --- Build vector DB
    vectorstore = build_vector_store(chunks)
    qa_chain = get_rag_chain(vectorstore)

    # --- User Q&A
    st.subheader("💬 Ask your questions")
    query = st.text_input("Type your question here:")

    if query:
        with st.spinner("Thinking..."):
            answer = qa_chain.run(query)
        st.write("### 🧠 Answer:")
        st.write(answer)

else:
    st.info("👈 Upload a file or paste a link to begin.")
