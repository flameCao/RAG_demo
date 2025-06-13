from langchain_text_splitters import HTMLHeaderTextSplitter, RecursiveCharacterTextSplitter

# html

label_split = [("h1", "Header 1"), ("h2", "Header 2"), ("h3", "Header 3"), ("h4", "Header 4")]

html_spliter = HTMLHeaderTextSplitter(label_split)
# html_str = ""
# html_docs = html_spliter.split_text(html_str) #从html字符串
html_docs = html_spliter.split_text_from_file('./data/example.html')  # 从html文件
print("----------------------------------")
print("文档数量", len(html_docs))
print(html_docs[0])

label_split2 = [("h1", "新闻标题"), ("p", "段落")]
html_spliter2 = HTMLHeaderTextSplitter(label_split)
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}
# 从html链接
html_docs2 = html_spliter2.split_text_from_url('https://news.qq.com/rain/a/20250524A05ER500', headers=headers)
print("----------------------------------")
print("文档数量", len(html_docs2))
print(html_docs2[0])

# 切割完后, 还可以对某段内容进行文本切割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
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

doc2_list = text_splitter.split_documents(html_docs2)  # 切doc
print("----------------------------------")
print("文档数量", len(doc2_list))
print(doc2_list[2])
