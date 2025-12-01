import numpy as np
from sentence_transformers import SentenceTransformer, util
from metrics import key_metrics, key_metric_synonyms

_lazy_model = None
def get_model():
    global _lazy_model
    if _lazy_model is None:
        _lazy_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _lazy_model


def match_columns(df):
    model = get_model()
    synonym_list = []
    synonym_to_metric = {}
    for cononical, synonyms in key_metric_synonyms.items():
        for s in synonyms:
          synonym_list.append(s)
          synonym_to_metric[s] = cononical

    syn_emb = model.encode(synonym_list,convert_to_tensor = True)
    df_emb = model.encode(df.columns,convert_to_tensor = True)
    sim = util.pytorch_cos_sim(df_emb,syn_emb)

    result = {
        "Income Statement": [],
        "Balance Sheet": [],
        "Cash Flow Statement": []
      }
    canonical_to_statement = {}

    for statement, metrics in key_metrics.items():
        for m in metrics:
          canonical_to_statement[m] = statement
    for i, col in enumerate(df.columns):
        best_idx = np.argmax(sim[i]).item()
        best_synonym = synonym_list[best_idx]
        best_score = sim[i][best_idx].item()
        canonical_metric = synonym_to_metric[best_synonym]
        statement = canonical_to_statement.get(canonical_metric)

        if best_score > 0.8 and statement:
          result[statement].append(col)
    return result