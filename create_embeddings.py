import json
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Load JSON data
with open("final_output.json", "r") as f:
    data = json.load(f)

documents = []

# Patient info
patient_info = data.get("patient_info", {})
patient_text = f"""
Patient Information:
Name: {patient_info.get('name', 'N/A')}
Age: {patient_info.get('age', 'N/A')}
Gender: {patient_info.get('gender', 'N/A')}
Lab Number: {patient_info.get('lab_no', 'N/A')}
Collected: {patient_info.get('collected', 'N/A')}
Report Status: {patient_info.get('report_status', 'N/A')}
"""
documents.append(Document(page_content=patient_text, metadata={"type": "patient_info"}))

# Test results
for test in data.get("tests", []):
    test_text = f"""
Test: {test.get('test_name', 'N/A')}
Result: {test.get('result', 'N/A')}
Units: {test.get('units', 'N/A')}
Reference Range: {test.get('reference_range', 'N/A')}
"""
    documents.append(Document(
        page_content=test_text,
        metadata={"type": "test_result", "test_name": test.get('test_name', 'Unknown')}
    ))

# Create embeddings using HuggingFace model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store embeddings in Pinecone 
print("Creating embeddings and uploading to Pinecone...")
vector_store = PineconeVectorStore.from_documents(
    documents=documents,
    embedding=embeddings,
    index_name="reschatbot"  # index_name 
)

print("Embeddings successfully created and stored in Pinecone!")
print(f"Total {len(documents)} documents uploaded to cloud.")
