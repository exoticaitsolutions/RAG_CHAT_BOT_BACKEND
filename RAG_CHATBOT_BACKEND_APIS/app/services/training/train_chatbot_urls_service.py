import hashlib
import logging
import os
import time
from uuid import uuid4
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from selenium.webdriver.chrome.service import Service
from RAG_Backend.settings import BASE_DIR
from RAG_CHATBOT_BACKEND_APIS.utils import ensure_directory_exists, format_name
from RAG_CHATBOT_BACKEND_APIS.models import *
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)
embed_fun = OpenAIEmbeddings(model='text-embedding-3-small')
def init_web_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
def extract_text_selenium(url):
        driver = init_web_driver()
        driver.get(url)
        time.sleep(5)
        text = driver.find_element(By.TAG_NAME, "body").text
        driver.quit()
        return text
def get_links_selenium(url):
        driver = init_web_driver()
        driver.get(url)
        time.sleep(8)
        elements = driver.find_elements(By.TAG_NAME, "a")
        links = {urljoin(url, elem.get_attribute("href")) for elem in elements if elem.get_attribute("href")}
        driver.quit()
        return list(links)
def process_urls_for_training(urllist,chat_data,user_data,webeite_url_id):
    website_data1 = WebsiteDB.objects.filter(id=webeite_url_id).first()
    website_data1.status = "processing" # type: ignore
    # website_data1.save() # type: ignore
    openai.api_key = chat_data.openai_key
    forment_username = format_name(str(user_data.username))
    forment_chat_name = format_name(str(chat_data.chatbot_name))
    if chat_data.vector_database == "chroma":
        ChromaDb_Dir = os.path.join(BASE_DIR, "chroma_db", forment_username, forment_chat_name)
        ensure_directory_exists(ChromaDb_Dir)
        collection = f"{forment_username}_{forment_chat_name}"
        print(f"[INFO] ChromaDB Path: {ChromaDb_Dir}")
        print(f"[INFO] Collection Name: {collection}")
        print(f"[INFO] urllist Name: {urllist}")
        # message = store_url_data_in_chromadb()
        # website_hash = hashlib.md5(urllist.encode('utf-8')).hexdigest()
        # website_persist_directory = os.path.join(ChromaDb_Dir, website_hash)
        # print(f"[INFO] website_persist_directory Name: {website_persist_directory}")
        # ensure_directory_exists(website_persist_directory)
        # print('website_hash', website_hash)
        links = get_links_selenium(urllist)
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
            ids = [str(uuid4()) for _ in documents]
            print(ids)
            full_page_content = "".join([text.page_content for text in documents])
        ids = []
        full_page_content = ''
        for x in range(len(documents)):
            full_page_content += str(documents[x].page_content)
            id_new = str(uuid4())
            ids.append(id_new)
            WebsiteCollectionIds.objects.create(web_id=id_new, web_name=urllist, collection=collection, chroma_dir=ChromaDb_Dir, chatbot=chat_data, user=user_data, website=website_data1)
        db = Chroma.from_documents(documents, embed_fun, persist_directory=ChromaDb_Dir, collection_name=collection,ids=ids)     
        website_data1.no_of_characters = len(full_page_content) # type: ignore
        website_data1.no_of_chunks = len(documents) # type: ignore
        website_data1.status = "completed" # type: ignore
        website_data1.save() # type: ignore


        






