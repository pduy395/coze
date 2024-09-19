import os
from repository.knowledge import KnowledgeDB_supabase, KnowledgeDB_posgresql
from repository.file import FileDB_postgresql
from dotenv import load_dotenv
import cohere
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.cuda

from utils.optimizing_rag import rewrite_query, enrich_context, rerank_context_bge, rerank_context_cohere
import gc
from service.embedding import get_embedding

knowledge_db = KnowledgeDB_posgresql()
file_db = FileDB_postgresql()

# model_name = 'BAAI/bge-reranker-v2-m3'
model_name = "hotchpotch/japanese-bge-reranker-v2-m3-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model_reranking = AutoModelForSequenceClassification.from_pretrained(model_name)
model_reranking.eval()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_reranking.to(device)




async def get_similarity_document(knowledge_ids,query_text,session, model_embed):

    # query_text = rewrite_query(query_text)

    query_embedding = model_embed.encode(query_text).tolist()
    # query_embedding = get_embedding(query_text)

    res = await knowledge_db.get_similarity_cosin(query_embedding,knowledge_ids,session)



    # code not enrich context
    # docs = []
    # for r in res:
    #     docs.append(r["content"])
    docs = await enrich_context(res,session)
    
    MAX_CONTEXT = 6
    
    # output = rerank_context_cohere(query_text,docs,MAX_CONTEXT)
    output = rerank_context_bge(query_text,docs,MAX_CONTEXT,model_reranking,tokenizer)

    return output
