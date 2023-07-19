import openai
from langchain.vectorstores import pinecone
import pinecone
import re 
import os 


#API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = 'asia-southeast1-gcp'

openai.api_key = os.getenv("OPENAI_API_KEY")


# Initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV
)
index_name = "access-vec"

index = pinecone.Index(index_name)


def getContext(user_input):
    embedding_model = "text-embedding-ada-002"
    embed_query = openai.Embedding.create(
            input=user_input,
            engine=embedding_model, 
            )

    #retrieve from Pinecone
    query_embeds = embed_query['data'][0]['embedding']

    # get relevent contexts, inluding question
    response = index.query(query_embeds, top_k=3, include_metadata=True, namespace="accessgpt2023-06-21")
    reponse = response.to_dict()
    contexts = []
    matches = response.get('matches', [])
    for match in matches:
        metadata = match.get('metadata', {})
        text = metadata.get('text', '')
        contexts.append(text)
    


    #joining context together in an orderly fashion
    ordered_context = "Provide your answers inside html <p> elements. Use only the context given by the user. If you cannot, simply say 'Sorry, I can't provide an answer based on the context provided to me. If you provide a link in your answer - use an html anchor element <a></a>. If you provide a list in your answer please provide it inside a <ul> element with the respective <li> elements nested inside."
    for i, context in enumerate(contexts,1):
        ordered_context += f"Context {i}: " + context + str(metadata) + "\n\n"

    sources = get_sources(ordered_context)

    return [ordered_context, sources]


def get_sources(text):
    # Fixes for errors in sources
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

#Previous full  namespace accessgpt2023-06-18