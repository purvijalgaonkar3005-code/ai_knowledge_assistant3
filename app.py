import streamlit as st
from groq import Groq
from pdf_reader import read_pdf

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("📚 AI Knowledge Assistant")

    st.write(
        "Upload a PDF and interact with it using AI."
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# MAIN TITLE
# -----------------------------
st.title("📚 AI Knowledge Assistant")
st.subheader(
    "Upload documents and chat with your knowledge base"
)

# -----------------------------
# PDF UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "📄 Upload a PDF Document",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file:
    pdf_text = read_pdf(uploaded_file)

    st.success("✅ PDF uploaded successfully!")

    st.info(f"""
📄 File Name: {uploaded_file.name}

📊 File Size: {round(uploaded_file.size/1024, 2)} KB

📝 Total Characters Extracted: {len(pdf_text)}
""")

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# -----------------------------
# CHAT MEMORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------
prompt = st.chat_input(
    "Ask a question about the uploaded PDF..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    messages = []

    if pdf_text:
        messages.append(
            {
                "role": "system",
                "content": f"""
You are an AI Knowledge Assistant.

Answer questions ONLY using information from the uploaded PDF.

If the answer is not available in the document,
say:

'I could not find that information in the uploaded document.'

PDF Content:

{pdf_text}
"""
            }
        )

    messages.extend(st.session_state.messages)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    with st.chat_message("assistant"):
        st.markdown(reply)

# -----------------------------
# DOWNLOAD CHAT HISTORY
# -----------------------------
if st.session_state.messages:

    chat_history = ""

    for msg in st.session_state.messages:
        chat_history += (
            f"{msg['role']}: "
            f"{msg['content']}\n\n"
        )

    st.download_button(
        label="📥 Download Chat History",
        data=chat_history,
        file_name="chat_history.txt",
        mime="text/plain"
    )

