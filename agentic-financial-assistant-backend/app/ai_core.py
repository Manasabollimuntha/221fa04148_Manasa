from typing import List
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA, LLMChain
from langchain.llms import OpenAI
from app.config import settings
import os

# Configure OpenAI or your LLM provider
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

def load_text_from_file(path: str, filename: str) -> str:
    # Simple loader that supports .txt and .pdf
    if filename.lower().endswith(".pdf"):
        loader = PyPDFLoader(path)
        docs = loader.load()
        return "\n".join([d.page_content for d in docs])
    else:
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load()
        return "\n".join([d.page_content for d in docs])

def chunk_text(text: str) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    return splitter.split_text(text)

def summarize_text(text: str) -> str:
    """
    Very simple summarization using OpenAI via LangChain. You may replace with other LLMs.
    """
    llm = OpenAI(temperature=0)
    # Use a small prompt to summarize financial documents with clarity for parents
    prompt = (
        "You're a helpful financial assistant for parents. Summarize the following university financial "
        "document into: (1) tuition/fees (list with amounts if found), (2) recurring expenses (hostel, food, transport), "
        "(3) one-time fees, (4) payment deadlines, (5) actionable next steps for the parent.\n\nDocument:\n"
        f"{text}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    resp = chain.run({})
    return resp

def build_retriever_from_texts(texts: List[str]):
    # Build embeddings and retriever for Q&A
    emb = OpenAIEmbeddings()
    # If you prefer local FAISS or Chroma, swap here; this is an example using in-memory approach via LangChain utilities.
    from langchain.vectorstores import Chroma
    vectordb = Chroma.from_texts(texts, embedding=emb)
    return vectordb.as_retriever()

def answer_query_with_docs(query: str, retriever):
    llm = OpenAI(temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa.run(query)
