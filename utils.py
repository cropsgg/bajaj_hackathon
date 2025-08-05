import requests
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredEmailLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from prompts import QA_PROMPT

def download_document(url: str) -> bytes:
    """Download document from URL (handles blob with SAS)."""
    response = requests.get(url)
    response.raise_for_status()  # Raise error if download fails
    return response.content

def load_and_chunk_document(content: bytes, url: str) -> list:
    """Load and chunk document based on format. Supports PDF, DOCX, Email."""
    # Extract file extension, handling URLs with query parameters
    url_without_params = url.split('?')[0]  # Remove query parameters
    ext = url_without_params.lower().split('.')[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    if ext == 'pdf':
        loader = PyPDFLoader(tmp_path)
    elif ext == 'docx':
        loader = Docx2txtLoader(tmp_path)
    elif ext in ['eml', 'msg']:  # Assume email
        loader = UnstructuredEmailLoader(tmp_path)
    else:
        raise ValueError(f"Unsupported format: {ext}. Supported formats: pdf, docx, eml, msg")

    docs = loader.load()
    os.remove(tmp_path)  # Clean up

    # Chunk for semantic search: small size for precision
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    return chunks

def build_vectorstore(chunks: list) -> FAISS:
    """Build FAISS vector store with OpenAI embeddings."""
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")  # Accurate, efficient
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def query_llm(vectorstore: FAISS, question: str) -> str:
    """Query LLM with retrieved context for accurate, explainable answer."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=500)  # Factual, token-efficient
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Stuff context for simplicity/accuracy
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),  # Top-5 for good recall
        return_source_documents=True,  # For internal traceability
        chain_type_kwargs={"prompt": QA_PROMPT}  # Custom prompt for explainability
    )
    result = qa_chain({"query": question})
    answer = result["result"].strip()
    
    # Optional: Append sources for extra traceability (e.g., pages)
    # sources = [f"Page {doc.metadata.get('page', 'N/A')}" for doc in result["source_documents"]]
    # answer += f" (Sources: {', '.join(sources)})"
    
    return answer