https://www.kaggle.com/datasets/azraimohamad/news-article-weekly-updated?select=news_v1.csv

# Q5

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

