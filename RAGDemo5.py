#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Time       ：2025/5/24 10:50
# Author     ：cyy
"""
组件	Demo
向量数据库	Chroma（内存优先）
嵌入模型	    实际使用魔塔社区的词向量模型
链构造方式	使用LCEL表达式式编程
文档分块策略	简单递归分割
"""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ModelScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

# 从向量化存储中取出数据
embeddings = ModelScopeEmbeddings(model_id="iic/nlp_gte_sentence-embedding_chinese-small", model_revision="v1.0.0")

vector_store = Chroma(
    persist_directory="faiss_index_company_heath_faq",
    embedding_function=embeddings
)


# 步骤3：构建检索器（Retriever）
retriever = vector_store.as_retriever(
    search_type="similarity",  # 可以是 "similarity", "mmr" 等
    search_kwargs={"k": 5},  # 返回最相关的5个文本块
)

# 步骤4：构建生成器（LLM）和提示模板
# 1. 初始化LLM
model = ChatOpenAI(
    model='gemini-2.0-flash',
    temperature=0,
    api_key='sk-xxx',
    base_url='https://xxx.xxx.com/v1'
)

# 2. 设计提示模板
template = """Answer the question based only on the following context, answer always return chinese:
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# 步骤5：构建RAG链（RAG Chain）并执行
output_parser = StrOutputParser()

start_retriever = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)

# 使用LCEL自定义链
chain = start_retriever | prompt | model | output_parser

# 提问与回答
user_query = "体检开始日期和结束日期？"
response = chain.invoke(user_query)
print(f"用户问题: {user_query}")
print(f"AI 回答: {response}")

user_query_2 = "体检必须要提前预约吗？"
response_2 = chain.invoke(user_query_2)
print(f"用户问题: {user_query_2}")
print(f"AI 回答: {response_2}")

# 测试一个文档中可能没有的问题
user_query_3 = "家属自费体检费用是多少？"  # 假设FAQ中没有此信息
response_3 = chain.invoke(user_query_3)
print(f"用户问题: {user_query_3}")
print(f"AI 回答: {response_3}")
