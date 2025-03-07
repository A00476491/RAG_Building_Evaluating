import ssl
import sys
import os

# 将上一级目录加入 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# 现在就能找到 components 文件夹了
from components.rag import query_answering_system


output = query_answering_system(
            query=question_text,
            document_dataset=document_csv,
            embedding_model_name=embedding_model,
            model_name=lm_model,
            k=top_k
        )
print(ssl.OPENSSL_VERSION)