import openai
from langchain.vectorstores import pinecone
import pinecone
import re 
import os 

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Pinecone Code

# Import the updated Pinecone client
from pinecone import Pinecone

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "access-vec"

index = pc.Index(index_name)

def getContext(user_input):
    """
    The getContext function retrieves the closest matching vectors in the Pinecone database based on similarity search. The purpose is to provide leading context to the chatbot as a part of the retrieval augmented generation approach. Doing so increases the "truthiness" of the results. You can learn more about retrieval augmented generation in this project's About page or here at : https://docs.aws.amazon.com/sagemaker/latest/dg/jumpstart-foundation-models-customize-rag.html. The number of returned results is dependent on the k number, which is important for determining how much context is there both in terms of content detail and the number of potential tokens the response takes.
    """
    embedding_model = "text-embedding-ada-002"
    embed_query = openai.Embedding.create(
        input=user_input,
        engine=embedding_model, 
    )

    # Retrieve from Pinecone
    query_embeds = embed_query['data'][0]['embedding']

    # Get relevant contexts, including question
    response = index.query(
        vector=query_embeds, 
        top_k=3, 
        include_metadata=True, 
        namespace="accessgpt2023-06-21"
    )
    
    response = response.to_dict()  # Typo fix: reponse -> response
    contexts = []
    matches = response.get('matches', [])
    for match in matches:
        metadata = match.get('metadata', {})
        text = metadata.get('text', '')
        contexts.append(text)

    # Joining context together in an orderly fashion
    ordered_context = ""
    for i, context in enumerate(contexts, 1):
        ordered_context += f"Context {i}: " + context + str(metadata) + "\n\n"

    sources = getSources(ordered_context)

    return [ordered_context, sources]

def getSources(text):
    """
    The getSources function is a helper function designed to clean up the data. Some of the sources ingested had different ways of referring to links and context. Standardizing these sources makes it easier to provide clean tables in the front end sources table. 
    """
    # Fixes for text formatting errors in sources
    text = text.replace('\\n', '')
    text = re.sub(r'(Page)source', r'\1 Source', text, flags=re.IGNORECASE)
    text = re.sub(r'(?i)https?(?=:)', 'https', text)
    text = re.sub(r'(?i)www', 'www', text)
    text = re.sub(r'(?i)\b(The Integrated Accessibility Standards)(\w+)?(regulation)\b', r'\1 \3', text)

    # Regular expression pattern
    pattern = r'\(Document Source:\s*(.*?), Page Source:\s*(.*?)\)\s*'

    # Find matches
    matches = re.findall(pattern, text)

    # Use set to remove duplicates and then convert back to list
    matches = list(set(matches))

    # Convert first item of each tuple to title case, leaving acronyms alone
    matches = [(' '.join(word if word.isupper() else word.title() for word in m[0].split()), m[1]) for m in matches]

    return matches

# Previous full namespace accessgpt2023-06-18
