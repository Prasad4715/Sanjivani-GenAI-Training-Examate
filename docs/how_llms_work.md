# How Large Language Models Work — ChalanCheck

## 1. What Is a Large Language Model?

A Large Language Model (LLM) is an AI model trained on large amounts of text. It learns patterns in language and uses them to understand questions and generate responses.

For example, when someone asks, "What is the fine for riding without a helmet?", an LLM can explain the answer in simple language.

However, an LLM does not automatically know the latest traffic laws. ChalanCheck must use reliable legal documents to provide accurate information.

## 2. How Does an LLM Work?

An LLM processes a question through several stages.

1. **Input:** The user enters a question.
2. **Tokenization:** The question is divided into smaller pieces called tokens.
3. **Embeddings:** Tokens are converted into numerical representations.
4. **Transformer:** The model uses attention mechanisms to understand relationships between tokens.
5. **Token Prediction:** The model predicts the next token based on the previous context.
6. **Output:** Tokens are combined to generate a response.

## 3. LLM Working Diagram

```text
       User Question
             |
             v
        Tokenization
             |
             v
         Embeddings
             |
             v
     Transformer Layers
       (Self-Attention)
             |
             v
    Next Token Prediction
             |
             v
       Generated Answer
```

## 4. How Will LLMs Help ChalanCheck?

ChalanCheck aims to help citizens understand traffic challans without needing to read complicated legal documents.

A future version of the application can use Retrieval-Augmented Generation (RAG).

The system will:

1. Receive the user's traffic challan question.
2. Search relevant legal records.
3. Retrieve the applicable section and penalty information.
4. Provide the retrieved information to an LLM.
5. Generate a simple explanation with references to the legal source.

For example, a user may ask about Section 194D. ChalanCheck should retrieve the relevant legal record before explaining the helmet-related offence.

## 5. Limitations of LLMs

LLMs have some important limitations:

- They may generate incorrect information, called hallucinations.
- Their training data may not include recent legal changes.
- They may confuse penalties under different sections.
- They cannot confirm local police station hours without a suitable source.
- They should not invent fine amounts or legal consequences.

For these reasons, ChalanCheck should use verified legal sources and clearly say when information is unavailable.

## 6. Ten Real ChalanCheck User Questions

### Questions from the Project Assignment

1. What is the fine for riding bike without helmet under section 194D?
2. What is section 196 in my challan, driving without insurance?
3. Under which section can the police seize my driving licence on the spot?
4. I got challan for no helmet and no insurance together, what is the total maximum fine?
5. My son is 16 and drove the scooty, what penalty for him and for me as the owner?
6. Can I pay my Maharashtra e-challan at Kopargaon police station on Sunday?

**Note:** Question 6 cannot be answered using the legal records alone because the dataset does not contain police station opening hours or local payment availability.

### Additional Questions

7. I received a challan under Section 183 for speeding. What is the maximum fine?
8. What happens if I am caught drunk driving for the second time under Section 185?
9. My challan mentions Section 184. What does dangerous driving mean, and what additional punishment can apply?
10. I received a challan with Sections 194D and 196. Can ChalanCheck explain both violations separately?

## 7. Conclusion

Large Language Models can make complicated legal information easier to understand. For ChalanCheck, an LLM should explain information retrieved from trusted legal documents rather than guessing.

The application should distinguish statutory maximum fines from actual challan amounts and Maharashtra-specific compounding rates. It should also explain when information cannot be verified.

ChalanCheck is intended to provide general legal information, not professional legal advice.