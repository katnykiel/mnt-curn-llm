# this script uses langchain w/ rag to answer questions about a given url
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
import re

# Create a langchain chat model using the Ollama model
chat = ChatOllama(model="llama3")

# Define the prompt template for the invoke statement
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Create a document chain
document_chain = create_stuff_documents_chain(chat, prompt)

# Load Ollama embeddings
embeddings = OllamaEmbeddings()

# Load a list of URLs: here, i provide an example
urls = ["https://apnews.com/article/universities-colleges-climate-studies-environmental-science-01f287f7ffd25cf27a03a4a5b3ce8a8a"]
    
# Loop through the URLs and invoke LLMs with article content
for url in urls:
    # Load the text from the url
    loader = WebBaseLoader(url)
    docs = loader.load()

    # Split the text into documents
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

    # Create a vector store using FAISS from the loaded pages and embeddings
    vector = FAISS.from_documents(documents, embeddings)

    # Add context from the news article
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain) 

    # Ask a question
    response = retrieval_chain.invoke({"input": "Which experts are listed in this news article? Please list them as <expert>Expert Name</expert>. and their respective institutions as <institution>Institution Name</institution>. There may be more than one, please list all that you find and add newlines between them."})
    print(response["answer"])

 