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
from langchain_community.document_loaders.web_base import WebBaseLoader

import pandas as pd
df = pd.read_excel("Book1.xlsx")
#print(df)
urls = df["URLS"].unique()

# This is just to clean up the output
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


from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
for url in urls:
    print(url)


llm = Ollama(model="llama2")
output_parser = StrOutputParser()


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm 

print(chain.invoke({"input": "how can langsmith help with testing?"}))
# Load the text from the sample-article.md file
#loader = TextLoader("/Users/bryan/Work/MNT-CURN/Purdue Internship/mnt-curn-llm/resources/sample-article.md")
loader = WebBaseLoader("")
pages = loader.load_and_split()

# Load Ollama embeddings
embeddings = OllamaEmbeddings()

# Create a vector store using FAISS from the loaded pages and embeddings
vector = FAISS.from_documents(pages, embeddings)

while True:
    # Get user input for the query
    query = input("\n>>> ")

    # Check if the user wants to exit the loop
    if query == "exit":
        break

    # Skip empty queries
    if query.strip() == "":
        continue

    # Define the prompt template for the QA chain
    template = """Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {question}"""
    QA_CHAIN_PROMPT = PromptTemplate(
        input_variables=["context", "question"],
        template=template,
    )

    # Create a langchain chat model using the Ollama model
    chat = ChatOllama(
        model="llama3",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )

    # Create a retrieval QA chain using the chat model, vector store, and prompt template
    qa_chain = RetrievalQA.from_chain_type(
        chat,
        retriever=vector.as_retriever(search_kwargs={"k": 20}),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )

    # Invoke the QA chain with the user query
    result = qa_chain.invoke({"query": query})
