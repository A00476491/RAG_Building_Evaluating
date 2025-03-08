# Dataset Introduction

For our knowledge base, we have selected the **Malaysian News Dataset**, which consists of **1,000 short news articles** covering topics from **Malaysia and international regions**. This dataset is sourced from **Kaggle**, and it is regularly updated with new events.

**Source:** [Kaggle - News Article (Weekly Updated)](https://www.kaggle.com/datasets/azraimohamad/news-article-weekly-updated?select=news_v1.csv)


## Dataset Structure

Each row in the dataset represents a news article and includes several columns:

- **Article ID**: A unique identifier for the news article  
- **Title**: The headline of the news article  
- **Text**: The main content of the article  
- **Category**: The category of the news (e.g., politics, economy, sports, etc.)  
- **Published Date**: The date the article was published  
- **Word Count**: The total number of words in the article  


# RAG Algorithm

Here is our RAG implementation. This is a simple version of RAG, consisting of three steps: **index, query, and generation**.

## 1. Index Step  
In this step, we map the news articles to embeddings using a model called **bge-small**. This model is recommended in the assignment requirements and performs well for this task.

## 2. Query Step  
We compute the **cosine similarity** between the query and the article embeddings, then retrieve the **three most relevant articles** as references.

## 3. Generation Step  
We use a model called **Qwen-2.5.0.5b**, which is a small language model but performs well for its size. Specifically, we provide this model with the query and the retrieved documents, and it generates the final answer.

To run the exeample code of RAG, use the following commands:

```bash
cd components
```
```bash
python rag.py
```
# Q3
- **Good Questions** are designed to test in-depth comprehension and extraction of key facts. They focus on the main impacts or core details of the news.
- **Bad Questions** intentionally ask for irrelevant or absurd details that are not mentioned in the news, to test how the AI handles out-of-scope queries.
- **General Questions** are basic fact-recall questions that do not require deep interpretation.

## Example of good performance

### Question: 
>Given the tensions between Hungary and its Western allies, what are the potential implications of the U.S.-Hungary relationship in the context of the ongoing conflict in Ukraine?

### Answer (Sample): 
>The potential implications of the U.S.-Hungary relationship in the context of the ongoing conflict in Ukraine could include increased cooperation between the two countries, as well as potential for a shift in the U.S. position on the conflict. Additionally, the U.S.-Hungary relationship could potentially lead to a more stable and cooperative relationship between the two countries, as well as a potential for a more peaceful resolution to the conflict. However, it is important to note that the U.S.-Hungary relationship is complex and multifaceted, and there are potential risks and challenges that could arise from any changes in the relationship.

### Explanation

- **Complex and Relevant Context:**  
  The question asks the model to consider both geopolitical tensions and their impact on bilateral relations, which requires integrating multiple layers of information (Hungary's relationship with Western allies, U.S. foreign policy, and the conflict in Ukraine).

- **Testing Analytical Abilities:**  
  By asking about potential implications, the question forces the model to reason about cause and effect. It needs to extract key factors from the news and evaluate how shifts in diplomatic relations might influence the ongoing conflict.

- **Synthesis of Multiple Factors:**  
  The answer shows that the model can identify several possible outcomes (increased cooperation, a shift in U.S. stance, more stable relationships, and even a more peaceful resolution) while acknowledging the complexity of the situation.

- **Demonstrates Deep Understanding:**  
  The question is not a simple fact-checking query; it requires the model to synthesize economic, diplomatic, and geopolitical insights. This is a strong indication that the model can handle multifaceted issues, which is why it is categorized as a "Good" question.

- **Source Information:**  
  - **News ID:** 1561362  
  - **Category:** Others

---

## Example of poor performance
### Question:  
>What is the estimated weight of a single Puncak Alam Factory brick?

### Answer (Sample):
>The estimated weight of a single Puncak Alam Factory brick can be estimated by multiplying the volume of the brick by its density. The density of a brick can be estimated by dividing its weight by its volume. The volume of a brick can be estimated by measuring its dimensions and using the formula for the volume of a rectangular prism. The density of a brick can be estimated by dividing its weight by its volume. The estimated weight of a single Puncak Alam Factory brick can be estimated by multiplying the volume of the brick by its density.

### Explanation:

- **Irrelevance to the News:**  
  The question asks for a technical calculation that is not related to any news content. It does not require extracting or analyzing information from a news article but merely applying a basic formula.

- **Repetitive, Formulaic Response:**  
  The answer provided is a generic explanation of how to calculate weight from volume and density. It repeats the same method several times without offering any specific details about the Puncak Alam Factory or any unique news context.

- **Lack of Depth and Analysis:**  
  A well-designed question should challenge the model to understand and synthesize complex, news-related information. This question, however, only triggers a standard, textbook-like response, which doesn't showcase the model's ability to process nuanced or contextually rich content.

- **Evaluation Impact:**  
  Since the question is too generic and disconnected from the news content, it fails to effectively evaluate the model's comprehension and reasoning abilities in a real-world news scenario.

**Source Information:**  
- **News ID:** 1566880  
- **Category:** Business
---

This example shows that while the question may be poorly chosen, the model's ability to generate a well-reasoned answer remains a positive sign of its comprehension and reasoning capabilities.

---

## Example of normal performance

### Question: 
>How much was the initial budget for the Cabagan-Santa Maria Bridge?

### Answer:
>The initial budget for the Cabagan-Santa Maria Bridge was 640 million pesos (US$11.6 million).

### Explanation:

- **Straightforward Fact Retrieval:**  
  The question asks for a specific, numerical fact directly from the news article. It doesn't require deep analysis but rather a precise extraction of a given number.

- **Clarity and Simplicity:**  
  Because the question is simple and clear, it serves to confirm that the model can accurately retrieve and present factual data without ambiguity.

- **Demonstrated Competence:**  
  Even though this is a general question, the model's correct and concise answer shows its capability to handle basic factual queries effectively.

- **Source Information:**  
  - **News ID:** 1567681  
  - **Category:** Politics

---

# Q5

## Overall

 While the answers often appear specific—sometimes citing statistics or discussing policy changes, many include references or details (e.g., different countries, unrelated figures) not found in the corresponding retrieved document titles. This discrepancy suggests the model occasionally “hallucinates” or mixes content from other articles. 

 Based on a quick sample inspection, some answers mention unrelated country details or numeric values not found in the retrieved titles. If we assume these are “hallucinations,” here is a **sample outcome**:

- **Answers with notable hallucinations**: ~6 out of 20  
- **Answers mostly consistent**: ~14 out of 20  
- **Estimated hallucination ratio**: ~30%

## Example for first One

1. **Question**  
   > *"How did the number of foreign tourists visiting North Korea change in 2024 compared to previous years?"*

2. **Model_Answer**  
   > *"The number of foreign tourists visiting North Korea in 2024 is expected to increase by 20.4% compared to the previous year..."*  
   It also mentions something about Cambodia’s government being strict against certain criminal activities, which appears unrelated to North Korea.

3. **Retrieved_Titles**  
   - *"Tourists step into N. Korea after five-year freeze."*
   - *"Sabah set to attract 3.5 million tourists in 2025."*
   - *"Cambodia’s not a base for kidnapping, cybercrime, human trafficking says PM Hun Manet."*

## Comparison / Analysis

### Does it directly answer the question?

- The question focuses on **whether the number of foreign tourists to North Korea in 2024 is different compared to previous years.**
- The model answer says it “is expected to increase by 20.4%.” That seems like a direct response, but we need to check whether it’s grounded in the retrieved information.

### Are the retrieved documents relevant?

- The first document title suggests something about North Korea reopening to tourists after a five-year freeze, but does it mention “+20.4%” growth? We don’t know yet.
- The second document is about Malaysia’s Sabah aiming for 3.5 million tourists in 2025—unrelated to North Korea.
- The third document concerns Cambodia and its stance on criminal activities—again, unrelated to North Korea’s tourist numbers.

**Observation**:  
- None of these titles explicitly mention “a 20.4% increase” in 2024 visitors to North Korea.  
- The model may have blended or fabricated data from the “3.5 million tourists in 2025” reference or other text, leading to inaccurate or “hallucinated” content.

### Accuracy and alignment

**Accuracy**  
   - The answer claims “+20.4%,” which is nowhere to be found in the retrieved titles. This likely indicates the model invented the figure.
  
**Alignment**  
   - The answer also references Cambodia’s government crackdown on illicit activities, which has no clear connection to North Korean tourism.

**Conclusion**:  
By comparing the question, the model answer, and the retrieved titles (or articles), we see the model’s response may have combined unrelated snippets—common in generative models when retrieval is off-target or the content is insufficient. This is why a careful review is essential to detect hallucinations or mismatch between the question and the retrieved documents.Breaking it down:


# Q6

## Automated evaluation Pipeline

### What Needs to Be Automated?
- Generate questions
- Check retrieval Performance
- Detect model hallucinations

### Pipeline

1. **Generate Questions:**  
   - Provide 100 case articles to ChatGPT and let it generate a question for each case article. 
   - Get (case article, question)

2. **Generate Answers:**  
   - Use our RAG model to answer the generated questions.
   - Get (case article, question, answer, retrieved articles)

3. **Evaluate Retrieval Performance:**  
   - Check if each case article is in the retrieved articles using:
     - Top1 Accuracy
     - Top2 Accuracy
     - Top3 Accuracy

4. **Detect Hallucination:**  
   - Provide the answer and retrieved articles to ChatGPT.  
   - Let ChatGPT determine if hallucinations occured and provide a reason.
   - Get (case article, answer, retrieved articles, hallucinated, reason)
