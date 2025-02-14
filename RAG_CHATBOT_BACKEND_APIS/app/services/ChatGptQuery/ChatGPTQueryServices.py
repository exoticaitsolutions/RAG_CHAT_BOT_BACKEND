import os
import openai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from RAG_Backend.settings import BASE_DIR
from RAG_CHATBOT_BACKEND_APIS.utils import format_name

def GetResponseFromQuery(chatbot, user, query_text):
    
    print("Query Text:", query_text)

    # Set OpenAI API Key
    openai.api_key = chatbot.openai_key

    if chatbot.vector_database == "chroma":
        # Define Chroma database directory
        forment_username = format_name(str(user.username))
        forment_chat_name = format_name(str(chatbot.chatbot_name))
        ChromaDb_Dir = os.path.join(BASE_DIR, "chroma_db", forment_username, forment_chat_name)
        print("ChromaDb Directory:", ChromaDb_Dir)

        # Collection name
        collection_name = f"{forment_username}_{forment_chat_name}"
        print("Collection:", collection_name)

        # Load Chroma database
        embed_fun = OpenAIEmbeddings(model='text-embedding-3-small')
        vectordb = Chroma(persist_directory=ChromaDb_Dir, embedding_function=embed_fun,collection_name=collection_name)
        results = vectordb.similarity_search(query_text, k=5)
        if results:
            return  [{'text': res.page_content, 'reference': res.metadata.get('source', 'Unknown')} for res in results]
        else:
            print("No matching results found.")
            return "I'm sorry, I couldn't find relevant information."

    return "Vector database not supported."

