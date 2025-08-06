from langchain.prompts import PromptTemplate

# Simplified prompt for Railway deployment stability
QA_PROMPT = PromptTemplate.from_template(
    """You are an insurance policy expert. Use only the provided context to answer the question accurately.
    
    If the information is not in the context, say "Not specified in the policy."
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
)