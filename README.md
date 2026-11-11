# AskMyPDF AI

A Streamlit app that lets you upload a searchable PDF and ask questions about
it. It extracts page text, splits it into overlapping chunks, embeds the chunks
with `all-MiniLM-L6-v2`, stores them in Qdrant, retrieves the most relevant
chunks for each question, and passes those chunks as context to Groq.

## Setup on Windows

1. Open a terminal in the `pdf_rag_system` folder and create a virtual
   environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set your Qdrant and Groq credentials.
   `QDRANT_API_KEY` may be left blank when connecting to a Qdrant instance
   that does not require authentication.

4. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

Using `python -m streamlit` ensures Streamlit runs with the same Python
interpreter where you installed the requirements. Keep the virtual environment
activated while installing dependencies and starting the app.

Upload a PDF and choose **Process PDF** before entering a question. Scanned PDFs
without selectable text need OCR before upload. The app does not delete or
replace other Qdrant collections; each PDF is indexed in a collection derived
from its content hash.
