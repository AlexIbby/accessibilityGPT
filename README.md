# AccessibilityGPT - An AODA Chatbot providing Information on Accessibility for Ontarians with Disabilities Act (AODA) 📖

This project is a chatbot designed to provide answers related to the Accessibility for Ontarians with Disabilities Act (AODA) and its regulation, the Integrated Accessibility Standards Regulation (IASR). The chatbot utilizes the powerful mechanism of retrieval augmented generation (RAG) to provide more reliable and accurate responses. 🎯💬

## How it works ❓

The process begins with a user's query. 🗣️ This query is then matched against a set of relevant documents within a Pinecone vector database. Pinecone is a state-of-the-art vector database that allows us to retrieve relevant documents based on the similarity of vectors. 📚

Following this, an OpenAI's API call is made to GPT-3.5, which serves as the language learning model (LLM) for the system. This LLM generates an answer to the user's query based solely on the matched documents from the database. 🤖💡

This approach significantly increases the "truthiness" of responses by restricting the responses to only the information found within the matched documents, effectively reducing hallucination. 🎉

## Live Demo

https://accessibilitygpt.up.railway.app/

## Tech Stack 🛠️

- Python's Flask for the web framework 🐍
- Pinecone for the vector database 🌲
- OpenAI's GPT-3.5 API for the language learning model 🧠
- LangChain, an open-source framework for developing applications powered by language models 🔗

## Why Use an AODA Chatbot? 🤔

The chatbot aims to provide easy and accurate information about the Accessibility for Ontarians with Disabilities Act (AODA). This can help ensure more people understand the act and its regulations, providing easy to understand and use reference. 🌍🤝

## Get Started 🚀

- Clone the repo using `git clone <repo_url>`
- Install dependencies using `pip install -r requirements.txt`
- Start the Flask app with `python app.py`

Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us. 

## License 📜

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments 👏

LangChain is awesome!
