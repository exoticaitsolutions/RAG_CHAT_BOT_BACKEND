import os
from typing import List
import openai
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from RAG_Backend.settings import BASE_DIR

def GetResponseFromQuery(chatbot, user, query_text):
    embeddings = OpenAIEmbeddings()

    print("Query Text:", query_text)

    # Set OpenAI API Key
    openai.api_key = chatbot.openai_key

    if chatbot.vector_database == "chroma":
        # Define Chroma database directory
        ChromaDb_Dir = os.path.join(BASE_DIR, "chroma_db", str(user.username), str(chatbot.chatbot_name))
        print("ChromaDb Directory:", ChromaDb_Dir)

        # Collection name
        collection_name = f"{user.username}_{chatbot.chatbot_name}"
        print("Collection:", collection_name)

        # Load Chroma database
        vectordb = Chroma(persist_directory=ChromaDb_Dir, embedding_function=embeddings)
        results = vectordb.similarity_search(query_text, k=5)
        print('result', results)
        # Perform a similarity search
        if results:
            return  [{'text': res.page_content, 'reference': res.metadata.get('source', 'Unknown')} for res in results]
        else:
            print("No matching results found.")
            return "I'm sorry, I couldn't find relevant information."

    return "Vector database not supported."

