import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# ChitChat Dictionary
CHITCHAT = {
    "hi": "Hello. How can I help you?",
    "hello": "Hello. How may I assist you?",
    "hey": "Hello. What can I do for you?",
    "bye": "Goodbye. Take care.",
    "thanks": "You are welcome."
}

# Function: Extract Proper Text from Gemini Responses
def extract_text(content):
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        texts = []
        for part in content:
            if isinstance(part, dict) and "text" in part:
                texts.append(part["text"])
            else:
                texts.append(str(part))
        return " ".join(texts).strip()
    return str(content)

# Initialize embeddings 
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Connect to Pinecone vector store 
print("Connecting to Pinecone cloud database...")
vector_store = PineconeVectorStore(
    index_name="reschatbot",
    embedding=embeddings
)
print("Connected to Pinecone successfully!")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0.3,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

print("\nMedical Chatbot (Pinecone Version)")
print("=" * 50)
print("Ask questions about the medical report.")
print("Type 'quit' or 'exit' to stop.\n")

while True:
    user_query = input("You: ").strip()
    
    if not user_query:
        continue
    
    if user_query.lower() in ["quit", "exit"]:
        print("Bot: Goodbye!")
        break
    
    # Check for chitchat
    if user_query.lower() in CHITCHAT:
        print(f"Bot: {CHITCHAT[user_query.lower()]}")
        continue
    
    # Retrieve relevant documents from Pinecone cloud
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.invoke(user_query)
    
    if not relevant_docs:
        print("Bot: I could not find relevant information in the medical report.")
        continue
    
    # Combine retrieved context
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # Create prompt for Gemini
    prompt = f"""
You are a helpful medical assistant. Use the following medical report information to answer the user's question.

Medical Report Data:
{context}

User Question: {user_query}

Instructions:
- Answer based ONLY on the provided medical data
- If information is not available, say so clearly
- Be concise and accurate
- Use medical terminology appropriately

Answer:
"""
    
    # Get response from Gemini
    response = llm.invoke(prompt)
    answer = extract_text(response.content)
    
    print(f"Bot: {answer}\n")
