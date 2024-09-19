import requests
from bs4 import BeautifulSoup

# URL của trang web mà bạn muốn craw dữ liệu
url = 'https://vnexpress.net/uob-tang-truong-viet-nam-2024-kha-nang-vuot-6-4787654.html'

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
p_tags = soup.find_all('p')
h_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

print("Nội dung các thẻ <p>:")
for p in p_tags:
    print(p.get_text())

print("\nNội dung các thẻ <h>:")
for h in h_tags:
    print(h.name, h.get_text())
