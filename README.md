# medical-report-rag-chatbot

A complete Retrieval-Augmented Generation (RAG) pipeline that extracts structured medical information from PDF lab reports, converts it into JSON, generates embeddings, stores them in ChromaDB, and answers user queries using Google Gemini.  
This project demonstrates the full workflow:

PDF → JSON → Embeddings → Vector Store → RAG Chatbot

---

## 🚀 Features

- Extracts patient information and test results from medical PDFs.
- Cleans and structures data into a machine-friendly JSON format.
- Generates high-quality embeddings with `all-MiniLM-L6-v2`.
- Stores embeddings persistently using ChromaDB.
- RAG-powered chatbot using Google Gemini.
- Lightweight terminal-based assistant with basic chitchat handling.

---

## 📁 Project Structure

```

medical-report-rag-chatbot/
│
├── extract_data_pdf.py        # Parse and extract structured content from PDF
├── final_output.json          # JSON output generated from PDF
├── create_embeddings.py       # Embeddings + ChromaDB storage
├── chatbot.py                 # Interactive RAG chatbot
│
├── chroma_db/                 # Vector store files
├── input/
│   └── file.pdf               # Medical report input file
│
├── .env                       # Environment variables
├── requirements.txt
└── README.md

```

---

## ⚙️ End-to-End Pipeline

### 1. Extract Structured Data From PDF

Parses text, tables, patient details, and test results.

Command:
```

python extract_data_pdf.py

```

Output:
`final_output.json`

---

### 2. Create Embeddings and Store in ChromaDB

```

python create_embeddings.py

```

This script:

- Loads `final_output.json`
- Creates document embeddings
- Saves them in the `chroma_db` directory

---

### 3. Run the RAG Chatbot

```

python chatbot.py

```

Example:

```

You: What is the patient's bilirubin level?
Bot: 1.2 mg/dL

```

---

## 🔑 Environment Setup

Install dependencies:

```

pip install -r requirements.txt

```

`.env` file format:

```

GEMINI_API_KEY=your_api_key_here

```

---

## 🛠️ Tech Stack

- Python 3.10+
- pdfplumber
- Regular expressions (regex)
- sentence-transformers
- ChromaDB
- LangChain
- Google Gemini Flash
- python-dotenv

---

## 📘 Example Query Flow

1. User asks a question  
2. RAG retrieves the most relevant medical entries  
3. Gemini summarizes the retrieved context  
4. Chatbot returns a minimal, clean answer  

Example:
```

You: What is the patient's age?
Bot: 42

```

---

## 📦 Regenerate Requirements

```

pip freeze > requirements.txt

```

---

## 📢 Upcoming Enhancements

- Multi-page PDF support  
- Improved table segmentation  
- Medical reference insights  
- Streamlit web UI  

Stay tuned — more improvements coming soon.
