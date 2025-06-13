from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import BaichuanTextEmbeddings
from langchain.docstore.document import Document
import numpy as np

# 初始化嵌入模型（需替换为有效API Key）
embeddings = BaichuanTextEmbeddings(baichuan_api_key="sk-3f2aefd9391fcaed4c8af92fda68ffff")

# 创建分块器（方案1：单句嵌入，buffer_size=0）
text_splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=20,  # 降低阈值
    add_start_index=True,
)

# 测试文本
news_text = """
昨日特斯拉发布新款Model 3，续航提升20%。苹果公司同时宣布iOS 17将于9月推送。马斯克表示特斯拉明年将推出自动驾驶出租车。
"""

# 执行分割
chunks = text_splitter.create_documents([news_text])

# 输出结果
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk.page_content}")
    print(f"Metadata: {chunk.metadata}\n{'-'*50}")