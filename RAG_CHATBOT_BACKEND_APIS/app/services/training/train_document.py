import os
import traceback
from uuid import uuid4
from django.conf import settings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import openai

from RAG_Backend.settings import BASE_DIR
from RAG_CHATBOT_BACKEND_APIS.models import ChatBotDB, Document, DocumentCollectionIds
from RAG_CHATBOT_BACKEND_APIS.utils import ensure_directory_exists

# Text Splitter Configuration
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# Embedding Function
embed_fun = OpenAIEmbeddings(model='text-embedding-3-small')

def inserting_doc_chromadb(reader_docs, ChromaDb_Dir, collection, document_id, chat_data, user_data):
    """Insert document chunks into ChromaDB and update document metadata."""
    print(f"[INFO] Starting ChromaDB insertion for document_id: {document_id}")
    
    # Fetch document from DB safely
    document = Document.objects.filter(id=document_id).first()
    if not document:
        print(f"[ERROR] Document with ID {document_id} not found.")
        return False

    texts = text_splitter.split_documents(reader_docs)
    print(f"[INFO] Splitting document into {len(texts)} chunks")

    ids = [str(uuid4()) for _ in texts]
    full_page_content = "".join([text.page_content for text in texts])

    # Store chunk metadata in DB
    for id_new in ids:
        DocumentCollectionIds.objects.create(
            doc_id=id_new, doc_name=document.name, collection=collection,
            chroma_dir=ChromaDb_Dir, chatbot=chat_data, user=user_data, document=document
        )

    # Store in ChromaDB
    print(f"[INFO] Storing {len(texts)} chunks in ChromaDB at {ChromaDb_Dir}")
    # db = Chroma.from_documents(texts, embed_fun, persist_directory=ChromaDb_Dir, collection_name=collection, ids=ids)
    db = Chroma.from_documents(texts, embed_fun, persist_directory=ChromaDb_Dir)
    # Update document details safely
    document.no_of_characters = int(len(full_page_content))
    document.no_of_chunks = int(len(texts))
    print(f"Char: {len(full_page_content)}\nChunks: {len(texts)}")
    db.persist()

    print(f"[SUCCESS] Document {document.name} added to collection: {collection}")
    return True,int(len(full_page_content)),len(texts)

def uploaded_document_and_train_llm(document_data, media_file, chat_data, user_data):
    """Process uploaded document, extract text, and store embeddings."""
    print(f"[INFO] Processing document upload for user: {user_data.username}, chatbot: {chat_data.chatbot_name}")
    
    try:
        document_id = document_data.get("id")
        document = Document.objects.filter(id=document_id).first()

        if not document:
            print(f"[ERROR] Document with ID {document_id} not found.")
            return False

        print(f"[INFO] Retrieved document from DB: {document.name}")

        if not media_file.endswith('.pdf'):
            print(f"[ERROR] Invalid file type: {media_file}")
            document.status = "error"
            document.save()
            return False

        print(f"[INFO] Loading PDF: {media_file}")
        pdf_loader = PyPDFLoader(media_file)
        reader_docs = pdf_loader.load()
        print(f"[INFO] PDF successfully loaded with {len(reader_docs)} pages")

        openai.api_key = chat_data.openai_key

        if chat_data.vector_database == "chroma":
            ChromaDb_Dir = os.path.join(BASE_DIR, "chroma_db", str(user_data.username), str(chat_data.chatbot_name))
            ensure_directory_exists(ChromaDb_Dir)
            collection = f"{user_data.username}_{chat_data.chatbot_name}"

            print(f"[INFO] ChromaDB Path: {ChromaDb_Dir}")
            print(f"[INFO] Collection Name: {collection}")

            success,no_of_characters ,test_leangh = inserting_doc_chromadb(reader_docs, ChromaDb_Dir, collection, document_id, chat_data, user_data) # type: ignore
            print(test_leangh,no_of_characters )
            document.no_of_characters = no_of_characters
            document.no_of_chunks = test_leangh
            if success:
                print(f"[SUCCESS] Document processing completed for: {document.name}")
                document.status = "success"
            else:
                print(f"[ERROR] Document insertion failed: {document.name}")
                document.status = "error"

        else:
            print(f"[ERROR] Unsupported vector database: {chat_data.vector_database}")
            document.status = "error"

    except Exception as e:
        print(f"[EXCEPTION] {e}")
        print(traceback.format_exc())
        if document:
            document.status = "error"

    finally:
        if document:
            document.save()
            print(f"[INFO] Document status updated to: {document.status}")

