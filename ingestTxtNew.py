from langchain.embeddings import OpenAIEmbeddings
import pinecone
import openai
import os 
from langchain.vectorstores import Chroma, Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Get the Relevant API Keys Ready
openai.api_key = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = 'asia-southeast1-gcp'

#OPEN AI Embeddings to convert each text chunk
embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

#Initiate your pinecone index 
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  
)
index_name = "access-vec"

#Get the document name 
documentName = " Accessibility in Ontario"
pageSource = "https://www.ontario.ca/page/accessibility-in-ontario"


#Get the document path and read into file.
text_path = r"documents\Multi-Page - Government Programs for PWDS.txt"

text_document = ""

with open(text_path, encoding="utf-8") as f:
    text_document = f.read()



#Set Recusrve Character Splitter and Text Size 
text_splitter = RecursiveCharacterTextSplitter(
    # Set chunk size
    chunk_size = 100000,
    chunk_overlap  = 40000,
    length_function = len
)


text_chunks =  text_splitter.create_documents([text_document])

#Remember it has become a document object now.
for chunk in text_chunks:
    chunk.page_content += f" \n \n(Document Source: {documentName}, Page Source: {pageSource})"


upload_chunks = Pinecone.from_documents(text_chunks, embeddings, index_name=index_name, namespace="accessgpt2023-06-21")
    
print("SUCCESS")