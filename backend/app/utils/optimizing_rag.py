from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import openai
from dotenv import load_dotenv
import os
from repository.file import FileDB_postgresql
import cohere
import torch
import torch.cuda
import numpy as np

file_db = FileDB_postgresql()
# Load environment variables from .env file
load_dotenv()




def sigmoid(x):
    """
    Hàm sigmoid tính toán giá trị sigmoid cho đầu vào x.

    Parameters:
    x (float, np.array): Đầu vào có thể là một số hoặc một mảng numpy.

    Returns:
    float, np.array: Giá trị sigmoid của đầu vào x.
    """
    return 1 / (1 + np.exp(-x))



def _parse(text):
    return text.strip('"').strip("**")

def rerank_context_cohere(query_text,docs,MAX_CONTEXT):
    output = []
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    co = cohere.Client(COHERE_API_KEY)
    response = co.rerank(
    model="rerank-multilingual-v3.0",
    query=query_text,
    documents=docs,
    top_n=MAX_CONTEXT,
    )
    
    for r in response.results:
        if r.relevance_score >= 0.3:
            tmp = {"content" : docs[int(r.index)]}
            tmp["relevance_score"] = r.relevance_score
            output.append(tmp)
    print(output)
    return output

def rerank_context_bge(query_text,docs,MAX_CONTEXT,model_reranking,tokenizer):
    output = []
    if docs == []:
        return output
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    with torch.no_grad():
        inputs = tokenizer([(query_text, doc) for doc in docs], 
                           padding=True, truncation=True, return_tensors='pt', max_length=2048)
        print(device)
        inputs = {key: value.to(device) for key, value in inputs.items()}
        scores = model_reranking(**inputs, return_dict=True).logits.view(-1, ).float()
        scores = sigmoid(scores.cpu())

    # Sắp xếp điểm từ cao đến thấp và lấy thứ tự
    ranked_indices = torch.argsort(scores, descending=True)

    # Chuyển tensor kết quả thành list
    scores_list = scores.tolist()
    ranking_list = ranked_indices.tolist()

    n = MAX_CONTEXT
    if len(ranking_list) < MAX_CONTEXT:
        n = len(ranking_list)
    for i in range(n):
        if scores_list[ranking_list[i]] > 0.25:
            tmp = {"content" : docs[int(ranking_list[i])]}
            tmp["relevance_score"] = scores_list[ranking_list[i]]
            output.append(tmp)

    return output


def rewrite_query(query):
    template = """\ に対してより適切なクエリを提供します
        コサイン類似度を利用した情報検索ツール \
        クエリを返すだけで、クエリを ** で終了します。\
        クエリ: {x} 応答:"""
    # template = """Cung cấp 1 câu truy vấn tốt hơn cho \
    #     công cụ tìm kiếm thông tin bằng độ tương đồng cosin, \
    #     chỉ trả về câu truy vấn, kết thúc câu truy vấn với **.\
    #     Truy vấn: {x} Câu trả lời:"""


    rewrite_prompt = ChatPromptTemplate.from_template(template)
    openai.api_key = os.getenv('OPENAI_API_KEY')
    model = ChatOpenAI(model="gpt-4o-mini",temperature=0)
    rewriter = rewrite_prompt | model | StrOutputParser() | _parse

    return rewriter.invoke({"x": query})



async def enrich_context(res,session):
    docs = []
    sorted_documents = sorted(res, key=lambda x: (x['file_id'], x['index']))
    i=0
    while i < len(sorted_documents):
        file_id = sorted_documents[i]["file_id"]
        start = sorted_documents[i]["index"]-1
        end = sorted_documents[i]["index"]+1
        while True:
            if i == len(sorted_documents)-1:
                new_content = await file_db.enrich_context(file_id,start,end,session)
                docs.append(new_content)
                break
            elif file_id == sorted_documents[i + 1]["file_id"] and end == sorted_documents[i+1]["index"]:
                end = end + 1
                i = i + 1
            else:
                new_content = await file_db.enrich_context(file_id,start,end,session)
                docs.append(new_content)
                break
        i = i+1

    return docs