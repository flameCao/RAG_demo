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
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ModelScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

# 步骤2：知识库准备与预处理
# 1. 加载文档
# 替换为你的FAQ文档路径
pdf_path = "./data/company_example.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# 2. 文本分块
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=100)
texts = text_splitter.split_documents(documents)
print(f"文档被切分成了 {len(texts)} 个块")
# 3. 向量化存储
# embeddings = HuggingFaceEmbeddings(
#     model_name="BAAI/bge-small-en-v1.5",  # 或其他支持的模型
#     # huggingfacehub_api_token = "你的API密钥"  # 仅远程API需要
# )
# embeddings = BaichuanTextEmbeddings(baichuan_api_key="sk-xxxxxxxxxxxx")
# 魔塔社区 => 文本向量 模型
# https://www.modelscope.cn/models?page=1&tabKey=task&tasks=sentence-embedding&type=nlp
# iic/nlp_gte_sentence-embedding_chinese-large 1.34G
# iic/nlp_gte_sentence-embedding_chinese-small 0.1G
# C:\\Users\\rd18\\.cache\\modelscope\\hub\\iic\\nlp_gte_sentence-embedding_chinese-large
embeddings = ModelScopeEmbeddings(model_id="iic/nlp_gte_sentence-embedding_chinese-small", model_revision="v1.0.0")
# vector_store = Chroma.from_documents(texts, embeddings)

# （可选）如果要持久化向量数据库到本地，方便后续加载使用
vector_store = Chroma.from_documents(texts, embeddings, persist_directory="faiss_index_company_heath_faq")
# 调用 persist 方法确认持久化（Chroma 需手动触发，否则可能不生效 ）
vector_store.persist()
# 加载示例：
# vector_store = Chroma(
#     persist_directory="faiss_index_company_faq",
#     embedding_function=embeddings
# )


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
    api_key='sk-rCV1f1Z5sfNPISzoA1Fd7c2d35C748729eB7BdE071D1C035',
    base_url='https://llm-hub.parcelpanel.com/v1'
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
