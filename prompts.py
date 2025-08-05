from langchain.prompts import PromptTemplate

# Custom prompt for explainable, accurate QA
QA_PROMPT = PromptTemplate.from_template(
    """You are an expert in insurance policies. Use only the following context from the policy document to answer the question. 
    Parse the query for key elements (e.g., coverage, conditions, waiting periods). Match relevant clauses semantically.
    Evaluate any logic or conditions. Provide an explainable rationale, citing specific clauses or sections if possible.
    If the information is not in the context, say "Not specified in the policy."
    Keep the answer concise but detailed, like: "Yes/No, [details], [conditions], [rationale]."

    Context: {context}

    Question: {question}

    Answer:"""
)