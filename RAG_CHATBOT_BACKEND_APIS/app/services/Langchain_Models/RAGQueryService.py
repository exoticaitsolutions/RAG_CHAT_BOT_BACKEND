import os
import openai
from langchain_chroma import Chroma  # Correct import
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # Updated imports
from langchain.chains import RetrievalQA
from RAG_Backend.settings import BASE_DIR
from RAG_CHATBOT_BACKEND_APIS.utils import create_directories, format_name

class RAGQueryService:
    """
    Service to handle querying from ChromaDB and generating AI-powered responses using an LLM.
    """

    @staticmethod
    def GetResponseFromQuery(chatbot, user, query_text):
        """
        Queries the ChromaDB to find relevant documents and generates a response using an LLM.

        :param chatbot: Chatbot instance containing config details.
        :param user: User instance requesting the query.
        :param query_text: The text query to search for in the vector database.
        :return: A generated response from the LLM model based on retrieved documents.
        """

        print("[INFO] Query Text:", query_text)

        # Validate OpenAI API Key
        if not chatbot.openai_key:
            print("[ERROR] Missing OpenAI API key.")
            return {"query": query_text, "response": "OpenAI API key is missing."}

        openai.api_key = chatbot.openai_key

        if chatbot.vector_database == "chroma":
            try:
                # Define ChromaDB directory
                formatted_username = format_name(str(user.username))
                formatted_chat_name = format_name(str(chatbot.chatbot_name))
                smedia_file, ChromaDb_Dir = create_directories(str(user.username), str(chatbot.chatbot_name))
                collection_name = f"{formatted_username}_{formatted_chat_name}"
                print("[INFO] Collection Name:", collection_name)

                # Load ChromaDB with OpenAI Embeddings
                embed_fun = OpenAIEmbeddings(model='text-embedding-3-small')
                vectordb = Chroma(persist_directory=ChromaDb_Dir, embedding_function=embed_fun, collection_name=collection_name)

                # Check available documents
                doc_count = len(vectordb.get()['documents'])  # Alternative to _collection.count()
                print(f"[INFO] Number of documents in ChromaDB: {doc_count}")
                if doc_count == 0:
                    return {"query": query_text, "response": "No relevant documents found in the database."}
                # Initialize LLM (GPT Model)
                llm = ChatOpenAI(model_name=chatbot.model, temperature=chatbot.temperature, openai_api_key=chatbot.openai_key) # type: ignore
                # Create RetrievalQA Chain
                retriever = vectordb.as_retriever(search_kwargs={"k": min(3, doc_count)})  # Ensure valid k
                qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
                # Generate Answer
                response = qa_chain.run(query_text)
                return {"query": query_text, "response": response}
            except Exception as e:
                print(f"[ERROR] Error querying ChromaDB or LLM: {str(e)}")
                return {"query": query_text, "response": f"An error occurred while processing your query: {str(e)}"}
        return {"query": query_text, "response": "Vector database not supported."}
