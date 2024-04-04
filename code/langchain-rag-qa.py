import sys
import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.document_loaders.text import TextLoader
from langchain_community.vectorstores.faiss import FAISS


class SuppressStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

loader = TextLoader("../meeting-notes/Papers.md")
pages = loader.load_and_split()
embeddings = OllamaEmbeddings()
vector = FAISS.from_documents(pages, embeddings)

while True:
    query = input("\n>>> ")
    if query == "exit":
        break
    if query.strip() == "":
        continue

    # Prompt
    template = """Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {question}"""
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )

    chat = ChatOllama(
        model="llama2",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )

    qa_chain = RetrievalQA.from_chain_type(
        chat,
        retriever=vector.as_retriever(search_kwargs={"k": 20}),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    result = qa_chain.invoke({"query": query})
    print(result["result"])
