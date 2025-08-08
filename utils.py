import requests
import tempfile
import os
import pdfplumber
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredEmailLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.docstore.document import Document
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
        # Enhanced PDF parsing with structure preservation using pdfplumber
        with pdfplumber.open(tmp_path) as pdf:
            text_pages = []
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""  # Handle empty pages
                text_pages.append(f"Page {i+1}:\n{text}")  # Add page metadata
            full_text = '\n\n'.join(text_pages)
        docs = [Document(page_content=full_text, metadata={"source": url})]  # Single doc with all pages
    elif ext == 'docx':
        loader = Docx2txtLoader(tmp_path)
        docs = loader.load()
    elif ext in ['eml', 'msg']:  # Assume email
        loader = UnstructuredEmailLoader(tmp_path)
        docs = loader.load()
    else:
        raise ValueError(f"Unsupported format: {ext}. Supported formats: pdf, docx, eml, msg")
    os.remove(tmp_path)  # Clean up

    # Enhanced chunking for better context capture - adaptive chunk size based on document size
    total_text_length = sum(len(doc.page_content) for doc in docs)
    
    if total_text_length > 200000:  # Very large documents (like academic texts)
        chunk_size = 600  # More aggressive chunking for Railway
        chunk_overlap = 150
        print(f"Using smaller chunks for large document (total length: {total_text_length})")
    elif total_text_length > 100000:  # Medium documents
        chunk_size = 1000  # Reduced size for Railway optimization
        chunk_overlap = 200
        print(f"Using medium chunks for document (total length: {total_text_length})")
    else:  # Small documents (like insurance policies)
        chunk_size = 1500
        chunk_overlap = 300
        print(f"Using standard chunks for document (total length: {total_text_length})")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=['\n\n', '\n', '.', 'Section ', 'Clause ', 'Article ', 'Policy ', 'Sub-limit ']  # Custom for various docs
    )
    chunks = splitter.split_documents(docs)
    return chunks

def build_vectorstore(chunks: list) -> tuple:
    """Build FAISS vector store with OpenAI embeddings and return chunks for hybrid retrieval."""
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")  # Accurate, efficient
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore, chunks

def query_llm(vectorstore: FAISS, chunks: list, question: str) -> str:
    """Simplified query LLM for Railway deployment stability."""
    try:
        # Optimized LLM configuration for Railway deployment
        llm = ChatOpenAI(
            model="gpt-3.5-turbo", 
            temperature=0, 
            max_tokens=200,  # Further reduced for faster response
            request_timeout=15  # Shorter timeout for Railway
        )
        
        # Adaptive retrieval based on vector store size
        total_chunks = len(chunks)
        if total_chunks > 500:  # Large document
            k_value = 2  # Use fewer chunks for large documents
            print(f"Using reduced retrieval for large document ({total_chunks} chunks, k={k_value})")
        else:  # Normal document
            k_value = 3  # Standard retrieval
            print(f"Using standard retrieval for document ({total_chunks} chunks, k={k_value})")
            
        retriever = vectorstore.as_retriever(search_kwargs={"k": k_value})
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False,  # Disable for speed
            chain_type_kwargs={"prompt": QA_PROMPT}
        )
        
        result = qa_chain.invoke({"query": question})
        answer = result["result"].strip()
        return answer.rstrip('.').strip()
        
    except Exception as e:
        print(f"Error in simplified QA chain: {e}")
        return f"Unable to process question due to system constraints."