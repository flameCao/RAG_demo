#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Time       ：2025/5/21 8:42
# Author     ：cyy
# loader01
# 1. 通用递归切割器（所有文件类型）
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader, CSVLoader, JSONLoader,
    UnstructuredHTMLLoader, UnstructuredMarkdownLoader, PyPDFLoader
)

# 递归切割器配置
recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        "?",
        "|",
        ". ",
        "! ",
        "? ",
        ",",
        ", ",
        " ",
        ""
    ]
)

# 示例：加载并切割文本文件
text_loader = TextLoader("./../data/example.txt", encoding="utf8")
text_docs = text_loader.load()
text_chunks = recursive_splitter.split_documents(text_docs)
print("------------------------------")
print("text文档数量", len(text_chunks))
print(text_chunks[0])


# 示例：加载并切割CSV文件
csv_loader = CSVLoader("./../data/example.csv", encoding="utf8")
csv_docs = csv_loader.load()
csv_chunks = recursive_splitter.split_documents(csv_docs)
print("------------------------------")
print("csv文档数量", len(csv_chunks))
print(csv_chunks[0])

# 示例：加载并切割JSON文件
json_loader = JSONLoader(
    file_path="./../data/example.json",
    jq_schema=".product.variants[].sku", #.product.variants[] | {id, sku}
    text_content=False
)
json_docs = json_loader.load()
print("------------------------------")
print("json数据", json_docs)
json_chunks = recursive_splitter.split_documents(json_docs)
print("json文档数量", len(json_chunks))
print(json_chunks)

# 示例：加载并切割JSON文件2, 自定义json metadata
def create_metadata(record: dict, metadata: dict) -> dict:
    metadata['id'] = record.get('id')
    metadata['sku'] = record.get('sku')
    return metadata

json_loader2 = JSONLoader(
    file_path="./../data/example.json",
    jq_schema=".product.variants[]", #.product.variants[] | {id, sku}
    metadata_func=create_metadata,
    text_content=False
)
json_docs2 = json_loader2.load()
print("------------------------------")
print("json2数据", json_docs2)
