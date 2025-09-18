import json
import pandas as pd
from tqdm import tqdm
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision
from dotenv import load_dotenv
from pathlib import Path
from src.retrieval.semantic_retrieval import init_retriever
from src.generation.chain import init_rag_chain
from src.vectorstore.embeddings import load_embeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def main():
    embeddings = load_embeddings()
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    rag_chain = init_rag_chain()
    retriever = init_retriever()
    questions_path = Path(__file__).parent / "test_questions.json"
    with open(questions_path, "r", encoding="utf-8") as f:
        test_questions = json.load(f)

    results_list = []
    print("Running evaluation on test questions...")
    for item in tqdm(test_questions, desc="Evaluating Questions"):
        question = item["question"]
        generated_answer = rag_chain.invoke(question)
        retrieved_contexts = [doc.page_content for doc in retriever.invoke(question)]
        results_list.append({
            "question": question, "ground_truth": item["ground_truth"],
            "answer": generated_answer, "contexts": retrieved_contexts
        })

    results_df = pd.DataFrame(results_list)
    results_dataset = Dataset.from_pandas(results_df)
    print("Results collected. Starting Ragas evaluation...")
    
    # 3. تنفيذ التقييم
    metrics = [faithfulness, answer_relevancy, context_precision, context_recall]
    result = evaluate(dataset=results_dataset, metrics=metrics , llm=llm , embeddings=embeddings)
    print("Evaluation complete!")
    evaluation_df = result.to_pandas()

    print("Detailed Evaluation Results")
    print(evaluation_df)

    print("Overall Performance (Final Average Scores")
    
    score_cols = ['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall']
    average_scores = evaluation_df[score_cols].mean()
    print(average_scores.round(3))

if __name__ == "__main__":
    main()