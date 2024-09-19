import os
import openai
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
import re
from pdfminer.high_level import extract_text
import requests
from langchain_core.documents import Document
import docx2txt
import uuid
from urllib.parse import urlparse
import os
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer


def get_filename_from_url(url):
    # Phân tích URL
    parsed_url = urlparse(url)
    # Lấy phần đường dẫn từ URL
    path = parsed_url.path
    # Lấy tên file từ đường dẫn
    filename = os.path.basename(path)
    return filename


def download_file(url, local_filename):
    response = requests.get(url)
    with open(local_filename, "wb") as f:
        f.write(response.content)
    return response.headers.get('Content-Type')

def get_content_type(url):
    try:
        # Gửi yêu cầu HEAD để lấy thông tin tiêu đề mà không tải xuống toàn bộ nội dung
        response = requests.head(url, allow_redirects=True)
        # Lấy giá trị Content-Type từ tiêu đề
        content_type = response.headers.get('Content-Type', '').lower()
        return content_type
    except requests.RequestException as e:
        print(f"Lỗi khi kiểm tra URL: {e}")
        raise e


def extract_text_from_file(url):
    uuid4 = uuid.uuid4()
    temp_filename = "temp" + str(uuid4)
    content_type = download_file(url, temp_filename)

    if "application/pdf" in content_type:
        temp_filename += ".pdf"
        os.rename("temp" + str(uuid4), temp_filename)
        text = extract_text(temp_filename)
    elif "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type:
        temp_filename += ".docx"
        os.rename("temp" + str(uuid4), temp_filename)
        text = docx2txt.process(temp_filename)
    elif "text/plain" in content_type:
        temp_filename += ".txt"
        os.rename("temp" + str(uuid4), temp_filename)
        with open(temp_filename, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        os.remove("temp" + str(uuid4))
        raise ValueError("Unsupported file type")

    # Xóa file tạm thời sau khi xử lý
    os.remove(temp_filename)

    return text

# "\n\n",    # Dấu xuống dòng kép
# "\n",      # Dấu xuống dòng
# " ",       # Dấu cách
# ".",       # Dấu chấm
# ",",       # Dấu phẩy
# "\u200b",  # Zero-width space
# "\uff0c",  # Fullwidth comma (dấu phẩy đầy đủ chiều rộng)
# "\u3001",  # Ideographic comma (dấu phẩy chữ Hán)
# "\uff0e",  # Fullwidth full stop (dấu chấm đầy đủ chiều rộng)
# "\u3002",  # Ideographic full stop (dấu chấm chữ Hán)
# "",        # Dấu chuỗi rỗng
def split_docs(file_path,segment, max_segment_length,rule_1,rule_2,knowledge_id):
    _ = load_dotenv(find_dotenv())

    
    openai.api_key = os.environ['OPENAI_API_KEY']

    
    text = extract_text_from_file(file_path)

    if rule_1:
        text = re.sub(r' +', ' ', text)
        # text = re.sub(r'.+', '.', text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\t+', '\t', text)
    if rule_2:
        text = re.sub(r"\S+@\S+", "", text)
        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

    doc =  [Document(page_content=text, metadata={"source": "local","knowledge":knowledge_id})]
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[
            segment
    ],
    # Set a really small chunk size, just to show.
    chunk_size = int(max_segment_length),
    chunk_overlap = 0,
    length_function=len,
    is_separator_regex=False,
)
    
    docs = text_splitter.split_documents(doc)
    return docs
    
def split_docs_from_text(text,segment, max_segment_length,rule_1,rule_2,knowledge_id):
    _ = load_dotenv(find_dotenv())

    if rule_1:
        text = re.sub(r' +', ' ', text)
        # text = re.sub(r'.+', '.', text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\t+', '\t', text)
    if rule_2:
        text = re.sub(r"\S+@\S+", "", text)
        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)

    doc =  [Document(page_content=text, metadata={"source": "local","knowledge":knowledge_id})]
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[
            segment
    ],
    # Set a really small chunk size, just to show.
    chunk_size = int(max_segment_length),
    chunk_overlap = 0,
    length_function=len,
    is_separator_regex=False,
)
    
    docs = text_splitter.split_documents(doc)
    return docs


    
