import os

import openai
from uuid import uuid4
from django.conf import settings
from langchain_community.document_loaders import CSVLoader, Docx2txtLoader, PyPDFLoader, TextLoader, UnstructuredExcelLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_openai import  ChatOpenAI  # Updated imports
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from RAG_CHATBOT_BACKEND_APIS.app.services.Langchain_Models.SeleniumScraperServices import SeleniumScraperServices
from RAG_CHATBOT_BACKEND_APIS.models import Document, DocumentCollectionIds, WebsiteCollectionIds, WebsiteDB
from RAG_CHATBOT_BACKEND_APIS.utils import create_directories, format_name
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


embed_fun = OpenAIEmbeddings()
class LangchainEmbeddingService:
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
                print("[INFO] ChromaDb_Dir Name:", ChromaDb_Dir)

                # Load ChromaDB with OpenAI Embeddings
                embed_fun = OpenAIEmbeddings(model='text-embedding-3-small')
                vectordb = Chroma(persist_directory=ChromaDb_Dir, embedding_function=embed_fun, collection_name=collection_name)
                # Initialize LLM (GPT Model)
                llm = ChatOpenAI(model_name=chatbot.model, temperature=chatbot.temperature, openai_api_key=chatbot.openai_key) # type: ignore
                # Create RetrievalQA Chain
                retriever = vectordb.as_retriever(search_kwargs={"k": 5})  # Ensure valid k
                qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
                # Generate Answer
                response = qa_chain.run(query_text)
                return {"query": query_text, "response": response}
            except Exception as e:
                print(f"[ERROR] Error querying ChromaDB or LLM: {str(e)}")
                return {"query": query_text, "response": f"An error occurred while processing your query: {str(e)}"}
        return {"query": query_text, "response": "Vector database not supported."}
    @staticmethod
    def process_urls_for_training(website_id, chat_data, user_data, ChromaDb_Dir):
        print(f"Processing website with ID {website_id} for user: {user_data.username}, chatbot: {chat_data.chatbot_name}.")
        website = None  # Initialize document to avoid reference before assignment
        try:
            website = WebsiteDB.objects.filter(id=website_id).first()
            if website:
                print(f"Processing website {website.url} for training with the LLM model.")
                website.status = "processing"
                website.status_message = "Processing the website for training with the LLM model."
                website.save()
                openai.api_key = chat_data.openai_key
                vector_database = chat_data.vector_database
                if vector_database == "chroma":
                    collection = f"{format_name(user_data.username)}_{format_name(chat_data.chatbot_name)}"
                    print(f"ChromaDB Path: {ChromaDb_Dir}")
                    print(f"Collection Name: {collection}")
                    response_status , response_messages ,extracted_texts = SeleniumScraperServices.get_links_selenium_get_response_data(website.url)
                    if not response_status:
                        if website:
                            website.status = "error"
                            website.status_message = response_messages
                            website.save()
                    print('Processing the INset the Scrapped the Website data in the Chroma db ')
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
                    documents = text_splitter.create_documents(extracted_texts)
                    ids = [str(uuid4()) for _ in documents]
                    full_page_content = "".join([text.page_content for text in documents])
                    ids = []
                    full_page_content = ''
                    for x in range(len(documents)):
                        full_page_content += str(documents[x].page_content)
                        id_new = str(uuid4())
                        ids.append(id_new)
                        WebsiteCollectionIds.objects.create(web_id=id_new, web_name=website.url, collection=collection, chroma_dir=ChromaDb_Dir, chatbot=chat_data, user=user_data, website=website)
                    db = Chroma.from_documents(documents, embed_fun, persist_directory=ChromaDb_Dir, collection_name=collection,ids=ids)  
                    if website:
                        website.no_of_characters = len(full_page_content) # type: ignore
                        website.no_of_chunks = len(documents) # type: ignore
                        website.status = "completed" # type: ignore
                        website.status_message = "Successfully scraped the website, embedded the website URL, and stored it in ChromaDB."
                        website.save() # type: ignore
                else:
                    print(f"[ERROR] Unsupported vector database: {chat_data.vector_database}")
                    website.status = "error"
                    website.status_message = f"[ERROR] Unsupported vector database: {chat_data.vector_database}"
                    website.save()
        except Exception as e:
            print(f"An error occurred while processing website {website_id}: {str(e)}.")
            if website:
                website.status = "error"
                website.status_message = f"An error occurred: {str(e)}"
                website.save()
        finally:
            print(f"Finished processing website {website_id}.")

            
    @staticmethod
    def uploaded_document_and_train_llm(document, chat_data, user_data,ChromaDb_Dir):
        print(f"Processing document upload for user: {user_data.username}, chatbot: {chat_data.chatbot_name}")
        try:
            file_name = os.path.join(settings.MEDIA_ROOT, str(document.filepath))
            print("📂 Full File Path:", file_name)
            print("File Exists:", os.path.exists(file_name))  # Should print True       
            if document:
                document.status = "Processing.."
            if file_name.endswith('.xlsx'):
                excel_loader = UnstructuredExcelLoader(file_name)
                doc = excel_loader.load()
                print(len(doc), "--------------xlsx")
            elif file_name.endswith('.docx'):
                docx_loader = Docx2txtLoader(file_name)
                doc = docx_loader.load()
                print(len(doc), "--------------docs")
            elif file_name.endswith('.csv'):
                csv_loader = CSVLoader(file_name)
                doc = csv_loader.load()
                print(len(doc), "------------csv")
            elif file_name.endswith('.pdf'):
                pdf_loader = PyPDFLoader(file_name)
                doc = pdf_loader.load()
                print(len(doc), "--------pdf")
            elif file_name.endswith('.txt'):
                txt_loader = TextLoader(file_name)
                doc = txt_loader.load()
                print(len(doc), "-----------txt")    
            else:
                print(f"[INFO] Please Choose the COrrect file name ")
                if document:
                    document.status = "error"
            openai.api_key = chat_data.openai_key
            if chat_data.vector_database == "chroma":
                collection = f"{format_name(user_data.username)}_{format_name(chat_data.chatbot_name)}"
                print(f"[INFO] ChromaDB Path: {ChromaDb_Dir}")
                print(f"[INFO] Collection Name: {collection}")
                texts = text_splitter.split_documents(doc)
                print(f"[INFO] Splitting document into {len(texts)} chunks")
                ids = [str(uuid4()) for _ in texts]
                full_page_content = "".join([text.page_content for text in texts])
                # Store chunk metadata in DB
                for id_new in ids:
                    DocumentCollectionIds.objects.create(
                        doc_id=id_new, doc_name=document.name, collection=collection, # type: ignore
                        chroma_dir=ChromaDb_Dir, chatbot=chat_data, user=user_data, document=document
                    )
                print(f"[INFO] Storing {len(texts)} chunks in ChromaDB at {ChromaDb_Dir}")
                db = Chroma.from_documents(texts, embed_fun, persist_directory=ChromaDb_Dir)
                if document:
                    document.no_of_characters = int(len(full_page_content))
                    document.no_of_chunks = int(len(texts))
                    document.status = "success"  
                    
                print(f"Char: {len(full_page_content)}\nChunks: {len(texts)}")
                print(f"[SUCCESS] Document {document.name} added to collection: {collection}") # type: ignore
            else:
                print(f"[ERROR] Unsupported vector database: {chat_data.vector_database}")
                if document:
                    document.status = "error"    
            
        except Exception as e:
            print(f"Error processing file : {str(e)}")
            if document:
                document.status = "error"
        
        finally:
            if document:
                document.save()
                print(f"[INFO] Document status updated to: {document.status}")