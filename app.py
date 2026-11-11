import hashlib
from html import escape

import streamlit as st

from rag import ask_question, process_pdf


st.set_page_config(
    page_title="PDF RAG | Document Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #17243a;
        --muted: #64748b;
        --line: #e4eaf2;
        --blue: #4263eb;
        --blue-dark: #3150cc;
        --canvas: #f5f7fb;
        --text-color: #17243a;
        --background-color: #f5f7fb;
        --secondary-background-color: #ffffff;
        --primary-color: #4263eb;
    }

    html, body, [class*="css"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                     BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .stApp {
        background: var(--canvas);
        color: var(--ink) !important;
        color-scheme: light;
    }
/* Chat input outer container */
[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D8E0EC !important;
    border-radius: 14px !important;
    box-shadow: 0 8px 30px #17243a12;
}

/* Inner input container */
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] [data-baseweb="textarea"] {
    background-color: #FFFFFF !important;
}

/* Text area */
[data-testid="stChatInput"] textarea {
    color: #17243a !important;
    background-color: #FFFFFF !important;
    caret-color: #4263eb !important;
}

/* Placeholder */
[data-testid="stChatInput"] textarea::placeholder {
    color: #718096 !important;
    opacity: 1;
}




    [data-testid="stMainBlockContainer"],
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"],
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] strong {
        color: var(--ink) !important;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"],
    [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] p {
        color: var(--muted) !important;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 1280px;
        padding: 2.4rem 3rem 5rem;
    }
    [data-testid="stSidebar"] {
        background: #111d32;
        border-right: 1px solid #26354d;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: #111d32;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #dbe5f3;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: #dbe5f3;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #93a4bd;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.55rem 0 1.65rem;
        margin-bottom: 1.4rem;
        border-bottom: 1px solid #293850;
    }
    .brand-mark {
        width: 40px;
        height: 40px;
        display: grid;
        place-items: center;
        border-radius: 12px;
        color: white;
        font-weight: 800;
        background: linear-gradient(145deg, #6d83ff, #4263eb);
        box-shadow: 0 8px 20px #4263eb44;
    }
    .brand-name {
        color: #f8fafc;
        font-size: 0.98rem;
        font-weight: 750;
        letter-spacing: 0.02em;
        line-height: 1.2;
    }
    .brand-name small {
        display: block;
        margin-top: 5px;
        color: #91a1b9;
        font-size: 0.62rem;
        font-weight: 650;
        letter-spacing: 0.13em;
    }
    .side-label, .eyebrow {
        color: #71839f;
        font-size: 0.68rem;
        font-weight: 750;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }
    .side-label {
        margin: 0.4rem 0 0.8rem;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        border: 1px dashed #536581;
        border-radius: 12px;
        background: #17253b;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
        color: #e8effa;
        border-color: #536581;
        background: #263650;
    }
    [data-testid="stSidebar"] .stButton > button {
        min-height: 2.8rem;
        border: 0;
        border-radius: 10px;
        color: white;
        background: linear-gradient(100deg, #526ff3, #4263eb);
        font-weight: 700;
        transition: transform 120ms ease, filter 120ms ease;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
    }
    [data-testid="stSidebar"] .stButton > button:disabled {
        color: #91a1b9;
        background: #293850;
    }
    .sidebar-divider {
        height: 1px;
        margin: 1.35rem 0;
        background: #293850;
    }
    .sidebar-note {
        color: #91a1b9;
        font-size: 0.78rem;
        line-height: 1.55;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 6px 10px;
        border: 1px solid #bcebd7;
        border-radius: 999px;
        color: #14764d;
        background: #e9f8f1;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.04em;
        white-space: nowrap;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #21a675;
    }
    .status-pill-warn {
        border-color: #f4d28a;
        color: #8a5a08;
        background: #fff6df;
    }
    .hero {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1.5rem;
        margin: 0.1rem 0 2rem;
    }
    .hero h1 {
        margin: 0.45rem 0 0.5rem;
        color: var(--ink);
        font-size: clamp(2rem, 3.5vw, 2.8rem);
        font-weight: 760;
        letter-spacing: -0.055em;
        line-height: 1.1;
    }
    .hero-copy {
        max-width: 650px;
        margin: 0;
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.65;
    }
    .panel {
        padding: 1.25rem 1.4rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: #fff;
        box-shadow: 0 8px 28px #17243a08;
    }
    .document-label {
        margin-bottom: 0.25rem;
        color: #8290a4;
        font-size: 0.65rem;
        font-weight: 750;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    .document-title {
        color: var(--ink);
        font-size: 0.98rem;
        font-weight: 700;
        overflow-wrap: anywhere;
    }
    .empty-state {
        margin-top: 2rem;
        padding: clamp(2rem, 6vw, 4.5rem) 2rem;
        border: 1px solid var(--line);
        border-radius: 20px;
        background:
            radial-gradient(ellipse at 50% 0%, #edf1ff 0%, transparent 58%),
            #fff;
        text-align: center;
        box-shadow: 0 12px 35px #17243a08;
    }
    .empty-icon {
        display: grid;
        width: 58px;
        height: 58px;
        place-items: center;
        margin: 0 auto 1.1rem;
        border: 1px solid #dce4ff;
        border-radius: 18px;
        color: var(--blue);
        background: #f1f4ff;
        font-size: 1.3rem;
        font-weight: 800;
    }
    .empty-state h3 {
        margin: 0 0 0.45rem;
        color: var(--ink);
        font-size: 1.25rem;
        font-weight: 730;
    }
    .empty-state p {
        max-width: 530px;
        margin: 0 auto;
        color: var(--muted);
        font-size: 0.93rem;
        line-height: 1.65;
    }
    .stButton > button {
        border-radius: 9px;
        font-weight: 650;
    }
    [data-testid="stMainBlockContainer"] .stButton > button {
        border: 1px solid #d7dfec !important;
        color: #23344e !important;
        background: #ffffff !important;
    }
    [data-testid="stMainBlockContainer"] .stButton > button p,
    [data-testid="stMainBlockContainer"] .stButton > button span {
        color: inherit !important;
    }
    [data-testid="stMainBlockContainer"] .stButton > button:hover {
        border-color: #b8c7f5 !important;
        color: #2948c7 !important;
        background: #f0f4ff !important;
    }
    [data-testid="stMainBlockContainer"] .stButton > button:focus-visible {
        outline: 3px solid #8da3ff !important;
        outline-offset: 2px;
    }
    [data-testid="stChatMessage"] {
        padding: 1.1rem 1.25rem;
        border: 1px solid var(--line);
        border-radius: 15px;
        background: #fff;
        box-shadow: 0 5px 18px #17243a06;
    }
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {
        color: #17243a !important;
    }
    [data-testid="stChatInput"] {
        border-color: #d8e0ec;
        border-radius: 14px;
        background: #ffffff;
        box-shadow: 0 8px 30px #17243a12;
    }
    [data-testid="stChatInput"] textarea {
        color: #17243a !important;
        background: #ffffff !important;
        caret-color: #4263eb;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #718096 !important;
        opacity: 1;
    }
    [data-testid="stExpander"] {
        border-color: #e7ecf3;
        border-radius: 10px;
        background: #fbfcfe;
    }
    @media (max-width: 760px) {
        [data-testid="stMainBlockContainer"] {
            padding: 1.5rem 1rem 4rem;
        }
        .hero {
            display: block;
        }
        .hero .status-pill {
            margin-top: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.session_state.setdefault("processed", False)
st.session_state.setdefault("chat_history", [])

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">P</div>
            <div class="brand-name">PDF RAG<small>DOCUMENT WORKSPACE</small></div>
        </div>
        <div class="side-label">Your document</div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Upload a searchable PDF",
        type=["pdf"],
        help="Text-based PDFs work best. Scanned PDFs need OCR first.",
    )
    st.caption("PDF files only · Maximum size follows your Streamlit settings")

    if uploaded_file:
        st.caption(f"Selected: {uploaded_file.name}")

    process_clicked = st.button(
        "Index document",
        type="primary",
        use_container_width=True,
        disabled=uploaded_file is None,
    )

    selected_hash = (
        hashlib.sha256(uploaded_file.getvalue()).hexdigest()
        if uploaded_file
        else None
    )

    if process_clicked and uploaded_file:
        try:
            with st.spinner("Extracting, chunking, and indexing your PDF..."):
                result = process_pdf(uploaded_file.getvalue())

            st.session_state.collection_name = result["collection_name"]
            st.session_state.document_hash = result["document_hash"]
            st.session_state.pdf_name = uploaded_file.name
            st.session_state.total_pages = result["total_pages"]
            st.session_state.total_chunks = result["total_chunks"]
            st.session_state.processed = True
            st.session_state.chat_history = []
            selected_hash = result["document_hash"]

            st.success("Your document is ready.")
        except Exception as error:
            st.error(f"Could not index this PDF: {error}")

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-label">Index status</div>', unsafe_allow_html=True)

    if st.session_state.processed:
        selected_document_is_indexed = (
            uploaded_file is None
            or selected_hash == st.session_state.document_hash
        )
        if selected_document_is_indexed:
            st.markdown(
                '<span class="status-pill"><span class="status-dot"></span>'
                'INDEXED</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<span class="status-pill status-pill-warn">'
                '<span class="status-dot" style="background:#d2931a"></span>'
                'REINDEX NEEDED</span>',
                unsafe_allow_html=True,
            )
        st.markdown(f"**{st.session_state.pdf_name}**")
        st.caption(
            f"{st.session_state.total_pages} pages · "
            f"{st.session_state.total_chunks} searchable chunks"
        )
    else:
        st.markdown(
            '<span class="status-pill" style="color:#aab8ca;background:#1a2940;'
            'border-color:#34445f"><span class="status-dot" '
            'style="background:#8797ad"></span>AWAITING PDF</span>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="sidebar-note">Upload a PDF and index it to start a '
            'document-grounded conversation.</p>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-note">Answers are generated from retrieved passages '
        'in your document. Expand a source to review the supporting text.</p>',
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="hero">
        <div>
            <div class="eyebrow">DOCUMENT INTELLIGENCE</div>
            <h1>Ask your PDF.</h1>
            <p class="hero-copy">Get clear, source-backed answers from your
            document. Upload once, ask naturally, and inspect the passages
            behind every response.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

document_is_current = (
    st.session_state.processed
    and (
        uploaded_file is None
        or selected_hash == st.session_state.document_hash
    )
)

if st.session_state.processed and uploaded_file and not document_is_current:
    st.warning(
        "A different PDF is selected. Choose **Index document** in the sidebar "
        "before asking questions about it."
    )

if not st.session_state.processed:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">PDF</div>
            <h3>Your document workspace starts here</h3>
            <p>Upload a searchable PDF in the left panel, then index it. The
            document will be split into passages and made searchable so you
            can ask focused questions and review the source pages.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif document_is_current:
    document_col, actions_col = st.columns([0.78, 0.22])
    with document_col:
        escaped_pdf_name = escape(st.session_state.pdf_name)
        st.markdown(
            f"""
            <div class="panel">
                <div class="document-label">Active document</div>
                <div class="document-title">{escaped_pdf_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with actions_col:
        if st.session_state.chat_history and st.button(
            "Clear conversation",
            use_container_width=True,
        ):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("#### Start with a question")
        st.caption("Choose a prompt or write your own below.")
        prompt_columns = st.columns(3)
        suggested_prompts = [
            "Summarize this document",
            "What are the key dates?",
            "What are the main takeaways?",
        ]
        quick_question = None
        for column, prompt in zip(prompt_columns, suggested_prompts):
            if column.button(prompt, use_container_width=True):
                quick_question = prompt
    else:
        quick_question = None

    for message_index, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                for source_index, source in enumerate(
                    message.get("sources", []),
                    start=1,
                ):
                    with st.expander(
                        f"Source {source_index} · page {source['page']} "
                        f"· score {source['score']:.3f}"
                    ):
                        st.write(source["text"])

    

    question = st.chat_input("Ask a question about this document...")
    question = question or quick_question

    if question:
        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Finding relevant passages and drafting an answer..."):
                try:
                    result = ask_question(
                        question=question,
                        collection_name=st.session_state.collection_name,
                        top_k=3,
                    )
                    st.markdown(result["answer"])

                    for source_index, source in enumerate(
                        result["sources"],
                        start=1,
                    ):
                        with st.expander(
                            f"Source {source_index} · page {source['page']} "
                            f"· score {source['score']:.3f}"
                        ):
                            st.write(source["text"])

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": result["answer"],
                            "sources": result["sources"],
                        }
                    )
                except Exception as error:
                    st.error(f"Could not answer this question: {error}")
