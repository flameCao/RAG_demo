#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Time       ：2025/5/24 22:25
# Author     ：cyy
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.parsers.html import bs4
from langchain_community.document_loaders import (
    CSVLoader, JSONLoader, WebBaseLoader, PyPDFLoader
)


# 示例：加载并切割CSV文件
csv_loader = CSVLoader("./../data/example.csv", encoding="utf8")
csv_docs = csv_loader.load()

json_loader = JSONLoader(
    file_path="./../data/example.json",
    jq_schema=".product.variants[].sku", #.product.variants[] | {id, sku}
    text_content=False
)
json_docs = json_loader.load()

online_html_loader = WebBaseLoader(
    web_paths="https://news.qq.com/rain/a/20250524A05ER500",
    encoding="utf-8",
    bs_kwargs=dict(parse_only=bs4.BS4HTMLParser(class_=('md-content',)))
)
html_docs = online_html_loader.load()
print("------------------------------")
print(html_docs)

# 示例：PDF按页面切割
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 按字符数切割
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", " ", ""]  # 按字符列表拆分
)
pdf_loader = PyPDFLoader("../../data/example.pdf")
pdf_docs = pdf_loader.load()
