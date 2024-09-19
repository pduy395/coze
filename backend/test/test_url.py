from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

from langchain.chains import create_extraction_chain

schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_summary": {"type": "string"},
    },
    "required": ["news_article_title", "news_article_summary"],
}


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

import pprint

from langchain_text_splitters import RecursiveCharacterTextSplitter


def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["p","h1"]
    )
    return docs_transformed[0].page_content
    # Grab the first 1000 tokens of the site
    # splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    #     chunk_size=1000, chunk_overlap=0
    # )
    # splits = splitter.split_documents(docs_transformed)

    # # Process the first split
    # extracted_content = extract(schema=schema, content=splits[0].page_content)
    # pprint.pprint(extracted_content)
    # return extracted_content
import re


urls = ["https://vnexpress.net/nhieu-ho-so-chuyen-muc-dich-su-dung-dat-o-tp-hcm-bi-treo-4778801.html"]
text = scrape_with_playwright(urls, schema=schema)


print(text)