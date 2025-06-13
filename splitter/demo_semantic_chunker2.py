from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import ModelScopeEmbeddings
import numpy as np
from typing import List

# 初始化嵌入模型
class NormalizedModelScopeEmbeddings(ModelScopeEmbeddings):
    def embed_query(self, text: str) -> List[float]:
        embedding = super().embed_query(text)
        print(f"原始嵌入长度: {len(embedding)}, 示例值: {embedding[:3]}")  # 调试输出
        norm = np.linalg.norm(embedding)
        print(f"归一化前范数: {norm:.4f}")  # 典型值应远大于1.0（如7.0+）
        normalized = [x / norm for x in embedding]
        print(f"归一化后范数: {np.linalg.norm(normalized):.4f}")  # 必须≈1.0
        return normalized

embeddings = NormalizedModelScopeEmbeddings(
    model_id="iic/nlp_gte_sentence-embedding_chinese-small"
)

# 创建分块器（添加更多参数）
text_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=20,  # 明确设置百分位值
)
# 测试文本
news_text = """
昨日特斯拉发布新款Model 3，续航提升20%。苹果公司同时宣布iOS 17将于9月推送。马斯克表示特斯拉明年将推出自动驾驶出租车。
"""

# 执行分割
chunks = text_splitter.create_documents([news_text])
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk.page_content}\n{'-'*50}")

