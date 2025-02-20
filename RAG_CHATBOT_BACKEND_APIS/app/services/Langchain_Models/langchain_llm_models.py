import openai
from uuid import uuid4
from langchain_community.document_loaders import CSVLoader, Docx2txtLoader, PyPDFLoader, TextLoader, UnstructuredExcelLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from RAG_CHATBOT_BACKEND_APIS.models import Document, DocumentCollectionIds
from RAG_CHATBOT_BACKEND_APIS.utils import format_name
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
embed_fun = OpenAIEmbeddings(model='text-embedding-3-small')

class LangchainEmbeddingService:
    @staticmethod
    def uploaded_document_and_train_llm(document_data, file_name, chat_data, user_data,ChromaDb_Dir):
        print(f"Processing document upload for user: {user_data.username}, chatbot: {chat_data.chatbot_name}")
        document = None  # Initialize document to avoid reference before assignment
        try:
            document_id=  document_data.get('id')
            document = Document.objects.filter(id=document_id).first()
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
            if document:
                document.status = "error"
        
        finally:
            if document:
                document.save()
                print(f"[INFO] Document status updated to: {document.status}")