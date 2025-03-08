# 5. 基于 TestQuestion20.csv 和 rag.py 检查生成的回答

import pandas as pd

# 假设 rag.py 与本脚本在同一目录，且内含 query_answering_system()
# 若不在同一目录，需要在 import 前指定正确路径
import sys
import os

# 将上一级目录加入 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from components.rag import query_answering_system

def check_generated_answers(question_csv= "../data/TestQuestion20.csv", 
                            document_csv="../data/1K_news.csv", 
                            embedding_model="BAAI/bge-small-en",
                            lm_model="Qwen/Qwen2.5-0.5B",
                            top_k=3):
    """
    从 TestQuestion20.csv 逐条读取问题，调用 rag.py 中的 query_answering_system() 执行检索+生成，
    最后返回包含模型回答的 DataFrame，便于查看或做进一步评估。
    
    参数：
    - question_csv: 含有问题的 CSV 文件，比如 TestQuestion20.csv。
    - document_csv: 指向语料文件，如 1K_news.csv。
    - embedding_model: 用于向量化的embedding模型名称 (默认 "BAAI/bge-small-en")。
    - lm_model: 用于生成回答的大模型名称 (默认 "Qwen/Qwen2.5-0.5B")。
    - top_k: 检索时取相似度最高的文档数量。
    """
    # 1) 读取含问题的 CSV
    qdf = pd.read_csv(question_csv)
    
    # 结果列表，用于存储 {问题，模型回答，检索到的标题...}
    results = []

    # 2) 遍历每个问题
    for idx, row in qdf.iterrows():
        # 假设 CSV 中有 "Question" 列
        question_text = row["Question"]
        
        # 3) 调用你的 RAG 函数来获取回答
        output = query_answering_system(
            query=question_text,
            document_dataset=document_csv,
        )
        
        # output 应该是一个 dict，形式大致为：
        # {
        #   "answer": "...",       # 模型回答
        #   "title": ["...", ...]  # 检索文档的标题
        # }
        model_answer = output.get("answer", "")
        retrieved_titles = output.get("title", [])
        
        # 4) 将当前结果放入列表
        results.append({
            "Index": idx + 1,
            "Question": question_text,
            "Model_Answer": model_answer,
            "Retrieved_Titles": retrieved_titles
        })
    
    # 5) 转成 DataFrame 方便查看或评估
    answer_df = pd.DataFrame(results)
    return answer_df

# 若想直接在此脚本里测试，可以写：
if __name__ == "__main__":
    # 调用函数得到一个 DataFrame
    df_answers = check_generated_answers(
        question_csv="TestQuestion20.csv",   # 你的问题文件
        document_csv="../data/1K_news.csv",  # 你的语料文件
        embedding_model="BAAI/bge-small-en",
        lm_model="Qwen/Qwen2.5-0.5B",
        top_k=3
    )
    
    # 打印查看前几条
    print(df_answers.head(5))
    
    # 如果需要保存到 CSV 以供后续人工审阅
    df_answers.to_csv("TestQuestion20_Answers.csv", index=False, encoding="utf-8-sig")