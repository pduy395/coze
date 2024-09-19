import concurrent
import concurrent.futures
from utils.embedding import get_filename_from_url, get_content_type
from utils.embedding import extract_text_from_file
import json
import uuid
from service.document import executor
import os
import threading
import requests
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_with_playwright(url):
    sys.path.insert(0, '/usr/local/lib/chromium-browser/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    dr = webdriver.Chrome(options=options)

    dr.get(url) # Website used for scraping
    name = str(dr.title)
    total_text = str(dr.title) + "\n"
    for i in dr.find_elements(By.TAG_NAME,'p'):
        text = i.text
        total_text += text
        total_text += "\n"
    dr.quit()
    return name, total_text

def scrape_with_playwright_2(url):
    # Tiêu đề bao gồm User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }

    # Gửi yêu cầu GET với tiêu đề User-Agent
    response = requests.get(url, headers=headers)

    # Kiểm tra nếu yêu cầu thành công
    response.raise_for_status()

    # Phân tích HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Lấy và in nội dung từ các thẻ <p> và <h>
    p_tags = soup.find_all(['p','h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    h_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    name = ""
    total_text = ""
    
    for p in p_tags:
        total_text = total_text + p.get_text() +"\n"

    for h in h_tags:
        name = h.get_text()
        break 

    return name, total_text
    
web_content_types = [
            "text/html", 'application/xhtml+xml', 
            'application/xml', 'text/css', 'application/javascript', 
            'application/json', 'text/javascript']
file_content_types = ["application/pdf", "text/plain","application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

file_locks = {}

def get_file_lock(file_id):
    if file_id not in file_locks:
        file_locks[file_id] = threading.Lock()
    return file_locks[file_id]

def write_data(data,json_file_path):
    if os.path.exists(json_file_path):
        # file_lock = get_file_lock(json_file_path)
        # print("write")
        # with file_lock:
        #     print("allow_write")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)


def get_data(url,json_file_path):
    try:
        content_type = get_content_type(url)
        file_name = ""
        text = ""
        print(content_type)
        if content_type in file_content_types:
            file_name = get_filename_from_url(url)
            text = extract_text_from_file(url)
        else:
            flag = False
            for w in web_content_types:
                if w in content_type:
                    flag = True     
            if flag:
                print("start")
                file_name, text = scrape_with_playwright(url)
                print("end")

        data = {
                    "status": True,
                    "name": file_name,
                    "content": text
                }
        write_data(data,json_file_path)
    except Exception as e:
        try:
            detail = str(e.args[0])
        except:
            detail = "url: " + str(url) + " is broken or some thing went wrong"
        data = {
                    "status": False,
                    "url": url,
                    "detail": detail,
                    "name": "",
                    "content": ""
                }
        write_data(data,json_file_path)

def create_thread_get_data(user_id,request):
    futures = []
    for i in range(len(request)):
        url = request[i].url
        init_data = {}
        tmp = uuid.uuid4()
        json_file_path = str(user_id) + "_" + str(tmp) + ".json"
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(init_data, json_file, ensure_ascii=False)
            
        future = executor.submit(get_data,url,json_file_path)
        futures.append(future)