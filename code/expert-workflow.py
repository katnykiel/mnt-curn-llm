# this script uses langchain w/ rag to answer questions about a given url
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
import json
import re
import pandas as pd

experts_list = []

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
'''
#load a list of URLs from json file
with open('data.json', 'r') as f:
    data = json.load(f)
urls = []
for articles in data["articles"]:
    if "url" in articles:
        urls.append(articles["url"])
'''

#load dataframe
df = pd.read_excel("/Users/bryan/Work/MNT-CURN/Purdue Internship/mnt-curn-llm/Book1.xlsx")
#extracts all urls from column and turns it into a list
urls = list(df['URLS'].unique())
#clears the NaN from the list
urls = [url for url in urls if pd.notna(url)]

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
    response = retrieval_chain.invoke({"input": '''
Please read the following news article and identify the experts mentioned. List each expert and their respective institution using the following format exactly:

<expert>Expert Name</expert>
<institution>Institution Name</institution>

Example:
<expert>John Doe</expert>
<institution>Harvard University</institution>

<expert>Jane Smith</expert>
<institution>MIT</institution>

Do not include any additional information, comments, explanations, or notes. Only list the experts and their institutions. Here is the news article:
                                  '''})
    
    print(response["answer"])
    
    experts = re.findall(r'<expert>(.*?)</expert>', response["answer"])
    experts_list.append(experts)
    print(experts)
print(experts_list)
