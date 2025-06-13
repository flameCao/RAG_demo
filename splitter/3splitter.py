from langchain_text_splitters import MarkdownHeaderTextSplitter

# markdown
with open('./data/example.md', encoding='utf8') as f:
    text_data = f.read()

label_split = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3"), ("####", "Header 4")]

# strip_headers 是否在内容中删除章节的标题
markdown_splitter = MarkdownHeaderTextSplitter(label_split, strip_headers=False)

docs_list = markdown_splitter.split_text(text_data)
print("------------------------------")
print(len(docs_list))
print(docs_list)