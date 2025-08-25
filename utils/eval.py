from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate_predictions(y_true, y_pred):
    return {
        "precision": precision_score(y_true, y_pred, average="weighted"),
        "recall": recall_score(y_true, y_pred, average="weighted"),
        "f1": f1_score(y_true, y_pred, average="weighted")
    }

# You could also implement "retrieval hit rate":
def retrieval_hit_rate(retrieved_docs, ground_truth):
    hits = sum(1 for doc in retrieved_docs if ground_truth.lower() in doc.page_content.lower())
    return hits / len(retrieved_docs) if retrieved_docs else 0