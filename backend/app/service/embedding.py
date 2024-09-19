import requests
from fastapi import HTTPException, status


url = "http://localhost:9000/embedding/"

def get_embedding(text):
    data = {
    "text": text
    }

    try:
        response = requests.post(url, json=data)
        
        # Kiểm tra mã trạng thái của phản hồi
        if response.status_code == 200:
            # Nếu thành công, in ra kết quả
            embedding_result = response.json()
            return embedding_result
        else:
            raise HTTPException(status_code=response.status_code,detail=response.text)
    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.args,
            )

# from langchain_openai import OpenAIEmbeddings
# from dotenv import load_dotenv
# import os

# # Tải biến môi trường từ tệp .env
# load_dotenv()

# # Lấy khóa API từ biến môi trường
# openai_api_key = os.getenv("OPENAI_API_KEY")

# def get_embedding(text):
#     try:
#         # Gọi API OpenAI để tạo embedding
#         embeddings = OpenAIEmbeddings(api_key=openai_api_key)

#         # Truy xuất embedding từ phản hồi
#         embedding = embeddings.embed_query(text)
#         return embedding
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# print(get_embedding("string"))

