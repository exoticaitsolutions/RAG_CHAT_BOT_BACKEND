import logging
import re
import time
import os
import shutil
import hashlib
from urllib.parse import urljoin
from django.conf import settings
from django.db import transaction

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Create a logger instance
logger = logging.getLogger(__name__)
def format_name(name):
    """Format names by converting to lowercase and replacing spaces with underscores."""
    return name.strip().lower().replace(" ", "_")


# Global variable declaration
def ensure_directory_exists(directory_path):
    """
    Ensure that the given directory exists. If not, create it.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)  # Creates all intermediate directories if necessary
        print(f"✅ Created directory: {directory_path}")
    else:
        print(f"✅ Directory already exists: {directory_path}")

def save_pdf_to_chroma(pdf_file_path):
    """Extract text from PDF and save it to Chroma DB."""
    try:
        loader = PyPDFLoader(pdf_file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
       
        vectordb = Chroma.from_documents(texts, embeddings, persist_directory="chroma_db")
        vectordb.get()

  
        return "PDF processed and stored in ChromaDB."
    except Exception as e:
        logger.error(f"Error processing PDF {pdf_file_path}: {e}")
        return str(e)



def query_chroma(query_text):
    """Queries ChromaDB and retrieves results."""
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    results = vectordb.similarity_search(query_text, k=5)
    if results:
        return  [{'text': res.page_content, 'reference': res.metadata.get('source', 'Unknown')} for res in results]
    else:
        vectordb.add_documents([query_text])
        vectordb.persist()
        return 'No matching results. Query stored for future reference.'


def store_url_data_in_chromadb(url):
    """
    Scrape the website using Selenium, split the text into chunks using LangChain,
    and store the embeddings in a ChromaDB instance.
    """

    # Set up Selenium Chrome options.
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())

    def get_links_selenium(url):

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(8)
        elements = driver.find_elements(By.TAG_NAME, "a")
        links = {urljoin(url, elem.get_attribute("href")) for elem in elements if elem.get_attribute("href")}
        driver.quit()
        return list(links)

    def extract_text_selenium(url):
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(5)
        text = driver.find_element(By.TAG_NAME, "body").text
        driver.quit()
        return text

    # Create a persistent storage directory for ChromaDB
    PERSIST_DIRECTORY = os.path.join(settings.BASE_DIR, "chroma_db")
    if not os.path.exists(PERSIST_DIRECTORY):
        os.makedirs(PERSIST_DIRECTORY)

    # Use a hash of the URL to generate a unique folder name
    website_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    website_persist_directory = os.path.join(PERSIST_DIRECTORY, website_hash)

    # Clear previous data if it exists
    if os.path.exists(website_persist_directory):
        shutil.rmtree(website_persist_directory)

    logger.info(f"Scraping website data for {url} and storing in ChromaDB...")

    links = get_links_selenium(url)
    extracted_texts = []
    for link in links:
        try:
            text = extract_text_selenium(link)
            if text:
                extracted_texts.append(text)
        except Exception as e:
            logger.error(f"Error extracting text from {link}: {str(e)}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=10)
    documents = text_splitter.create_documents(extracted_texts)
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory=website_persist_directory)
    # vectordb.persist()
    
    message = f"Website data for {url} stored in ChromaDB at {website_persist_directory}"
    logger.info(message)
    return message


def save_url_to_chromadb_threaded(url_upload):
    """
    Saves website URL embeddings to ChromaDB asynchronously.
    """
    try:
        with transaction.atomic():
            url_upload.embedding_status = "processing"
            url_upload.embedding_error_or_message = "Processing URL embedding"
            url_upload.save()

        message = store_url_data_in_chromadb(url_upload.url)
        logger.info(f'URL Embedding Result: {message}')

        with transaction.atomic():
            url_upload.embedding_status = "completed"
            url_upload.embedding_error_or_message = message
            url_upload.save()

    except Exception as e:
        logger.error(f"Error processing URL {url_upload.url}: {str(e)}")
        with transaction.atomic():
            url_upload.embedding_status = "failed"
            url_upload.embedding_error_or_message = str(e)
            url_upload.save()